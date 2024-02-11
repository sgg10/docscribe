import rich
import click

from app.constants import DIRECTORY


def run(doc_name: str, repository: str = "local"):
    """Delete a doc from the given repository."""
    repo_path = DIRECTORY / repository

    if not repo_path.exists():
        rich.print(f"[red]Repository {repository} does not exist[/red]")
        raise click.Abort()

    doc_path = repo_path / doc_name
    if not doc_path.exists():
        rich.print(f"[red]Document {doc_name} does not exist in {repository}[/red]")
        raise click.Abort()

    rich.print(f"[blue]Deleting {doc_name} document from {repository}[/blue]")

    # Remove the all the files and the directory
    for file in doc_path.iterdir():
        file.unlink()

    # Remove directory
    doc_path.rmdir()

    rich.print(f"[green]Document {doc_name} deleted successfully[/green]")
