from pathlib import Path

import rich
import click

from docscribe.constants import DIRECTORY, TEMPLATES_TYPES


def run(doc_name: str, repository: str = "local"):
    """Delete a doc from the given repository."""
    repo_path = Path(DIRECTORY) / repository

    if not repo_path.exists():
        raise click.Abort(f"Repository {repository} does not exist")

    doc_path = repo_path / doc_name
    if not doc_path.exists():
        raise click.Abort(f"Document {doc_name} does not exist in {repository}")

    click.echo(f"Deleting {doc_name} document from {repository}")

    # Remove the all the files and the directory
    for file in doc_path.iterdir():
        file.unlink()

    # Remove directory
    doc_path.rmdir()

    rich.print(f"[green]Document {doc_name} deleted successfully[/green]")
