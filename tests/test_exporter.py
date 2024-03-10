import json
from pathlib import Path

from click.testing import CliRunner

from app.cli import cli
from app.commands import cmd_init
from app.commands.exporter import cmd_add, cmd_delete

from tests.common import read_config


class TestExporter:
    def setup_method(self):
        self.runner = CliRunner()
        self.runner.invoke(cmd_init.command, args="-p pipenv")
        self.ROOT_PATH = Path(__file__).parent.parent.resolve()

    def test_base_exporter(self):
        result = self.runner.invoke(cli, args=["exporter"])
        assert "add" in result.output
        assert "delete" in result.output
        assert result.exit_code == 0

    def test_add_s3_exporter(self):
        result = self.runner.invoke(
            cmd_add.command,
            input="sample\ns3\nsample-bucket\nsample-prefix\nprofile\nsample-profile\n",
        )
        config = read_config(self.ROOT_PATH)
        assert "exporters" in config
        assert "sample" in config["exporters"]
        assert config["exporters"]["sample"]["type"] == "s3"
        assert result.exit_code == 0

    def test_add_local_exporter(self):
        result = self.runner.invoke(
            cmd_add.command,
            input="samples\nlocal\n",
        )
        config = read_config(self.ROOT_PATH)
        assert "exporters" in config
        assert "local" in config["exporters"]
        assert config["exporters"]["local"]["type"] == "local"
        assert result.exit_code == 0

    def test_delete_exporter(self):
        result = self.runner.invoke(cmd_delete.command, args="sample")
        config = read_config(self.ROOT_PATH)
        assert "sample" not in config["exporters"]
        assert result.exit_code == 0
