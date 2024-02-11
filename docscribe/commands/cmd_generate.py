import json
from pathlib import Path

import rich
import click

from docscribe.constants import (
    DIRECTORY,
    CONFIG_FILE,
)
from docscribe.services.generator.main import run


@click.command()
@click.option("-n", "--name", "doc_name", help="Name of the document to delete")
@click.option(
    "-r", "--repository", help="Repository to delete the document from", default="local"
)
@click.option(
    "--use-default-kwargs",
    is_flag=True,
    default=False,
    help="Use default kwargs for the document",
)
def command(doc_name, repository, use_default_kwargs):
    """Generate a document"""
    config_file = Path(CONFIG_FILE)

    if not config_file.exists():
        raise click.Abort(f"Config file {config_file} does not exist")

    with config_file.open("r") as file:
        config = json.load(file)

    repositories = config.get("repositories")
    if not repositories:
        repositories = {"local": {}}

    if repository not in repositories:
        raise click.Abort(f"Repository {repository} does not exist in config")

    if not doc_name:
        # Prompt for doc name
        doc_name = click.prompt("Enter the name of the document to delete")
        while not doc_name:
            rich.print("[red]Document name cannot be empty[/red]")
            doc_name = click.prompt("Enter the name of the document to delete")

    run(doc_name, repository, use_default_kwargs)
