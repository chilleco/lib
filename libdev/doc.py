"""Utility helpers for dealing with document/JSON serialization.

These functions are referenced by the integration guide to make sure assets
and structured logs look the same across repositories (e.g., ``log.json`` uses
``to_json`` under the hood).
"""

import base64
import json


def to_base64(image, mime="image/jpg"):
    """Return a ``data:`` URL for the given file-like ``image``.

    Reads the stream, base64-encodes the bytes, and prefixes it with the MIME
    Type so downstream clients (frontends, bots) can embed the payload directly
    without touching disk.
    """
    data = base64.b64encode(image.read())
    return f"data:{mime};base64,{data.decode('utf-8')}"


def to_json(data):
    """Serialize ``data`` to a UTF-8 friendly JSON string.

    Uses tab indentation and ``ensure_ascii=False`` to preserve Cyrillic or
    emoji content mentioned in ``LIBDEV_DOCUMENTATION.md``.
    """
    return json.dumps(data, indent="\t", ensure_ascii=False)
