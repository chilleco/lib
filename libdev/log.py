"""
Unified Loguru logging:
- JSON logs to stdout (Alloy -> Loki -> Grafana)
- Telegram notifications for important/silent=False events
"""

from __future__ import annotations

import contextvars
import json
import sys
from typing import Any, Iterable

from loguru import logger

from .cfg import cfg
from .doc import to_json
from .notify import notify_log_record, setup_notify


_request_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "request_id", default=None
)
_trace_id_var: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "trace_id", default=None
)

_PROJECT = cfg("PROJECT_NAME") or cfg("name") or "untitled"
_SERVICE = cfg("service", "app")
_ENV = cfg("env", "test")
_VERSION = cfg("release", "unknown")
_LEVEL = cfg("log.level", "INFO")

_INTERNAL_EXTRA_KEYS = {"_notify", "_notify_type", "request_id", "trace_id"}


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    return str(value)


def _normalize_tags(tags: str | Iterable[str] | None) -> list[str]:
    if not tags:
        return []
    if isinstance(tags, str):
        return [tags] if tags else []
    return [str(tag) for tag in tags if tag]


def _safe_json_text(value: Any) -> str:
    try:
        return json.dumps(_json_safe(value), ensure_ascii=False)
    except Exception:  # pylint: disable=broad-except
        return str(value)


def _message_with_payload(record: dict[str, Any]) -> str:
    payload = record["extra"].get("payload")
    if payload is None:
        return record["message"]
    return f"{record['message']} | {_safe_json_text(payload)}"


def _has_active_exception() -> bool:
    return sys.exc_info()[0] is not None


def set_request_context(request_id: str, trace_id: str | None = None) -> None:
    _request_id_var.set(request_id)
    _trace_id_var.set(trace_id)


def clear_request_context() -> None:
    _request_id_var.set(None)
    _trace_id_var.set(None)


def _inject_context(record: dict[str, Any]) -> dict[str, Any]:
    request_id = _request_id_var.get()
    trace_id = _trace_id_var.get()
    if request_id:
        record["extra"]["request_id"] = request_id
    if trace_id:
        record["extra"]["trace_id"] = trace_id
    return record


def _serialize_exception(exception: Any | None) -> dict[str, Any]:
    if not exception:
        return {}
    stack = None
    if exception.traceback is not None:
        try:
            stack = "".join(exception.traceback.format())
        except Exception:  # pylint: disable=broad-except
            stack = str(exception.traceback)
    return {
        "type": getattr(exception.type, "__name__", None),
        "message": str(exception.value) if exception.value is not None else None,
        "stack": stack,
    }


def _json_sink(message) -> None:
    record = message.record
    exception = record.get("exception")
    error_payload = _serialize_exception(exception)

    output: dict[str, Any] = {
        "project": _PROJECT,
        "service": _SERVICE,
        "env": _ENV,
        "version": _VERSION,
        "level": record["level"].name,
        "trace_id": record["extra"].get("trace_id"),
        "request_id": record["extra"].get("request_id"),
        "msg": _message_with_payload(record),
        "time": record["time"].isoformat(),
    }

    if error_payload.get("stack"):
        output["error.stack"] = error_payload["stack"]
    if error_payload.get("message"):
        output["error.message"] = error_payload["message"]
    if error_payload.get("type"):
        output["error.type"] = error_payload["type"]

    extra = {
        key: _json_safe(value)
        for key, value in record["extra"].items()
        if key not in _INTERNAL_EXTRA_KEYS
    }
    if extra:
        output["extra"] = extra

    sys.stdout.write(json.dumps(output, ensure_ascii=True) + "\n")


def _notify_sink(message) -> None:
    record = message.record
    if not record["extra"].get("_notify"):
        return
    error_payload = _serialize_exception(record.get("exception"))
    notify_log_record(_PROJECT, _SERVICE, _ENV, record, error_payload)


