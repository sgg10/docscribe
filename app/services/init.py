import json

import rich

from app.constants import CONFIG_FILE, DIRECTORY


def run():
    """Initialize docscribe configuration"""
    path = DIRECTORY / "local"
    try:
        path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        rich.print(f"[red]Error[/red]: {e}")
        return

    config = {"repositories_directory": str(path.parent)}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

    rich.print(f"[green]Configuration file created at {CONFIG_FILE}[/green]")
