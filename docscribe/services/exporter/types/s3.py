import os
from pathlib import Path

import rich
import click
import boto3
from botocore.exceptions import (
    NoCredentialsError,
    ClientError,
    ProfileNotFound,
)

from docscribe.constants import DIRECTORY
from docscribe.services.exporter.types.base import Exporter


class S3(Exporter):
    def __init__(self, name: str, config: dict | None = None):
        super().__init__(name, "s3", config)

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
            rich.print("[red]No AWS credentials found.[/red]")
            os._exit(1)
        except ProfileNotFound:
            rich.print(f"[red]Profile {self.config['profile_name']} not found.[/red]")
            os._exit(1)

    def make_output_uri(self, file_name: str, full_uri: bool = False) -> str:
        if full_uri:
            return f"s3://{self.config['bucket']}/{self.config['prefix'].rstrip('/')}/{file_name}"
        return f"{self.config['prefix'].rstrip('/')}/{file_name}"

    def export(self, file_name: str, content) -> None:
        self._auth()
        try:
            self.s3.put_object(
                Bucket=self.config["bucket"],
                Key=f"{self.config['prefix'].rstrip('/')}/{file_name}",
                Body=content,
            )
            click.echo(
                f"Report saved at {self.make_output_uri(file_name, full_uri=True)}"
            )
        except NoCredentialsError:
            print("No AWS credentials found.")
        except ClientError as e:
            print(e)

    def _create_config(self, *args, **kwargs) -> dict:
        click.echo("Please provide the following information to configure S3")
        bucket = click.prompt("Enter your bucket name", type=str)
        prefix = click.prompt(
            "Enter your prefix", type=str, default="generated-reports/"
        )

        result = {"bucket": bucket, "prefix": prefix}

        method = click.prompt("Method", type=click.Choice(["profile", "keys"]))
        if method == "profile":
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