class AppLogger:
    """Project logger wrapper around Loguru with notify controls."""

    def __init__(self, raw_logger):
        self._logger = raw_logger

    def catch(self, *args, **kwargs):
        return self._logger.catch(*args, **kwargs)

    def bind(self, **kwargs):
        return self._logger.bind(**kwargs)

    def _fallback(self, level: str, message: Any, exc: Exception) -> None:
        try:
            payload = {
                "project": _PROJECT,
                "service": _SERVICE,
                "env": _ENV,
                "version": _VERSION,
                "level": "ERROR",
                "msg": "logger emit failed",
                "log_level": level.upper(),
                "log_message": str(message),
                "error": str(exc),
            }
            sys.stderr.write(json.dumps(payload, ensure_ascii=True) + "\n")
        except Exception:  # pylint: disable=broad-except
            return

    def _extract_payload(
        self, message: Any, args: tuple[Any, ...], extra: Any | None
    ) -> tuple[tuple[Any, ...], Any | None]:
        if extra is not None:
            return args, extra
        if (
            len(args) == 1
            and isinstance(args[0], (dict, list, tuple, set))
            and isinstance(message, str)
            and "{" not in message
        ):
            return tuple(), args[0]
        return args, None

    def _emit(
        self,
        level: str,
        message: Any,
        *args: Any,
        tags: str | Iterable[str] | None = None,
        silent: bool = True,
        extra: Any | None = None,
        notify_type: str | None = None,
    ) -> None:
        fmt_args, payload = self._extract_payload(message, args, extra)
        context: dict[str, Any] = {}
        normalized_tags = _normalize_tags(tags)
        if normalized_tags:
            context["tags"] = normalized_tags
        if payload is not None:
            context["payload"] = _json_safe(payload)
        if not silent:
            context["_notify"] = True
            if notify_type:
                context["_notify_type"] = notify_type

        target = self._logger.bind(**context) if context else self._logger
        try:
            if _has_active_exception():
                target.opt(exception=True).log(level.upper(), message, *fmt_args)
            else:
                target.log(level.upper(), message, *fmt_args)
        except Exception as exc:  # pylint: disable=broad-except
            self._fallback(level, message, exc)

    def log(
        self,
        level: str,
        message: Any,
        *args: Any,
        tags: str | Iterable[str] | None = None,
        silent: bool = True,
        extra: Any | None = None,
    ) -> None:
        self._emit(
            level,
            message,
            *args,
            tags=tags,
            silent=silent,
            extra=extra,
        )

    def trace(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("TRACE", message, *args, **kwargs)

    def debug(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("DEBUG", message, *args, **kwargs)

    def info(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("INFO", message, *args, **kwargs)

    def json(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("INFO", to_json(message), *args, **kwargs)

    def success(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("SUCCESS", message, *args, **kwargs)

    def warning(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("WARNING", message, *args, **kwargs)

    def error(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("ERROR", message, *args, **kwargs)

    def critical(self, message: Any, *args: Any, **kwargs) -> None:
        self._emit("CRITICAL", message, *args, **kwargs)

    def exception(
        self,
        message: Any,
        *args: Any,
        tags: str | Iterable[str] | None = None,
        silent: bool = True,
        extra: Any | None = None,
    ) -> None:
        fmt_args, payload = self._extract_payload(message, args, extra)
        context: dict[str, Any] = {}
        normalized_tags = _normalize_tags(tags)
        if normalized_tags:
            context["tags"] = normalized_tags
        if payload is not None:
            context["payload"] = _json_safe(payload)
        if not silent:
            context["_notify"] = True
            context["_notify_type"] = "ERROR"

        target = self._logger.bind(**context) if context else self._logger
        try:
            target.opt(exception=True).error(message, *fmt_args)
        except Exception as exc:  # pylint: disable=broad-except
            self._fallback("ERROR", message, exc)

    def important(
        self,
        message: Any,
        *args: Any,
        tags: str | Iterable[str] | None = None,
        silent: bool = False,
        extra: Any | None = None,
    ) -> None:
        self._emit(
            "INFO",
            message,
            *args,
            tags=tags,
            silent=silent,
            extra=extra,
            notify_type="IMPORTANT",
        )

    def request(
        self,
        message: Any,
        *args: Any,
        tags: str | Iterable[str] | None = None,
        silent: bool = True,
        extra: Any | None = None,
    ) -> None:
        self._emit(
            "INFO",
            message,
            *args,
            tags=tags,
            silent=silent,
            extra=extra,
            notify_type="REQUEST",
        )

    def except_(self, message: Any, *args: Any, **kwargs) -> None:
        self.exception(message, *args, **kwargs)


log = AppLogger(logger)
setattr(AppLogger, "except", AppLogger.exception)


def add_external_sink(
    sink: Any,
    *,
    level: str | None = None,
    enqueue: bool = False,
    catch: bool = True,
) -> int:
    return logger.add(sink, level=level or _LEVEL, enqueue=enqueue, catch=catch)


def setup_logging(
    project: str | None = None,
    service: str | None = None,
    env: str | None = None,
    version: str | None = None,
    level: str | None = None,
    notify_token: str | None = None,
    notify_chat: str | int | None = None,
) -> None:
    global _PROJECT, _SERVICE, _ENV, _VERSION, _LEVEL
    if project:
        _PROJECT = project
    if service:
        _SERVICE = service
    if env:
        _ENV = env
    if version:
        _VERSION = version
    if level:
        _LEVEL = level

    setup_notify(token=notify_token, chat=notify_chat)

    logger.remove()
    logger.configure(patcher=_inject_context)
    logger.add(_json_sink, level=_LEVEL, enqueue=True, catch=True)
    logger.add(_notify_sink, level=_LEVEL, enqueue=True, catch=True)
