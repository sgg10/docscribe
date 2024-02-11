import click

from app.utils.validations import validate_config
from app.services.exporter.main import delete_exporter as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    if not repository:
        exporters = validate_config("exporters")

        repository = click.prompt(
            "Enter the name of the repository to delete",
            type=click.Choice(exporters.keys()),
        )

    run(repository)
