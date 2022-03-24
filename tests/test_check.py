from libdev.check import fake_phone, fake_login


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
