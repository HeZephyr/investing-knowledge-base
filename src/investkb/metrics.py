"""透明、口径明确的日线绩效与风险指标。"""

from __future__ import annotations

import math
from typing import Any

import pandas as pd


def _equity(equity: pd.Series) -> pd.Series:
    values = pd.to_numeric(equity, errors="raise").dropna().astype(float)
    if len(values) < 2:
        raise ValueError("equity requires at least two observations")
    if (values <= 0).any():
        raise ValueError("equity values must be positive")
    return values


def max_drawdown(equity: pd.Series) -> float:
    values = _equity(equity)
    drawdown = values / values.cummax() - 1.0
    return float(drawdown.min())


def performance_summary(
    equity: pd.Series,
    annualization: int = 252,
    annual_risk_free_rate: float = 0.0,
) -> dict[str, Any]:
    values = _equity(equity)
    returns = values.pct_change().dropna()
    periods = len(values) - 1
    total_return = float(values.iloc[-1] / values.iloc[0] - 1.0)
    cagr = float((values.iloc[-1] / values.iloc[0]) ** (annualization / periods) - 1.0)
    volatility = float(returns.std(ddof=1) * math.sqrt(annualization)) if len(returns) > 1 else None
    daily_rf = (1.0 + annual_risk_free_rate) ** (1.0 / annualization) - 1.0
    excess = returns - daily_rf
    excess_std = excess.std(ddof=1)
    sharpe = (
        float(excess.mean() / excess_std * math.sqrt(annualization))
        if len(excess) > 1 and excess_std > 0
        else None
    )
    downside = excess[excess < 0]
    downside_std = downside.std(ddof=1)
    sortino = (
        float(excess.mean() / downside_std * math.sqrt(annualization))
        if len(downside) > 1 and downside_std > 0
        else None
    )
    drawdown = max_drawdown(values)
    calmar = float(cagr / abs(drawdown)) if drawdown < 0 else None
    return {
        "total_return": total_return,
        "cagr": cagr,
        "annualized_volatility": volatility,
        "max_drawdown": drawdown,
        "sharpe": sharpe,
        "sortino": sortino,
        "calmar": calmar,
        "win_rate": float((returns > 0).mean()),
        "observations": len(values),
        "annualization": annualization,
        "annual_risk_free_rate": annual_risk_free_rate,
    }
