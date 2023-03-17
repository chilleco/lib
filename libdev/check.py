"""
Checking functionality
"""

import re


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
