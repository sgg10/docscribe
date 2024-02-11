import click

from app.services.init import run


@click.command()
def command():
    """Initialize docscribe configuration"""
    run()
