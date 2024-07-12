from libdev.cfg import cfg, set_cfg


def test_cfg_json():
    assert cfg("key") == "value"
    assert cfg("test") == "test"
    assert cfg("olo.ulu") == 123
    assert cfg("olo") == {"ulu": 123}
    assert cfg("ola.foo.bar") == True
    assert cfg("olx.foo.bar") is None
    assert cfg("ola.foa") is None
    assert cfg("ola.foo.bor") is None
    assert cfg("olx", "test") == "test"


def test_cfg_environ():
    assert cfg("TEST") == "test"
    assert cfg("TEST_TEST", "value") == "test_test"
    assert cfg("VALUE", "value") == "value"
    assert cfg("DIGIT") == 123
    assert isinstance(cfg("FLOAT"), float)
    assert cfg("BOOL") == False
    assert cfg("LIST") == [{"foo": "bar"}]
    assert cfg("KEY") == None


def test_set_cfg():
    assert cfg("NEW") is None
    set_cfg("NEW", "value")
    assert cfg("NEW") == "value"


def test_set_cfg_nested():
    assert cfg("ulu.olo") is None
    set_cfg("ulu.olo", "value")
    assert cfg("ulu") == {"olo": "value"}
