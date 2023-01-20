"""
Natural language processing functionality
"""

import re
from urllib.parse import unquote


TRANSLITERATION = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'kh',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'shch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'yu',
    'я': 'ya',
}


def get_form(count, variations):
    """ Get form of a noun with a number """

    count = abs(count)

    if count % 10 == 1 and count % 100 != 11:
        return variations[0]

    if count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        return variations[1]

    return variations[2]

def transliterate(data, separator=' '):
    """ Transliterate RU → EN """

    if data is None:
        return ''

    data = ''.join((
        i
        if 'a' <= i <= 'z' else
        TRANSLITERATION.get(i, separator)
    ) for i in unquote(data).strip().lower())
    data = re.sub(rf'{separator}{{2,}}', separator, data)

    return data

def to_letters(data, separator=''):
    """ To letters & numbers """

    if data is None:
        return ''

    data = re.sub(
        '[^a-zа-я0-9]+',
        ' ' if separator else '',
        unquote(data).lower()
    )
    if separator:
        data = data.strip().replace(' ', separator)

    return data

def to_url(data, separator='-'):
    """ To url format """

    if not data:
        return None

    data = ''.join((
        i
        if 'a' <= i <= 'z' or '0' <= i <= '9' else
        TRANSLITERATION.get(i, separator)
    ) for i in unquote(data).strip().lower())
    data = re.sub(rf'{separator}{{2,}}', separator, data)
    data = re.sub(rf'^{separator}', '', data)
    data = re.sub(rf'{separator}$', '', data)

    if not data:
        return None

    return data
