"""
Functionality of getting configuration
"""

import os
import json

from dotenv import load_dotenv


if os.path.isfile('sets.json'):
    with open('sets.json', 'r', encoding='utf-8') as file:
        sets = json.loads(file.read())
else:
    sets = {}

if os.path.isfile('.env'):
    load_dotenv()


def cfg(name, default=None):
    """ Get config value by key """

    # NOTE: upper → not to mix when we need it in such a register and it is not
    if name not in sets and name.isupper():
        name = name.replace('.', '_').upper()
        value = os.getenv(name, default)

        if value:
            try:
                value = json.loads(value)
            except (json.decoder.JSONDecodeError, TypeError):
                pass

        return value

    keys = name.split('.')
    data = sets

    for key in keys:
        if key not in data:
            return default

        data = data[key]

    return data

def set_cfg(name, value):
    """ Set config value """
    sets[name] = value
