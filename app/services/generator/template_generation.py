import sys
import importlib.util

import rich
import click
from docxtpl import DocxTemplate
from jinja2 import Environment, FileSystemLoader

from app.constants import REPOSITORIES_DIR, TEMPLATES_TYPES, TMP_DIR


def exec_document_script(
    document_name: str, repository_name: str = "local", document_kwargs: dict = {}
):
    """Executes the document script."""
    script_file = REPOSITORIES_DIR.joinpath(repository_name, document_name, "script.py")

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


def render_document_template(
    document_name: str,
    repository_name: str = "local",
    document_info: dict = {},
    document_type: str = TEMPLATES_TYPES.default(),
):
    """Renders the document template."""

    template_file = REPOSITORIES_DIR.joinpath(
        repository_name, document_name, f"template.{document_type}"
    )

    if not template_file.exists():
        rich.print(f"[red]Document template {template_file} not found![/red]")
        raise click.Abort()

    output = TMP_DIR.joinpath(f"{document_name}.{document_type}")
    output.parent.mkdir(exist_ok=True, parents=True)

    if document_type == TEMPLATES_TYPES.DOCX.value:
        doc = DocxTemplate(template_file)
        doc.render(document_info)
        doc.save(f"{output}")
    else:
        env = Environment(loader=FileSystemLoader(template_file.parent))
        template = env.get_template(template_file.name)

        # Render the template
        rendered_template = template.render(document_info)

        with output.open("w") as file:
            file.write(rendered_template)

    rich.print(f"[green]Document {document_name} generated successfully![/green]")

    return output
