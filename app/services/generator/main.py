import json

import rich
import click
from jsonschema import validate, ValidationError

from app.services.exporter.main import export
from app.constants import REPOSITORIES_DIR

from app.services.generator.template_requirements import (
    install_requirements,
    request_document_kwargs,
)
from app.services.generator.template_generation import (
    exec_document_script,
    render_document_template,
)


def read_document_config(
    document_name: str,
    repository_name: str = "local",
) -> dict:
    """
    Reads the document's configuration from its JSON configuration file.

    Parameters:
    - document_name (str): Name of the document.
    - repository_name (str): Name of the repository where the document is located. Defaults to 'local'.

    Returns:
    - dict: The document's configuration.

    Raises:
    - click.Abort: If the configuration file does not exist.
    """
    config_file = REPOSITORIES_DIR.joinpath(
        repository_name, document_name, "config.json"
    )

    if not config_file.exists():
        rich.print(f"[red]Document {document_name} not found![/red]")
        raise click.Abort()

    with open(config_file, "r") as file:
        document_config = json.load(file)

    return document_config


def validate_document_result(body: dict, schema: dict):
    """
    Validates the generated document information against a JSON schema.

    Parameters:
    - body (dict): The document's information to be validated.
    - schema (dict): The JSON schema to validate against.

    Raises:
    - click.Abort: If validation fails.
    """
    try:
        validate(instance=body, schema=schema)
    except ValidationError as e:
        rich.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


def run(
    document_name: str,
    repository_name: str = "local",
    use_default_kwargs: bool = False,
    exporter_name: str = "local",
):
    """
    Main function to generate a document and optionally export it.

    This function performs the full document generation process,
    including reading the document configuration, installing required dependencies,
    generating the document based on the template and script, and exporting the generated document.

    Parameters:
    - document_name (str): Name of the document to generate.
    - repository_name (str): Name of the repository where the document is located. Defaults to 'local'.
    - use_default_kwargs (bool): Whether to use the default keyword arguments for the document. Defaults to False.
    - exporter_name (str): The name of the exporter to use. Defaults to 'local'.

    """

    document_config = read_document_config(document_name, repository_name)
    install_requirements(document_config)

    document_kwargs, have_update = (
        (document_config.get("kwargs", {}), False)
        if use_default_kwargs
        else request_document_kwargs(document_config)
    )

    # Ask the user if they want to save the keyword arguments if have_update is True
    if have_update:
        click.confirm(
            "Do you want to save the keyword arguments for future use?",
            default=True,
        )

        document_config["kwargs"] = document_kwargs

        # Save the keyword arguments
        with open(
            REPOSITORIES_DIR.joinpath(repository_name, document_name, "config.json"),
            "w",
        ) as file:
            json.dump(document_config, file, indent=4)

    result = exec_document_script(document_name, repository_name, document_kwargs)

    validate_document_result(result, document_config.get("template_schema", {}))

    output_path = render_document_template(
        document_name,
        repository_name,
        result,
        document_config["template_type"],
    )

    # Export the document
    export(
        exporter_name,
        output_path,
        "rb" if document_config["template_type"] == "docx" else "r",
    )
