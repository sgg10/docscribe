import click

from app.services.repository.main import download as run


@click.command()
@click.argument("repository", required=True)
@click.argument("report_name", required=True)
def command(repository, report_name):
    """
    Initiates the download of a specified report from a given repository.

    This command facilitates the downloading of reports from configured repositories by specifying the repository and report name. It leverages the `download` function from `app.services.repository.main`, allowing users to directly interact with repositories through the command line.

    Args:
        repository (str): The name of the repository from which the report will be downloaded. This argument is mandatory.
        report_name (str): The name of the report to download. This argument is mandatory.

    """
    run(repository, report_name)
