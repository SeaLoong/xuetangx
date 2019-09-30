import requests

session = requests.session()


def load(config):
    session.headers = config["headers"]
    session.headers["cookies"] = config["cookies"]


def save(config):
    config.cookies = requests.utils.dict_from_cookiejar(session.cookies)


def get(url, params=None, **kwargs):
    r = session.get(url, params=params, **kwargs)
    return r


def post(url, data=None, **kwargs):
    r = session.post(url, data=data, **kwargs)
    return r


def put(url, data=None, **kwargs):
    r = session.put(url, data=data, **kwargs)
    return r
