"""Centralized configuration loader for LibDev consumers.

This module mirrors the behavior documented in `LIBDEV_DOCUMENTATION.md`:
it first ingests a project level ``sets.json`` file, then overlays values
from ``.env`` (via ``python-dotenv``) by translating dotted keys to
``UPPER_SNAKE_CASE`` environment variables. Use the helpers below instead of
calling ``os.getenv`` throughout the codebase so the hierarchy stays uniform.
"""

import os
import json

from dotenv import load_dotenv


if os.path.isfile("sets.json"):
    with open("sets.json", "r", encoding="utf-8") as file:
        sets = json.loads(file.read())
else:
    sets = {}

if os.path.isfile(".env"):
    load_dotenv()


def cfg(name, default=None):
    """Return a config value stored in ``sets.json``/``.env``.

    The lookup walks dotted paths inside the parsed JSON structure and, when a
    key is missing, falls back to an environment variable where dots are
    replaced with underscores and the string is upper-cased (``api.base`` →
    ``API_BASE``). Environment values are JSON-decoded automatically so booleans
    and numeric strings turn into native Python types. ``default`` is returned
    when a key is absent in both sources.
    """

    keys = name.split(".")
    data = sets

    for key in keys:
        if key not in data:
            break
        data = data[key]
    else:
        return data

    name = name.replace(".", "_").upper()
    value = os.getenv(name, default)

    if value:
        try:
            value = json.loads(value)
        except (json.decoder.JSONDecodeError, TypeError):
            pass

    return value


def set_cfg(name, value):
    """Mutate the in-memory ``sets`` dictionary for tests or overrides.

    Writes scoped dotted keys back into the ``sets`` mapping without touching
    disk. This mirrors the behavior in consumer repos that temporarily adjust
    configuration for integration tests or AI agents. Changes live only for the
    current process and should be reset between tests.
    """

    array_name = name.split(".")
    dictionary = {}
    tmp_dict = {}

    if len(array_name) == 1:
        sets[name] = value
        return

    index = len(array_name) - 1
    dictionary[array_name[index]] = value
    index -= 1
    while index > 0:
        if array_name[index] in sets:
            tmp_dict[array_name[index]].append(dictionary)
        else:
            tmp_dict[array_name[index]] = dictionary
        dictionary = tmp_dict
        tmp_dict = {}
        index -= 1

    if array_name[0] not in sets:
        sets[array_name[0]] = dictionary
    else:
        sets[array_name[0]].update(dictionary)
