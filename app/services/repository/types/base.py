from typing import Iterable
from abc import ABC, abstractmethod

from app.utils.segment import Segment


class Repository(Segment, ABC):
    """
    Abstract base class for defining repository services.

    This class extends the Segment class to include functionalities specific to repository
    services, providing a template for implementing repository operations such as downloading
    reports and listing available reports.

    Attributes:
        name (str): The name of the repository.
        _type (str): The type of the repository (e.g., "local", "s3").
        config (dict | None): Configuration details for the repository. Defaults to None.

    Methods:
        download(report_name: str): Abstract method to download a report by its name.
        list_reports(*args, **kwargs): Abstract method to list available reports.
    """

    def __init__(self, name: str, _type: str, config: dict | None = None):
        super().__init__(name, _type, "repositories", config)

    @abstractmethod
    def download(self, report_name: str) -> None:
        """
        Download a specific report by its name.

        Parameters:
            report_name (str): The name of the report to download.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        ...

    @abstractmethod
    def list_reports(self, *args, **kwargs) -> Iterable[str]:
        """
        List the names of available reports.

        This method may accept additional arguments and keyword arguments specific to
        the repository implementation.

        Returns:
            Iterable[str]: An iterable of strings, each representing a report name.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        ...
