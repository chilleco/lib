from libdev.num import (
    is_float,
    to_num,
    to_int,
    get_float,
    find_decimals,
    get_whole,
    simplify_value,
    add_sign,
    add_radix,
    to_step,
    add,
    pretty,
    to_plain,
    compress_zeros,
)


def test_float():
    assert is_float("0") == True
    assert is_float("-0.") == True
    assert is_float("-.0") == True
    assert is_float(".1") == True
    assert is_float("-.2") == True
    assert is_float("-3.") == True
    assert is_float("4.0") == True
    assert is_float("-5.678") == True
    assert is_float("6.7x") == False
    assert is_float("-7..8") == False
    assert is_float("") == False
    assert is_float(".") == False
    assert is_float(1) == True
    assert is_float(-2.0) == True
    assert is_float(None) == False


def test_num():
    assert to_num("0") == 0
    assert to_num("1.") == 1
    assert to_num("-2.0") == -2
    assert to_num("3.45") == 3.45
    assert to_num("-.0") == 0
    assert to_num(-4.5) == -4.5
    assert to_num(5.0) == 5


def test_int():
    assert to_int(None) == 0
    assert to_int(0) == 0
    assert to_int("") == 0
    assert to_int("0") == 0
    assert to_int("&nbsp;0") == 0
    assert to_int("    \t\n12 -34 .&7a8") == 123478


def test_get_float():
    assert get_float(None) == []
    assert get_float("") == []
    assert get_float("asd") == []
    assert get_float("0.0") == [0.0]
    assert get_float("0.") == [0.0]
    assert get_float(".0") == [0.0]
    assert get_float("0") == [0.0]
    assert get_float("123") == [123.0]
    assert get_float("asd 1.2") == [1.2]
    assert get_float("asd1.2fgh") == [1.2]
    assert get_float("asd1.2fgh3") == [1.2, 3.0]
    assert get_float("1 2") == [1.0, 2.0]
    assert get_float("1.2%.3") == [1.2, 0.3]
    assert get_float("1.2-.3") == [1.2, -0.3]
    assert get_float("1.2.3") == [1.2, 0.3]
    assert get_float("1..2") == [1.0, 0.2]
    assert get_float("1...2") == [1.0, 0.2]


def test_decimals():
    assert find_decimals(0) == 0
    assert find_decimals(1.0) == 1
    assert find_decimals(0.120) == 2
    assert find_decimals("1000.00012000") == 5
    assert find_decimals(-0.000000000123456700) == 16


def test_whole():
    assert get_whole(0) == "0"
    assert get_whole(0.0) == "0.0"
    assert get_whole(12.340) == "12.34"
    assert get_whole("12.003400") == "12.0034"
    assert get_whole(-0.0000000001234567) == "-0.0000000001234567"
    assert get_whole("-0.0000000001234567000") == "-0.0000000001234567"


def test_simplify():
    assert simplify_value("0") == "0"
    assert simplify_value("0.") == "0"
    assert simplify_value(-25901050.0425) == "-25901050"
    assert simplify_value(-0.0000000001234567) == "-0.0000000001234"
    assert simplify_value("12.345000") == "12.34"
    assert simplify_value(0.01234, 2) == "0.012"
    assert simplify_value("012340000000") == "12340000000"


def test_add_sign():
    assert add_sign(0) == "0"
    assert add_sign("0") == "0"
    assert add_sign("0.") == "0.0"
    assert add_sign(-0.0) == "0.0"
    assert add_sign("-0") == "0"
    assert add_sign(1) == "+1"
    assert add_sign(-100) == "-100"
    assert add_sign(-0.000000001) == "-0.000000001"
    assert add_sign(1.23e-10) == "+0.000000000123"


def test_add_radix():
    assert add_radix(None) == None
    assert add_radix(0) == "0"
    assert add_radix(0.0) == "0.0"
    assert add_radix(0.1) == "0.1"
    assert add_radix(1234) == "1’234"
    assert add_radix(123456) == "123’456"
    assert add_radix(1234567.89012) == "1’234’567.89012"


def test_to_step():
    assert to_step(None) == None
    assert to_step(0) == 0
    assert to_step(0.0) == 0
    assert to_step(0.1) == 0
    assert to_step(1.2) == 1
    assert to_step(1.2, 0.1) == 1.2
    assert to_step(1.234, 0.1) == 1.2
    assert to_step(1.234, 0.1, True) == 1.3
    assert to_step(1.2, 0.1, True) == 1.2
    assert to_step(1.2, 10) == 0
    assert to_step(1.2, 10, True) == 10
    assert to_step(123.456, 10) == 120
    assert isinstance(to_step(12, 0.1), float)
    assert isinstance(to_step(12.456, 1), int)


def test_add():
    assert add(0.7, 0.2) == 0.9


