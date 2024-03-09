import click

from app.utils.validations import validate_config
from app.services.repository.main import delete_repository as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    """
    Deletes a specified repository or prompts the user to select one to delete from a list of configured repositories.

    This command deletes a repository configuration from the application's configuration settings.
    If the repository name is not provided as a command-line argument, it retrieves a list of currently
    configured repositories and prompts the user to select one for deletion. This interactive approach ensures
    the user is aware of which repository is being deleted, reducing the risk of accidental deletions.

    Parameters:
        repository (str, optional): The name of the repository to be deleted. If not provided, the command will prompt the user to choose from a list of existing repositories.
    """
    if not repository:

        repositories = validate_config("repositories")

        repository = click.prompt(
            "Enter the name of the repository to delete",
            type=click.Choice(repositories.keys()),
        )

    run(repository)
