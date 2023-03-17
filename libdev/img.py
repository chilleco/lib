"""
Functionality of Amazon Web Services
"""

import io
import base64

import requests

from PIL import Image, ExifTags


def fix_rotation(image):
    """ Fix image rotation """

    orientation = None
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break

    # pylint: disable=protected-access
    exif = image._getexif()
    if exif and orientation in exif:
        exif = dict(exif.items())
        if exif[orientation] == 3:
            image = image.transpose(Image.ROTATE_180)
        if exif[orientation] == 6:
            image = image.transpose(Image.ROTATE_270)
        if exif[orientation] == 8:
            image = image.transpose(Image.ROTATE_90)

    return image

def convert(image, image_type='webp'):
    """ Convert image format """

    if not image:
        return None

    if isinstance(image, str):
        if image[:4] == 'http':
            image = requests.get(image, timeout=30, stream=True).raw

        else:
            if 'base64,' in image:
                image = image.split(',')[1]
            image = base64.b64decode(image)

    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))
    else:
        image = Image.open(image)

    image = fix_rotation(image)
    image = image.convert('RGB')
    data = io.BytesIO()
    image.save(data, format=image_type)

    return data.getvalue()
