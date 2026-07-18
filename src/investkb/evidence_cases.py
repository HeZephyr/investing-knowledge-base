"""Deterministic calculations for public company, factor, and portfolio cases."""

from __future__ import annotations

import math
from statistics import stdev
from typing import Any

from .cases import CaseSnapshot


class EvidenceCaseError(ValueError):
    """A public evidence case is incomplete or has invalid assumptions."""


def _series(snapshot: CaseSnapshot, name: str) -> dict[int, float]:
    selected = snapshot.observations.loc[
        snapshot.observations["series"].astype(str) == name, ["period", "value"]
    ]
    if selected.empty:
        raise EvidenceCaseError(f"required series is missing: {name}")
    try:
        result = {int(row.period): float(row.value) for row in selected.itertuples(index=False)}
    except (TypeError, ValueError) as exc:
        raise EvidenceCaseError(f"series {name} must have integer years") from exc
    if len(result) != len(selected):
        raise EvidenceCaseError(f"series {name} has duplicate years")
    return result


def _continuous(series: dict[int, float], *, start: int | None = None) -> list[int]:
    years = sorted(series)
    if start is not None:
        years = [year for year in years if year >= start]
    if not years or years != list(range(years[0], years[-1] + 1)):
        raise EvidenceCaseError("series must contain continuous annual observations")
    return years


def _growth(current: float, previous: float) -> float:
    if previous == 0:
        raise EvidenceCaseError("growth denominator cannot be zero")
    return (current / previous - 1) * 100


def _compound(returns: list[float]) -> float:
    wealth = 1.0
    for value in returns:
        wealth *= 1 + value
    return wealth


def _company(snapshot: CaseSnapshot) -> dict[str, Any]:
    if snapshot.case_id != "company-positive":
        raise EvidenceCaseError("company analysis requires company-positive snapshot")
    revenue = _series(snapshot, "meta_revenue")
    operating = _series(snapshot, "meta_operating_income")
    cash = _series(snapshot, "meta_free_cash_flow")
    shares = _series(snapshot, "meta_diluted_shares")
    required = {2022, 2024}
    if any(not required.issubset(values) for values in (revenue, operating, cash, shares)):
        raise EvidenceCaseError("company case requires 2022 and 2024 observations")
    op_change = operating[2024] / revenue[2024] * 100 - operating[2022] / revenue[2022] * 100
    cash_change = cash[2024] / revenue[2024] * 100 - cash[2022] / revenue[2022] * 100
    revenue_growth = _growth(revenue[2024], revenue[2022])
    share_change = _growth(shares[2024], shares[2022])
    per_share_growth = _growth(cash[2024] / shares[2024], cash[2022] / shares[2022])
    return {
        "case_id": snapshot.case_id,
        "revenue_growth_pct": round(revenue_growth, 2),
        "operating_margin_change_pp": round(op_change, 2),
        "fcf_margin_change_pp": round(cash_change, 2),
        "diluted_share_change_pct": round(share_change, 2),
        "fcf_per_diluted_share_growth_pct": round(per_share_growth, 2),
        "hypothesis_supported": revenue_growth > 0
        and op_change >= 10
        and cash_change >= 10
        and share_change <= 0,
    }


def _factor(snapshot: CaseSnapshot) -> dict[str, Any]:
    if snapshot.case_id != "factor-strategy":
        raise EvidenceCaseError("factor analysis requires factor-strategy snapshot")
    hml = _series(snapshot, "hml")
    years = _continuous(hml)
    returns = [hml[year] / 100 for year in years]
    arithmetic = sum(returns) / len(returns) * 100
    compounded = (_compound(returns) - 1) * 100
    return {
        "case_id": snapshot.case_id,
        "years": len(years),
        "hml_arithmetic_mean_pct": round(arithmetic, 2),
        "hml_compound_return_pct": round(compounded, 2),
        "hml_positive_years": sum(value > 0 for value in returns),
        "hypothesis_supported": arithmetic > 0 and compounded > 0,
    }


