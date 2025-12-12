"""
Functionality of Amazon Web Services
"""

import base64
import io

import aiohttp
from PIL import ExifTags, Image, UnidentifiedImageError

try:
    from pillow_heif import register_heif_opener
except ImportError:
    register_heif_opener = None


HEIC_SIGNATURES = (
    b"ftypheic",
    b"ftypheix",
    b"ftyphevc",
    b"ftyphevx",
    b"ftypmif1",
    b"ftypmsf1",
)

_HEIF_REGISTERED = False


def fix_rotation(image):
    """Fix image rotation"""

    orientation = None
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == "Orientation":
            break

    # pylint: disable=protected-access
    get_exif = getattr(image, "_getexif", None)
    if not callable(get_exif):
        return image

    exif = get_exif()
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


def _register_heif_plugins():
    """Enable HEIC/HEIF support if pillow_heif is installed."""

    global _HEIF_REGISTERED

    if _HEIF_REGISTERED or not register_heif_opener:
        return

    register_heif_opener()
    _HEIF_REGISTERED = True


def _looks_like_heic(data):
    return any(signature in data[:32] for signature in HEIC_SIGNATURES)


def _normalize_image_type(image_type):
    if image_type and image_type.lower() in ("heic", "heif"):
        return "HEIF"

    return image_type.upper() if image_type else image_type


async def convert(image, image_type="webp"):
    """Convert image format"""

    if not image:
        return None

    _register_heif_plugins()
    target_format = _normalize_image_type(image_type)
    raw_image = None

    if isinstance(image, str):
        if image[:4] == "http":
            image = await fetch_content(image)
        else:
            if "base64," in image:
                image = image.split(",")[1]
            image = base64.b64decode(image)

    if isinstance(image, bytes):
        raw_image = image
        image = io.BytesIO(image)

    try:
        image = Image.open(image)
    except UnidentifiedImageError as exc:
        if raw_image and _looks_like_heic(raw_image) and not register_heif_opener:
            raise ValueError(
                "HEIC images require pillow-heif. Install pillow-heif to enable HEIC conversion."
            ) from exc

        raise

    if target_format == "HEIF" and not register_heif_opener:
        raise ValueError(
            "Saving as HEIC requires pillow-heif. Install pillow-heif to enable HEIC conversion."
        )

    image = fix_rotation(image)
    image = image.convert("RGB")
    data = io.BytesIO()
    image.save(data, format=target_format)

    return data.getvalue()
