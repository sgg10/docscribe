import click

from docscribe.services.repository.main import download as run


@click.command()
@click.argument("repository", required=True)
@click.argument("report_name", required=True)
def command(repository, report_name):
    """Download a report from a repository"""
    run(repository, report_name)
