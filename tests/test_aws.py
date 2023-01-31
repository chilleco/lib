import requests

from libdev.cfg import cfg
from libdev.aws import upload_file


FILE_LOCAL = 'tests/test_aws.py'
FILE_REMOTE = 'https://lh3.googleusercontent.com/a/AEdFTp4x--V0C6UB594hqXtdYCR3yvBFeiydvCi3q_eW=s96-c'
FILE_REMOTE_EXTENSION = 'https://s1.1zoom.ru/big0/621/359909-svetik.jpg'


def test_upload_file():
    if cfg('amazon.id'):
        assert upload_file(FILE_LOCAL)[:8] == 'https://'

        with open(FILE_LOCAL, 'rb') as file:
            assert upload_file(file, file_type='Py')[-3:] == '.py'

        assert upload_file(FILE_REMOTE)[:8] == 'https://'
        assert upload_file(FILE_REMOTE_EXTENSION)[-4:] == '.jpg'

        assert upload_file(
            requests.get(FILE_REMOTE, timeout=30).content, file_type='png'
        )[-4:] == '.png'
