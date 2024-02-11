import rich

from docscribe.services.exporter.manager import ExporterManager


def create_exporter() -> None:
    manager = ExporterManager(None)
    manager.create_segment()
    rich.print("[bold green]Exporter created.[/bold green]")


def delete_exporter(exporter_name: str) -> None:
    manager = ExporterManager(exporter_name)
    manager.delete_segment()
    rich.print("[bold green]Exporter deleted.[/bold green]")


def export(exporter_name: str | None, file_name, file_type) -> None:
    manager = ExporterManager(exporter_name)
    manager.export(file_name, mode=file_type)
