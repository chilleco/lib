from libdev.codes import get_network, get_language


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
    assert get_language(0) == 0
    assert get_language(1) == 1
    assert get_language(None) is None
