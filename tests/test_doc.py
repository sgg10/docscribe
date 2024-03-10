import json
from pathlib import Path

from click.testing import CliRunner

from app.cli import cli
from app.commands import cmd_init
from app.commands.doc import cmd_create, cmd_delete


class TestDoc:
    def setup_method(self):
        self.runner = CliRunner()
        self.runner.invoke(cmd_init.command, args="-p pipenv")
        self.ROOT_PATH = Path(__file__).parent.parent.resolve()
        self.DOCSCRIBE_PATH = self.ROOT_PATH / "docscribe"

    def read_config(self):
        with open(self.ROOT_PATH / ".docscribe_config.json", "r") as f:
            return json.load(f)

    def test_base_doc(self):
        result = self.runner.invoke(cli, args=["doc"])
        assert "create" in result.output
        assert "delete" in result.output
        assert result.exit_code == 0

    def test_create_doc(self):
        result = self.runner.invoke(
            cmd_create.command, args=["-n", "test-doc-pkg", "-t", "md"]
        )
        assert result.exit_code == 0
        path = self.DOCSCRIBE_PATH / "repositories" / "local" / "test-doc-pkg"
        assert path.exists()
        assert (path / "config.json").exists()
        assert (path / "script.py").exists()
        assert (path / "template.md").exists()

    def test_delete_doc(self):
        result = self.runner.invoke(
            cmd_delete.command, args=["-n", "test-doc-pkg"], input="y\n"
        )
        assert result.exit_code == 0
        path = self.DOCSCRIBE_PATH / "repositories" / "local" / "test-doc-pkg"
        assert not path.exists()
