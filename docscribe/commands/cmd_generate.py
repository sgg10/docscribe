import rich
import click

from docscribe.constants import CONFIG, CONFIG_FILE

from docscribe.services.generator.main import run


@click.command()
@click.option("-n", "--name", "doc_name", help="Name of the document to delete")
@click.option(
    "-r", "--repository", help="Repository to delete the document from", default="local"
)
@click.option("-e", "--exporter", "exporter", help="Exporter to use")
@click.option(
    "--use-default-kwargs",
    is_flag=True,
    default=False,
    help="Use default kwargs for the document",
)
def command(doc_name, repository, use_default_kwargs, exporter):
    """Generate a document"""

    if not CONFIG_FILE.exists():
        raise click.Abort(f"Config file {CONFIG_FILE} does not exist")

    repositories = CONFIG.get("repositories")
    if not repositories:
        repositories = {"local": {}}

    if repository not in repositories:
        raise click.Abort(f"Repository {repository} does not exist in config")

    if not doc_name:
        # Prompt for doc name
        doc_name = click.prompt("Enter the name of the document to delete")
        while not doc_name:
            rich.print("[red]Document name cannot be empty[/red]")
            doc_name = click.prompt("Enter the name of the document to delete")

    if not exporter:
        exporter = click.prompt(
            "Enter the name of the exporter to use",
            type=click.Choice(CONFIG.get("exporters", {}).keys()),
        )
    else:
        if exporter not in CONFIG.get("exporters", {}):
            raise click.Abort(f"Exporter {exporter} does not exist in config")

    run(doc_name, repository, use_default_kwargs, exporter)
