from click.testing import CliRunner

from docscribe.main import cli


def test_cli_base_execution():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert "Usage: " in result.output
