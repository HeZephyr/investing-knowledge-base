"""只依赖当前及过去数据的无状态研究信号。"""

from __future__ import annotations

import pandas as pd


def buy_and_hold_signal(length: int) -> pd.Series:
    if length <= 0:
        raise ValueError("length must be positive")
    return pd.Series(1, index=range(length), dtype="int64", name="signal")


def moving_average_signal(prices: pd.Series, fast: int, slow: int) -> pd.Series:
    if fast <= 0 or slow <= 0 or fast >= slow:
        raise ValueError("moving-average windows require 0 < fast < slow")
    values = pd.to_numeric(prices, errors="raise")
    fast_average = values.rolling(fast, min_periods=fast).mean()
    slow_average = values.rolling(slow, min_periods=slow).mean()
    signal = (fast_average > slow_average).fillna(False).astype("int64")
    signal.name = "signal"
    return signal
