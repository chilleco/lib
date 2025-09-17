"""
Numbers functionality
"""

import re
import math
from decimal import Decimal, ROUND_HALF_UP


_SUBSCRIPTS = {
    "0": "₀",
    "1": "₁",
    "2": "₂",
    "3": "₃",
    "4": "₄",
    "5": "₅",
    "6": "₆",
    "7": "₇",
    "8": "₈",
    "9": "₉",
}


def is_float(value: str) -> bool:
    """Check value for float"""

    try:
        float(value)
    except (ValueError, TypeError):
        return False

    return True


def to_num(value) -> bool:
    """Convert value to int or float"""

    if value is None:
        return None

    if isinstance(value, str):
        value = float(value.strip())

    if not value % 1:
        value = int(value)

    return value


def to_int(value) -> int:
    """Choose only decimal"""

    if not value:
        return 0

    return int(re.sub(r"\D", "", str(value)))


def get_float(value) -> list:
    """Get a list of floats"""

    if value is None:
        return []

    numbers = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", value)
    return [float(number) for number in numbers]


def find_decimals(value):
    """Get count of decimal"""

    if isinstance(value, str):
        while value[-1] == "0":
            value = value[:-1]

    return abs(Decimal(str(value)).as_tuple().exponent)


def get_whole(value):
    """Get whole view of a number"""

    if isinstance(value, int) or (isinstance(value, str) and "." not in value):
        # NOTE: to remove 0 in the start of the string
        return str(int(value))

    # NOTE: float for add . to int & support str
    value = float(value)

    # NOTE: to avoid the exponential form of the number
    return f"{value:.{find_decimals(value)}f}"


def simplify_value(value, decimals=4):
    """Get the significant part of a number"""

    if value is None:
        return None

    value = get_whole(value)
    if "." not in value:
        value += "."

    whole, fractional = value.split(".")

    if value[0] == "-":
        sign = "-"
        whole = whole[1:]
    else:
        sign = ""

    if whole != "0":
        digit = len(whole)
        value = whole + "." + fractional[: max(0, decimals - digit)]

    else:
        offset = 0
        while fractional and fractional[0] == "0":
            offset += 1
            fractional = fractional[1:]

        value = "0." + "0" * offset + fractional[:decimals]

    while value[-1] == "0":
        value = value[:-1]

    if value[-1] == ".":
        value = value[:-1]

    return sign + value


def pretty(value, decimals=None, sign=False, symbol="’"):
    """Decorate the number beautifully"""

    if value is None:
        return None

    data = str(float(value))

    if decimals is not None:
        cur = len(data.split(".", maxsplit=1)[0])
        data = str(round(value, max(0, decimals - cur)))

    if data.rsplit(".", maxsplit=1)[-1] == "0":
        data = data.split(".", maxsplit=1)[0]

    if data == "0":
        return "0"

    if symbol:
        data = add_radix(data, symbol)

    if sign:
        if data[0] != "-":
            data = "+" + data

    return data


def add_sign(value):
    """Add sign to a number"""

    if value is None:
        return None

    sign = ""

    if float(value) > 0:
        sign = "+"
    elif value == 0:
        value = abs(value)

    return f"{sign}{get_whole(value)}"


def add_radix(value, symbol="’"):
    """Add radix to a number"""

    if value is None:
        return None

    value = str(value)

    if "." in value:
        integer, fractional = value.split(".")
    else:
        integer = value
        fractional = ""

    if integer[0] == "-":
        sign = "-"
        integer = integer[1:]
    # elif integer[0] == '+':
    #     sign = '+'
    #     integer = integer[1:]
    else:
        sign = ""

    data = ""
    ind = 0
    for i in integer[::-1]:
        if ind and ind % 3 == 0:
            data = symbol + data
        ind += 1
        data = i + data

    data = sign + data
    if fractional:
        data += "." + fractional

    return data


def mul(x, y):
    """Multiply fractions correctly"""
    if x is None or y is None:
        return None
    return float(Decimal(str(x)) * Decimal(str(y)))


def div(x, y):
    """Divide fractions correctly"""
    if x is None or y is None:
        return None
    return float(Decimal(str(x)) / Decimal(str(y)))


def add(x, y):
    """Subtract fractions correctly"""
    if x is None or y is None:
        return None
    return float(Decimal(str(x)) + Decimal(str(y)))


def sub(x, y):
    """Subtract fractions correctly"""
    if x is None or y is None:
        return None
    return float(Decimal(str(x)) - Decimal(str(y)))


def to_step(value, step=1, side=False):
    """Change value step"""

    if value is None:
        return None

    value = div(value, step)
    if side:
        value = math.ceil(value)
    else:
        value = math.floor(value)
    value = mul(value, step)

    if step >= 1:
        value = int(value)

    return value


from decimal import Decimal

_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def _to_plain(d: Decimal) -> str:
    """Плейн-строка без экспоненты и без хвостовых нулей."""
    sign, digits, exp = d.as_tuple()
    ds = "".join(map(str, digits)) or "0"
    if exp >= 0:
        int_part = ds + "0" * exp
        frac = ""
    else:
        split = len(ds) + exp
        if split > 0:
            int_part, frac = ds[:split], ds[split:]
        else:
            int_part, frac = "0", "0" * (-split) + ds
    int_part = int_part.lstrip("0") or "0"
    frac = frac.rstrip("0")
    return f"{int_part}.{frac}" if frac else int_part


def compress_zeros(x, round=None) -> str:
    """
    0.000012 -> '0.0₄12'
    round: кол-во цифр после блока нулей (округляет).
    """

    if x is None:
        return None

    d = Decimal(str(x))
    if d == 0:
        return "0"
    s_abs = _to_plain(abs(d))

    # если нужна точность "после нулей" — сначала считаем длину нулей
    if round is not None and "." in s_abs:
        frac0 = s_abs.split(".", 1)[1]
        k0 = 0
        for c in frac0:
            if c == "0":
                k0 += 1
            else:
                break
        total_places = k0 + int(round)
        if total_places > 0:
            d = abs(d).quantize(Decimal(1).scaleb(-total_places))
        else:
            d = abs(d)  # нечего округлять
        s_abs = _to_plain(d)

    # сжатие
    if "." not in s_abs:
        out = s_abs
    else:
        int_part, frac = s_abs.split(".", 1)
        k = 0
        for c in frac:
            if c == "0":
                k += 1
            else:
                break
        if k >= 2:
            out = f"{int_part}.0{str(k).translate(_SUB)}{frac[k:]}"
        else:
            out = s_abs

    return f"-{out}" if x and Decimal(str(x)) < 0 else out
