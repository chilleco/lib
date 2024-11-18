"""
Time functionality
"""

# TODO: Учитывать летнее / зимнее время в прошлых датах, которого теперь нет

import time
import datetime

# import pytz
import re

from .lang import get_form


MONTHS = {
    "01": ("январь", "января", "янв"),
    "02": ("февраль", "февраля", "февр", "фев"),
    "03": ("март", "марта", "мар"),
    "04": ("апрель", "апреля", "апр"),
    "05": ("май", "мая"),
    "06": ("июнь", "июня", "июн"),
    "07": ("июль", "июля", "июл"),
    "08": ("август", "августа", "авг"),
    "09": ("сентябрь", "сентября", "сент", "сен"),
    "10": ("октябрь", "октября", "окт"),
    "11": ("ноябрь", "ноября", "нояб", "ноя"),
    "12": ("декабрь", "декабря", "дек"),
}
DAYS_OF_WEEK = (
    "пн",
    "вт",
    "ср",
    "чт",
    "пт",
    "сб",
    "вс",
)


def to_tz(hours):
    """
    Create a timezone object with the specified offset in hours.

    Args:
        hours (int): The timezone offset in hours (e.g., 3 for UTC+3 or -5 for UTC-5).

    Returns:
        datetime.timezone: A timezone object with the specified offset.
    """
    return datetime.timezone(datetime.timedelta(hours=hours))


def get_time(data=None, template="%d.%m.%Y %H:%M:%S", tz=0):
    """Get time from timestamp"""

    if data is None:
        data = time.time()
    if isinstance(data, str):
        return data

    # TODO: smart TZ

    if isinstance(data, datetime.datetime):
        data = data.timestamp()

    return time.strftime(template, time.gmtime(data + tz * 3600))


def get_date(data=None, template="%d.%m.%Y", tz=0):
    """Get date from timestamp"""
    return get_time(data, template, tz)


def decode_time(data=None, template="%d.%m.%Y %H:%M:%S", tz=0):
    """Get timestamp from time"""

    if not data:
        return None
    if isinstance(data, int):
        return data

    try:
        data = datetime.datetime.strptime(data, template)
    except ValueError:
        return None

    data = data.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=tz)))

    return int(data.timestamp())


def decode_date(data=None, template="%d.%m.%Y", tz=0):
    """Get timestamp from date"""
    return decode_time(data, template, tz)


# pylint: disable=too-many-branches,too-many-statements
def parse_time(data: str, tz=0):
    """Parse time"""

    # TODO: 16 year -> 2016 year

    data = data.lower()

    # Cut special characters
    data = re.sub(r"[^a-zа-я0-9:.]", "", data)

    # Cut the day of the week
    for day in DAYS_OF_WEEK:
        data = data.replace(day, "")

    data = data.strip()

    if len(data) < 4:
        return None

    for month_number, month_names in MONTHS.items():
        for month_name in month_names:
            if month_name in data:
                ind = data.index(month_name)
                data = data.replace(month_name, month_number)
                day = re.sub(r"[^0-9]", "", data[:ind])
                if day:
                    data = day + "." + data[ind:]
                else:
                    data = "01." + data[ind:]
                break
        else:
            continue
        break
    else:
        if len(data) != 8:
            proc = True
            if ":" in data:
                if len(re.sub(r"[^0-9]", "", data[: data.index(":") - 2])) >= 6:
                    proc = False
            if proc:
                if "." not in data:
                    data = "01." + data
                if data.count(".") < 2:
                    data = "01." + data

    if ":" not in data and len(data) < 15 and len(re.sub(r"[^0-9]", "", data)) <= 8:
        data += "00:00:00"

    # Parse day
    if not data[1].isdigit():
        data = "0" + data
    if data[2] != ".":
        data = data[:2] + "." + data[2:]

    # Parse month
    if data[5] != ".":
        data = data[:5] + "." + data[5:]

    # Parse year
    data = data.replace("года", " ")
    data = data.replace("год", " ")
    data = data.replace("г.", " ")
    if data[10] != " ":
        data = data[:10] + " " + data[10:]

    # Timezone
    if "msk" in data:
        data = data.replace("msk", "")
        tz_delta = 3
        # tz = pytz.timezone('Europe/Moscow')
    else:
        tz_delta = tz
        # tz = pytz.utc

    colon_count = data.count(":")
    if colon_count == 0 or colon_count > 2:
        return None
    if colon_count == 1:
        data += ":00"

    try:
        data = datetime.datetime.strptime(data, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        return None

    data = data.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=tz_delta)))

    return int(data.timestamp())


