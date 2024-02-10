from docscribe.services.repository.manager import (
    RepositoryManager,
    REPOSITORY_TYPES,
)


def create_repository() -> None:
    manager = RepositoryManager(None)
    manager.create_repository()
    print("Repository created.")


def list_reports(repository_name: str | None) -> None:
    manager = RepositoryManager(repository_name)
    reports = manager.list_reports()
    print(reports)


def download(repository_name: str | None, report_name: str) -> None:
    manager = RepositoryManager(repository_name)
    manager.download(report_name)
    print(f"{report_name} downloaded.")
