import rich
import click

from app.utils.validations import validate_config
from app.services.repository.main import list_reports as run


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    if not repository:
        repositories = validate_config("repositories")

        for repo in repositories:
            click.echo(repo)
        return

    if repository == "local":
        rich.print("[green]Local repository is always available[/green]")
        return

    run(repository)
