from abc import ABC, abstractmethod

from docscribe.utils.segment import Segment


class Exporter(Segment, ABC):
    def __init__(self, name: str, _type: str, config: dict | None = None):
        super().__init__(name, _type, "exporters", config)

    @abstractmethod
    def export(self, file_name: str, content) -> None: ...

    @abstractmethod
    def make_output_uri(self, file_name: str) -> str: ...