def _negative_strategy(snapshot: CaseSnapshot, fee_bps: int) -> dict[str, Any]:
    if snapshot.case_id != "factor-strategy":
        raise EvidenceCaseError("negative_strategy analysis requires factor-strategy snapshot")
    market = _series(snapshot, "mkt_rf")
    risk_free = _series(snapshot, "rf")
    years = _continuous(market)
    if sorted(risk_free) != years:
        raise EvidenceCaseError("market and risk-free years must match")
    evaluated = years[1:]
    previous_position = 0
    changes = 0
    invested = 0
    strategy_returns: list[float] = []
    benchmark_returns: list[float] = []
    for year in evaluated:
        position = int(market[year - 1] < 0)
        turnover = abs(position - previous_position)
        changes += turnover
        invested += position
        market_total = (market[year] + risk_free[year]) / 100
        gross = market_total if position else risk_free[year] / 100
        strategy_returns.append(gross - fee_bps / 10_000 * turnover)
        benchmark_returns.append(market_total)
        previous_position = position
    strategy_wealth = _compound(strategy_returns)
    benchmark_wealth = _compound(benchmark_returns)
    periods = len(evaluated)
    strategy_cagr = strategy_wealth ** (1 / periods) - 1
    benchmark_cagr = benchmark_wealth ** (1 / periods) - 1
    return {
        "case_id": snapshot.case_id,
        "strategy_cumulative_return_pct": round((strategy_wealth - 1) * 100, 2),
        "benchmark_cumulative_return_pct": round((benchmark_wealth - 1) * 100, 2),
        "strategy_cagr_pct": round(strategy_cagr * 100, 2),
        "benchmark_cagr_pct": round(benchmark_cagr * 100, 2),
        "invested_years": invested,
        "position_changes": changes,
        "fee_bps": fee_bps,
        "hypothesis_supported": strategy_cagr > benchmark_cagr,
    }


def _portfolio(snapshot: CaseSnapshot, fee_bps: int) -> dict[str, Any]:
    if snapshot.case_id != "portfolio-public":
        raise EvidenceCaseError("portfolio analysis requires portfolio-public snapshot")
    names = ("cn_equity_etf_close", "cn_bond_etf_close", "cn_gold_etf_close")
    prices = [_series(snapshot, name) for name in names]
    years = _continuous(prices[0])
    if any(sorted(values) != years for values in prices):
        raise EvidenceCaseError("portfolio price years must match")
    if any(
        value <= 0 or not math.isfinite(value) for values in prices for value in values.values()
    ):
        raise EvidenceCaseError("portfolio prices must be finite and positive")
    target = [1 / len(prices)] * len(prices)
    prior_returns: list[float] | None = None
    portfolio_returns: list[float] = []
    benchmark_returns: list[float] = []
    for index, year in enumerate(years[1:], start=1):
        asset_returns = [values[year] / values[years[index - 1]] - 1 for values in prices]
        if prior_returns is None:
            turnover = 1.0
        else:
            denominator = sum(weight * (1 + value) for weight, value in zip(target, prior_returns))
            drifted = [
                weight * (1 + value) / denominator for weight, value in zip(target, prior_returns)
            ]
            turnover = sum(abs(weight - drift) for weight, drift in zip(target, drifted)) / 2
        gross = sum(weight * value for weight, value in zip(target, asset_returns))
        fee = fee_bps / 10_000 * turnover
        portfolio_returns.append((1 - fee) * (1 + gross) - 1)
        benchmark_returns.append(asset_returns[0])
        prior_returns = asset_returns
    wealth = _compound(portfolio_returns)
    benchmark_wealth = _compound(benchmark_returns)
    periods = len(portfolio_returns)
    cagr = wealth ** (1 / periods) - 1
    benchmark_cagr = benchmark_wealth ** (1 / periods) - 1
    volatility = stdev(portfolio_returns)
    benchmark_volatility = stdev(benchmark_returns)
    path = [1.0]
    for value in portfolio_returns:
        path.append(path[-1] * (1 + value))
    peak = path[0]
    max_drawdown = 0.0
    for value in path:
        peak = max(peak, value)
        max_drawdown = min(max_drawdown, value / peak - 1)
    return {
        "case_id": snapshot.case_id,
        "portfolio_cumulative_return_pct": round((wealth - 1) * 100, 2),
        "portfolio_cagr_pct": round(cagr * 100, 2),
        "benchmark_cumulative_return_pct": round((benchmark_wealth - 1) * 100, 2),
        "benchmark_cagr_pct": round(benchmark_cagr * 100, 2),
        "annual_volatility_pct": round(volatility * 100, 2),
        "benchmark_annual_volatility_pct": round(benchmark_volatility * 100, 2),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "fee_bps": fee_bps,
        "hypothesis_supported": cagr > benchmark_cagr and volatility < benchmark_volatility,
    }


def evidence_metrics(snapshot: CaseSnapshot, *, analysis: str, fee_bps: int = 0) -> dict[str, Any]:
    """Calculate one named public-evidence analysis from a validated snapshot."""

    if isinstance(fee_bps, bool) or not isinstance(fee_bps, int) or not 0 <= fee_bps <= 10_000:
        raise EvidenceCaseError("fee_bps must be an integer between 0 and 10000")
    handlers = {
        "company": lambda: _company(snapshot),
        "factor": lambda: _factor(snapshot),
        "negative_strategy": lambda: _negative_strategy(snapshot, fee_bps),
        "portfolio": lambda: _portfolio(snapshot, fee_bps),
    }
    try:
        handler = handlers[analysis]
    except KeyError as exc:
        raise EvidenceCaseError(f"unknown analysis: {analysis}") from exc
    return handler()
