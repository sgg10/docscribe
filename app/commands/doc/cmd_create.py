import rich
import click

from app.constants import (
    CONFIG_FILE,
    TEMPLATES_TYPES,
)
from app.services.doc.create import run
from app.utils.validations import validate_config


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

    if not CONFIG_FILE.exists():
        rich.print(f"[red]Config file {CONFIG_FILE} does not exist[/red]")
        raise click.Abort()

    repositories = validate_config("repositories", abort=False)

    if not repositories:
        repositories = {"local": {}}

    if repository not in repositories:
        rich.print(f"[red]Repository {repository} does not exist in config[/red]")
        raise click.Abort()

    if not doc_name:
        # Prompt for doc name
        doc_name = click.prompt("Enter the name of the document")
        while not doc_name:
            rich.print("[red]Document name cannot be empty[/red]")
            doc_name = click.prompt("Enter the name of the document")

    run(doc_name, repository, doc_type)
