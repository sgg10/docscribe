import rich
import click

from app.constants import CONFIG_FILE

from app.services.doc.delete import run
from app.utils.validations import validate_config


@click.command()
@click.option("-n", "--name", "doc_name", help="Name of the document to delete")
@click.option(
    "-r", "--repository", help="Repository to delete the document from", default="local"
)
def command(doc_name, repository):
    """
    Deletes a specified document from a given repository.

    This command allows users to delete a document by specifying its name and the repository
    it resides in. The command validates the existence of the configuration file and checks
    if the specified repository is configured. Before performing the deletion, it prompts the
    user to confirm the action. If the document name is not provided through the command line,
    the user will be prompted to enter it.

    Args:
        doc_name (str): The name of the document to delete.
        repository (str): The name of the repository from which the document will be deleted. Defaults to 'local'.

    Raises:
        click.Abort: If the configuration file does not exist, if the specified repository is not found in the configuration,
                     or if the document name is not provided. Also, if the user does not confirm the deletion action.
    """

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
