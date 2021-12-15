from libdev.aws import upload_file


FILE = 'tests/test_aws.py'


def test_upload_file():
    assert upload_file(FILE)[:8] == 'https://'

    with open(FILE, 'rb') as file:
        assert upload_file(file, file_type='Py')[-3:] == '.py'
