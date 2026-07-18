"""Offline, deterministic calculations for company research exercises."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Iterable, Mapping, Sequence


class CompanyResearchError(ValueError):
    """Company research input is invalid or internally inconsistent."""


def _finite(name: str, value: float) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise CompanyResearchError(f"{name} must be finite")
    return number


@dataclass(frozen=True)
class FilingFact:
    metric: str
    period: str
    value: float
    filed_at: datetime
    accession: str

    def __post_init__(self) -> None:
        if not self.metric.strip() or not self.period.strip() or not self.accession.strip():
            raise CompanyResearchError("filing fact text fields must be non-empty")
        _finite("filing fact value", self.value)
        if self.filed_at.tzinfo is None or self.filed_at.utcoffset() is None:
            raise CompanyResearchError("filing timestamp must include timezone")


def select_point_in_time_facts(
    facts: Iterable[FilingFact], *, decision_at: datetime
) -> dict[tuple[str, str], FilingFact]:
    """Select the latest version of each metric-period available at a decision time."""

    if decision_at.tzinfo is None or decision_at.utcoffset() is None:
        raise CompanyResearchError("decision timestamp must include timezone")
    selected: dict[tuple[str, str], FilingFact] = {}
    for fact in facts:
        if fact.filed_at > decision_at:
            continue
        key = (fact.metric, fact.period)
        previous = selected.get(key)
        if previous is None or (fact.filed_at, fact.accession) > (
            previous.filed_at,
            previous.accession,
        ):
            selected[key] = fact
    return selected


def reconcile_statements(
    *,
    assets: float,
    liabilities: float,
    equity: float,
    opening_cash: float,
    cash_from_operations: float,
    cash_from_investing: float,
    cash_from_financing: float,
    fx_effect: float,
    closing_cash: float,
    tolerance: float = 1e-6,
) -> dict[str, float]:
    """Fail closed unless the balance-sheet and cash-flow identities reconcile."""

    values = {
        name: _finite(name, value)
        for name, value in {
            "assets": assets,
            "liabilities": liabilities,
            "equity": equity,
            "opening_cash": opening_cash,
            "cash_from_operations": cash_from_operations,
            "cash_from_investing": cash_from_investing,
            "cash_from_financing": cash_from_financing,
            "fx_effect": fx_effect,
            "closing_cash": closing_cash,
        }.items()
    }
    tolerance = _finite("tolerance", tolerance)
    if tolerance < 0:
        raise CompanyResearchError("tolerance must be nonnegative")
    balance_gap = values["assets"] - values["liabilities"] - values["equity"]
    cash_gap = (
        values["opening_cash"]
        + values["cash_from_operations"]
        + values["cash_from_investing"]
        + values["cash_from_financing"]
        + values["fx_effect"]
        - values["closing_cash"]
    )
    if abs(balance_gap) > tolerance:
        raise CompanyResearchError(f"balance-sheet identity does not reconcile: {balance_gap}")
    if abs(cash_gap) > tolerance:
        raise CompanyResearchError(f"cash-flow identity does not reconcile: {cash_gap}")
    return {"balance_sheet_gap": round(balance_gap, 12), "cash_flow_gap": round(cash_gap, 12)}


def cash_conversion_metrics(
    revenue: float,
    cost_of_goods_sold: float,
    receivables_open: float,
    receivables_close: float,
    inventory_open: float,
    inventory_close: float,
    payables_open: float,
    payables_close: float,
    cash_from_operations: float,
    capital_expenditure: float,
    days: int = 365,
) -> dict[str, float]:
    """Calculate cash-conversion diagnostics using average working-capital balances."""

    revenue = _finite("revenue", revenue)
    cost = _finite("cost_of_goods_sold", cost_of_goods_sold)
    if revenue <= 0 or cost <= 0:
        raise CompanyResearchError("revenue and cost_of_goods_sold must be positive")
    if isinstance(days, bool) or not isinstance(days, int) or days <= 0:
        raise CompanyResearchError("days must be a positive integer")
    balances = [
        _finite(name, value)
        for name, value in (
            ("receivables_open", receivables_open),
            ("receivables_close", receivables_close),
            ("inventory_open", inventory_open),
            ("inventory_close", inventory_close),
            ("payables_open", payables_open),
            ("payables_close", payables_close),
        )
    ]
    if any(value < 0 for value in balances):
        raise CompanyResearchError("working-capital balances must be nonnegative")
    average_receivables = (balances[0] + balances[1]) / 2
    average_inventory = (balances[2] + balances[3]) / 2
    average_payables = (balances[4] + balances[5]) / 2
    dso = average_receivables / revenue * days
    dio = average_inventory / cost * days
    dpo = average_payables / cost * days
    return {
        "dso_days": round(dso, 2),
        "dio_days": round(dio, 2),
        "dpo_days": round(dpo, 2),
        "cash_conversion_cycle_days": round(dso + dio - dpo, 2),
        "free_cash_flow": _finite("cash_from_operations", cash_from_operations)
        - _finite("capital_expenditure", capital_expenditure),
    }


def fully_diluted_shares(
    basic_shares: float,
    restricted_stock_units: float,
    option_shares: float,
    option_exercise_price: float,
    average_market_price: float,
) -> dict[str, float]:
    """Apply a simplified treasury-stock method to option dilution."""

    values = [
        _finite(name, value)
        for name, value in (
            ("basic_shares", basic_shares),
            ("restricted_stock_units", restricted_stock_units),
            ("option_shares", option_shares),
            ("option_exercise_price", option_exercise_price),
            ("average_market_price", average_market_price),
        )
    ]
    if any(value < 0 for value in values[:-1]) or values[-1] <= 0 or values[0] <= 0:
        raise CompanyResearchError(
            "share inputs must be nonnegative and prices/basic shares positive"
        )
    basic, units, options, exercise, market = values
    incremental = options * max(1 - exercise / market, 0)
    return {
        "incremental_option_shares": incremental,
        "fully_diluted_shares": basic + units + incremental,
    }


def _dcf_value(
    revenue: float,
    growth: float,
    margin: float,
    discount_rate: float,
    terminal_growth: float,
    years: int,
) -> float:
    present_value = 0.0
    forecast_revenue = revenue
    final_cash_flow = 0.0
    for year in range(1, years + 1):
        forecast_revenue *= 1 + growth
        final_cash_flow = forecast_revenue * margin
        present_value += final_cash_flow / (1 + discount_rate) ** year
    terminal = final_cash_flow * (1 + terminal_growth) / (discount_rate - terminal_growth)
    return present_value + terminal / (1 + discount_rate) ** years


def reverse_dcf_growth(
    enterprise_value: float,
    revenue: float,
    free_cash_flow_margin: float,
    discount_rate: float,
    terminal_growth: float,
    forecast_years: int,
    *,
    lower_growth: float = -0.5,
    upper_growth: float = 1.0,
    tolerance: float = 1e-8,
    max_iterations: int = 200,
) -> float:
    """Solve the constant forecast growth implied by an enterprise value."""

    target = _finite("enterprise_value", enterprise_value)
    revenue = _finite("revenue", revenue)
    margin = _finite("free_cash_flow_margin", free_cash_flow_margin)
    discount = _finite("discount_rate", discount_rate)
    terminal = _finite("terminal_growth", terminal_growth)
    lower = _finite("lower_growth", lower_growth)
    upper = _finite("upper_growth", upper_growth)
    if target <= 0 or revenue <= 0 or margin <= 0:
        raise CompanyResearchError("enterprise value, revenue, and margin must be positive")
    if discount <= terminal or discount <= -1 or terminal <= -1:
        raise CompanyResearchError("discount_rate must exceed terminal_growth")
    if (
        isinstance(forecast_years, bool)
        or not isinstance(forecast_years, int)
        or forecast_years <= 0
    ):
        raise CompanyResearchError("forecast_years must be a positive integer")
    if not -1 < lower < upper:
        raise CompanyResearchError("growth bounds must satisfy -1 < lower < upper")
    low_value = _dcf_value(revenue, lower, margin, discount, terminal, forecast_years)
    high_value = _dcf_value(revenue, upper, margin, discount, terminal, forecast_years)
    if not low_value <= target <= high_value:
        raise CompanyResearchError("enterprise value is not bracketed by growth bounds")
    for _ in range(max_iterations):
        midpoint = (lower + upper) / 2
        value = _dcf_value(revenue, midpoint, margin, discount, terminal, forecast_years)
        if abs(value - target) <= tolerance:
            return midpoint
        if value < target:
            lower = midpoint
        else:
            upper = midpoint
    return (lower + upper) / 2


def scenario_valuation(
    scenarios: Sequence[Mapping[str, Any]], net_debt: float, diluted_shares: float
) -> dict[str, float]:
    """Calculate probability-weighted enterprise and per-share equity value."""

    if not scenarios:
        raise CompanyResearchError("scenarios must not be empty")
    net_debt = _finite("net_debt", net_debt)
    shares = _finite("diluted_shares", diluted_shares)
    if shares <= 0:
        raise CompanyResearchError("diluted_shares must be positive")
    probability_sum = 0.0
    weighted_value = 0.0
    names: set[str] = set()
    for scenario in scenarios:
        name = str(scenario.get("name", "")).strip()
        if not name or name in names:
            raise CompanyResearchError("scenario names must be unique and non-empty")
        names.add(name)
        probability = _finite("probability", scenario.get("probability", math.nan))
        value = _finite("enterprise_value", scenario.get("enterprise_value", math.nan))
        if not 0 <= probability <= 1 or value < 0:
            raise CompanyResearchError("scenario probability/value is invalid")
        probability_sum += probability
        weighted_value += probability * value
    if not math.isclose(probability_sum, 1.0, abs_tol=1e-9):
        raise CompanyResearchError("scenario probabilities must sum to 1")
    return {
        "weighted_enterprise_value": weighted_value,
        "weighted_equity_value_per_share": (weighted_value - net_debt) / shares,
    }


def normalized_multiples(
    *,
    enterprise_value: float,
    equity_value: float,
    revenue: float,
    ebitda: float,
    net_income: float,
) -> dict[str, float | None]:
    """Return comparable multiples while keeping nonpositive denominators undefined."""

    enterprise = _finite("enterprise_value", enterprise_value)
    equity = _finite("equity_value", equity_value)
    revenue = _finite("revenue", revenue)
    ebitda = _finite("ebitda", ebitda)
    earnings = _finite("net_income", net_income)
    if enterprise < 0 or equity < 0 or revenue <= 0:
        raise CompanyResearchError("values must be nonnegative and revenue positive")
    return {
        "ev_to_revenue": enterprise / revenue,
        "ev_to_ebitda": enterprise / ebitda if ebitda > 0 else None,
        "price_to_earnings": equity / earnings if earnings > 0 else None,
    }
