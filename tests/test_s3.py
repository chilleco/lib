import pytest

from libdev.cfg import cfg
from libdev.img import fetch_content
from libdev.s3 import upload, get, remove


FILE_LOCAL = "tests/test_s3.py"
FILE_REMOTE = "https://lh3.googleusercontent.com/a/AEdFTp4x--V0C6UB594hqXtdYCR3yvBFeiydvCi3q_eW=s96-c"
FILE_REMOTE_EXTENSION = "https://s1.1zoom.ru/big0/621/359909-svetik.jpg"


@pytest.mark.asyncio
async def test_s3():
    if cfg("s3.pass"):
        # Upload
        file1 = await upload(FILE_LOCAL)
        assert file1[:8] == "https://"

        with open(FILE_LOCAL, "rb") as file:
            file2 = await upload(file, file_type="Py")
            assert file2[-3:] == ".py"

        file3 = await upload(FILE_REMOTE)
        assert file3[:8] == "https://"

        file4 = await upload(FILE_REMOTE_EXTENSION)
        assert file4[-4:] == ".jpg"

        file5 = await upload(await fetch_content(FILE_REMOTE), file_type="png")
        assert file5[-4:] == ".png"

        # Check list
        files = {file1, file2, file3, file4, file5}
        assert files == {
            f"{cfg('s3.host')}{cfg('project_name')}/{file}" for file in get()
        }

        # Remove
        for file in files:
            assert remove(file)

        assert get() == []
