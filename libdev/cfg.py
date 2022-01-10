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

    if not sets or name.isupper():
        name = name.replace('.', '_').upper()
        return os.getenv(name, default)

    keys = name.split('.')
    data = sets

    for key in keys:
        if key not in data:
            return default

        data = data[key]

    return data
