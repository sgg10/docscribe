import json
from typing import Iterable

import click

from docscribe.services.exporter.types import local, s3
from docscribe.constants import CONFIG_FILE, DIRECTORY


EXPORTER_TYPES = {
    "local": local.Local,
    "s3": s3.S3,
}


class ExporterManager:
    def __init__(self, name: str | None = None) -> None:
        self.exporter = None
        if name:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)

            exporters = data.get("exporters", {})

            if name in exporters:
                exporter_data = exporters[name]
                self.exporter = EXPORTER_TYPES[exporter_data["type"]](
                    name, exporter_data["config"]
                )

    def export(self, file_name: str, content) -> None:
        if not self.exporter:
            click.echo(f"Exporter {self.exporter} not found.")
            return
        self.exporter.export(file_name, content)

    def make_output_uri(self, file_name: str) -> str:
        if not self.exporter:
            click.echo(f"Exporter {self.exporter} not found.")
            return
        return self.exporter.make_output_uri(file_name)

    def create_exporter(self) -> None:
        if self.exporter:
            click.echo(f"Exporter {self.exporter} already exists.")
            return

        name = click.prompt("Enter the name of the exporter")

        _type = click.prompt(
            "Enter the type of exporter", type=click.Choice(EXPORTER_TYPES.keys())
        )

        self.exporter = EXPORTER_TYPES[_type](name)

    def delete_exporter(self) -> None:
        if not self.exporter:
            click.echo(f"Exporter {self.exporter} not found.")
            return
        self.exporter.delete()
