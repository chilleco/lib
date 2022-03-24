from libdev.check import is_float, fake_phone, fake_login


def test_float():
    assert is_float('0') == True
    assert is_float('.1') == True
    assert is_float('-.2') == True
    assert is_float('-3.') == True
    assert is_float('4.0') == True
    assert is_float('-5.678') == True
    assert is_float('6.7x') == False
    assert is_float('-7..8') == False

def test_phone():
    assert fake_phone(79000000001) == True
    assert fake_phone('+79121231234') == True
    assert fake_phone('79697366730') == False

def test_mail():
    assert fake_login('test@check.ru') == True
    assert fake_login('ASD@Qwe.rTy') == True
    assert fake_login('ads@123.ru') == True
    assert fake_login('polozhev@mail.ru') == False

def test_name():
    assert fake_login('Тест') == True
    assert fake_login('aSdR') == True
    assert fake_login('Алексей') == False
