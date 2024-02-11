from enum import Enum
from pathlib import Path
from typing import Literal

from docscribe.utils.read_config import read_config


DIRECTORY = Path("docscribe_repos")
CONFIG_FILE = Path(".docscribe_config.json")
TMP_DIR = DIRECTORY / ".tmp"

CONFIG = read_config()

CONFIG_SEGMENTS = Literal["repositories", "exporters"]


class TEMPLATES_TYPES(Enum):
    DOCX: str = "docx"
    MD: str = "md"
    HTML: str = "html"

    @classmethod
    def choices(cls):
        return [choice.value for choice in cls]

    @classmethod
    def default(cls):
        return cls.DOCX.value

    @classmethod
    def validate(cls, value):
        if value not in cls.choices():
            raise ValueError(
                f"Invalid report type: {value}. Must be one of {cls.choices()}"
            )
        return value
