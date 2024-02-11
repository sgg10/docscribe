import json

from docscribe.constants import CONFIG_FILE


def read_config():
    with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
    return data
