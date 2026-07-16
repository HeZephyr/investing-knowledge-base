from pathlib import Path

import yaml


def test_required_github_automation_files_exist_and_parse() -> None:
    paths = [
        Path(".github/workflows/ci.yml"),
        Path(".github/workflows/codeql.yml"),
        Path(".github/workflows/link-check.yml"),
        Path(".github/dependabot.yml"),
    ]

    for path in paths:
        assert path.is_file(), path
        assert yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


def test_workflows_use_least_privilege_and_avoid_pull_request_target() -> None:
    for path in Path(".github/workflows").glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        assert "pull_request_target" not in text
        assert "permissions:" in text
        assert "contents: read" in text
