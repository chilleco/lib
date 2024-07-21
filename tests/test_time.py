"""
https://www.epochconverter.com/
"""

import datetime

from libdev.time import (
    get_time,
    get_date,
    decode_time,
    decode_date,
    parse_time,
    format_delta,
    get_midnight,
    get_month_start,
    get_next_day,
    get_next_month,
)


def test_get_time():
    assert get_time(1641061152.467365) == "01.01.2022 18:19:12"
    assert get_time(1641061152, tz=3) == "01.01.2022 21:19:12"
    assert get_time(1641061152, template="%Y%m%d%H%M%S", tz=3) == "20220101211912"

    tz = datetime.timezone(datetime.timedelta(hours=0), name="UTC")
    assert (
        get_time(
            datetime.datetime(year=2018, month=7, day=16, tzinfo=tz),
            template="%d.%m.%Y",
        )
        == "16.07.2018"
    )


def test_get_date():
    assert get_date(1641061152.4) == "01.01.2022"


def test_decode_time():
    assert decode_time("") == None
    assert decode_time("01.01.2022 21:19:12", tz=3) == 1641061152
    assert decode_time("01.01.2022 18:19:12") == 1641061152
    assert decode_time("2024-10-07", "%Y-%m-%d", 4) == 1728244800


def test_decode_date():
    assert decode_date("01.01.2022", tz=3) == 1640984400


def test_parse_time():
    assert parse_time("07.10.1998", tz=3) == 907707600
    assert parse_time("7.10.1998 7:00:00") == 907743600
    assert parse_time("07.10.1998 12:00", 3) == 907750800
    # custom timezone
    assert parse_time("7 октября 1998 года 12:00:00", tz=5) == 907743600
    # extra symbols
    assert parse_time("🕒 пн, 20 дек. 2021 г., 00:32:44 MSK") == 1639949564
    # case: r'сен' + сент → 09.т
    assert parse_time("1 сент 2021 года 00:00:00") == 1630454400
    # min symbols
    assert parse_time("010119700:0:0") == 0
    assert parse_time("1мая19700:0:0") == 10368000
    # before time started
    assert parse_time("1мая10000:0:0") == -30599856000
    assert parse_time("июнь 2020", tz=3) == 1590958800
    assert parse_time("06.2020") == 1590969600
    assert parse_time("2023") == 1672531200


def test_parse_wrong_time():
    assert parse_time("") == None
    assert parse_time("1") == None
    assert parse_time("0101197000000") == None


def test_format_delta():
    assert format_delta(0, locale="ru") == "0 секунд"
    assert format_delta(30, locale="ru") == "30 секунд"
    assert format_delta(31, locale="ru") == "31 секунда"
    assert format_delta(59, locale="ru") == "59 секунд"
    assert format_delta(60, locale="ru") == "60 секунд"
    assert format_delta(180, locale="ru") == "180 секунд"
    assert format_delta(181, locale="ru") == "3 минуты"
    assert format_delta(300, locale="ru") == "5 минут"
    assert format_delta(10799, locale="ru") == "180 минут"
    assert format_delta(10800, locale="ru") == "3 часа"
    assert format_delta(12345, locale="ru") == "3 часа"
    assert format_delta(259200, locale="ru") == "3 дня"
    assert format_delta(259201, locale="ru") == "3 дня"
    assert format_delta(1036800, locale="ru") == "12 дней"
    assert format_delta(8726400, locale="ru") == "101 день"
    assert format_delta(-1, locale="ru") == "-1 секунда"
    assert format_delta(-181, locale="ru") == "-3 минуты"
    assert format_delta(-432000, locale="ru") == "-5 дней"
    assert format_delta(1, locale="en") == "1 second"
    assert format_delta(1000, locale="en") == "17 minutes"
    assert format_delta(173000, True, "en") == "48h"
    assert format_delta(259500, True, "en") == "3d"
    assert format_delta(173000, locale="en") == "48 hours"


def test_format_delta_short():
    assert format_delta(0, short=True, locale="ru") == "0сек"
    assert format_delta(1, short=True, locale="ru") == "1сек"
    assert format_delta(180, short=True, locale="ru") == "180сек"
    assert format_delta(181, short=True, locale="ru") == "3мин"
    assert format_delta(18000, short=True, locale="ru") == "5ч"
    assert format_delta(1814400, short=True, locale="ru") == "21д"


def test_get_midnight():
    assert get_midnight(1721597607.049283) == 1721520000
    assert get_midnight(1721597607, tz=3) == 1721595600
    assert get_midnight(1704056399, tz=3) == 1703970000


def test_get_month_start():
    assert get_month_start(1704060061.049283) == 1701388800
    assert get_month_start(1704060061, tz=3) == 1704056400


def test_get_next_day():
    assert get_next_day(1704060061) == 1704067200
    assert get_next_day(1704060061, tz=3) == 1704142800


def test_get_next_month():
    assert get_next_month(1703980800) == 1704067200
    assert get_next_month(1703970000, tz=3) == 1704056400
