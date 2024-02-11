import click

from app.services.exporter.main import create_exporter as run


@click.command()
def command():
    """Create a new exporter"""
    run()
