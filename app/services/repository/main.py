from rich.console import Console
from rich.markdown import Markdown

from app.services.repository.manager import RepositoryManager

console = Console()


def create_repository() -> None:
    manager = RepositoryManager(None)
    manager.create_segment()
    console.print("[green]Repository created.[/green]")


def list_reports(repository_name: str | None) -> None:
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
    manager = RepositoryManager(repository_name)
    manager.download(report_name)
    console.print(f"[green]{report_name} downloaded.[/green]")


def delete_repository(repository_name: str) -> None:
    manager = RepositoryManager(repository_name)
    manager.delete_segment()
    console.print(f"[green]{repository_name} deleted.[/green]")
