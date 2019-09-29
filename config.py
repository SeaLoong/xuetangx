import json
import os

cfg = {}
cookies = {}


def load(file=None):
    if file is None:
        file = os.getcwd() + "\\config.cfg"
    global cfg, cookies
    try:
        f = open(file, "r")
        data = f.read()
    except Exception:
        data = "{}"
    cfg = json.loads(data)
    cookies = cfg.get("cookies")


def save(file=None):
    if file is None:
        file = os.getcwd() + "\\config.cfg"
    global cfg, cookies
    cfg["cookies"] = cookies
    open(file, "w").write(json.dumps(cfg))
