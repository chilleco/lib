from libdev.check import fake_phone, fake_login, check_mail, fake_mail


def test_phone():
    assert fake_phone(79000000001) == True
    assert fake_phone('+79121231234') == True
    assert fake_phone('79697366730') == False

def test_mail():
    assert check_mail(None) == False
    assert check_mail('') == False
    assert check_mail('null') == False
    assert check_mail('@.') == False
    assert check_mail('1@2.3') == True
    assert check_mail('asd@qwe.rty') == True
    assert check_mail('a' * 65 + '@qwe.rty') == False

def test_fake_mail():
    assert fake_mail('test@check.ru') == True
    assert fake_mail('ASD@Qwe.rTy') == True
    assert fake_mail('ads@123.ru') == True
    assert fake_mail('polozhev@mail.ru') == False
    assert fake_mail('a' * 65 + '@qwe.rty') == True

def test_name():
    assert fake_login('Тест') == True
    assert fake_login('aSdR') == True
    assert fake_login('Алексей') == False
