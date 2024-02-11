import click

from docscribe.services.init import run


@click.command()
# @click.option(
#     "-d",
#     "--directory",
#     default="docscribe_repos",
#     help="Path to save the reports/documents repositories",
# )
# @click.option(
#     "-f",
#     "--file",
#     default=".docscribe_config.json",
#     help="File to save docscribe configuration",
# )
# def command(directory, file):
def command():
    """Initialize docscribe configuration"""
    run()
