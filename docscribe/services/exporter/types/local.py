from pathlib import Path

import click

from docscribe.constants import DIRECTORY
from docscribe.services.exporter.types.base import Exporter


class Local(Exporter):

    def __init__(self, name: str, config: dict | None = None):
        super().__init__(name, "local", config)

    def make_output_uri(self, file_name) -> str:
        path = Path(DIRECTORY).joinpath("outputs", self.name)
        path.mkdir(exist_ok=True, parents=True)
        return str(path.joinpath(file_name))

    def export(self, file_name: str, content) -> None:
        path = Path(self.make_output_uri(file_name))
        with path.open("w") as f:
            f.write(content)
        click.echo(f"Report saved at {path}")

    def _auth(self):
        pass

    def _create_config(self, *args, **kwargs) -> dict:
        click.echo("Local exporter does not require any configuration.")
        return {}
