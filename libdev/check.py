"""
Checking functionality
"""


def fake_phone(value: str) -> bool:
    """ Check a phone for a test format """

    if value is None:
        return False

    value = str(value)

    return any(
        fake in value
        for fake in (
            '0000', '111', '222', '333', '444', '555', '666', '777', '888',
            '9999', '123', '987',
        )
    )

def fake_login(value: str) -> bool:
    """ Check a login / name / mail for a test format """

    if value is None:
        return False

    value = value.lower()

    return any(
        fake in value
        for fake in (
            'test', 'тест', 'check',
            'asd', 'qwe', 'rty', 'sdf', 'sfg', 'sfd', 'hgf', 'gfd',
            'qaz', 'wsx', 'edc', 'rfv',
            '111', '123',
            'ыва', 'фыв', 'йцу', 'орп',
        )
    )
