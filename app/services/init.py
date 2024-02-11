import json

import rich

from app.constants import CONFIG_FILE, REPOSITORIES_DIR


def run():
    """Initialize docscribe configuration"""
    path = REPOSITORIES_DIR / "local"
    try:
        path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        rich.print(f"[red]Error[/red]: {e}")
        return

    config = {
        "repositories_directory": str(REPOSITORIES_DIR),
        "repositories": {
            "local": {
                "type": "local",
                "config": {},
            }
        },
        "exporters": {
            "local": {
                "type": "local",
                "config": {},
            }
        },
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    rich.print(f"[green]Configuration file created at {CONFIG_FILE}[/green]")
