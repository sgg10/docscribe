from abc import ABC, abstractmethod

from docscribe.utils.config_operations import (
    write_item_by_segment,
    delete_item_by_segment,
)


class Segment(ABC):
    def __init__(self, name: str, _type: str, segment: str, config: dict | None = None):
        self.name = name
        self._type = _type
        self.segment = segment
        if config is None:
            self.config = self._create_config()
            self._write_config()
        else:
            self.config = config

    @abstractmethod
    def _auth(self): ...

    @abstractmethod
    def _create_config(self, *args, **kwargs) -> dict:
        return {}

    def _write_config(self) -> None:
        write_item_by_segment(self.segment, self.name, self._type, self.config)

    def delete(self) -> None:
        delete_item_by_segment(self.segment, self.name)
