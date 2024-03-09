import json


def read_config(config_file):
    """
    Reads and parses a JSON configuration file.

    Attempts to open and read the specified configuration file, parsing its content
    from JSON format into a Python dictionary. If the file does not exist, it returns
    an empty dictionary instead.

    Args:
        config_file (Path): A pathlib.Path object pointing to the location of the
            configuration file to be read.

    Returns:
        dict: The parsed content of the configuration file as a dictionary if the file
            exists; otherwise, an empty dictionary.

    """
    try:
        with config_file.open("r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data
