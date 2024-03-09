from pathlib import Path

import rich

from app.constants import LOCAL_EXPORTS_DIR
from app.services.exporter.types.base import Exporter


class Local(Exporter):
    """
    An exporter that saves documents to a local directory.

    This class implements the abstract methods of the `Exporter` class to provide
    functionality for exporting documents to the local filesystem. It utilizes
    the LOCAL_EXPORTS_DIR from the application's constants to determine the base
    directory for exports.

    Attributes:
        name (str): The name of the local exporter.
        config (dict | None): Configuration for the local exporter. This is optional
            as the local exporter does not require specific configuration.
    """

    def __init__(self, name: str, config: dict | None = None):
        """
        Initializes a new instance of the Local exporter class.

        Args:
            name (str): The name of the exporter.
            config (dict | None): Configuration for the exporter. Defaults to None
                                since the local exporter does not require any.
        """
        super().__init__(name, "local", config)

    def make_output_uri(self, file_name) -> str:
        """
        Generates the local file path for the exported file.

        Args:
            file_name (str): The name of the file to be exported.

        Returns:
            str: The full path where the file will be saved.
        """
        path = LOCAL_EXPORTS_DIR / self.name
        path.mkdir(exist_ok=True, parents=True)
        return str(path.joinpath(file_name))

    def export(self, file_name: str, *args, **kwargs) -> None:
        """
        Exports the content to a file in the local filesystem.

        The file is read from the given file name and then written to the local
        export directory. The original file is removed after export.

        Args:
            file_name (str): The name of the file containing the content to export.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Supports "mode" to specify file reading mode.

        Note:
            The file is deleted after being exported to the local directory.
        """
        mode = kwargs.get("mode", "rb")

        file = Path(file_name)

        with file.open(mode) as f:
            content = f.read()

        output_uri = self.make_output_uri(file_name.name)
        output_uri = Path(output_uri)
        output_uri.parent.mkdir(exist_ok=True, parents=True)
        with output_uri.open("w" if mode == "r" else "wb") as f:
            f.write(content)

        file.unlink()
        rich.print(f"[green]Report saved at {output_uri}[/green]")

    def _auth(self):
        """
        Local exporter does not require authentication.

        This method is implemented as a formality and does not perform any action.
        """
        pass

    def _create_config(self, *args, **kwargs) -> dict:
        """
        Returns an empty configuration dictionary.

        Local exporter does not require any specific configuration. This method
        is overridden to provide informational output indicating no configuration
        is necessary.

        Returns:
            dict: An empty dictionary.
        """
        rich.print(
            "[blue][INFO]Local exporter does not require any configuration.[/blue]"
        )
        return {}
