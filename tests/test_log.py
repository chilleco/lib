from libdev.log import log, setup_logging


def test_log():
    assert log.info("Text") == None
    assert log.json([{"хола": "☺️"}]) == None


def test_custom():
    setup_logging()
    assert log.info("Text") == None
    assert (
        log.info(
            "Text",
            extra={
                "search": None,
                "post_id": "underline",
                "status": 1,
                "user": 0,
            },
            tags=["suka", "one"],
        )
        == None
    )
