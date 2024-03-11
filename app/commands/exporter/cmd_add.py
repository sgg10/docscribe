import click

from app.services.exporter.main import create_exporter as run


@click.command()
def command():
    """
    CLI command to create a new exporter.

    This command invokes the functionality to create a new exporter instance within the application.
    It does not require any arguments or options from the user; all necessary inputs will be gathered
    interactively if required by the underlying `create_exporter` function.

    Upon successful execution, an exporter is created according to the user-provided configuration,
    and relevant feedback is displayed to the user.
    """
    run()
