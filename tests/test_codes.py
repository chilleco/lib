from libdev.codes import get_network, get_locale, get_flag


def test_get_network():
    assert get_network("web") == 1
    assert get_network(1) == 1
    assert get_network(0) == 0
    assert get_network(None) == 0
    assert get_network(999) == 0
    assert get_network("ola") == 0


def test_get_locale():
    assert get_locale("en") == 0
    assert get_locale("ru") == 1
    assert get_locale("on") == 0  # NOTE: cfg('locale', 0)
    assert get_locale(0) == 0
    assert get_locale(1) == 1
    assert get_locale(None) == 0  # NOTE: cfg('locale', 0)


def test_get_flag():
    assert get_flag("ru") == "🇷🇺"
    assert get_flag(3) == "🇪🇸"
    assert get_flag(14) == "🇻🇳"
    assert get_flag(None) == "🇬🇧"
    assert get_flag("ulu") == "🇬🇧"
    assert get_flag(999) == "🇬🇧"
    assert get_flag("") == "🇬🇧"
    assert get_flag(None) == "🇬🇧"
