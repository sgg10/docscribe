import json

from app.constants import CONFIG, CONFIG_FILE, CONFIG_SEGMENTS


def write_item_by_segment(
    segment_name: CONFIG_SEGMENTS, name: str, _type: str, config: dict
) -> None:
    """
    Writes a new item or updates an existing item in a specific configuration segment.

    This function updates the application's configuration by adding or modifying an item
    in the specified segment with the provided details. It then writes the updated
    configuration back to the configuration file.

    Args:
        segment_name (CONFIG_SEGMENTS): The segment of the configuration to update,
            e.g., 'exporters' or 'repositories'.
        name (str): The name of the item to add or update.
        _type (str): The type of the item, which helps in identifying the subclass
            or specific handler.
        config (dict): The configuration details for the item.

    """
    segment = CONFIG.get(segment_name, {})
    segment[name] = {"type": _type, "config": config}
    CONFIG[segment_name] = segment

    with CONFIG_FILE.open("w") as f:
        json.dump(CONFIG, f, indent=4)


def delete_item_by_segment(segment_name: CONFIG_SEGMENTS, name: str) -> None:
    """
    Deletes an item from a specific configuration segment.

    This function removes an item by its name from the specified configuration segment.
    If the item exists, it is removed, and the updated configuration is written back to
    the configuration file.

    Args:
        segment_name (CONFIG_SEGMENTS): The segment of the configuration from which to
            delete the item, e.g., 'exporters' or 'repositories'.
        name (str): The name of the item to delete.

    """
    segment = CONFIG.get(segment_name, {})
    if name not in segment:
        return

    del segment[name]
    CONFIG[segment_name] = segment

    with CONFIG_FILE.open("w") as f:
        json.dump(CONFIG, f, indent=4)
