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
    """
    Creates a new document in the specified repository with the given name and type.

    This command initializes a new document creation process, which includes validating
    the existence of the configuration file and repository. It then proceeds to create
    the document if all validations pass. If any validation fails, the process is aborted,
    and an appropriate error message is displayed.

    Args:
        doc_name (str): The name of the new document. If not provided, the user will be prompted.
        repository (str): The name of the repository where the document will be created. Defaults to 'local'.
        doc_type (str): The type of the document (e.g., 'docx', 'md', 'html'). Defaults to the system's default type.

    Raises:
        click.Abort: If the config file does not exist, if the specified repository is not found in the configuration,
                     or if no document name is provided.
    """

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
