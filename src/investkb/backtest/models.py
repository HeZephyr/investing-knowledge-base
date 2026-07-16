"""回测配置与输出数据结构。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class FeeModel:
    commission_rate: float = 0.0003
    minimum_commission: float = 5.0
    stamp_duty_rate: float = 0.0

    def calculate(self, side: str, gross: float) -> float:
        commission = max(self.minimum_commission, gross * self.commission_rate)
        tax = gross * self.stamp_duty_rate if side == "sell" else 0.0
        return commission + tax


@dataclass(frozen=True)
class MarketRules:
    board_lot: int = 100
    slippage_bps: float = 5.0


@dataclass(frozen=True)
class BacktestResult:
    equity: pd.Series
    positions: pd.DataFrame
    orders: pd.DataFrame
    trades: pd.DataFrame
    assumptions: dict[str, Any]
