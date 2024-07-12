"""
Functionality of S3
"""

import os.path
from urllib.parse import urlparse
from io import BytesIO
from mimetypes import guess_extension

import aiohttp
import boto3
from botocore.exceptions import NoCredentialsError

from .cfg import cfg
from .gen import generate


# pylint: disable=invalid-name
s3 = None
if cfg("s3.pass"):
    s3 = boto3.client(
        "s3",
        endpoint_url=cfg("s3.host"),
        aws_access_key_id=cfg("s3.user"),
        aws_secret_access_key=cfg("s3.pass"),
        region_name="us-east-1",
    )


async def fetch_file(url):
    """
    Fetch the content and content type of a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        tuple: The content of the response and its content type.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=30) as response:
            response.raise_for_status()
            return await response.read(), response.headers.get("Content-Type")


async def upload_file(
    file,
    directory=cfg("mode").lower(),
    bucket=cfg("project_name"),
    file_type=None,
):
    """Upload file"""

    name = f"{directory}/{generate()}"

    if isinstance(file, str):
        parsed_url = urlparse(file)
        if parsed_url.netloc:
            content, content_type = await fetch_file(file)

            if not file_type:
                file_type = os.path.splitext(parsed_url.path)[-1]
            if not file_type:
                file_type = guess_extension(content_type.split(";")[0])

            file = BytesIO(content)
            handler = s3.upload_fileobj

        else:
            if not file_type:
                file_type = os.path.splitext(file)[-1]
            handler = s3.upload_file

    elif isinstance(file, bytes):
        file = BytesIO(file)
        handler = s3.upload_fileobj

    else:
        handler = s3.upload_fileobj

    if file_type:
        if file_type[0] != ".":
            file_type = "." + file_type
        name += file_type.lower()

    try:
        handler(file, bucket, name)
    except FileNotFoundError:
        return None
    except NoCredentialsError:
        return None

    return f"{cfg('s3.host')}{bucket}/{name}"


def get_buckets():
    """Get list of buckets"""
    return [bucket["Name"] for bucket in s3.list_buckets()["Buckets"]]


__all__ = (
    "s3",
    "upload_file",
    "get_buckets",
)
