import aiohttp


# def load(config)
#     session = aiohttp.ClientSession(headers=config["headers"], cookies=config["cookies"])
#     print("session", session)
#
#
# def save(config):
#     config["cookies"] = session.cookie_jar
#     print("session.cookie_jar", session.cookie_jar)


def process_url(url: str):
    if not url.startswith(("http://", "https://")):
        url = "https://scutspoc.xuetangx.com" + url
    return url


def cookie_to_dic(cookie):
    return {item.split('=')[0]: item.split('=')[1] for item in cookie.split('; ')}


class Client:
    session = None

    def __init__(self, headers=None,  cookies=None, **kwargs):
        if isinstance(cookies, str):
            cookies = cookie_to_dic(cookies)
        self.session = aiohttp.ClientSession(headers=headers, cookies=cookies, **kwargs)

    async def close(self):
        await self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        await self.session.close()

    def get(self, url: str, params=None, **kwargs):
        return self.session.get(process_url(url), params=params, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.session.post(process_url(url), data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.session.put(process_url(url), data=data, **kwargs)
