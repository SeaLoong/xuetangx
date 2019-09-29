import requests
import config

headers = {
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Host": "scut.xuetangx.com"
}
# cookies = requests.cookies.RequestsCookieJar
session = requests.session()


def init():
    global session
    session.headers = headers
    session.headers["cookies"] = config.cookies


def get(url, params=None, **kwargs):
    r = session.get(url, params=params, **kwargs)
    config.cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return r


def post(url, data=None, **kwargs):
    r = session.post(url, data=data, **kwargs)
    config.cookies = requests.utils.dict_from_cookiejar(session.cookies)
    return r
