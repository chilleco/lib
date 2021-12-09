"""
Natural language processing functionality
"""

def get_form(count, variations):
    """ Get form of a noun with a number """

    count = abs(count)

    if count % 10 == 1 and count % 100 != 11:
        return variations[0]

    if count % 10 in (2, 3, 4) and count % 100 not in (12, 13, 14):
        return variations[1]

    return variations[2]

def format_time(sec):
    """ Format time in words by seconds """

    if abs(sec) >= 3 * 24 * 60 * 60: # 3 days
        time_def = round(sec / (24 * 60 * 60))
        delta = f"{time_def} {get_form(time_def, ('день', 'дня', 'дней'))}"

    elif abs(sec) >= 3 * 60 * 60:
        time_def = round(sec / (60 * 60))
        delta = f"{time_def} {get_form(time_def, ('час', 'часа', 'часов'))}"

    else:
        time_def = round(sec / 60)
        delta = (
            f"{time_def}"
            f" {get_form(time_def, ('минута', 'минуты', 'минут'))}"
        )

    return delta
