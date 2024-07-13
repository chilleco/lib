"""
Custom logger module
--------------------

Provides an extension to the Loguru logger with a custom methods

Usage:
    from libdev.log import log
    log.json({"event": "startup", "status": "success"})
"""

import sys
import atexit as _atexit

from loguru import _defaults
from loguru._logger import (
    Core as _Core,
    Logger as _Logger,
)

from .doc import to_json


class Logger(_Logger):
    """
    Extends the Loguru logger to include a method for logging JSON formatted messages
    """

    def json(self, data):
        """Log a message in JSON format"""
        self.info(to_json(data))


log = Logger(
    core=_Core(),
    exception=None,
    depth=0,
    record=False,
    lazy=False,
    colors=False,
    raw=False,
    capture=True,
    patchers=[],
    extra={},
)

if _defaults.LOGURU_AUTOINIT and sys.stderr:
    log.add(sys.stderr)
_atexit.register(log.remove)


__all__ = (
    "log",
    "Logger",
)
