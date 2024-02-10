import click

from docscribe.services.repository.main import create_repository as run


@click.command()
def command():
    """Create a new repository"""
    run()
