from libdev.dev import check_public_ip


def test_check_public_ip():
    assert check_public_ip(None) == None
    assert check_public_ip("") == None
    assert check_public_ip("0.0.0.0") == "0.0.0.0"
    assert check_public_ip("1.1.1.1") == "1.1.1.1"
    assert check_public_ip("10.0.0.0") == None
    assert check_public_ip("127.0.0.1") == None
    assert check_public_ip("127.168.0.1") == None
    assert check_public_ip("172.15.255.255") == "172.15.255.255"
    assert check_public_ip("172.17.0.1") == None
    assert check_public_ip("172.168.0.1") == "172.168.0.1"
    assert check_public_ip("192.168.0.0") == None
    assert check_public_ip("192.168.255.255") == None
    assert check_public_ip("192.169.255.255") == "192.169.255.255"
