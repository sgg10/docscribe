import json
import click
from docscribe.constants import CONFIG_FILE

from docscribe.services.exporter.main import delete_exporter as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    if not repository:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        exporters = data.get("exporters", {})

        if not exporters:
            click.echo("No exporters found.")
            return

        repository = click.prompt(
            "Enter the name of the repository to delete",
            type=click.Choice(exporters.keys()),
        )

    run(repository)
