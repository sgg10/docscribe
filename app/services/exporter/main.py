import rich

from app.services.exporter.manager import ExporterManager


def create_exporter() -> None:
    """
    Creates a new exporter segment by prompting the user for required configuration details.
    """
    manager = ExporterManager(None)
    manager.create_segment()
    rich.print("[bold green]Exporter created.[/bold green]")


def delete_exporter(exporter_name: str) -> None:
    """
    Deletes an existing exporter segment specified by the exporter name.

    Args:
        exporter_name (str): The name of the exporter to be deleted.
    """
    manager = ExporterManager(exporter_name)
    manager.delete_segment()
    rich.print("[bold green]Exporter deleted.[/bold green]")


def export(exporter_name: str | None, file_name, file_type) -> None:
    """
    Exports a file using the specified exporter segment.

    Args:
        exporter_name (str | None): The name of the exporter to use for exporting. If None, prompts the user to select an exporter.
        file_name (str): The name of the file to export.
        file_type (str): The mode/type of the file to be used for exporting.
    """
    manager = ExporterManager(exporter_name)
    manager.export(file_name, mode=file_type)
