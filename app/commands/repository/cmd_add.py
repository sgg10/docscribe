import click

from app.services.repository.main import create_repository as run


@click.command()
def command():
    """Create a new repository"""
    run()
