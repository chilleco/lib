from libdev.aws import upload_file


def test_upload_file():
    assert upload_file('tests/test_aws.py')[:8] == 'https://'
