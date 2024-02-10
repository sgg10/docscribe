import json
import click
from docscribe.constants import CONFIG_FILE

from docscribe.services.repository.main import delete_repository as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    if not repository:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        repositories = data.get("repositories", {})

        if not repositories:
            click.echo("No repositories found.")
            return

        repository = click.prompt(
            "Enter the name of the repository to delete",
            type=click.Choice(repositories.keys()),
        )

    run(repository)
