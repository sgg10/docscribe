import rich
import click
import boto3
from botocore.exceptions import NoCredentialsError, ProfileNotFound

from app.constants import S3_AUTH_TYPES


def create_s3_segment_config() -> dict:
    """
    Interactively collects information from the user to configure an S3 segment.

    Returns:
        dict: A dictionary containing the configured S3 segment information, including bucket name, prefix, and either profile name or keys.
    """
    rich.print("[bold]Please provide the following information to configure S3[/bold]")
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
    """
    Authenticates to AWS S3 using the specified method and configuration.

    Args:
        method (S3_AUTH_TYPES): The authentication method, either 'profile' or 'keys'.
        **config: Additional keyword arguments containing the authentication details.

    Returns:
        boto3.client: A boto3 client object authenticated to S3.

    Raises:
        click.Abort: If no credentials are found or the specified profile is not found.
    """
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
