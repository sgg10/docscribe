import click

from app.utils.validations import validate_config
from app.services.exporter.main import delete_exporter as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    """
    CLI command to delete an exporter.

    This command allows for the deletion of an existing exporter. The name of the exporter
    can be provided as an argument. If not provided, the command will interactively prompt the user
    to choose from a list of available exporters.

    Parameters:
    - repository (str, optional): The name of the exporter to delete. Defaults to None, triggering
        an interactive selection process.

    Upon successful execution, the specified exporter is deleted, and a confirmation message is displayed.
    """
    if not repository:
        exporters = validate_config("exporters")

        repository = click.prompt(
            "Enter the name of the repository to delete",
            type=click.Choice(exporters.keys()),
        )

    run(repository)
