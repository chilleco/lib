from libdev.log import log


def test_log():
    assert log.json([{"хола": "☺️"}]) == None
