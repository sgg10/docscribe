import rich
import click

from app.constants import CONFIG, CONFIG_SEGMENTS


def validate_config(config_segment: CONFIG_SEGMENTS, abort: bool = True):
    """
    Validates the presence of a specific configuration segment within the application's
    configuration. If the specified segment is not found and abort is True, the function
    will print an error message and abort the CLI command execution.

    Args:
        config_segment (CONFIG_SEGMENTS): The configuration segment to validate. This
            should be one of the predefined segments in CONFIG_SEGMENTS.
        abort (bool, optional): Determines whether to abort the CLI command execution if
            the configuration segment is not found. Defaults to True.

    Returns:
        dict: The configuration segment if found; otherwise, an empty dictionary.

    Raises:
        click.Abort: If the configuration segment is not found and abort is set to True.
    """
    segment = CONFIG.get(config_segment, {})

    if not segment:
        rich.print("[red]No repositories found[/red]")
        if abort:
            raise click.Abort()

    return segment
