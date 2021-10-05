from libdev.time import get_date


def test_get_date():
    assert get_date(1633427647.018819) == '20211005'
    assert get_date(1633427647.018819, '%d.%m.%Y %H:%M:%S') == '05.10.2021 12:54:07'
