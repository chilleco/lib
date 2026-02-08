"""
Telegram notification transport for logging alerts.
"""

from __future__ import annotations

import json
import sys
from typing import Any
from urllib import parse as urllib_parse
from urllib import request as urllib_request

from .cfg import cfg


_NOTIFY_TOKEN: str | None = None
_NOTIFY_CHAT: str | int | None = None

_TYPE_SYMBOLS = {
    "DEBUG": "💬",
    "INFO": "🟢",
    "WARNING": "⚠️",
    "ERROR": "❗️",
    "CRITICAL": "‼️",
    "EXCEPT": "‼️",
    "EXCEPTION": "‼️",
    "IMPORTANT": "✅",
    "REQUEST": "🛎",
}

_MARKDOWN_V2_SPECIALS = set("_[]()~`>#+-=|{}.!*")


def _as_float(value: Any, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


_NOTIFY_TIMEOUT = _as_float(cfg("log.notify_timeout"), 3.0)


def _json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    return str(value)


def _safe_json(value: Any) -> str:
    try:
        return json.dumps(_json_safe(value), ensure_ascii=False)
    except Exception:  # pylint: disable=broad-except
        return str(value)


def _escape_markdown_v2(text: Any) -> str:
    source = str(text)
    escaped: list[str] = []
    for char in source:
        if char == "\\" or char in _MARKDOWN_V2_SPECIALS:
            escaped.append("\\" + char)
        else:
            escaped.append(char)
    return "".join(escaped)


def _notify_enabled() -> bool:
    return bool(_NOTIFY_TOKEN and _NOTIFY_CHAT)


def _build_extra_lines(payload: Any) -> list[str]:
    if not payload:
        return []

    lines: list[str] = [""]

    if isinstance(payload, dict):
        for key, value in payload.items():
            if value is None or value == "":
                continue
            lines.append(_escape_markdown_v2(f"{key} = {_safe_json(value)}"))
    else:
        lines.append(_escape_markdown_v2(_safe_json(payload)))

    return lines


def _build_notify_text(
    project: str,
    service: str,
    env: str,
    record: dict[str, Any],
    error_payload: dict[str, Any],
) -> str:
    notify_type = str(
        record["extra"].get("_notify_type") or record["level"].name or "INFO"
    ).upper()
    symbol = _TYPE_SYMBOLS.get(notify_type, _TYPE_SYMBOLS["INFO"])

    request_id = record["extra"].get("request_id")
    trace_id = record["extra"].get("trace_id")
    tags = record["extra"].get("tags")
    payload = record["extra"].get("payload")

    lines: list[str] = [
        f"{symbol} {(env or '').upper()} {notify_type}",
        f"{_escape_markdown_v2(project)} / {env} / {_escape_markdown_v2(service)}",
        "",
    ]
    if record.get("message"):
        lines.append(f"*{_escape_markdown_v2(record["message"])}*")

    lines.extend(_build_extra_lines(payload))

    if error_payload.get("message"):
        lines.append("")
        lines.append(_escape_markdown_v2(error_payload["message"]))

    lines.append("")
    if tags:
        if isinstance(tags, (list, tuple, set)):
            tags_text = " ".join(f"#{tag}" for tag in tags)
        else:
            tags_text = str(tags)
        lines.append(_escape_markdown_v2(tags_text))

    if request_id:
        lines.append(f"`{request_id}`")
    if trace_id:
        lines.append(f"trace_id: `{trace_id}`")

    text = "\n".join(lines)
    if len(text) > 3800:
        return text[:3797] + "..."
    return text


def _send_notify(project: str, service: str, text: str) -> None:
    if not _notify_enabled():
        return
    data = urllib_parse.urlencode(
        {
            "chat_id": str(_NOTIFY_CHAT),
            "text": text,
            "parse_mode": "MarkdownV2",
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")
    req = urllib_request.Request(
        f"https://api.telegram.org/bot{_NOTIFY_TOKEN}/sendMessage",
        data=data,
        method="POST",
    )
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib_request.urlopen(req, timeout=_NOTIFY_TIMEOUT):
            return
    except Exception as exc:  # pylint: disable=broad-except
        sys.stderr.write(
            json.dumps(
                {
                    "project": project,
                    "service": service,
                    "level": "ERROR",
                    "msg": "notify failed",
                    "error": str(exc),
                },
                ensure_ascii=True,
            )
            + "\n"
        )


def setup_notify(
    token: str | None = None,
    chat: str | int | None = None,
) -> None:
    global _NOTIFY_TOKEN, _NOTIFY_CHAT
    _NOTIFY_TOKEN = token
    _NOTIFY_CHAT = chat


def notify_log_record(
    project: str,
    service: str,
    env: str,
    record: dict[str, Any],
    error_payload: dict[str, Any],
) -> None:
    if not _notify_enabled():
        return
    _send_notify(
        project,
        service,
        _build_notify_text(
            project,
            service,
            env,
            record,
            error_payload,
        ),
    )
