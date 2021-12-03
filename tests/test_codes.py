from libdev.codes import get_network, get_language, get_flag


def test_get_network():
    assert get_network('web') == 1
    assert get_network(1) == 1
    assert get_network(0) == 0
    assert get_network(None) == 0
    assert get_network(999) == 0
    assert get_network('ola') == 0

def test_get_language():
    assert get_language('en') == 0
    assert get_language('ru') == 1
    assert get_language('on') == 0 # NOTE: cfg('locale', 0)
    assert get_language(0) == 0
    assert get_language(1) == 1
    assert get_language(None) == 0 # NOTE: cfg('locale', 0)

def test_get_flag():
    assert get_flag('ru') == '🇷🇺'
    assert get_flag(2) == '🇪🇸'
    assert get_flag(None) == '🇬🇧'
    assert get_flag('ulu') == '🇬🇧'
    assert get_flag(999) == '🇬🇧'
