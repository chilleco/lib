"""
Numbers functionality
"""

import re
import math
from decimal import Decimal, InvalidOperation


_SUBSCRIPTS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


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


def pretty(
    value,
    decimals=None,
    sign=False,
    symbol="’",
    zeros=4,
    compress=None,
):
    """Decorate the number beautifully"""

    if value is None:
        return None

    # Handle decimals parameter first (takes precedence)
    if decimals is not None:
        # Use the original decimals logic for backward compatibility
        s = to_plain(abs(value))
        if "." in s:
            int_part = s.split(".", 1)[0]
            cur = len(int_part)
            target_decimals = max(0, decimals - cur)
            # Apply rounding first
            rounded_value = round(float(value), target_decimals)
            # If target_decimals is 0, convert to int for proper formatting
            if target_decimals == 0:
                rounded_value = int(rounded_value)
            # Then use compress_zeros without round parameter
            data = compress_zeros(rounded_value, zeros=zeros)
        else:
            data = compress_zeros(value, zeros=zeros)
    elif zeros is None and compress is None:
        # No compression or special formatting requested, use plain representation
        data = to_plain(value)
    else:
        # Use compress_zeros with specified parameters
        compress_zeros_args = {}

        if zeros is not None:
            compress_zeros_args["zeros"] = zeros

        if compress is not None:
            compress_zeros_args["round"] = compress

        data = compress_zeros(value, **compress_zeros_args)

    if data == "0":
        return "0"

    # Remove trailing zeros after decimal point for cleaner formatting
    if "." in data and data.rsplit(".", maxsplit=1)[-1] == "0":
        data = data.split(".", maxsplit=1)[0]

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


def to_plain(value) -> str:
    if value is None:
        return None
    try:
        if isinstance(value, str):
            d = Decimal(value)
        elif isinstance(value, float):
            d = Decimal(str(value))
        else:
            d = Decimal(value)

        s = format(d.normalize(), "f")

        if "." in s:
            s = s.rstrip("0").rstrip(".")
        if s == "-0":
            s = "0"
        return s
    except (InvalidOperation, ValueError, TypeError):
        return str(value)


def _round_to_decimals(x, decimals):
    """Helper function to round to specified decimal places"""
    if decimals <= 0:
        return float(int(x))
    return round(float(x), decimals)


def compress_zeros(x, zeros=2, round=None) -> str:
    """
    0.000012 -> '0.0₄12'
    1.000045 -> '1.0₄45'
    round: number of digits after the zero block (rounds).
    zeros: minimum count of consecutive zeros to compress (default: 2).
    """

    if x is None:
        return None

    # Store original string representation for rounding calculations
    original_str = None
    if isinstance(x, str):
        original_str = x.strip()
        x = original_str
        # Remove trailing zeros from string
        if "." in x:
            x = x.rstrip("0").rstrip(".")
        # Convert to appropriate numeric type
        try:
            if "." in x:
                x = float(x)
            else:
                x = int(x)
        except ValueError:
            return str(x)

    # Determine if original was float or int to preserve format
    is_float_type = isinstance(x, float) or (isinstance(x, str) and "." in str(x))

    # Handle rounding if specified
    if round is not None:
        # For rounding, use original string if available, otherwise convert to plain string
        if original_str and "." in original_str:
            s = original_str.lstrip("-")
        else:
            # Use to_plain to avoid scientific notation
            s = to_plain(abs(x))

        if "." in s:
            int_part, frac_part = s.split(".")
            # Count leading zeros in fractional part
            leading_zeros = 0
            for c in frac_part:
                if c == "0":
                    leading_zeros += 1
                else:
                    break

            # Count trailing zeros in fractional part
            trailing_zeros = 0
            for c in reversed(frac_part):
                if c == "0":
                    trailing_zeros += 1
                else:
                    break

            # Apply rounding logic
            if leading_zeros > 0:
                # If there are leading zeros, round after them (regardless of compression)
                total_decimals = leading_zeros + round
                x = _round_to_decimals(x, total_decimals)
            else:
                # No leading zeros, apply normal rounding
                x = _round_to_decimals(x, round)

    # Convert to string representation
    if isinstance(x, int) and not is_float_type:
        s = str(x)
    else:
        # For floats, use format that preserves trailing decimals when needed
        if x == int(x) and is_float_type:
            s = f"{int(x)}.0"
        else:
            s = str(float(x))
            # Remove scientific notation if present
            if "e" in s.lower():
                s = f"{float(x):.15f}".rstrip("0")
                if s.endswith("."):
                    s += "0"

    # Handle negative sign
    negative = s.startswith("-")
    if negative:
        s = s[1:]

    # Process compression
    if "." not in s:
        result = s
    else:
        int_part, frac_part = s.split(".")

        # Compress leading zeros in fractional part
        leading_zeros = 0
        for c in frac_part:
            if c == "0":
                leading_zeros += 1
            else:
                break

        # Compress trailing zeros in fractional part
        trailing_zeros = 0
        for c in reversed(frac_part):
            if c == "0":
                trailing_zeros += 1
            else:
                break

        # Apply compression
        if leading_zeros >= zeros:
            # Compress leading zeros
            remaining_frac = frac_part[leading_zeros:]
            result = f"{int_part}.0{str(leading_zeros).translate(_SUBSCRIPTS)}{remaining_frac}"
        elif trailing_zeros >= zeros and leading_zeros == 0:
            # Compress trailing zeros (but not if there are leading zeros)
            remaining_frac = frac_part[:-trailing_zeros]
            if remaining_frac:
                result = f"{int_part}.{remaining_frac}0{str(trailing_zeros).translate(_SUBSCRIPTS)}"
            else:
                result = f"{int_part}.0{str(trailing_zeros).translate(_SUBSCRIPTS)}"
        else:
            result = s

    return f"-{result}" if negative else result
