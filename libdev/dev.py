"""Development-environment helpers tied to LibDev guidelines.

Currently exposes public IP validation logic that mirrors the rules documented
in ``LIBDEV_DOCUMENTATION.md`` for analytics and logging pipelines. Extend this
module instead of sprinkling regex checks throughout consumer projects.
"""

import re


def check_public_ip(ip):
    """Return ``ip`` if it is routable on the public internet.

    Private (RFC1918), loopback, and carrier-grade NAT subnets are filtered
    out, ensuring only analyzable public addresses pass downstream. ``None`` is
    returned for empty inputs or addresses that match reserved ranges.
    """

    if not ip:
        return None

    return (
        None
        if re.match(
            r"^(172\.(1[6-9]\.|2[0-9]\.|3[0-1]\.)|192\.168\.|10\.|127\.)",
            ip,
        )
        else ip
    )
