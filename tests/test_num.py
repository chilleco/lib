from libdev.num import is_float, to_num


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
