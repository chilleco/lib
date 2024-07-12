"""
Functionality of Amazon Web Services
"""

import io
import base64

import aiohttp
from PIL import Image, ExifTags


def fix_rotation(image):
    """Fix image rotation"""

    orientation = None
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == "Orientation":
            break

    # pylint: disable=protected-access
    exif = image._getexif()
    if exif and orientation in exif:
        exif = dict(exif.items())
        if exif[orientation] == 3:
            image = image.transpose(3)
        if exif[orientation] == 6:
            image = image.transpose(4)
        if exif[orientation] == 8:
            image = image.transpose(2)

    return image


async def fetch_content(url):
    """
    Fetch the content of a URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        bytes: The content of the response.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=30) as response:
            response.raise_for_status()
            return await response.read()


async def convert(image, image_type="webp"):
    """Convert image format"""

    if not image:
        return None

    if isinstance(image, str):
        if image[:4] == "http":
            image = await fetch_content(image)
        else:
            if "base64," in image:
                image = image.split(",")[1]
            image = base64.b64decode(image)

    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))
    else:
        image = Image.open(image)

    image = fix_rotation(image)
    image = image.convert("RGB")
    data = io.BytesIO()
    image.save(data, format=image_type)

    return data.getvalue()
