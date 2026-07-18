"""investkb 统一命令行入口。"""

from __future__ import annotations

from datetime import date, datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import typer
import yaml

from investkb.backtest.engine import run_backtest
from investkb.backtest.models import FeeModel, MarketRules
from investkb.coverage import (
    CoverageFormatError,
    coverage_score,
    load_coverage,
    render_coverage_report,
    validate_coverage,
)
from investkb.data.models import normalize_bars
from investkb.data.providers import AKShareProvider, BaoStockProvider, DataUnavailableError
from investkb.data.store import ParquetStore
from investkb.private_research import (
    PrivateWorkspaceError,
    initialize_private_workspace,
    validate_private_workspace,
)
from investkb.reporting import build_report
from investkb.sources import SourceFormatError, audit_source_card
from investkb.strategies import buy_and_hold_signal, moving_average_signal
from investkb.validation.market import validate_bars
from investkb.wiki import lint_wiki

app = typer.Typer(help="A 股与港股知识库、数据和量化研究工具", no_args_is_help=True)
sources_app = typer.Typer(help="Raw 来源管理", no_args_is_help=True)
wiki_app = typer.Typer(help="Wiki 健康检查", no_args_is_help=True)
data_app = typer.Typer(help="免费日线数据", no_args_is_help=True)
fund_app = typer.Typer(help="开放式基金净值数据", no_args_is_help=True)
backtest_app = typer.Typer(help="策略回测", no_args_is_help=True)
demo_app = typer.Typer(help="可离线运行的教程示例", no_args_is_help=True)
coverage_app = typer.Typer(help="知识覆盖与完成证据", no_args_is_help=True)
private_app = typer.Typer(help="本地私密研究工作区", no_args_is_help=True)
app.add_typer(sources_app, name="sources")
app.add_typer(wiki_app, name="wiki")
app.add_typer(data_app, name="data")
app.add_typer(fund_app, name="fund")
app.add_typer(backtest_app, name="backtest")
app.add_typer(demo_app, name="demo")
app.add_typer(coverage_app, name="coverage")
app.add_typer(private_app, name="private")

NON_CARDS = {"README.md", "catalog.md", "source-catalog.md"}


def _provider(name: str) -> AKShareProvider | BaoStockProvider:
    if name == "akshare":
        return AKShareProvider()
    if name == "baostock":
        return BaoStockProvider()
    raise ValueError(f"unknown provider: {name}")


@sources_app.command("audit")
def sources_audit(path: Path = typer.Argument(Path("raw"))) -> None:
    """审计 Raw 来源卡必填字段。"""
    cards = [item for item in path.glob("**/*.md") if item.name not in NON_CARDS]
    errors: list[str] = []
    for card in cards:
        try:
            errors.extend(f"{card}: {field}" for field in audit_source_card(card))
        except SourceFormatError as exc:
            errors.append(f"{card}: {exc}")
    if errors:
        for error in errors:
            typer.echo(error, err=True)
        raise typer.Exit(1)
    typer.echo(f"PASS: {len(cards)} source cards")


@wiki_app.command("lint")
def wiki_lint(wiki_path: Path = Path("wiki"), raw_path: Path = Path("raw")) -> None:
    """检查双链、来源 ID 与孤儿页。"""
    report = lint_wiki(wiki_path, raw_path)
    failures = report.broken_links + report.missing_sources + report.orphans
    if failures:
        for failure in failures:
            typer.echo(failure, err=True)
        raise typer.Exit(1)
    typer.echo("PASS: wiki links, sources, and reachability")


def _coverage_or_exit(config: Path, root: Path):
    try:
        manifest = load_coverage(config)
    except CoverageFormatError as exc:
        typer.echo(f"ERROR: {exc}", err=True)
        raise typer.Exit(1) from exc
    errors = validate_coverage(manifest, root)
    if errors:
        for error in errors:
            typer.echo(f"ERROR: {error}", err=True)
        raise typer.Exit(1)
    return manifest


@coverage_app.command("validate")
def coverage_validate(
    config: Path = typer.Option(Path("config/knowledge-coverage.yaml")),
    root: Path = typer.Option(Path(".")),
) -> None:
    """验证覆盖状态、日期和证据文件。"""
    manifest = _coverage_or_exit(config, root)
    typer.echo(
        f"PASS: {len(manifest.requirements)} requirements, "
        f"repository readiness={coverage_score(manifest):.1f}%"
    )


@coverage_app.command("report")
def coverage_report(
    config: Path = typer.Option(Path("config/knowledge-coverage.yaml")),
    output: Path = typer.Option(Path("output/reports/knowledge-coverage.md")),
    root: Path = typer.Option(Path(".")),
) -> None:
    """验证清单并生成确定性的公开覆盖报告。"""
    manifest = _coverage_or_exit(config, root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_coverage_report(manifest), encoding="utf-8")
    typer.echo(f"PASS: {coverage_score(manifest):.1f}% -> {output}")


def _private_summary(action: str, root: Path) -> None:
    try:
        summary = (
            initialize_private_workspace(root)
            if action == "init"
            else validate_private_workspace(root)
        )
    except PrivateWorkspaceError as exc:
        typer.echo(f"ERROR: {exc}", err=True)
        raise typer.Exit(1) from exc
    typer.echo(
        f"PASS: private workspace {action}; watchlist={summary.watchlist}, "
        f"positions={summary.positions}, journal={summary.journal_entries}"
    )


@private_app.command("init")
def private_init(root: Path = typer.Option(Path("."))) -> None:
    """创建被 Git 忽略的空白私人研究层；绝不覆盖已有内容。"""

    _private_summary("init", root)


@private_app.command("validate")
def private_validate(root: Path = typer.Option(Path("."))) -> None:
    """只验证私人层结构并输出计数，不回显内容。"""

    _private_summary("validate", root)


