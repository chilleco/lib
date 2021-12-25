"""
https://www.epochconverter.com/
"""

from libdev.time import get_date, parse_time


def test_get_date():
    assert get_date(1633427647.018819) == '20211005'
    assert get_date(1633427647.018819, '%d.%m.%Y %H:%M:%S') == '05.10.2021 12:54:07'

def test_parse_time():
    assert parse_time('7.10.1998 7:00:00') == 907743600
    assert parse_time('7 октября 1998 года 12:00:00', tz=5) == 907743600
    assert parse_time('🕒 пн, 20 дек. 2021 г., 00:32:44 MSK') == 1639949564
