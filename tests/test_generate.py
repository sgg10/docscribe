import json
from pathlib import Path

from click.testing import CliRunner

from app.cli import cli
from app.commands import cmd_init
from app.commands import cmd_generate
from app.commands.doc import cmd_create, cmd_delete


class TestGenerate:
    def setup_method(self):
        self.runner = CliRunner()
        self.runner.invoke(cmd_init.command, args="-p pipenv")
        self.ROOT_PATH = Path(__file__).parent.parent.resolve()
        self.DOCSCRIBE_PATH = self.ROOT_PATH / "docscribe"

        self.create_doc()

    def read_config(self):
        with open(self.ROOT_PATH / ".docscribe_config.json", "r") as f:
            return json.load(f)

    def create_doc(self):
        result = self.runner.invoke(
            cmd_create.command, args=["-n", "test-doc-pkg", "-t", "md"]
        )
        assert result.exit_code == 0
        path = self.DOCSCRIBE_PATH / "repositories" / "local" / "test-doc-pkg"
        assert path.exists()
        assert (path / "config.json").exists()
        assert (path / "script.py").exists()
        assert (path / "template.md").exists()

        with open(path / "template.md", "w") as f:
            template = "#{{title}}\n\n{{description}}"
            f.write(template)

        with open(path / "config.json", "r") as f:
            data = json.load(f)

        config = {
            **data,
            "template_schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
        }

        with open(path / "config.json", "w") as f:
            json.dump(config, f, indent=4)

        # Read script.py and put custom string
        with open(path / "script.py", "w") as f:
            script = "def run(*args, **kwargs):\n\tdata = {'title': 'Hello, World!', 'description': 'This is a test'}\n\treturn data"
            f.write(script)

    def test_generate(self):
        result = self.runner.invoke(
            cmd_generate.command, args=["-n", "test-doc-pkg", "-e", "local"]
        )
        assert result.exit_code == 0
        assert "Document test-doc-pkg generated successfully!" in result.output
        assert (
            "Report saved at docscribe/outputs/local/test-doc-pkg.md" in result.output
        )
        output = self.DOCSCRIBE_PATH / "outputs" / "local" / "test-doc-pkg.md"
        assert output.exists()
        assert output.read_text() == "#Hello, World!\n\nThis is a test"

    def test_base_generate(self):
        result = self.runner.invoke(cli, args=["generate", "--help"])
        assert result.exit_code == 0

    def teardown_method(self):
        result = self.runner.invoke(
            cmd_delete.command, args=["-n", "test-doc-pkg"], input="y\n"
        )
        assert result.exit_code == 0
        path = self.DOCSCRIBE_PATH / "repositories" / "local" / "test-doc-pkg"
        assert not path.exists()
