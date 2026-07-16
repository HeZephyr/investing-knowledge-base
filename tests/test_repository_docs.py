from pathlib import Path


def test_required_repository_entrypoints_exist() -> None:
    paths = [
        "README.md",
        "AGENTS.md",
        "wiki/dashboard.md",
        "wiki/index.md",
        "wiki/log.md",
        "raw/README.md",
        "output/README.md",
    ]
    for path in paths:
        assert Path(path).is_file(), path


def test_readme_links_learning_dashboard() -> None:
    assert "wiki/dashboard.md" in Path("README.md").read_text(encoding="utf-8")
