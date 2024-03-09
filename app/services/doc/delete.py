import rich
import click

from app.constants import REPOSITORIES_DIR


def run(doc_name: str, repository: str = "local"):
    """
    Deletes a specified document and its associated files from a given repository.

    This function first verifies the existence of the specified repository and document.
    If both are confirmed to exist, it proceeds to delete the document's directory and all
    files within it, effectively removing the document from the repository. If the repository
    or document does not exist, it prints an error message and aborts the operation.

    Args:
        doc_name (str): The name of the document to be deleted.
        repository (str, optional): The repository from which the document will be deleted.
                                    Defaults to "local".

    Raises:
        click.Abort: If either the repository or the document does not exist.

    The deletion process includes removing all files associated with the document, followed
    by the removal of the document's directory itself. Upon successful deletion, a confirmation
    message is printed.
    """
    repo_path = REPOSITORIES_DIR / repository

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
