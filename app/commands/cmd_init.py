import click

from app.services.init import run


@click.command()
# Add option to specify the python package manager (pipenv, pip, etc.)
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
    """Initialize docscribe configuration"""
    run(package_manager)
