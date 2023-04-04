from libdev.check import (
    fake_phone, fake_login, check_mail, fake_mail, check_url, get_last_url,
)


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

def test_check_url():
    assert check_url(None) == False
    assert check_url('') == False
    assert check_url('http') == False
    assert check_url('http://') == False
    assert check_url('http://a/') == False
    assert check_url('http://a.b') == False
    assert check_url('http://a.bc') == True
    assert check_url('https://chill.services/') == True
    assert check_url('https://t.me/kosyachniy') == True

def test_get_last_url():
    assert get_last_url(None) == None
    assert get_last_url('') == ''
    assert get_last_url('https://vk.com/alexeypoloz/') == 'alexeypoloz'
    assert get_last_url('https://vk.com/alexeypoloz') == 'alexeypoloz'
    assert get_last_url('://vk.com/alexeypoloz') == 'alexeypoloz'
    assert get_last_url('//vk.com/alexeypoloz') == 'alexeypoloz'
    assert get_last_url('/vk.com/alexeypoloz') == 'alexeypoloz'
    assert get_last_url('vk.com/alexeypoloz') == 'alexeypoloz'
    assert get_last_url('/alexeypoloz') == 'alexeypoloz'
    assert get_last_url('alexeypoloz') == 'alexeypoloz'
