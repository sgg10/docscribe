import json
from typing import Iterable

import click

from docscribe.services.repository.types.s3 import S3
from docscribe.constants import CONFIG_FILE, DIRECTORY


REPOSITORY_TYPES = {
    "s3": S3,
}


class RepositoryManager:
    def __init__(self, name: str | None = None) -> None:
        self.repository = None
        if name:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)

            repositories = data.get("repositories", {})

            if name in repositories:
                repo_data = repositories[name]
                self.repository = REPOSITORY_TYPES[repo_data["type"]](
                    name, repo_data["config"]
                )

    def download(self, report_name: str) -> None:
        # self.repository.download(report_name)
        if not self.repository:
            click.echo(f"Repository {self.repository} not found.")
            return
        self.repository.download(report_name)

    def list_reports(self, *args, **kwargs) -> Iterable[str]:
        # return self.repository.list_reports(*args, **kwargs)
        if not self.repository:
            click.echo(f"Repository {self.repository} not found.")
            return
        return self.repository.list_reports(*args, **kwargs)

    def create_repository(self) -> None:
        # return REPOSITORY_TYPES[_type](name, config)
        if self.repository:
            click.echo(f"Repository {self.repository} already exists.")
            return

        name = click.prompt("Enter the name of the repository")

        _type = click.prompt(
            "Enter the type of repository", type=click.Choice(REPOSITORY_TYPES.keys())
        )

        self.repository = REPOSITORY_TYPES[_type](name)
