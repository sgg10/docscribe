import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from packaging import version

import rich
import click
from docxtpl import DocxTemplate
from jsonschema import validate, ValidationError
from jinja2 import Environment, FileSystemLoader

from docscribe.constants import CONFIG_FILE, DIRECTORY, TEMPLATES_TYPES


def read_document_config(
    document_name: str,
    repository_name: str = "local",
) -> dict:
    """Reads the document configuration from the configuration file."""
    config_file = Path(DIRECTORY).joinpath(
        repository_name, document_name, "config.json"
    )

    if not config_file.exists():
        rich.print(f"[red]Document {document_name} not found![/red]")
        raise click.Abort()

    with open(config_file, "r") as file:
        document_config = json.load(file)

    return document_config


def check_module(module: str) -> bool:
    """Checks if the module and optionally a specific version are installed."""
    module_parts = module.split("==")
    module_name = module_parts[0].lower()
    version_required = module_parts[1] if len(module_parts) > 1 else None

    try:
        mod = importlib.import_module(module_name)
        if version_required:
            current_version = getattr(mod, "__version__", None)
            if not current_version or version.parse(current_version) < version.parse(
                version_required
            ):
                return False

            if version.parse(current_version) > version.parse(version_required):
                if click.confirm(
                    f"Module {module_name} version {current_version} is installed. Do you want to install version {version_required}?"
                ):
                    return False

    except ImportError:
        return False

    return True


def install_requirements(config: dict):
    """Installs the requirements for the document."""
    requirements = config.get("require_modules", [])
    if not requirements:
        return

    # Validate if the required modules are installed
    uninstalled_modules = [
        module for module in requirements if not check_module(module)
    ]

    uninstalled_modules = " ".join(uninstalled_modules)

    if not uninstalled_modules:
        return

    # Ask the user if they want to install the required modules
    click.confirm(
        f"Do you want to install the required modules? ({uninstalled_modules.replace(' ', ', ')})",
        default=True,
        abort=True,
    )

    # TODO: Add support for multiple package managers
    result = os.system(f"pipenv install {uninstalled_modules}")

    if result != 0:
        rich.print("[red]Failed to install the required modules![/red]")
        raise click.Abort()


def request_document_kwargs(config: dict) -> dict:
    """Requests the document specific keyword arguments from the user."""
    # Get the document specific keyword arguments

    have_update = False

    document_kwargs = {}
    for key, value in config.get("kwargs", {}).items():
        document_kwargs[key] = click.prompt(
            f"Please enter the value for {key}:", default=value
        )
        if document_kwargs[key] != value:
            have_update = True

    return document_kwargs, have_update


def exec_document_script(
    document_name: str, repository_name: str = "local", document_kwargs: dict = {}
):
    """Executes the document script."""
    script_file = Path(DIRECTORY).joinpath(repository_name, document_name, "script.py")

    if not script_file.exists():
        rich.print(f"[red]Document script {script_file} not found![/red]")
        raise click.Abort()

    spec = importlib.util.spec_from_file_location("module.name", script_file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    # Execute the document script
    if hasattr(module, "run"):
        try:
            result = module.run(**document_kwargs)
            return result
        except Exception as e:
            rich.print(f"[red]Error: {e}[/red]")
            raise click.Abort()

    rich.print("[red]run function not found in the document script![/red]")
    raise click.Abort()


def validate_document_result(body: dict, schema: dict):
    """Validates the document info body."""
    try:
        validate(instance=body, schema=schema)
    except ValidationError as e:
        rich.print(f"[red]Error: {e}[/red]")
        raise click.Abort()


def render_document_template(
    document_name: str,
    repository_name: str = "local",
    document_info: dict = {},
    document_type: str = TEMPLATES_TYPES.default(),
):
    """Renders the document template."""

    template_file = Path(DIRECTORY).joinpath(
        repository_name, document_name, f"template.{document_type}"
    )

    if not template_file.exists():
        rich.print(f"[red]Document template {template_file} not found![/red]")
        raise click.Abort()

    if document_type == TEMPLATES_TYPES.DOCX.value:
        doc = DocxTemplate(template_file)
        doc.render(document_info)
        doc.save(f"{document_name}.docx")
    else:
        env = Environment(loader=FileSystemLoader(template_file.parent))
        template = env.get_template(template_file.name)

        # Render the template
        rendered_template = template.render(document_info)

        with open(f"{document_name}.md", "w") as file:
            file.write(rendered_template)

    print(f"Document {document_name} generated successfully!")


def run(
    document_name: str, repository_name: str = "local", use_default_kwargs: bool = False
):
    """Main function to run the generator."""

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
            Path(DIRECTORY).joinpath(repository_name, document_name, "config.json"), "w"
        ) as file:
            json.dump(document_config, file, indent=4)

    result = exec_document_script(document_name, repository_name, document_kwargs)

    validate_document_result(result, document_config.get("template_schema", {}))

    render_document_template(
        document_name,
        repository_name,
        result,
        document_config["template_type"],
    )
