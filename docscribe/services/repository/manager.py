from typing import Iterable

import click

from docscribe.utils.managers import SegmentManager


class RepositoryManager(SegmentManager):
    def __init__(self, name: str | None = None) -> None:
        super().__init__(name, "repositories")

    def download(self, report_name: str) -> None:
        self._validate_segment()
        self.segment.download(report_name)

    def list_reports(self, *args, **kwargs) -> Iterable[str]:
        self._validate_segment()
        return self.segment.list_reports(*args, **kwargs)
