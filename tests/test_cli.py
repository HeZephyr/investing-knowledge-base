from pathlib import Path

from typer.testing import CliRunner

import pytest

from investkb.cli import _provider, app


ROOT = Path(__file__).parents[1]


def test_cli_help_and_offline_demo(tmp_path: Path, monkeypatch) -> None:
    runner = CliRunner()
    monkeypatch.chdir(tmp_path)

    assert runner.invoke(app, ["--help"]).exit_code == 0
    assert runner.invoke(app, ["fund", "--help"]).exit_code == 0
    result = runner.invoke(app, ["demo", "backtest", "--offline"])

    assert result.exit_code == 0, result.output
    assert Path("output/reports/demo/report.md").exists()


def test_sources_and_wiki_commands_pass_from_repository() -> None:
    runner = CliRunner()

    assert runner.invoke(app, ["sources", "audit", "raw"]).exit_code == 0
    assert runner.invoke(app, ["wiki", "lint"]).exit_code == 0


def test_provider_factory_rejects_unknown_name() -> None:
    with pytest.raises(ValueError, match="unknown provider"):
        _provider("mystery")


def test_coverage_cli_validates_and_reproduces_committed_report(tmp_path: Path) -> None:
    runner = CliRunner()

    validation = runner.invoke(app, ["coverage", "validate"])
    generated = tmp_path / "knowledge-coverage.md"
    report = runner.invoke(app, ["coverage", "report", "--output", str(generated)])

    assert validation.exit_code == 0, validation.output
    assert "PASS:" in validation.output
    assert report.exit_code == 0, report.output
    assert generated.read_bytes() == (ROOT / "output/reports/knowledge-coverage.md").read_bytes()
