"""
Time functionality
"""

import time
import datetime
# import pytz
import re


MONTHS = {
    '01': ('январь', 'января', 'янв'),
    '02': ('февраль', 'февраля', 'фев', 'февр'),
    '03': ('март', 'марта', 'мар'),
    '04': ('апрель', 'апреля', 'апр'),
    '05': ('май', 'мая'),
    '06': ('июнь', 'июня', 'июн'),
    '07': ('июль', 'июля', 'июл'),
    '08': ('август', 'августа', 'авг'),
    '09': ('сентябрь', 'сентября', 'сен', 'сент'),
    '10': ('октябрь', 'октября', 'окт'),
    '11': ('ноябрь', 'ноября', 'ноя', 'нояб'),
    '12': ('декабрь', 'декабря', 'дек'),
}
DAYS_OF_WEEK = (
    'пн',
    'вт',
    'ср',
    'чт',
    'пт',
    'сб',
    'вс',
)


def get_date(text, template='%Y%m%d'):
    """ Get date from timestamp """
    # TODO: get_date -> get_time
    # TODO: change template
    return time.strftime(template, time.localtime(text))

def parse_time(data, tz=0):
    """ Parse time """

    data = data.lower()

    # Cut special characters
    data = re.sub(r'[^a-zа-я0-9:.]', '', data)

    # Cut the day of the week
    for day in DAYS_OF_WEEK:
        data = data.replace(day, '')

    # Parse day
    if not data[1].isdigit():
        data = '0' + data
    if data[2] != '.':
        data = data[:2] + '.' + data[2:]

    # Parse month
    for month_number, month_names in MONTHS.items():
        for month_name in month_names:
            data = data.replace(month_name, month_number)
    if data[5] != '.':
        data = data[:5] + '.' + data[5:]

    # Parse year
    data = data.replace('года', ' ')
    data = data.replace('год', ' ')
    data = data.replace('г.', ' ')
    if data[10] != ' ':
        data = data[:10] + ' ' + data[10:]

    # Timezone
    if 'msk' in data:
        data = data.replace('msk', '')
        tz_delta = 3
        # tz = pytz.timezone('Europe/Moscow')
    else:
        tz_delta = tz
        # tz = pytz.utc

    data = datetime.datetime.strptime(data, '%d.%m.%Y %H:%M:%S')
    data = data.replace(
        tzinfo=datetime.timezone(datetime.timedelta(hours=tz_delta))
    )

    return int(data.timestamp())
