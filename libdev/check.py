"""
Checking functionality
"""

import re
from typing import Union


def check_phone(value: Union[str, int]) -> bool:
    """ Check phone validity """
    if isinstance(value, int):
        value = str(value)
    return re.match(r'^\(?\+?[0-9\s\-\(\)./]{7,30}$', value) is not None

def fake_phone(value: str) -> bool:
    """ Check a phone for a test format """

    if value is None:
        return False

    value = str(value)

    return any(
        fake in value
        for fake in (
            '0000', '1111', '2222', '3333', '4444', '5555', '6666', '7777',
            '8888', '9999', '1234', '2345', '3456', '4567', '5678', '6789',
            '9876', '8765', '7654', '6543', '5432', '4321',
        )
    )

def fake_login(value: str) -> bool:
    """ Check a login / name for a test format """

    if value is None:
        return False

    value = value.lower()

    return any(
        fake in value
        for fake in (
            'test', 'тест', 'check',
            'asd', 'qwe', 'rty', 'sdf', 'sfg', 'sfd', 'hgf', 'gfd',
            'qaz', 'wsx', 'edc', 'rfv',
            'lalala', 'lolkek',
            '111', '123',
            'ыва', 'фыв', 'йцу', 'орп',
        )
    )

def check_mail(value: str) -> bool:
    """ Check mail validity """
    if value is None:
        return False
    return re.match(r'.{1,64}@.{1,63}\..{1,15}', value) is not None

def fake_mail(value: str) -> bool:
    """ Check a mail for a test format """
    return not check_mail(value) or fake_login(value)

def check_url(data: str) -> bool:
    """ Check url validity """
    if data is None:
        return False
    return re.match(r"^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$", data) is not None

def get_last_url(data: str) -> str:
    """ Get the last part of a URL """
    if data is None:
        return None
    return re.sub(r'.*/(.+?)/?$', r'\1', data)
