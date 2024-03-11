from typing import Iterable

from app.utils.managers import SegmentManager


class RepositoryManager(SegmentManager):
    """
    Manages repository segments to facilitate operations such as downloading reports
    and listing available reports within a specific repository.

    This class leverages the functionality provided by the SegmentManager class to
    handle repository-specific actions, ensuring that operations are performed on
    valid repository segments.

    Attributes:
        name (str | None): The name of the repository. If None, operations may target
            a default or all repositories, based on implementation. Defaults to None.

    Methods:
        download(report_name: str): Downloads a report from the repository.
        list_reports(*args, **kwargs): Lists all available reports in the repository.
    """

    def __init__(self, name: str | None = None) -> None:
        """
        Initializes the RepositoryManager with a specific repository name.

        Parameters:
            name (str | None): The name of the repository to manage. Defaults to None.
        """
        super().__init__(name, "repositories")

    def download(self, report_name: str) -> None:
        """
        Downloads a report by its name from the managed repository.

        Validates that the repository segment is properly set before attempting to
        download the report.

        Parameters:
            report_name (str): The name of the report to download.
        """
        self._validate_segment()
        self.segment.download(report_name)

    def list_reports(self, *args, **kwargs) -> Iterable[str]:
        """
        Lists the names of all available reports within the managed repository.

        Validates that the repository segment is properly set before listing the
        reports. This method may accept additional arguments and keyword arguments
        that are passed directly to the underlying segment's list_reports method.

        Returns:
            Iterable[str]: An iterable of strings, each representing a report name.
        """
        self._validate_segment()
        return self.segment.list_reports(*args, **kwargs)
