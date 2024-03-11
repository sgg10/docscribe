from pathlib import Path

from click.testing import CliRunner

from app.cli import cli
from app.commands import cmd_init
from app.commands.doc import cmd_create, cmd_delete

from tests.common import common_create_doc, common_delete_doc


class TestDoc:
    def setup_method(self):
        self.runner = CliRunner()
        self.runner.invoke(cmd_init.command, args="-p pipenv")
        self.ROOT_PATH = Path(__file__).parent.parent.resolve()
        self.DOCSCRIBE_PATH = self.ROOT_PATH / "docscribe"

    def test_base_doc(self):
        result = self.runner.invoke(cli, args=["doc"])
        assert "create" in result.output
        assert "delete" in result.output
        assert result.exit_code == 0

    def test_create_doc(self):
        common_create_doc(self.runner, cmd_create.command, self.DOCSCRIBE_PATH)

    def test_delete_doc(self):
        common_delete_doc(self.runner, cmd_delete.command, self.DOCSCRIBE_PATH)
