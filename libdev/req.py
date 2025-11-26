"""Async HTTP gateway used across LibDev powered projects.

Centralizes ``aiohttp`` usage so upstream services benefit from the same request
construction (JSON vs form payloads, multipart file uploads) and response
parsing rules described in ``LIBDEV_DOCUMENTATION.md``. Always ``await`` the
helpers in this module to stay inside the async boundary.
"""

import aiohttp


async def fetch(
    url,
    payload=None,
    files=None,
    type_req="post",
    type_data="json",
    headers=None,
    timeout=None,
):
    """Perform an HTTP request and normalize the response payload.

    Parameters mirror the rules from the integration guide: ``files`` may be a
    mapping of field name to bytes/file-like objects (forcing multipart form
    uploads), ``type_data`` controls whether the ``payload`` is supplied via the
    ``json`` or ``data`` keyword, and ``type_req`` is the lowercase HTTP verb. A
    status code integer and the decoded response body (JSON dict, plain text, or
    raw bytes) are returned. Callers are expected to provide their own retries
    or circuit breaking logic.
    """
    if payload is None:
        payload = {}

    if files is not None:
        form = aiohttp.FormData()
        for name, fdata in files.items():
            form.add_field(name, fdata)
        payload = form
        type_data = "data"

    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=timeout),
    ) as session:
        if type_req == "post":
            req = session.post
        elif type_req == "put":
            req = session.put
        elif type_req == "delete":
            req = session.delete
        elif type_req == "patch":
            req = session.patch
        elif type_req == "options":
            req = session.options
        else:
            req = session.get

        async with req(
            url,
            headers=headers,
            **{type_data: payload},
        ) as response:
            code = response.status

            try:
                data = await response.json()
            except aiohttp.ContentTypeError:
                try:
                    data = await response.text()
                except UnicodeDecodeError:
                    data = await response.read()

            return code, data
