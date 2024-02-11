import rich
import click

from app.constants import CONFIG, CONFIG_SEGMENTS


def validate_config(config_segment: CONFIG_SEGMENTS, abort: bool = True):
    segment = CONFIG.get(config_segment, {})

    if not segment:
        rich.print("[red]No repositories found[/red]")
        if abort:
            raise click.Abort()

    return segment
