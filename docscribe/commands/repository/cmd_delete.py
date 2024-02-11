import click

from docscribe.utils.validations import validate_config
from docscribe.services.repository.main import delete_repository as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    if not repository:

        repositories = validate_config("repositories")

        repository = click.prompt(
            "Enter the name of the repository to delete",
            type=click.Choice(repositories.keys()),
        )

    run(repository)
