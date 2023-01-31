"""
Development tools
"""

import re


def check_private_ip(ip):
    """ Check if the IP address is public """

    if not ip:
        return None

    return re.match(
        r'^(172\.(1[6-9]\.|2[0-9]\.|3[0-1]\.)|192\.168\.|10\.|127\.)', ip,
    ) == None
