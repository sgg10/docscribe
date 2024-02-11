import json

from app.constants import CONFIG, CONFIG_FILE, CONFIG_SEGMENTS


def write_item_by_segment(
    segment_name: CONFIG_SEGMENTS, name: str, _type: str, config: dict
) -> None:

    segment = CONFIG.get(segment_name, {})
    segment[name] = {"type": _type, "config": config}
    CONFIG[segment_name] = segment

    with CONFIG_FILE.open("w") as f:
        json.dump(CONFIG, f, indent=4)


def delete_item_by_segment(segment_name: CONFIG_SEGMENTS, name: str) -> None:
    segment = CONFIG.get(segment_name, {})
    if name not in segment:
        return

    del segment[name]
    CONFIG[segment_name] = segment

    with CONFIG_FILE.open("w") as f:
        json.dump(CONFIG, f, indent=4)
