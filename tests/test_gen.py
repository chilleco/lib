from libdev.gen import generate, generate_id, generate_password


def test_generate():
    assert len(generate()) == 32


def test_generate_id():
    assert 10000000 <= generate_id() <= 99999999
    assert 0 <= generate_id(1) <= 9


def test_generate_password():
    assert len(generate_password()) == 8
    assert len(generate_password(7)) == 7
    assert len(generate_password(6)) == 6
    assert len(generate_password(5)) == 5
    assert len(generate_password(4)) == 4
    assert len(generate_password(3)) == 3
    assert len(generate_password(2)) == 2
    assert len(generate_password(1)) == 1
