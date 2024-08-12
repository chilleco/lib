"""
Provides an asynchronous function to fetch data from a URL using aiohttp
"""

import aiohttp


async def fetch(
    url,
    payload=None,
    type_req="post",
    type_data="json",
    headers=None,
    timeout=None,
):
    """
    Fetch data from a URL using aiohttp.

    Args:
        url (str): The URL to fetch data from.
        payload (dict, optional): The payload to send with the request.
            Defaults to None.
        type_req (str, optional): The type of request (e.g., 'post', 'put',
            'delete', etc.). Defaults to 'post'.
        type_data (str, optional): The type of data (e.g., 'json', 'data').
            Defaults to 'json'.
        headers (dict, optional): The headers to include with the request.
            Defaults to None.
        timeout (float, optional): The timeout for the request in seconds.
            Defaults to None.

    Returns:
        tuple: A tuple containing the status code and the response data.
    """
    if payload is None:
        payload = {}

    async with aiohttp.ClientSession(
        timeout=timeout and aiohttp.ClientTimeout(total=timeout),
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
