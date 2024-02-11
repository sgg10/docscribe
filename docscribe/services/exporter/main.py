import rich

from docscribe.services.exporter.manager import (
    ExporterManager,
    EXPORTER_TYPES,
)


def create_exporter() -> None:
    manager = ExporterManager(None)
    manager.create_exporter()
    rich.print("[bold green]Exporter created.[/bold green]")


def delete_exporter(exporter_name: str) -> None:
    manager = ExporterManager(exporter_name)
    manager.delete_exporter()
    rich.print("[bold green]Exporter deleted.[/bold green]")


def export(exporter_name: str | None, file_name: str, content) -> None:
    manager = ExporterManager(exporter_name)
    manager.export(file_name, content)
    rich.print(f"{file_name} exported.")