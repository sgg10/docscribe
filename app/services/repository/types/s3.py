from botocore.exceptions import NoCredentialsError, ClientError, ProfileNotFound

from app.constants import DIRECTORY
from app.services.repository.types.base import Repository
from app.utils.s3 import create_s3_segment_config, s3_auth


class S3(Repository):

    def __init__(self, name: str, config: dict | None = None):
        super().__init__(name, "s3", config)

    def _auth(self):
        self.s3 = s3_auth(**self.config)

    def download(self, report_name: str) -> None:
        self._auth()
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            response_iterator = paginator.paginate(
                Bucket=self.config["bucket"],
                Prefix=f"{self.config['prefix'].rstrip('/')}/{report_name}",
            )
            path = DIRECTORY.joinpath(self.name, report_name)
            path.mkdir(exist_ok=True, parents=True)

            for page in response_iterator:
                for obj in page.get("Contents", []):
                    self.s3.download_file(
                        self.config["bucket"],
                        obj["Key"],
                        f"{path}/{obj['Key'].split('/')[-1]}",
                    )
        except NoCredentialsError:
            print("No AWS credentials found.")
        except ClientError as e:
            print(e)

    def list_reports(self, *args, **kwargs) -> list[str]:
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
        except NoCredentialsError:
            print("No AWS credentials found.")

    def _create_config(self, *args, **kwargs) -> dict:
        return create_s3_segment_config()