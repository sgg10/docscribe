import click

from docscribe.utils.validations import validate_config
from docscribe.services.repository.main import list_reports as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    if not repository:
        repositories = validate_config("repositories")

        for repo in repositories:
            click.echo(repo)
        return

    run(repository)
