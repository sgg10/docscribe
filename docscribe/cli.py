import os
from pathlib import Path
from typing import Iterable, List, MutableMapping, Sequence, Any

import click
from click.formatting import HelpFormatter
from click.core import Command, Context, Group


COMMANDS_TYPE = MutableMapping[str, Command] | Sequence[Command]


class CLIGroup(click.Group):

    def __init__(
        self,
        name: str | None = None,
        commands: COMMANDS_TYPE | None = None,
        **attrs: Any,
    ) -> None:
        super().__init__(name, commands, **attrs)

        self.commands_directory = Path(__file__).parent.resolve() / "commands"

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        formatter.write_usage(
            ctx.command_path, "<command> [<subcommand>] [OPTIONS] [ARGS]"
        )
        # if ctx.info_name == "docscribe":
        #     formatter.write_usage(ctx.command_path, "")
        # else:
        #     super().format_usage(ctx, formatter)

    def _get_command_list(self, base_path: Path) -> Iterable[str]:
        return [
            filename.stem.replace("cmd_", "")
            for filename in base_path.rglob("cmd_*.py")
            if filename.is_file()
        ]

    def list_commands(self, ctx: Context) -> List[str]:
        commands = self._get_command_list(self.commands_directory)
        groups = [
            group.name
            for group in self.commands_directory.iterdir()
            if group.is_dir() and group.name != "__pycache__"
        ]

        return sorted(commands) + sorted(groups)

    def get_command(self, ctx: Context, name: str) -> Command | Group | None:
        base = self.commands_directory / name
        if base.is_dir() and base.exists():
            commands = self._get_command_list(base)

            @click.group(
                name=name,
                help=f"Commands Group for {name.capitalize()} resource",
            )
            def group():
                f"""{name.capitalize()} resource commands"""
                pass

            for command in commands:
                try:
                    module = __import__(
                        f"docscribe.commands.{name}.cmd_{command}",
                        None,
                        None,
                        ["command"],
                    )
                    group.add_command(module.command, name=command)
                except ImportError as e:
                    print(e)
                    continue
            return group
        else:
            try:
                module = __import__(
                    f"docscribe.commands.cmd_{name}", None, None, ["command"]
                )
                return module.command
            except ImportError as e:
                print(e)
                return


@click.group(cls=CLIGroup)
def cli():
    pass
