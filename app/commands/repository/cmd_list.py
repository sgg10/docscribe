import click
from rich.console import Console
from rich.markdown import Markdown

from app.utils.validations import validate_config
from app.services.repository.main import list_reports as run


console = Console()


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    if not repository:
        repositories = validate_config("repositories")

        repositories_str = "\n\n- ".join(repositories)
        console.print(Markdown(f"**Available repositories:**\n\n- {repositories_str}"))

        return

    if repository == "local":
        console.print("[green]Local repository is always available[/green]")
        return

    run(repository)
