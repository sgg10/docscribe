from pathlib import Path

import rich

from botocore.exceptions import NoCredentialsError, ClientError
from app.services.exporter.types.base import Exporter
from app.utils.s3 import create_s3_segment_config, s3_auth


class S3(Exporter):
    def __init__(self, name: str, config: dict | None = None):
        super().__init__(name, "s3", config)

    def _auth(self):
        self.s3 = s3_auth(**self.config)

    def make_output_uri(self, file_name: str, full_uri: bool = False) -> str:
        if full_uri:
            return f"s3://{self.config['bucket']}/{self.config['prefix'].rstrip('/')}/{file_name}"
        return f"{self.config['prefix'].rstrip('/')}/{file_name}"

    def export(self, file_path: str, *args, **kwargs) -> None:
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
        return create_s3_segment_config()
