"""
Checking functionality
"""

import re
from typing import Union
from urllib.parse import urlparse


PATTERN_PHONE = r"\(?\+?[0-9\s\-\(\)./]{7,30}"


def check_phone(value: Union[str, int]) -> bool:
    """Check phone validity"""
    if isinstance(value, int):
        value = str(value)
    return re.match(PATTERN_PHONE, value) is not None


def rm_phone(value: Union[str, int]) -> str:
    """Remove phone number"""
    return re.sub(PATTERN_PHONE, "", value).strip()


def fake_phone(value: str) -> bool:
    """Check a phone for a test format"""

    if value is None:
        return False

    value = str(value)

    return any(
        fake in value
        for fake in (
            "00000",
            "11111",
            "22222",
            "33333",
            "44444",
            "55555",
            "66666",
            "77777",
            "88888",
            "99999",
            "12345",
            "98765",
            #'2345', '3456', '4567', '5678', '6789',
            # '8765', '7654', '6543', '5432', '4321',
        )
    )


def fake_login(value: str) -> bool:
    """Check a login / name for a test format"""

    if value is None:
        return False

    value = value.lower()

    return any(
        fake in value
        for fake in (
            "test",
            "тест",
            "check",
            "demo",
            "asd",
            "asf",
            "qwe",
            "sdf",
            "sfg",
            "sfd",
            "hgf",
            "gfd",
            "dgf",
            "qaz",
            "wsx",
            "edc",
            "rfv",
            "qwd",
            "lalala",
            "lolkek",
            "0000",
            "1111",
            "2222",
            "3333",
            "4444",
            "5555",
            "6666",
            "7777",
            "8888",
            "9999",
            "1234",
            "9876",  # '1212', '2323'
            "ыва",
            "фыв",
            "йцу",
            "aaaa",
            "bbb",
            "ccc",
            "rrr",
            "zzz",
            "ааа",
            "ббб",
            "ввв",
            "ггг",
            "ддд",
            "еее",
            "ёёё",
            "жжж",
            "ззз",
            "иии",
            "ййй",
            "ккк",
            "ллл",
            "ммм",
            "ннн",
            "ооо",
            "ппп",
            "ррр",
            "ссс",
            "ттт",
            "ууу",
            "ффф",
            "ххх",
            "ццц",
            "ччч",
            "шшш",
            "щщщ",
            "ъъъ",
            "ыыы",
            "ььь",
            "эээ",
            "ююю",
            "яяя",
        )
    )


def check_mail(value: str) -> bool:
    """Check mail validity"""
    if value is None:
        return False
    return re.match(r".{1,64}@.{1,63}\..{1,15}", value) is not None


def fake_mail(value: str) -> bool:
    """Check a mail for a test format"""

    if value is None:
        return False

    fake = (
        not check_mail(value)
        or fake_login(value)
        or not re.search(r"@[a-zA-Z]+\.", value)
    )
    return fake


def check_url(data: str) -> bool:
    """Check url validity"""
    if data is None:
        return False
    # pylint: disable=line-too-long
    return (
        re.match(
            r"^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$",
            data,
        )
        is not None
    )


def get_base_url(data: str, protocol: bool = False) -> str | None:
    """Get domain"""

    if not data or "." not in data:
        return None
    data = data.strip().split()[0]

    if "://" not in data:
        data = "http://" + data

    parsed = urlparse(data)
    if not parsed.netloc:
        return None

    if protocol:
        base_url = f"{parsed.scheme}://{parsed.netloc}"
    else:
        base_url = parsed.netloc

    return base_url


def get_last_url(data: str) -> str:
    """Get the last part of a URL"""
    if data is None:
        return None
    return re.sub(r".*/(.+?)/?$", r"\1", data)
