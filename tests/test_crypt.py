from libdev.crypt import encrypt, decrypt


def test_cfg_json():
    assert encrypt(None) == None
    assert encrypt(0)[-2:] == "00"
    assert encrypt(0, length=0) == "00"
    assert encrypt(0, length=10)[-2:] == "00"
    assert decrypt(encrypt(0, length=15)) == 0
    assert decrypt(encrypt(123, length=15)) == 123
    for i in range(0, 1000):
        assert decrypt(encrypt(i)) == i