@data_app.command("fetch")
def data_fetch(
    market: str,
    symbol: str,
    start: str = typer.Option(...),
    end: str = typer.Option(...),
    adjustment: str = typer.Option("qfq"),
    provider: str = typer.Option("akshare"),
    store_root: Path = typer.Option(Path("data/cache")),
) -> None:
    """抓取、校验并缓存一只证券的日线。"""
    try:
        selected = _provider(provider)
        bars = selected.daily_bars(
            market.upper(), symbol, date.fromisoformat(start), date.fromisoformat(end), adjustment
        )
    except (ValueError, DataUnavailableError) as exc:
        typer.echo(f"ERROR: {exc}", err=True)
        raise typer.Exit(1) from exc
    errors = [issue for issue in validate_bars(bars) if issue.severity == "error"]
    if errors:
        typer.echo(f"ERROR: data validation failed: {errors[0].code}", err=True)
        raise typer.Exit(1)
    manifest = ParquetStore(store_root).write_bars(
        bars,
        request={"market": market.upper(), "symbol": symbol, "start": start, "end": end},
    )
    typer.echo(f"PASS: {manifest.rows} rows, sha256={manifest.sha256}")


@data_app.command("validate")
def data_validate(market: str, symbol: str, store_root: Path = Path("data/cache")) -> None:
    bars = ParquetStore(store_root).read_bars(market.upper(), symbol)
    issues = validate_bars(bars)
    for issue in issues:
        typer.echo(f"{issue.severity}: {issue.code}: {issue.message}")
    if any(issue.severity == "error" for issue in issues):
        raise typer.Exit(1)
    typer.echo(f"PASS: {len(bars)} rows")


@fund_app.command("nav")
def fund_nav(
    symbol: str,
    start: str = typer.Option(...),
    end: str = typer.Option(...),
    output: Path | None = typer.Option(None),
) -> None:
    """获取场外开放式基金单位净值并保存 Parquet。"""
    try:
        nav = AKShareProvider().fund_nav(symbol, date.fromisoformat(start), date.fromisoformat(end))
    except (ValueError, DataUnavailableError) as exc:
        typer.echo(f"ERROR: {exc}", err=True)
        raise typer.Exit(1) from exc
    destination = output or Path("data/cache/funds") / f"{symbol}.parquet"
    destination.parent.mkdir(parents=True, exist_ok=True)
    nav.to_parquet(destination, index=False)
    typer.echo(f"PASS: {len(nav)} rows -> {destination}")


def _run_from_config(config_path: Path) -> Path:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    bars = ParquetStore(config.get("store_root", "data/cache")).read_bars(
        config["market"], str(config["symbol"])
    )
    strategy = config["strategy"]
    if strategy == "buy_and_hold":
        signal = buy_and_hold_signal(len(bars))
    elif strategy == "moving_average":
        parameters = config["parameters"]
        signal = moving_average_signal(bars["close"], parameters["fast"], parameters["slow"])
    else:
        raise ValueError(f"unknown strategy: {strategy}")
    fees = config["fees"]
    result = run_backtest(
        bars,
        signal,
        float(config["initial_cash"]),
        FeeModel(**fees),
        MarketRules(
            board_lot=int(config.get("board_lot", 100)), slippage_bps=config["slippage_bps"]
        ),
    )
    output = Path("output/reports") / config["name"]
    return build_report(
        result,
        output,
        title=config["name"],
        data_description=f"{config['market']} {config['symbol']} cached standardized bars",
        benchmark_description=str(config["benchmark"]),
        reproduction_command=f"investkb backtest run {config_path}",
    )


@backtest_app.command("run")
def backtest_run(config: Path) -> None:
    try:
        path = _run_from_config(config)
    except (KeyError, TypeError, ValueError, FileNotFoundError) as exc:
        typer.echo(f"ERROR: {exc}", err=True)
        raise typer.Exit(1) from exc
    typer.echo(path)


def _demo_bars() -> pd.DataFrame:
    dates = pd.date_range("2023-01-02", periods=260, freq="B")
    close = 100 + np.linspace(0, 18, len(dates)) + 6 * np.sin(np.arange(len(dates)) / 13)
    raw = pd.DataFrame(
        {
            "date": dates,
            "open": close * 0.998,
            "high": close * 1.01,
            "low": close * 0.99,
            "close": close,
            "volume": np.full(len(dates), 1_000_000),
            "amount": close * 1_000_000,
        }
    )
    return normalize_bars(
        raw,
        "DEMO",
        "SYNTHETIC",
        "CNY",
        "offline-fixture",
        "none",
        retrieved_at=datetime(2026, 7, 16, tzinfo=timezone.utc),
    )


@demo_app.command("backtest")
def demo_backtest(offline: bool = typer.Option(False, help="明确使用合成离线数据")) -> None:
    if not offline:
        typer.echo(
            "ERROR: demo requires --offline so synthetic data cannot be mistaken for market data",
            err=True,
        )
        raise typer.Exit(2)
    bars = _demo_bars()
    signal = moving_average_signal(bars["close"], fast=20, slow=60)
    result = run_backtest(
        bars,
        signal,
        100_000,
        FeeModel(commission_rate=0.0003, minimum_commission=5, stamp_duty_rate=0.001),
        MarketRules(board_lot=100, slippage_bps=5),
    )
    path = build_report(
        result,
        Path("output/reports/demo"),
        title="离线合成数据均线示例",
        data_description="合成数据，仅用于验证代码；不是任何真实证券行情。",
        benchmark_description="未设置真实市场基准；本结果不得用于投资判断。",
        reproduction_command="investkb demo backtest --offline",
    )
    typer.echo(path)


if __name__ == "__main__":
    app()
