"""
Documents processing functionality
"""

import base64
import json


def to_base64(image, mime="image/jpg"):
    """Convert image to base64"""
    data = base64.b64encode(image.read())
    return f"data:{mime};base64,{data.decode('utf-8')}"


def to_json(data):
    """Convert object to json"""
    return json.dumps(data, indent="\t", ensure_ascii=False)
