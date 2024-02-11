from typing import Iterable

import click

from docscribe.utils.managers import SegmentManager


class RepositoryManager(SegmentManager):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name, "repositories")

    def download(self, report_name: str) -> None:
        if not self.repository:
            click.echo(f"Repository {self.repository} not found.")
            return
        self.repository.download(report_name)

    def list_reports(self, *args, **kwargs) -> Iterable[str]:
        if not self.repository:
            click.echo(f"Repository {self.repository} not found.")
            return
        return self.repository.list_reports(*args, **kwargs)
