from botocore.exceptions import NoCredentialsError, ClientError, ProfileNotFound

import rich

from app.constants import REPOSITORIES_DIR
from app.services.repository.types.base import Repository
from app.utils.s3 import create_s3_segment_config, s3_auth


class S3(Repository):
    """
    S3 Repository class for handling operations with S3 as a storage backend.

    This class implements methods to authenticate with AWS S3, download reports from S3
    to a local repository directory, and list reports available in the S3 bucket.

    Attributes:
        name (str): The name of the repository.
        _type (str): Set to "s3" to indicate the repository type.
        config (dict | None): Configuration details specific to the S3 repository.
            Should include bucket name, prefix, and authentication method.

    Methods:
        _auth(): Authenticate with AWS S3 using the provided configuration.
        download(report_name: str): Download a report from S3 to the local repository directory.
        list_reports(*args, **kwargs): List the names of reports available in the S3 bucket.
        _create_config(*args, **kwargs): Generate the initial configuration for an S3 repository.
    """

    def __init__(self, name: str, config: dict | None = None):
        super().__init__(name, "s3", config)

    def _auth(self):
        """
        Authenticate with AWS S3 using the configuration provided during initialization.

        This method sets up an S3 client to be used for subsequent operations.
        """
        self.s3 = s3_auth(**self.config)

    def download(self, report_name: str) -> None:
        """
        Download a report from S3 to the local repository directory.

        Parameters:
            report_name (str): The name of the report to download.

        This method downloads the specified report from the S3 bucket to the local
        repository directory, creating necessary subdirectories as needed.
        """
        self._auth()
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            response_iterator = paginator.paginate(
                Bucket=self.config["bucket"],
                Prefix=f"{self.config['prefix'].rstrip('/')}/{report_name}",
            )
            path = REPOSITORIES_DIR.joinpath(self.name, report_name)
            path.mkdir(exist_ok=True, parents=True)

            for page in response_iterator:
                for obj in page.get("Contents", []):
                    self.s3.download_file(
                        self.config["bucket"],
                        obj["Key"],
                        f"{path}/{obj['Key'].split('/')[-1]}",
                    )
        except (NoCredentialsError, ClientError) as e:
            rich.print(f"[red][ERROR] {e}[/red]")

    def list_reports(self, *args, **kwargs) -> list[str]:
        """
        List the names of reports available in the configured S3 bucket.

        Returns:
            list[str]: A list of report names available in the S3 bucket.
        """
        self._auth()
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            response_iterator = paginator.paginate(
                Bucket=self.config["bucket"],
                Prefix=self.config["prefix"],
                Delimiter="/",
            )
            return [
                obj["Prefix"].split("/")[-2]
                for page in response_iterator
                for obj in page.get("CommonPrefixes", [])
            ]
        except (NoCredentialsError, ClientError) as e:
            rich.print(f"[red][ERROR] {e}[/red]")

    def _create_config(self, *args, **kwargs) -> dict:
        """
        Generate the initial configuration for an S3 repository.

        This method prompts the user for necessary configuration details and returns
        a dictionary representing the S3 repository configuration.

        Returns:
            dict: The generated configuration dictionary.
        """
        return create_s3_segment_config()
