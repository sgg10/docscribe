import json

import rich
import click

from app.constants import DIRECTORY, TEMPLATES_TYPES


def run(
    doc_name: str,
    repository: str = "local",
    doc_type: str = TEMPLATES_TYPES.default(),
):
    """Create a doc from the given repository."""
    repo_path = DIRECTORY / repository
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