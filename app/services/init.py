import json

import rich

from app.constants import CONFIG_FILE, REPOSITORIES_DIR


def run(package_manager):
    """
    Initializes the DocScribe configuration with default settings.

    This function sets up the initial configuration for DocScribe by creating a local repository
    directory (if it doesn't already exist) and generating a configuration file with default
    settings for both repositories and exporters. The configuration includes a local repository
    and exporter by default, alongside the specified package manager.

    Args:
        package_manager (str): The package manager to be used within the DocScribe environment.

    Note:
        If the local directory creation or configuration file writing fails, it prints an error
        message and exits the function early.

    """
    if CONFIG_FILE.exists():
        rich.print(
            f"[bold blue]Info:[/bold blue] Configuration file already exists at {CONFIG_FILE}"
        )
        return

    path = REPOSITORIES_DIR / "local"
    try:
        path.mkdir(exist_ok=True, parents=True)
    except Exception as e:
        rich.print(f"[red]Error[/red]: {e}")
        return

    config = {
        "repositories_directory": str(REPOSITORIES_DIR),
        "package_manager": package_manager,
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
