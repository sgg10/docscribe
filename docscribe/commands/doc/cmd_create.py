import json
from pathlib import Path

import rich
import click

from docscribe.constants import (
    DIRECTORY,
    TEMPLATES_TYPES,
    CONFIG_FILE,
)
from docscribe.services.doc.create import run


@click.command()
@click.option("-n", "--name", "doc_name", help="Name of the new document")
@click.option(
    "-r", "--repository", help="Repository to create the document in", default="local"
)
@click.option(
    "-t",
    "--type",
    "doc_type",
    type=click.Choice(TEMPLATES_TYPES.choices()),
    help="Type of the document",
    default=TEMPLATES_TYPES.default(),
)
def command(doc_name, repository, doc_type):
    """Create a new document."""

    # Load config file
    config_file = Path(CONFIG_FILE)

    if not config_file.exists():
        raise click.Abort(f"Config file {config_file} does not exist")

    with config_file.open("r") as file:
        config = json.load(file)

    if repository not in config.get("repositories", {"local": {}}):
        raise click.Abort(f"Repository {repository} does not exist in config")

    if not doc_name:
        # Prompt for doc name
        doc_name = click.prompt("Enter the name of the document")
        while not doc_name:
            rich.print("[red]Document name cannot be empty[/red]")
            doc_name = click.prompt("Enter the name of the document")

    run(doc_name, repository, doc_type)
