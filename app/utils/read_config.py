import json


def read_config(config_file):
    try:
        with config_file.open("r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data
