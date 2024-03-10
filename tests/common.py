import json


def read_config(root_path):
    with open(root_path / ".docscribe_config.json", "r") as f:
        return json.load(f)


def common_create_doc(runner, command, base_path):
    result = runner.invoke(command, args=["-n", "test-doc-pkg", "-t", "md"])
    assert result.exit_code == 0
    path = base_path / "repositories" / "local" / "test-doc-pkg"
    assert path.exists()
    assert (path / "config.json").exists()
    assert (path / "script.py").exists()
    assert (path / "template.md").exists()
    return path


def common_delete_doc(runner, command, base_path):
    result = runner.invoke(command, args=["-n", "test-doc-pkg"], input="y\n")
    assert result.exit_code == 0
    path = base_path / "repositories" / "local" / "test-doc-pkg"
    assert not path.exists()

    return path