def test_pretty():
    assert pretty(None) == None
    assert pretty(0) == "0"
    assert pretty(0.0) == "0"
    assert pretty(0.0) == "0"
    assert pretty(1.0) == "1"
    assert pretty(0.1) == "0.1"
    assert pretty(1.1, 2) == "1.1"
    assert pretty(0.1, 2) == "0.1"
    assert pretty(1.1, 0) == "1"
    assert pretty(1.7, 0) == "2"
    assert pretty(123.456, 1) == "123"
    assert pretty(123.456, 1, True) == "+123"
    assert pretty(12345.6, 3, True) == "+12’346"
    assert pretty(-0.000000235235, zeros=None, compress=None) == "-0.000000235235"
    assert pretty(-0.000000235235, zeros=4, compress=2) == "-0.0₆24"


def test_to_plain():
    assert to_plain(None) == None
    assert to_plain(0) == "0"
    # assert to_plain(0.0) == "0.0"
    # assert to_plain(1.0) == "1.0"
    assert to_plain(1.1) == "1.1"
    assert to_plain(0.000000235235) == "0.000000235235"
    assert to_plain(-0.000000235235) == "-0.000000235235"
    assert to_plain("0.000000235235") == "0.000000235235"
    assert to_plain(2.35235e-07) == "0.000000235235"
    assert to_plain("1e-12") == "0.000000000001"
    assert to_plain("123.4500") == "123.45"


def test_pretty_with_compression():
    # Test pretty function with compression parameters

    # Test zeros parameter (minimum zeros to compress)
    assert pretty(0.00012, zeros=2) == "0.0₃12"  # Default behavior, compress >=2 zeros
    assert pretty(0.01, zeros=1) == "0.0₁1"  # Compress single zero with zeros=1
    assert pretty(0.01, zeros=3) == "0.01"  # Don't compress with zeros=3 (only 1 zero)
    assert pretty(0.0001, zeros=3) == "0.0₃1"  # Compress with zeros=3 (3 zeros)

    # Test compress parameter (round after zero block)
    assert (
        pretty(0.00012345, zeros=2, compress=2) == "0.0₃12"
    )  # Round to 2 digits after zeros
    assert (
        pretty(0.00012345, zeros=4, compress=4) == "0.0001234"
    )  # No compression (3 < 4 zeros), 4 digits after 3 zeros
    assert pretty(0.00012345, zeros=4, compress=8) == "0.00012345"
    assert (
        pretty(0.00012345, zeros=2, compress=3) == "0.0₃123"
    )  # Round to 3 digits after zeros
    assert (
        pretty(-0.0010959999999999997522, compress=3) == "-0.0011"
    )  # Negative with rounding

    # Test both parameters together
    assert (
        pretty("0.0000012345", zeros=4, compress=2) == "0.0₅12"
    )  # 5 zeros, round to 2 digits
    assert (
        pretty("0.00012345", zeros=4, compress=2) == "0.00012"
    )  # Only 3 zeros, no compression, 2 digits after 3 zeros

    # Test that other pretty parameters still work with compression
    assert pretty(0.00012, zeros=2, sign=True) == "+0.0₃12"  # With sign
    assert pretty(12000.00012, zeros=2, symbol="'") == "12'000.0₃12"  # With radix
    assert (
        pretty(-0.00012, zeros=2, sign=True, symbol="'") == "-0.0₃12"
    )  # Negative with sign and radix

    # Test edge cases
    assert pretty(0, zeros=1) == "0"  # Zero value
    assert pretty(None, zeros=2) == None  # None value
    assert (
        pretty(1.0, zeros=2) == "1"
    )  # No fractional zeros to compress, trailing zero removed for clean formatting


def test_compress_zeros():
    assert compress_zeros(None) == None
    assert compress_zeros(0) == "0"
    assert compress_zeros(0.0) == "0.0"
    assert compress_zeros(1) == "1"
    assert compress_zeros(1.0) == "1.0"
    assert compress_zeros(1.0, round=0) == "1.0"
    assert compress_zeros(0.00012) == "0.0₃12"
    assert compress_zeros(0.00012, round=2) == "0.0₃12"
    assert compress_zeros(0.0123) == "0.0123"
    assert compress_zeros(0.0123456, round=3) == "0.0123"
    assert compress_zeros(1.000045) == "1.0₄45"
    assert compress_zeros(0.0010859999999999997522, round=3) == "0.0₂109"
    assert compress_zeros(-0.0010959999999999997522, round=3) == "-0.0₂11"
    assert compress_zeros("-0.012300") == "-0.0123"
    assert compress_zeros(0.01, zeros=1) == "0.0₁1"
    assert compress_zeros(0.001, zeros=1) == "0.0₂1"
    assert compress_zeros("1.10", zeros=1) == "1.1"
    assert compress_zeros(0.01, zeros=3) == "0.01"
    assert compress_zeros(0.001, zeros=3) == "0.001"
    assert compress_zeros(0.0001, zeros=3) == "0.0₃1"
    assert compress_zeros(0.00001, zeros=3) == "0.0₄1"
    assert compress_zeros(0.0000012, zeros=1) == "0.0₅12"
    assert compress_zeros(0.0000012, zeros=5) == "0.0₅12"
    assert compress_zeros(0.0000012, zeros=6) == "0.0000012"
