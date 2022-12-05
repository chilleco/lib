from libdev.num import (
    is_float, to_num, find_decimals, get_whole, simplify_value,
)


def test_float():
    assert is_float('0') == True
    assert is_float('-0.') == True
    assert is_float('-.0') == True
    assert is_float('.1') == True
    assert is_float('-.2') == True
    assert is_float('-3.') == True
    assert is_float('4.0') == True
    assert is_float('-5.678') == True
    assert is_float('6.7x') == False
    assert is_float('-7..8') == False
    assert is_float('') == False
    assert is_float('.') == False
    assert is_float(1) == True
    assert is_float(-2.) == True
    assert is_float(None) == False

def test_num():
    assert to_num('0') == 0
    assert to_num('1.') == 1
    assert to_num('-2.0') == -2
    assert to_num('3.45') == 3.45
    assert to_num('-.0') == 0
    assert to_num(-4.5) == -4.5
    assert to_num(5.0) == 5

def test_decimals():
    assert find_decimals(0) == 0
    assert find_decimals(1.) == 1
    assert find_decimals(0.120) == 2
    assert find_decimals('1000.00012000') == 5
    assert find_decimals(-0.000000000123456700) == 16

def test_whole():
    assert get_whole(0) == '0'
    assert get_whole(0.) == '0.0'
    assert get_whole(12.340) == '12.34'
    assert get_whole('12.003400') == '12.0034'
    assert get_whole(-0.0000000001234567) == '-0.0000000001234567'
    assert get_whole('-0.0000000001234567000') == '-0.0000000001234567'

def test_simplify():
    assert simplify_value('0') == '0'
    assert simplify_value('0.') == '0'
    assert simplify_value(-25901050.0425) == '-25901050'
    assert simplify_value(-0.0000000001234567) == '-0.0000000001234'
    assert simplify_value('12.345000') == '12.34'
    assert simplify_value(0.01234, 2) == '0.012'
    assert simplify_value('012340000000') == '12340000000'
