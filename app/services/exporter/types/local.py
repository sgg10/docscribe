from pathlib import Path

import rich
import click

from app.constants import LOCAL_EXPORTS_DIR
from app.services.exporter.types.base import Exporter


class Local(Exporter):

    def __init__(self, name: str, config: dict | None = None):
        super().__init__(name, "local", config)

    def make_output_uri(self, file_name) -> str:
        path = LOCAL_EXPORTS_DIR / self.name
        path.mkdir(exist_ok=True, parents=True)
        return str(path.joinpath(file_name))

    def export(self, file_name: str, *args, **kwargs) -> None:
        # Move the file to the outputs directory
        mode = kwargs.get("mode", "rb")

        file = Path(file_name)

        with file.open(mode) as f:
            content = f.read()

        output_uri = self.make_output_uri(file_name.name)
        output_uri = Path(output_uri)
        output_uri.parent.mkdir(exist_ok=True, parents=True)
        with output_uri.open("w" if mode == "r" else "wb") as f:
            f.write(content)

        file.unlink()
        rich.print(f"[green]Report saved at {output_uri}[/green]")

    def _auth(self):
        pass

    def _create_config(self, *args, **kwargs) -> dict:
        rich.print(
            "[blue][INFO]Local exporter does not require any configuration.[/blue]"
        )
        return {}
