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

    keys = name.split('.')
    data = sets

    for key in keys:
        if key not in data:
            break
        data = data[key]
    else:
        return data

    name = name.replace('.', '_').upper()
    value = os.getenv(name, default)

    if value:
        try:
            value = json.loads(value)
        except (json.decoder.JSONDecodeError, TypeError):
            pass

    return value


def set_cfg(name, value):
    """ Set config value """
    array_name = name.split(".")
    dictionary = {}
    tmp_dict = {}
    if len(array_name) == 1:
        sets[name] = value
        return
    else:
        index = len(array_name) - 1
        dictionary[array_name[index]] = value
        index -= 1 
        while index > 0:
            tmp_dict[array_name[index]] = dictionary
            dictionary = tmp_dict
            tmp_dict = {}
            index -= 1        
    sets[array_name[0]] = dictionary
