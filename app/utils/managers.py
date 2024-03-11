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
    """
    Retrieves a specific segment configuration by name and initializes it.

    This function looks up the configuration for a given name within a specified
    configuration segment (exporters or repositories). If found, it initializes
    the segment with the stored configuration.

    Args:
        name (str): The name of the segment to retrieve.
        segment_name (CONFIG_SEGMENTS): The type of segment to look up, e.g., 'exporters' or 'repositories'.

    Returns:
        An instance of the specified segment with its configuration, or None if not found.
    """
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
    """
    Manages the creation, validation, and deletion of configurable segments (exporters or repositories).

    This class provides an interface for managing segments within the application, allowing
    for the dynamic creation, validation, and deletion based on user input and existing configuration.
    """

    def __init__(self, name: str | None, segment_name: CONFIG_SEGMENTS) -> None:
        """
        Initializes the SegmentManager with a specific name and segment type.

        Args:
            name (str | None): The name of the segment to manage.
            segment_name (CONFIG_SEGMENTS): The type of segment to manage, e.g., 'exporters' or 'repositories'.
        """
        self.name = name
        self.segment_name = segment_name
        self.segment = set_segment_config_by_name(name, segment_name)

    def _validate_segment(self) -> None:
        """
        Validates the existence of the current segment.

        If the segment does not exist, prints an error message and aborts the operation.
        """
        if not self.segment:
            rich.print(
                f"[bold red]{self.segment_name.capitalize()} not found.[/bold red]"
            )
            click.Abort()

    def create_segment(self) -> None:
        """
        Creates a new segment based on user input.

        If the segment already exists, it prints a warning message and does not proceed
        with creation. Otherwise, it prompts the user for necessary information to create
        and configure a new segment.
        """
        if self.segment:
            rich.print(
                f"[bold yellow]{self.segment_name.capitalize()} '{self.name}' already exists.[/bold yellow]"
            )
            return

        name = click.prompt(f"Enter the name of the {self.segment_name.rstrip('s')}")

        _type = click.prompt(
            f"Enter the type of {self.segment}",
            type=click.Choice(SEGMENTS[self.segment_name].keys()),
        )

        self.segment = SEGMENTS[self.segment_name][_type](name)

    def delete_segment(self) -> None:
        """
        Deletes the current segment.

        If the segment does not exist, it prints an error message. Otherwise, it proceeds
        to delete the segment and its configuration.
        """
        if not self.segment:
            rich.print(
                f"[bold red]{self.segment_name.capitalize()} '{self.name}' not found.[/bold red]"
            )
            return

        self.segment.delete()