def format_delta(sec, short=False, locale="en"):
    """Format time delta in words by seconds"""

    if abs(sec) >= 259200:  # 3 days
        time_def = round(sec / (24 * 60 * 60))
        delta = f"{time_def}"

        if locale == "ru":
            if short:
                delta += "д"
            else:
                delta += f" {get_form(time_def, ('день', 'дня', 'дней'))}"
        else:
            if short:
                delta += "d"
            else:
                if time_def == 1:
                    delta += " day"
                else:
                    delta += " days"

    elif abs(sec) >= 10800:  # 3 hours
        time_def = round(sec / (60 * 60))
        delta = f"{time_def}"

        if locale == "ru":
            if short:
                delta += "ч"
            else:
                delta += f" {get_form(time_def, ('час', 'часа', 'часов'))}"
        else:
            if short:
                delta += "h"
            else:
                if time_def == 1:
                    delta += " hour"
                else:
                    delta += " hours"

    elif abs(sec) > 180:  # 3 min
        time_def = round(sec / 60)
        delta = f"{time_def}"

        if locale == "ru":
            if short:
                delta += "мин"
            else:
                delta += f" {get_form(time_def, ('минута', 'минуты', 'минут'))}"
        else:
            if short:
                delta += "min"
            else:
                if time_def == 1:
                    delta += " minute"
                else:
                    delta += " minutes"

    else:
        time_def = int(sec)
        delta = f"{time_def}"

        if locale == "ru":
            if short:
                delta += "сек"
            else:
                delta += f" {get_form(time_def, ('секунда', 'секунды', 'секунд'))}"
        else:
            if short:
                delta += "s"
            else:
                if time_def == 1:
                    delta += " second"
                else:
                    delta += " seconds"

    return delta


def get_midnight(timestamp=None, tz=0):
    """
    Get the start of the day (midnight) for a given timestamp in a specified timezone.

    Args:
        timestamp (float): The original timestamp (in seconds since epoch).
        tz_offset_hours (int): The timezone offset in hours (e.g., 3 for UTC+3).

    Returns:
        float: The timestamp for the start of the day (midnight) in the specified timezone.
    """
    if timestamp is None:
        timestamp = time.time()
    dt_local = datetime.datetime.fromtimestamp(timestamp, tz=to_tz(tz))
    start_day = dt_local.replace(hour=0, minute=0, second=0, microsecond=0)
    return int(start_day.timestamp())


def get_month_start(timestamp=None, tz=0):
    """
    Get the start of the month (midnight on the first day of the month) for a given timestamp in a specified timezone.

    Args:
        timestamp (float): The original timestamp (in seconds since epoch). Defaults to the current time if None.
        tz (int): The timezone offset in hours (e.g., 3 for UTC+3).

    Returns:
        float: The timestamp for the start of the month in the specified timezone.
    """
    if timestamp is None:
        timestamp = time.time()
    dt_local = datetime.datetime.fromtimestamp(timestamp, tz=to_tz(tz))
    start_month = dt_local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return int(start_month.timestamp())


def get_next_day(timestamp=None, tz=0):
    """
    Get the start of the next day (midnight) for a given timestamp in a specified timezone.

    Args:
        timestamp (float): The original timestamp (in seconds since epoch). Defaults to the current time if None.
        tz (int): The timezone offset in hours (e.g., 3 for UTC+3).

    Returns:
        float: The timestamp for the start of the next day (midnight) in the specified timezone.
    """
    if timestamp is None:
        timestamp = time.time()
    dt_local = datetime.datetime.fromtimestamp(timestamp, tz=to_tz(tz))
    next_day = (dt_local + datetime.timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    return int(next_day.timestamp())


# TODO: get previous month (params=-1 +1)
def get_next_month(timestamp=None, tz=0):
    """
    Get the start of the next month (midnight on the first day of the next month) for a given timestamp in a specified timezone.

    Args:
        timestamp (float): The original timestamp (in seconds since epoch). Defaults to the current time if None.
        tz (int): The timezone offset in hours (e.g., 3 for UTC+3).

    Returns:
        float: The timestamp for the start of the next month in the specified timezone.
    """

    if timestamp is None:
        timestamp = time.time()

    dt_local = datetime.datetime.fromtimestamp(timestamp, tz=to_tz(tz))

    if dt_local.month == 12:
        next_month = dt_local.replace(
            year=dt_local.year + 1,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
    else:
        next_month = dt_local.replace(
            month=dt_local.month + 1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

    return int(next_month.timestamp())
