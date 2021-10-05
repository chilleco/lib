"""
Functionality of getting configuration
"""

import json


with open('sets.json', 'r', encoding='utf-8') as file:
    sets = json.loads(file.read())


def cfg(name, default=None):
    """ Get config value by key """

    keys = name.split('.')
    data = sets

    for key in keys:
        if key not in data:
            return default

        data = data[key]

    return data
