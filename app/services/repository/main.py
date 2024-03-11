from rich.console import Console
from rich.markdown import Markdown

from app.services.repository.manager import RepositoryManager

console = Console()


def create_repository() -> None:
    """
    Creates a new repository by invoking the repository management interface.

    This function instantiates a RepositoryManager with no specific repository name,
    allowing the user to create a new repository segment through the command-line interface.
    A success message is printed upon the successful creation of the repository.
    """
    manager = RepositoryManager(None)
    manager.create_segment()
    console.print("[green]Repository created.[/green]")


def list_reports(repository_name: str | None) -> None:
    """
    Lists all reports available in a specified repository.

    Parameters:
        repository_name (str | None): The name of the repository from which to list reports.
            If None, a default or all repositories may be targeted, based on implementation.

    This function fetches and displays a list of reports from the specified repository.
    If no reports are available, a message is printed indicating the lack of available reports.
    """
    manager = RepositoryManager(repository_name)
    reports = manager.list_reports()

    if not reports:
        console.print(f"[blue]{repository_name} has not available reports.[/blue]")
        return

    report_names = "\n\n- ".join(reports)

    result = f"**{repository_name}** reports:\n\n - {report_names}"
    md = Markdown(result)
    console.print(md)


def download(repository_name: str | None, report_name: str) -> None:
    """
    Downloads a specific report from a repository.

    Parameters:
        repository_name (str | None): The name of the repository from which to download the report.
            If None, a default or specific logic may determine the repository.
        report_name (str): The name of the report to download.

    This function attempts to download the specified report from the given repository,
    printing a success message upon completion.
    """
    manager = RepositoryManager(repository_name)
    manager.download(report_name)
    console.print(f"[green]{report_name} downloaded.[/green]")


def delete_repository(repository_name: str) -> None:
    """
    Deletes a specified repository.

    Parameters:
        repository_name (str): The name of the repository to delete.

    This function invokes the repository management interface to delete a repository by name,
    printing a success message upon the successful deletion of the repository.
    """
    manager = RepositoryManager(repository_name)
    manager.delete_segment()
    console.print(f"[green]{repository_name} deleted.[/green]")
