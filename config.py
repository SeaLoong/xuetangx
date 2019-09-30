import json
import os

config = {}


def load(file=None):
    if file is None:
        file = os.getcwd() + "\\config.json"
    try:
        f = open(file, "r")
        data = f.read()
    except Exception:
        data = "{}"
    global config
    config = json.loads(data)


def save(file=None):
    if file is None:
        file = os.getcwd() + "\\config.json"
    open(file, "w").write(json.dumps(config))
