import json
from pathlib import Path

import rich
import click

from docscribe.constants import CONFIG_FILE

from docscribe.services.doc.delete import run
from docscribe.utils.validations import validate_config


@click.command()
@click.option("-n", "--name", "doc_name", help="Name of the document to delete")
@click.option(
    "-r", "--repository", help="Repository to delete the document from", default="local"
)
def command(doc_name, repository):
    """Delete a document."""

    if not CONFIG_FILE.exists():
        raise click.Abort(f"Config file {CONFIG_FILE} does not exist")

    repositories = validate_config("repositories", abort=False)
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

    # ask for confirmation
    if not click.confirm(
        f"Are you sure you want to delete {doc_name} from {repository}"
    ):
        rich.print("[red]Aborted![/red]")
        return
    run(doc_name, repository)
