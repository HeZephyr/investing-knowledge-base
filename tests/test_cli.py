from pathlib import Path

from typer.testing import CliRunner

import pytest

from investkb.cli import _provider, app


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
