import json


def read_config(config_file):
    with config_file.open("r") as f:
        data = json.load(f)
    return data
