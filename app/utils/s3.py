import rich
import click
import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound

from app.constants import S3_AUTH_TYPES


def create_s3_segment_config() -> dict:
    click.echo("Please provide the following information to configure S3")
    bucket = click.prompt("Enter your bucket name", type=str)
    prefix = click.prompt("Enter your prefix", type=str)

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


def s3_auth(method: S3_AUTH_TYPES, **config) -> boto3.client:
    try:
        if method == "profile":
            session = boto3.Session(profile_name=config.get("profile_name"))
            return session.client("s3")

        return boto3.client(
            "s3",
            aws_access_key_id=config.get("aws_access_key_id"),
            aws_secret_access_key=config.get("aws_secret_access_key"),
        )
    except NoCredentialsError:
        rich.print("[red]No AWS credentials found.[/red]")
        raise click.Abort()
    except ProfileNotFound:
        rich.print(f"[red]Profile {config['profile_name']} not found.[/red]")
        raise click.Abort()
