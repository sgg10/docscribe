import json

import click

from docscribe.constants import CONFIG_FILE, DIRECTORY
from docscribe.services.repository.main import list_reports as run


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

        for repo in repositories:
            click.echo(repo)
        return

    run(repository)
