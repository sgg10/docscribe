import rich
import click

from app.utils.validations import validate_config
from app.constants import CONFIG_SEGMENTS
from app.services.exporter import EXPORTER_TYPES
from app.services.repository import REPOSITORY_TYPES


SEGMENTS = {
    "exporters": EXPORTER_TYPES,
    "repositories": REPOSITORY_TYPES,
}


def set_segment_config_by_name(name: str, segment_name: CONFIG_SEGMENTS):
    if not name:
        return None

    segment = validate_config(segment_name, abort=False)

    if name in segment:
        segment_data = segment[name]
        return SEGMENTS[segment_name][segment_data["type"]](
            name, segment_data["config"]
        )

    return None


class SegmentManager:

    def __init__(self, name: str | None, segment_name: CONFIG_SEGMENTS) -> None:
        self.name = name
        self.segment_name = segment_name
        self.segment = set_segment_config_by_name(name, segment_name)

    def _validate_segment(self) -> None:
        if not self.segment:
            rich.print(
                f"[bold red]{self.segment_name.capitalize()} not found.[/bold red]"
            )
            click.Abort()

    def create_segment(self) -> None:
        if self.segment:
            click.echo(
                f"{self.segment_name.rstrip('s').capitalize()} '{self.name}' already exists."
            )
            return

        name = click.prompt(f"Enter the name of the {self.segment_name.rstrip('s')}")

        _type = click.prompt(
            f"Enter the type of {self.segment}",
            type=click.Choice(SEGMENTS[self.segment_name].keys()),
        )

        self.segment = SEGMENTS[self.segment_name][_type](name)

    def delete_segment(self) -> None:
        if not self.segment:
            click.echo(
                f"{self.segment_name.rstrip('s').capitalize()} {self.name} not found."
            )
            return

        self.segment.delete()
