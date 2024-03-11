from pathlib import Path

import rich

from botocore.exceptions import NoCredentialsError, ClientError
from app.services.exporter.types.base import Exporter
from app.utils.s3 import create_s3_segment_config, s3_auth


class S3(Exporter):
    """
    Implements the Exporter interface for exporting files to AWS S3.

    This class handles authentication with AWS, generating the correct output URI,
    and performing the file upload to the specified S3 bucket.

    Attributes:
        name (str): The name of the exporter.
        config (dict, optional): Configuration for the S3 exporter, including bucket and authentication details.

    Methods:
        _auth(): Authenticates with AWS S3 using the provided configuration.
        make_output_uri(file_name: str, full_uri: bool = False) -> str: Generates the S3 path or full URI for the exported file.
        export(file_path: str, *args, **kwargs) -> None: Uploads the given file to AWS S3.
        _create_config(*args, **kwargs) -> dict: Prompts the user for S3 configuration details and returns them.
    """

    def __init__(self, name: str, config: dict | None = None):
        """
        Initializes a new instance of the S3 exporter.

        Args:
            name (str): The name of the exporter.
            config (dict | None): Optional configuration for the S3 exporter. Defaults to None.
        """
        super().__init__(name, "s3", config)

    def _auth(self):
        """
        Authenticates with AWS S3 using the provided configuration.
        """
        self.s3 = s3_auth(**self.config)

    def make_output_uri(self, file_name: str, full_uri: bool = False) -> str:
        """
        Generates the S3 path or full URI for the exported file.

        Args:
            file_name (str): The name of the file to export.
            full_uri (bool, optional): Whether to return the full URI or just the path. Defaults to False.

        Returns:
            str: The S3 path or full URI for the exported file.
        """
        if full_uri:
            return f"s3://{self.config['bucket']}/{self.config['prefix'].rstrip('/')}/{file_name}"
        return f"{self.config['prefix'].rstrip('/')}/{file_name}"

    def export(self, file_path: str, *args, **kwargs) -> None:
        """
        Uploads the given file to AWS S3.

        Args:
            file_path (str): The path of the file to upload.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self._auth()
        try:
            # Upload the file
            self.s3.upload_file(
                Filename=file_path,
                Bucket=self.config["bucket"],
                Key=f"{self.config['prefix'].rstrip('/')}/{Path(file_path).name}",
            )

            # Delete the local file
            file_path = Path(file_path)
            file_path.unlink()

            rich.print(
                f"[green]Report saved at {self.make_output_uri(file_path.name, full_uri=True)}[/green]"
            )
        except (NoCredentialsError, ClientError) as e:
            rich.print(f"[red][ERROR] {e}[/red]")

    def _create_config(self, *args, **kwargs) -> dict:
        """
        Prompts the user for S3 configuration details and returns them.

        Returns:
            dict: The configuration details for the S3 exporter.
        """
        return create_s3_segment_config()
