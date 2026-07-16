"""跨提供商的日线行情数据契约。"""

from __future__ import annotations

from datetime import datetime, timezone

import pandas as pd

VENDOR_BAR_COLUMNS = ["date", "open", "high", "low", "close", "volume", "amount"]
EXPECTED_BAR_COLUMNS = [
    "market",
    "symbol",
    "date",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "amount",
    "currency",
    "adjustment",
    "provider",
    "retrieved_at",
]


def normalize_bars(
    frame: pd.DataFrame,
    market: str,
    symbol: str,
    currency: str,
    provider: str,
    adjustment: str,
    retrieved_at: datetime | None = None,
) -> pd.DataFrame:
    """把已映射为英文列名的提供商响应转换为标准日线 frame。"""
    missing = sorted(set(VENDOR_BAR_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"bar data is missing required columns: {', '.join(missing)}")
    if frame.empty:
        raise ValueError("bar data is empty")

    result = frame[VENDOR_BAR_COLUMNS].copy()
    result["date"] = pd.to_datetime(result["date"]).dt.normalize()
    for column in ["open", "high", "low", "close", "volume", "amount"]:
        result[column] = pd.to_numeric(result[column], errors="raise")
    result.insert(0, "symbol", str(symbol))
    result.insert(0, "market", market)
    result["currency"] = currency
    result["adjustment"] = adjustment
    result["provider"] = provider
    stamp = retrieved_at or datetime.now(timezone.utc)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    result["retrieved_at"] = pd.Timestamp(stamp).tz_convert("UTC")
    return result[EXPECTED_BAR_COLUMNS].sort_values("date").reset_index(drop=True)
