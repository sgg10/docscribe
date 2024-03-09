import click
from rich.console import Console
from rich.markdown import Markdown

from app.utils.validations import validate_config
from app.services.repository.main import list_reports as run


console = Console()


@click.command()
@click.argument("repository", required=False, default=None)
def command(repository):
    """
    Lists the reports available in a specified repository or displays available
    repositories if none is specified.

    This command provides the user with a list of reports available in the specified repository.
    If no repository is specified, it lists all available repositories.
    For the 'local' repository, a specific message indicates its always available status.

    Args:
        repository (str, optional): The name of the repository to list the reports from.
            If not provided, the command will list all available repositories.

    """
    if not repository:
        repositories = validate_config("repositories")

        repositories_str = "\n\n- ".join(repositories)
        console.print(Markdown(f"**Available repositories:**\n\n- {repositories_str}"))

        return

    if repository == "local":
        console.print("[green]Local repository is always available[/green]")
        return

    run(repository)
