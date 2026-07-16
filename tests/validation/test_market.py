from datetime import datetime, timezone

import pandas as pd
import pytest

from investkb.data.models import normalize_bars
from investkb.validation.market import validate_bars


def good_bars() -> pd.DataFrame:
    raw = pd.DataFrame(
        {
            "date": ["2024-01-02", "2024-01-03", "2024-01-04"],
            "open": [10.0, 10.2, 10.3],
            "high": [10.4, 10.5, 10.6],
            "low": [9.9, 10.0, 10.1],
            "close": [10.2, 10.3, 10.5],
            "volume": [100, 110, 120],
            "amount": [1020, 1133, 1260],
        }
    )
    return normalize_bars(
        raw,
        "CN",
        "600000",
        "CNY",
        "fixture",
        "qfq",
        retrieved_at=datetime(2026, 7, 16, tzinfo=timezone.utc),
    )


def mutate(frame: pd.DataFrame, mutation: str) -> pd.DataFrame:
    result = frame.copy()
    if mutation == "duplicate":
        return pd.concat([result, result.iloc[[0]]], ignore_index=True)
    if mutation == "negative":
        result.loc[0, "close"] = -1
    elif mutation == "bad_ohlc":
        result.loc[0, "high"] = 5
    elif mutation == "unsorted":
        result = result.iloc[::-1].reset_index(drop=True)
    return result


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        ("duplicate", "duplicate-key"),
        ("negative", "non-positive-price"),
        ("bad_ohlc", "ohlc-inconsistent"),
        ("unsorted", "date-order"),
    ],
)
def test_validate_bars_reports_structured_issues(mutation: str, code: str) -> None:
    issues = validate_bars(mutate(good_bars(), mutation))

    assert code in {issue.code for issue in issues}


def test_good_bars_have_no_error_issues() -> None:
    issues = validate_bars(good_bars())

    assert [issue for issue in issues if issue.severity == "error"] == []
