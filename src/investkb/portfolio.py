"""Public, holdings-free portfolio governance and risk exercises."""

from __future__ import annotations

import math
from datetime import date
from typing import Any, Mapping, Sequence

import numpy as np


class PortfolioLabError(ValueError):
    """Portfolio lab inputs violate an explicit governance or math contract."""


def _finite(name: str, value: float) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise PortfolioLabError(f"{name} must be numeric") from exc
    if not math.isfinite(number):
        raise PortfolioLabError(f"{name} must be finite")
    return number


def _date(name: str, value: Any) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError as exc:
            raise PortfolioLabError(f"{name} must be ISO YYYY-MM-DD") from exc
    raise PortfolioLabError(f"{name} must be a date")


def _weight_mapping(weights: Mapping[str, float], *, tolerance: float = 1e-9) -> dict[str, float]:
    if not weights or any(not str(label).strip() for label in weights):
        raise PortfolioLabError("weight labels must be non-empty")
    result = {str(label): _finite(f"weight[{label}]", value) for label, value in weights.items()}
    if any(value < 0 for value in result.values()):
        raise PortfolioLabError("weights must be nonnegative")
    if not math.isclose(sum(result.values()), 1.0, abs_tol=tolerance):
        raise PortfolioLabError("weights must sum to 1")
    return result


def _weight_array(weights: Sequence[float], *, tolerance: float = 1e-9) -> np.ndarray:
    array = np.asarray(weights, dtype=float)
    if array.ndim != 1 or array.size == 0 or not np.isfinite(array).all():
        raise PortfolioLabError("weights must be a finite one-dimensional vector")
    if (array < 0).any() or not math.isclose(float(array.sum()), 1.0, abs_tol=tolerance):
        raise PortfolioLabError("weights must be nonnegative and sum to 1")
    return array


def validate_ips(policy: Mapping[str, Any], *, as_of: date) -> dict[str, Any]:
    """Validate a minimal public/example investment policy statement."""

    required = {
        "objective",
        "horizon_years",
        "emergency_reserve_months",
        "max_equity_weight",
        "max_single_asset_weight",
        "decision_date",
        "next_review_date",
    }
    missing = sorted(required - set(policy))
    if missing:
        raise PortfolioLabError(f"IPS missing fields: {', '.join(missing)}")
    objective = str(policy["objective"]).strip()
    if not objective:
        raise PortfolioLabError("objective must be non-empty")
    horizon = _finite("horizon_years", policy["horizon_years"])
    reserve = _finite("emergency_reserve_months", policy["emergency_reserve_months"])
    equity_limit = _finite("max_equity_weight", policy["max_equity_weight"])
    asset_limit = _finite("max_single_asset_weight", policy["max_single_asset_weight"])
    if horizon <= 0 or reserve < 0 or not 0 <= equity_limit <= 1 or not 0 < asset_limit <= 1:
        raise PortfolioLabError("IPS horizon, reserve, or weight constraints are invalid")
    decision = _date("decision_date", policy["decision_date"])
    review = _date("next_review_date", policy["next_review_date"])
    if decision > as_of or review <= as_of or review <= decision:
        raise PortfolioLabError("IPS decision/review dates are invalid for the review cycle")
    normalized = dict(policy)
    normalized["decision_date"] = decision.isoformat()
    normalized["next_review_date"] = review.isoformat()
    return {"policy": normalized, "review_interval_days": (review - decision).days}


def allocation_diagnostics(
    weights: Mapping[str, float], *, expected_returns: Mapping[str, float] | None = None
) -> dict[str, float | None]:
    """Describe concentration and an assumption-weighted expected return."""

    normalized = _weight_mapping(weights)
    hhi = sum(value**2 for value in normalized.values())
    expected: float | None = None
    if expected_returns is not None:
        if set(expected_returns) != set(normalized):
            raise PortfolioLabError("expected-return labels must match weight labels")
        expected = sum(
            normalized[label] * _finite(f"expected_return[{label}]", expected_returns[label])
            for label in normalized
        )
    return {
        "herfindahl_index": hhi,
        "effective_holdings": 1 / hhi,
        "expected_return": expected,
    }


def rebalance_plan(
    current_values: Mapping[str, float],
    target_weights: Mapping[str, float],
    *,
    cash_flow: float = 0,
    fee_bps: int = 0,
) -> dict[str, Any]:
    """Create a paper rebalance plan and charge fees on one-way traded value."""

    weights = _weight_mapping(target_weights)
    if set(current_values) != set(weights):
        raise PortfolioLabError("current-value labels must match target labels")
    current = {
        label: _finite(f"current_value[{label}]", value) for label, value in current_values.items()
    }
    if any(value < 0 for value in current.values()):
        raise PortfolioLabError("current values must be nonnegative")
    cash = _finite("cash_flow", cash_flow)
    if isinstance(fee_bps, bool) or not isinstance(fee_bps, int) or not 0 <= fee_bps <= 10_000:
        raise PortfolioLabError("fee_bps must be an integer between 0 and 10000")
    total = sum(current.values()) + cash
    if total <= 0:
        raise PortfolioLabError("post-flow portfolio value must be positive")
    target_values = {label: total * weight for label, weight in weights.items()}
    trades = {label: target_values[label] - current[label] for label in weights}
    gross_traded_value = sum(abs(value) for value in trades.values())
    one_way_traded_value = gross_traded_value / 2
    cost = gross_traded_value * fee_bps / 10_000
    return {
        "target_values": target_values,
        "trades": trades,
        "gross_traded_value": gross_traded_value,
        "one_way_turnover": one_way_traded_value / total,
        "estimated_cost": cost,
        "post_cost_value": total - cost,
        "fee_bps": fee_bps,
    }


