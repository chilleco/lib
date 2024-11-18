from libdev.check import (
    check_phone,
    rm_phone,
    fake_phone,
    fake_login,
    check_mail,
    fake_mail,
    check_url,
    get_base_url,
    get_last_url,
)


def test_phone():
    assert check_phone(79000000001) == True
    assert check_phone("+79121231234") == True
    assert check_phone("79697366730") == True
    assert check_phone("+7 (969) 736 67 30") == True
    assert check_phone("(+351) 282 43 50 50") == True
    assert check_phone("1-234-567-8901") == True
    assert check_phone("1 (234) 567-8901") == True
    assert check_phone("1.234.567.8901") == True
    assert check_phone("1/234/567/8901") == True
    assert check_phone("12345678901") == True
    assert check_phone("+63.917.123.4567  ") == True
    assert check_phone("+63-917-123-4567	") == True
    assert check_phone("+63 917 123 4567\t") == True
    assert check_phone("+639171234567\n") == True
    assert check_phone("09171234567") == True
    assert check_phone("90191919908") == True
    assert check_phone("555-8909") == True
    assert check_phone("001 6867684") == True
    assert check_phone("1 (234) 567-8901") == True
    assert check_phone("(123)8575973") == True
    assert check_phone("(0055)(123)8575973") == True
    assert check_phone("+1 282 282 2828") == True
    # assert check_phone('1-234-567-8901 x1234') == True
    # assert check_phone('1-234-567-8901 ext1234') == True
    # assert check_phone('001 6867684x1') == True
    # assert check_phone('1-234 567.89/01 ext.1234') == True
    # assert check_phone('1(234)5678901x1234') == True
    assert check_phone("On $n, it saves:") == False
    assert check_phone("privet") == False
    assert check_phone("privet 123") == False
    assert check_phone("1") == False
    assert check_phone("123.") == False
    assert check_phone("+971509282748") == True


def test_rm_phone():
    assert rm_phone("Prado 2,7л TX\n+971509282748") == "Prado 2,7л TX"
    assert rm_phone("test") == "test"


def test_fake_phone():
    assert fake_phone(79000000001) == True
    # assert fake_phone('+79121231234') == True
    assert fake_phone("79697366730") == False


def test_mail():
    assert check_mail(None) == False
    assert check_mail("") == False
    assert check_mail("null") == False
    assert check_mail("@.") == False
    assert check_mail("1@2.3") == True
    assert check_mail("asd@qwe.rty") == True
    assert check_mail("a" * 65 + "@qwe.rty") == False


def test_fake_mail():
    assert fake_mail("test@check.ru") == True
    assert fake_mail("ASD@Qwe.rTy") == True
    assert fake_mail("ads@123.ru") == True
    assert fake_mail("polozhev@mail.ru") == False
    assert fake_mail("a" * 65 + "@qwe.rty") == True


def test_name():
    assert fake_login("Тест") == True
    assert fake_login("aSdR") == True
    assert fake_login("Алексей") == False


def test_check_url():
    assert check_url(None) == False
    assert check_url("") == False
    assert check_url("http") == False
    assert check_url("http://") == False
    assert check_url("http://a/") == False
    assert check_url("http://a.b") == False
    assert check_url("http://a.bc") == True
    assert check_url("https://chill.services/") == True
    assert check_url("https://t.me/kosyachniy") == True
    assert check_url("http2://www.asd.atcsd.ru\nhttp://www.asd.atcsd.ru/") == False


def test_get_base_url():
    assert get_base_url(None) == None
    assert get_base_url("") == None
    assert get_base_url("http") == None
    assert get_base_url("http://") == None
    assert get_base_url("http://a/") == None
    assert get_base_url("http://a.b") == "a.b"
    assert get_base_url("http://a.bc", protocol=True) == "http://a.bc"
    assert (
        get_base_url("https://chill.services/", protocol=True)
        == "https://chill.services"
    )
    assert get_base_url("https://t.me/kosyachniy", protocol=True) == "https://t.me"
    assert (
        get_base_url("http://www.atcsd.ru\nhttp://www.asd.atcsd.ru/", protocol=True)
        == "http://www.atcsd.ru"
    )
    assert (
        get_base_url(
            "http2://www.asd.atcsd.ru\nhttp://www.asd.atcsd.ru/", protocol=True
        )
        == "http2://www.asd.atcsd.ru"
    )
    assert (
        get_base_url("https2://127.0.0.1:8080?query=string#fragment", protocol=True)
        == "https2://127.0.0.1:8080"
    )
    assert (
        get_base_url("127.0.0.1:8080/path/to/page?query=string#fragment", protocol=True)
        == "http://127.0.0.1:8080"
    )


def test_get_last_url():
    assert get_last_url(None) == None
    assert get_last_url("") == ""
    assert get_last_url("https://vk.com/alexeypoloz/") == "alexeypoloz"
    assert get_last_url("https://vk.com/alexeypoloz") == "alexeypoloz"
    assert get_last_url("://vk.com/alexeypoloz") == "alexeypoloz"
    assert get_last_url("//vk.com/alexeypoloz") == "alexeypoloz"
    assert get_last_url("/vk.com/alexeypoloz") == "alexeypoloz"
    assert get_last_url("vk.com/alexeypoloz") == "alexeypoloz"
    assert get_last_url("/alexeypoloz") == "alexeypoloz"
    assert get_last_url("alexeypoloz") == "alexeypoloz"
