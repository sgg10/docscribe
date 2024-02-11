from typing import Iterable
from abc import ABC, abstractmethod

from app.utils.segment import Segment


class Repository(Segment, ABC):
    def __init__(self, name: str, _type: str, config: dict | None = None):
        super().__init__(name, _type, "repositories", config)

    @abstractmethod
    def download(self, report_name: str) -> None: ...

    @abstractmethod
    def list_reports(self, *args, **kwargs) -> Iterable[str]: ...
