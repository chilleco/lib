from libdev.cfg import cfg


def test_cfg():
    assert cfg('key') == 'value'
    assert cfg('test') is None
    assert cfg('olo.ulu') == 123
    assert cfg('olo') == {'ulu': 123}
    assert cfg('ola.foo.bar') == True
    assert cfg('olx.foo.bar') is None
    assert cfg('ola.foa') is None
    assert cfg('ola.foo.bor') is None
    assert cfg('olx', 'test') == 'test'
