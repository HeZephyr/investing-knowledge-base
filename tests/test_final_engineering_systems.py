from pathlib import Path

from investkb.coverage import coverage_score, load_coverage


ROOT = Path(__file__).parents[1]


def test_final_engineering_requirements_are_validated_at_one_hundred_percent() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}

    assert requirements["engineering-global-data"].status == "validated"
    assert requirements["engineering-private-research"].status == "validated"
    assert coverage_score(manifest) == 100.0


def test_public_repository_documents_optional_provider_and_ignored_private_layer() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")

    assert "yfinance" in pyproject
    assert "private/" in gitignore
    assert (ROOT / "wiki/engineering/全球免费数据适配.md").is_file()
    assert (ROOT / "wiki/engineering/私人研究工作区.md").is_file()
