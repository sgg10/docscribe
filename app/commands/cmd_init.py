import click

from app.services.init import run


@click.command()
@click.option(
    "--package-manager",
    "-p",
    "package_manager",
    required=True,
    help="Python package manager to use",
    type=click.Choice(
        [
            "pip",
            "pip3",
            "pipenv",
        ]
    ),
)
def command(package_manager):
    """
    Initializes the DocScribe environment with the specified package manager.

    This CLI command is responsible for setting up the initial configuration for the DocScribe
    environment. It requires the user to specify a Python package manager, which will be used
    by DocScribe for managing Python packages. The supported package managers are pip, pip3,
    and pipenv.
    """
    run(package_manager)
