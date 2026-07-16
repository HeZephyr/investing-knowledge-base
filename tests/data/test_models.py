from datetime import datetime, timezone

import pandas as pd

from investkb.data.models import EXPECTED_BAR_COLUMNS, normalize_bars


def raw_bars() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": ["2024-01-02", "2024-01-03"],
            "open": [10.0, 10.5],
            "high": [10.8, 11.0],
            "low": [9.9, 10.2],
            "close": [10.6, 10.8],
            "volume": [1000, 1200],
            "amount": [10500, 12800],
        }
    )


def test_bar_frame_normalizes_columns_and_types() -> None:
    frame = normalize_bars(
        raw_bars(),
        market="CN",
        symbol="510300",
        currency="CNY",
        provider="fixture",
        adjustment="qfq",
        retrieved_at=datetime(2026, 7, 16, tzinfo=timezone.utc),
    )

    assert list(frame.columns) == EXPECTED_BAR_COLUMNS
    assert str(frame["date"].dtype) == "datetime64[us]"
    assert frame["symbol"].unique().tolist() == ["510300"]


def test_bar_frame_rejects_missing_vendor_column() -> None:
    incomplete = raw_bars().drop(columns="amount")

    try:
        normalize_bars(incomplete, "CN", "510300", "CNY", "fixture", "qfq")
    except ValueError as exc:
        assert "amount" in str(exc)
    else:
        raise AssertionError("normalize_bars accepted a missing amount column")
