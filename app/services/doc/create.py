import json

import rich
import click

from app.constants import REPOSITORIES_DIR, TEMPLATES_TYPES


def run(
    doc_name: str,
    repository: str = "local",
    doc_type: str = TEMPLATES_TYPES.default(),
):
    """
    Creates a new document template set within the specified repository.

    This function sets up the necessary files for a new document template, including a template file
    (in the specified format), a Python script for data fetching or processing, and a JSON configuration
    file. It checks if the document already exists to prevent overwriting and ensures the document type
    is supported.

    Args:
        doc_name (str): The name of the document/template to create.
        repository (str, optional): The name of the repository where the document will be created. Defaults to "local".
        doc_type (str, optional): The type of document to create. Supported types are defined in TEMPLATES_TYPES. Defaults to the default value defined in TEMPLATES_TYPES.

    Raises:
        click.Abort: If the document type is invalid or if the document already exists in the repository.

    This command is interactive and will prompt the user for necessary details if not provided as arguments.
    """
    repo_path = REPOSITORIES_DIR / repository
    repo_path.mkdir(parents=True, exist_ok=True)

    try:
        doc_type = TEMPLATES_TYPES.validate(doc_type)
    except ValueError as e:
        raise click.Abort(str(e))

    doc_path = repo_path / doc_name
    if doc_path.exists():
        rich.print(f"[red]Document {doc_name} already exists in {repository}[/red]")
        raise click.Abort()

    rich.print(
        f"[blue]Creating {doc_name} document for {repository} of type {doc_type}[/blue]"
    )

    doc_path.mkdir(parents=True)

    for file in [f"template.{doc_type}", "script.py"]:
        file_path = doc_path / file
        file_path.touch()

    with open(doc_path / "config.json", "w") as f:
        data = {
            "default_export_name": doc_name,
            "kwargs": {},
            "template_schema": {},
            "required_modules": [],
            "template_type": doc_type,
        }
        json.dump(data, f, indent=4)

    rich.print(f"[green]Document {doc_name} created successfully[/green]")
