import json
import os


def load(file=None):
    if file is None:
        file = os.getcwd() + "\\config.json"
    try:
        f = open(file, "r")
        data = f.read()
    except Exception:
        data = "{}"
    return json.loads(data)


def save(_c, file=None):
    if file is None:
        file = os.getcwd() + "\\config.json"
    open(file, "w").write(json.dumps(_c))
