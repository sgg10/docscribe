from pathlib import Path
from typing import Iterable, List, MutableMapping, Sequence, Any

import rich
import click
from click.formatting import HelpFormatter
from click.core import Command, Context, Group


COMMANDS_TYPE = MutableMapping[str, Command] | Sequence[Command]


class CLIGroup(click.Group):
    """
    A custom CLI group class to organize and dynamically load command groups and commands
    from a directory structure.

    Attributes:
        commands_directory (Path): The directory where command groups and commands are stored.

    Methods:
        format_usage: Overrides the default usage formatting to include command and subcommand structure.
        list_commands: Dynamically lists all commands and groups based on the directory structure.
        get_command: Dynamically loads a command or group based on its name.
    """

    def __init__(
        self,
        name: str | None = None,
        commands: COMMANDS_TYPE | None = None,
        **attrs: Any,
    ) -> None:
        """
        Initializes a new instance of the CLIGroup.

        Args:
            name (str, optional): The name of the group. Defaults to None.
            commands (COMMANDS_TYPE, optional): Initial set of commands or groups. Defaults to None.
            **attrs: Additional attributes passed to the click.Group initializer.
        """
        super().__init__(name, commands, **attrs)

        self.commands_directory = Path(__file__).parent.resolve() / "commands"

    def format_usage(self, ctx: Context, formatter: HelpFormatter) -> None:
        """
        Formats the usage string to include command and subcommand structure.

        Args:
            ctx (Context): The Click context object.
            formatter (HelpFormatter): The formatter for writing the usage string.
        """
        formatter.write_usage(
            ctx.command_path, "<command> [<subcommand>] [OPTIONS] [ARGS]"
        )

    def _get_command_list(self, base_path: Path) -> Iterable[str]:
        """
        Retrieves a list of command names from a directory.

        Args:
            base_path (Path): The directory from which to list commands.

        Returns:
            Iterable[str]: An iterable of command names.
        """
        return [
            filename.stem.replace("cmd_", "")
            for filename in base_path.iterdir()
            if filename.is_file() and filename.name.startswith("cmd_")
        ]

    def list_commands(self, ctx: Context) -> List[str]:
        """
        Lists all commands and groups available in the commands directory.

        Args:
            ctx (Context): The Click context object.

        Returns:
            List[str]: A list of all command and group names, sorted alphabetically.
        """
        commands = self._get_command_list(self.commands_directory)
        groups = [
            group.name
            for group in self.commands_directory.iterdir()
            if group.is_dir() and group.name != "__pycache__"
        ]

        return sorted(commands) + sorted(groups)

    def get_command(self, ctx: Context, name: str) -> Command | Group | None:
        """
        Dynamically loads a command or group based on its name.

        Args:
            ctx (Context): The Click context object.
            name (str): The name of the command or group to load.

        Returns:
            Command | Group | None: The loaded command or group, or None if not found.
        """
        base = self.commands_directory / name
        if base.is_dir() and base.exists():
            commands = self._get_command_list(base)
            # Group creation and command loading logic

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
                        f"app.commands.{name}.cmd_{command}",
                        None,
                        None,
                        ["command"],
                    )
                    group.add_command(module.command, name=command)
                except ImportError as e:
                    rich.print(f"[red][ERROR] {e}[/red]")
                    continue
            return group
        else:
            # Single command loading logic
            try:
                module = __import__(f"app.commands.cmd_{name}", None, None, ["command"])
                return module.command
            except ImportError as e:
                rich.print(f"[red][ERROR] {e}[/red]")
                return


@click.group(cls=CLIGroup)
def cli():
    pass
