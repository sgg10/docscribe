import json
from typing import Iterable
from abc import ABC, abstractmethod

from docscribe.constants import CONFIG_FILE


class Repository(ABC):
    def __init__(self, name: str, _type: str, config: dict | None = None):
        self.name = name
        self._type = _type
        if config is None:
            self.config = self._create_config()
            self._write_config()
        else:
            self.config = config

    @abstractmethod
    def _auth(self):
        pass

    @abstractmethod
    def download(self, report_name: str) -> None:
        pass

    @abstractmethod
    def list_reports(self, *args, **kwargs) -> Iterable[str]:
        pass

    @abstractmethod
    def _create_config(self, *args, **kwargs) -> dict:
        return {}

    def _write_config(self) -> None:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        repos = data.get("repositories", {})
        repos[self.name] = {"type": self._type, "config": self.config}
        data["repositories"] = repos

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def delete(self) -> None:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        repos = data.get("repositories", {})
        del repos[self.name]
        data["repositories"] = repos

        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f, indent=4)