def liquidity_diagnostics(
    *,
    positions: Mapping[str, float],
    average_daily_value: Mapping[str, float],
    participation_rate: float,
    max_days: float,
) -> dict[str, Any]:
    """Estimate liquidation days under a fixed share of average traded value."""

    if set(positions) != set(average_daily_value) or not positions:
        raise PortfolioLabError("position and liquidity labels must match")
    participation = _finite("participation_rate", participation_rate)
    limit = _finite("max_days", max_days)
    if not 0 < participation <= 1 or limit <= 0:
        raise PortfolioLabError("participation_rate and max_days are invalid")
    days: dict[str, float] = {}
    for label in positions:
        position = _finite(f"position[{label}]", positions[label])
        daily = _finite(f"average_daily_value[{label}]", average_daily_value[label])
        if position < 0 or daily <= 0:
            raise PortfolioLabError("positions must be nonnegative and daily value positive")
        days[label] = position / (daily * participation)
    return {
        "days_to_liquidate": days,
        "breaches": sorted(label for label, value in days.items() if value > limit),
    }


def risk_contributions(weights: Sequence[float], covariance: np.ndarray) -> dict[str, Any]:
    """Decompose volatility into marginal and component risk contributions."""

    vector = _weight_array(weights)
    matrix = np.asarray(covariance, dtype=float)
    if matrix.shape != (vector.size, vector.size) or not np.isfinite(matrix).all():
        raise PortfolioLabError("covariance shape/values are invalid")
    if not np.allclose(matrix, matrix.T, atol=1e-12):
        raise PortfolioLabError("covariance must be symmetric")
    if float(np.linalg.eigvalsh(matrix).min()) < -1e-10:
        raise PortfolioLabError("covariance must be positive semidefinite")
    variance = float(vector @ matrix @ vector)
    if variance <= 0:
        raise PortfolioLabError("portfolio volatility must be positive")
    volatility = math.sqrt(variance)
    marginal = matrix @ vector / volatility
    component = vector * marginal
    return {
        "portfolio_volatility": volatility,
        "marginal_contributions": marginal.tolist(),
        "component_contributions": component.tolist(),
        "contribution_shares": (component / volatility).tolist(),
    }


def stress_loss(weights: Mapping[str, float], shocks: Mapping[str, float]) -> float:
    """Calculate the signed first-order portfolio return under asset shocks."""

    normalized = _weight_mapping(weights)
    if set(normalized) != set(shocks):
        raise PortfolioLabError("shock labels must match weight labels")
    return sum(
        normalized[label] * _finite(f"shock[{label}]", shocks[label]) for label in normalized
    )


def reverse_stress_shock(
    weights: Mapping[str, float],
    *,
    known_shocks: Mapping[str, float],
    solve_asset: str,
    target_loss: float,
) -> float:
    """Solve the one asset shock needed to reach a signed portfolio loss."""

    normalized = _weight_mapping(weights)
    if solve_asset not in normalized or set(known_shocks) != set(normalized) - {solve_asset}:
        raise PortfolioLabError("reverse-stress labels are invalid")
    if normalized[solve_asset] <= 0:
        raise PortfolioLabError("solve asset must have positive weight")
    target = _finite("target_loss", target_loss)
    known = sum(
        normalized[label] * _finite(f"shock[{label}]", known_shocks[label])
        for label in known_shocks
    )
    return (target - known) / normalized[solve_asset]


def brinson_attribution(
    *,
    portfolio_weights: Sequence[float],
    benchmark_weights: Sequence[float],
    portfolio_returns: Sequence[float],
    benchmark_returns: Sequence[float],
) -> dict[str, float]:
    """Perform single-period Brinson-Fachler attribution and reconcile active return."""

    wp = _weight_array(portfolio_weights)
    wb = _weight_array(benchmark_weights)
    rp = np.asarray(portfolio_returns, dtype=float)
    rb = np.asarray(benchmark_returns, dtype=float)
    if wp.shape != wb.shape or rp.shape != wp.shape or rb.shape != wp.shape:
        raise PortfolioLabError("attribution vectors must have matching shapes")
    if not np.isfinite(rp).all() or not np.isfinite(rb).all():
        raise PortfolioLabError("attribution returns must be finite")
    portfolio_return = float(wp @ rp)
    benchmark_return = float(wb @ rb)
    allocation = float((wp - wb) @ (rb - benchmark_return))
    selection = float(wb @ (rp - rb))
    interaction = float((wp - wb) @ (rp - rb))
    active = portfolio_return - benchmark_return
    if not math.isclose(allocation + selection + interaction, active, abs_tol=1e-12):
        raise PortfolioLabError("attribution effects do not reconcile to active return")
    return {
        "portfolio_return": portfolio_return,
        "benchmark_return": benchmark_return,
        "active_return": active,
        "allocation": allocation,
        "selection": selection,
        "interaction": interaction,
    }


def validate_decision_journal(journal: Mapping[str, Any]) -> dict[str, Any]:
    """Score preregistered process fields without inspecting investment outcomes."""

    required = (
        "decision_date",
        "thesis",
        "base_rate",
        "success_condition",
        "failure_condition",
        "horizon",
        "size_limit",
        "evidence",
    )
    missing: list[str] = []
    for field in required:
        value = journal.get(field)
        if field == "decision_date":
            try:
                _date(field, value)
            except PortfolioLabError:
                missing.append(field)
        elif field == "evidence":
            if (
                not isinstance(value, list)
                or not value
                or any(not str(item).strip() for item in value)
            ):
                missing.append(field)
        elif not isinstance(value, str) or not value.strip():
            missing.append(field)
    return {
        "complete": not missing,
        "completeness_score": (len(required) - len(missing)) / len(required),
        "missing_fields": missing,
    }
