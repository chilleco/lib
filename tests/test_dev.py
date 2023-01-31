from libdev.dev import check_private_ip


def test_check_private_ip():
    assert check_private_ip(None) == None
    assert check_private_ip('') == None
    assert check_private_ip('0.0.0.0') == True
    assert check_private_ip('1.1.1.1') == True
    assert check_private_ip('10.0.0.0') == False
    assert check_private_ip('127.0.0.1') == False
    assert check_private_ip('127.168.0.1') == False
    assert check_private_ip('172.15.255.255') == True
    assert check_private_ip('172.17.0.1') == False
    assert check_private_ip('172.168.0.1') == True
    assert check_private_ip('192.168.0.0') == False
    assert check_private_ip('192.168.255.255') == False
    assert check_private_ip('192.169.255.255') == True
