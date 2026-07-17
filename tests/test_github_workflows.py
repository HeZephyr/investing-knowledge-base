from pathlib import Path

import yaml


def test_required_github_automation_files_exist_and_parse() -> None:
    paths = [
        Path(".github/workflows/ci.yml"),
        Path(".github/workflows/codeql.yml"),
        Path(".github/workflows/link-check.yml"),
        Path(".github/workflows/provider-smoke.yml"),
        Path(".github/workflows/pages.yml"),
        Path(".github/workflows/pr-policy.yml"),
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


def test_ci_and_provider_checks_have_deliberate_schedules() -> None:
    ci = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")
    provider = Path(".github/workflows/provider-smoke.yml").read_text(encoding="utf-8")

    assert 'cron: "20 22 * * 0"' in ci
    assert 'cron: "10 23 * * 1,4"' in provider


def test_test_helpers_are_explicit_python_packages() -> None:
    assert Path("tests/__init__.py").is_file()
    assert Path("tests/data/__init__.py").is_file()


def test_ci_builds_the_static_site_strictly() -> None:
    workflow = Path(".github/workflows/ci.yml").read_text(encoding="utf-8")

    assert "python -m investkb.site" in workflow
    assert "mkdocs build --strict" in workflow
    assert "investkb.publication" in workflow
    assert "investkb.cli coverage validate" in workflow


def test_pr_policy_enforces_conventional_titles_and_body() -> None:
    workflow = Path(".github/workflows/pr-policy.yml").read_text(encoding="utf-8")

    assert "pull_request:" in workflow
    assert "PR_TITLE" in workflow
    assert "PR_BODY" in workflow
