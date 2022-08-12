"""
Documents processing functionality
"""

import base64


def to_base64(image, mime='image/jpg'):
    data = base64.b64encode(image.read())
    return f"data:{mime};base64,{data.decode('utf-8')}"
