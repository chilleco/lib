import pytest

from libdev.req import fetch


@pytest.mark.asyncio
async def test_req():
    assert await fetch("http://httpbin.org/status/200") == (200, "")
    assert await fetch("https://postman-echo.com/get") == (404, "")
