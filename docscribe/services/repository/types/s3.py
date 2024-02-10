import os
from pathlib import Path

import click
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

from docscribe.constants import DIRECTORY
from docscribe.services.repository.types.base import Repository


class S3(Repository):

    def __init__(self, name: str, config: dict | None = None):
        super().__init__(name, "s3", config)
        self._auth()

    def _auth(self):
        try:
            if self.config["method"] == "profile":
                session = boto3.Session(profile_name=self.config["profile_name"])
                self.s3 = session.client("s3")
                return

            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=self.config["aws_access_key_id"],
                aws_secret_access_key=self.config["aws_secret_access_key"],
            )
        except NoCredentialsError:
            print("No AWS credentials found.")
            os._exit(1)

    def download(self, report_name: str) -> None:
        try:
            paginator = self.s3.get_paginator("list_objects_v2")
            response_iterator = paginator.paginate(
                Bucket=self.config["bucket"],
                Prefix=f"{self.config['prefix'].rstrip('/')}/{report_name}",
            )
            path = Path(DIRECTORY).joinpath(self.name, report_name)
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
        click.echo("Please provide the following information to configure S3")
        bucket = click.prompt("Enter your bucket name", type=str)
        prefix = click.prompt("Enter your prefix", type=str, default="")

        result = {"bucket": bucket, "prefix": prefix}

        # Ask the user to choose between using profile or access key and secret key
        profile = click.confirm(
            "Do you want to use a profile? (If not, you will be asked for access key and secret key)"
        )
        if profile:
            profile_name = click.prompt("Enter your profile name", type=str)
            return {**result, "profile_name": profile_name, "method": "profile"}
        else:
            aws_access_key_id = click.prompt("Enter your AWS access key", type=str)
            aws_secret_access_key = click.prompt("Enter your AWS secret key", type=str)
            return {
                **result,
                "aws_access_key_id": aws_access_key_id,
                "aws_secret_access_key": aws_secret_access_key,
                "method": "keys",
            }
