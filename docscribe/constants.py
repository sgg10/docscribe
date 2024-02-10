from enum import Enum


DIRECTORY = "docscribe_repos"
CONFIG_FILE = ".docscribe_config.json"


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

    # @classmethod
    # def __iter__(cls):
    #     return iter(cls.choices())

    # @classmethod
    # def __contains__(cls, value):
    #     return value in cls.choices()
