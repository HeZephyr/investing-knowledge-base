"""标准日线行情的结构化质量规则。"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from investkb.data.models import EXPECTED_BAR_COLUMNS


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    severity: str
    row: int | None
    message: str


def _rows(mask: pd.Series) -> list[int]:
    return [int(index) for index in mask[mask].index]


def validate_bars(frame: pd.DataFrame) -> list[ValidationIssue]:
    """返回阻断性 error 和需要人工检查的 warning。"""
    issues: list[ValidationIssue] = []
    missing = sorted(set(EXPECTED_BAR_COLUMNS) - set(frame.columns))
    if missing:
        return [ValidationIssue("schema-missing", "error", None, f"missing: {', '.join(missing)}")]
    if frame.empty:
        return [ValidationIssue("empty", "error", None, "bar frame is empty")]

    duplicate = frame.duplicated(["market", "symbol", "date"], keep=False)
    for row in _rows(duplicate):
        issues.append(
            ValidationIssue("duplicate-key", "error", row, "duplicate market/symbol/date")
        )

    if not frame["date"].is_monotonic_increasing:
        issues.append(ValidationIssue("date-order", "error", None, "dates must be increasing"))

    price_columns = ["open", "high", "low", "close"]
    non_positive = (frame[price_columns] <= 0).any(axis=1)
    for row in _rows(non_positive):
        issues.append(ValidationIssue("non-positive-price", "error", row, "OHLC must be positive"))

    inconsistent = (frame["high"] < frame[price_columns].max(axis=1)) | (
        frame["low"] > frame[price_columns].min(axis=1)
    )
    for row in _rows(inconsistent):
        issues.append(
            ValidationIssue("ohlc-inconsistent", "error", row, "low/high do not contain OHLC")
        )

    negative_activity = (frame[["volume", "amount"]] < 0).any(axis=1)
    for row in _rows(negative_activity):
        issues.append(
            ValidationIssue(
                "negative-activity", "error", row, "volume and amount cannot be negative"
            )
        )

    if frame["adjustment"].nunique(dropna=False) != 1:
        issues.append(
            ValidationIssue("mixed-adjustment", "error", None, "one frame has mixed adjustments")
        )

    gaps = frame["date"].sort_values().diff().dt.days > 10
    for row in _rows(gaps):
        issues.append(
            ValidationIssue("large-date-gap", "warning", row, "gap exceeds ten calendar days")
        )

    extreme = frame["close"].pct_change().abs() > 0.5
    for row in _rows(extreme):
        issues.append(
            ValidationIssue("extreme-return", "warning", row, "absolute daily return exceeds 50%")
        )
    return issues
