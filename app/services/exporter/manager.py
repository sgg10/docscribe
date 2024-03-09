from app.utils.managers import SegmentManager


class ExporterManager(SegmentManager):
    """
    Manages exporter segments, facilitating the export of files through dynamically
    chosen export strategies, such as local filesystem or cloud services like AWS S3.

    Inherits from SegmentManager to utilize common segment handling functionality while
    adding specific behaviors related to file exporting.

    Attributes:
        name (str | None): The name of the exporter segment to manage. If None, the manager operates without a specific exporter segment.

    Methods:
        export(file_name: str, *args, **kwargs) -> None: Exports a file using the configured exporter segment.
        make_output_uri(file_name: str) -> str: Generates the output URI for a file using the configured exporter segment.
    """

    def __init__(self, name: str | None = None) -> None:
        """
        Initializes a new instance of ExporterManager with an optional name for the exporter segment.

        Args:
            name (str | None): The name of the exporter segment to manage. Defaults to None.
        """
        super().__init__(name, "exporters")

    def export(self, file_name: str, *args, **kwargs) -> None:
        """
        Exports a file using the configured exporter segment.

        This method validates the current segment and delegates the export process
        to the exporter's export method.

        Args:
            file_name (str): The name of the file to export.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, potentially including a 'mode' to specify how the file should be opened.
        """
        self._validate_segment()
        self.segment.export(file_name, mode=kwargs.get("mode", "rb"))

    def make_output_uri(self, file_name: str) -> str:
        """
        Generates the output URI for a file using the configured exporter segment.

        This method validates the current segment and calls its make_output_uri method
        to generate the appropriate URI for the exported file.

        Args:
            file_name (str): The name of the file for which to generate the output URI.

        Returns:
            str: The output URI for the file.
        """
        self._validate_segment()
        return self.segment.make_output_uri(file_name)
