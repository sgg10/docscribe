from abc import ABC, abstractmethod

from app.utils.segment import Segment


class Exporter(Segment, ABC):
    """
    Abstract base class for defining exporters in the application.

    Exporters are responsible for exporting documents to various destinations
    or formats as specified by their implementations. This class extends the
    `Segment` class, categorizing itself under the 'exporters' segment.

    Attributes:
        name (str): The name of the exporter.
        _type (str): The type of the exporter (e.g., 'local', 's3').
        config (dict, optional): Configuration options specific to the exporter type.

    Methods:
        export(file_name: str, content) -> None: Abstract method to export content to a file.
        make_output_uri(file_name: str) -> str: Abstract method to generate the output URI for the exported file.
    """

    def __init__(self, name: str, _type: str, config: dict | None = None):
        """
        Initializes a new instance of the Exporter class.

        Args:
            name (str): The name of the exporter.
            _type (str): The type of the exporter.
            config (dict | None): Optional configuration for the exporter. Defaults to None.
        """
        super().__init__(name, _type, "exporters", config)

    @abstractmethod
    def export(self, file_name: str, content) -> None:
        """
        Exports content to a specified file.

        This method should be implemented by subclasses to handle the export logic
        for the specific exporter type.

        Args:
            file_name (str): The name of the file to export the content to.
            content: The content to export.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        ...

    @abstractmethod
    def make_output_uri(self, file_name: str) -> str:
        """
        Generates the output URI for the exported file.

        This method should be implemented by subclasses to construct the URI or
        path where the exported file will be accessible.

        Args:
            file_name (str): The name of the file for which to generate the URI.

        Returns:
            str: The output URI for the exported file.

        Raises:
            NotImplementedError: If the subclass does not implement this method.
        """
        ...
