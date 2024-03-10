import json
from pathlib import Path

from click.testing import CliRunner

from app.cli import cli
from app.commands import cmd_init
from app.commands.repository import cmd_add, cmd_delete, cmd_list


class TestRepository:
    def setup_method(self):
        self.runner = CliRunner()
        self.runner.invoke(cmd_init.command, args="-p pipenv")
        self.ROOT_PATH = Path(__file__).parent.parent.resolve()

    def read_config(self):
        with open(self.ROOT_PATH / ".docscribe_config.json", "r") as f:
            return json.load(f)

    def test_base_repository(self):
        result = self.runner.invoke(cli, args=["repository"])
        assert "add" in result.output
        assert "delete" in result.output
        assert "list" in result.output
        assert result.exit_code == 0

    def test_add_repository(self):
        result = self.runner.invoke(
            cmd_add.command,
            input="sample\ns3\nsample-bucket\nsample-prefix\nprofile\nsample-profile\n",
        )
        config = self.read_config()
        assert "repositories" in config
        assert "sample" in config["repositories"]
        assert config["repositories"]["sample"]["type"] == "s3"
        assert result.exit_code == 0

    def test_list_repository(self):
        result = self.runner.invoke(cmd_list.command)
        assert "local" in result.output
        assert result.exit_code == 0

    def test_delete_repository(self):
        result = self.runner.invoke(cmd_delete.command, args="sample")
        config = self.read_config()
        assert "sample" not in config["repositories"]
        assert result.exit_code == 0
