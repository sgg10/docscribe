import rich
import click

from app.constants import CONFIG, CONFIG_FILE

from app.services.generator.main import run


@click.command()
@click.option("-n", "--name", "doc_name", help="Name of the document package")
@click.option("-r", "--repository", help="Repository to use", default="local")
@click.option("-e", "--exporter", "exporter", help="Exporter to use")
@click.option(
    "--use-default-kwargs",
    is_flag=True,
    default=False,
    help="Use default kwargs for the document",
)
def command(doc_name, repository, use_default_kwargs, exporter):
    """
    Executes the document generation process with the specified parameters.

    This CLI command is responsible for initiating the document generation process.
    It requires the user to specify a document name, repository, and exporter.
    If the document name or exporter is not provided, it will prompt the user for input.
    The repository defaults to 'local' if not specified.

    The command also supports a flag for using default kwargs for the document.
    If the specified repository or exporter does not exist in the configuration,
    or if the configuration file itself does not exist, the command will abort with an appropriate error message.
    """

    if not CONFIG_FILE.exists():
        raise click.Abort(f"Config file {CONFIG_FILE} does not exist")

    repositories = CONFIG.get("repositories")
    if not repositories:
        repositories = {"local": {}}

    if repository not in repositories:
        raise click.Abort(f"Repository {repository} does not exist in config")

    if not doc_name:
        # Prompt for doc name
        doc_name = click.prompt("Enter the name of the document")
        while not doc_name:
            rich.print("[red]Document name cannot be empty[/red]")
            doc_name = click.prompt("Enter the name of the document")

    if not exporter:
        exporter = click.prompt(
            "Enter the name of the exporter to use",
            type=click.Choice(CONFIG.get("exporters", {}).keys()),
        )
    else:
        if exporter not in CONFIG.get("exporters", {}):
            raise click.Abort(f"Exporter {exporter} does not exist in config")

    run(doc_name, repository, use_default_kwargs, exporter)
