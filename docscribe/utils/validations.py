from typing import Literal

import rich
import click

from docscribe.constants import CONFIG


def validate_config(
    config_segment: Literal["repositories", "exporters"], abort: bool = True
):
    segment = CONFIG.get(config_segment, {})

    if not segment:
        rich.print("[red]No repositories found[/red]")
        if abort:
            raise click.Abort()

    return segment
