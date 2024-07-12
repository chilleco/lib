import pytest

from libdev.cfg import cfg
from libdev.img import fetch_content
from libdev.s3 import upload_file


FILE_LOCAL = "tests/test_s3.py"
FILE_REMOTE = "https://lh3.googleusercontent.com/a/AEdFTp4x--V0C6UB594hqXtdYCR3yvBFeiydvCi3q_eW=s96-c"
FILE_REMOTE_EXTENSION = "https://s1.1zoom.ru/big0/621/359909-svetik.jpg"


@pytest.mark.asyncio
async def test_upload_file():
    if cfg("s3.pass"):
        assert (await upload_file(FILE_LOCAL))[:8] == "https://"

        with open(FILE_LOCAL, "rb") as file:
            assert (await upload_file(file, file_type="Py"))[-3:] == ".py"

        assert (await upload_file(FILE_REMOTE))[:8] == "https://"
        assert (await upload_file(FILE_REMOTE_EXTENSION))[-4:] == ".jpg"

        assert (await upload_file(await fetch_content(FILE_REMOTE), file_type="png"))[
            -4:
        ] == ".png"
