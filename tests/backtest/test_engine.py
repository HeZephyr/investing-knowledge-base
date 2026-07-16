from datetime import datetime, timezone

import pandas as pd
import pytest

from investkb.backtest.engine import run_backtest
from investkb.backtest.models import FeeModel, MarketRules
from investkb.data.models import normalize_bars


def sample_bars() -> pd.DataFrame:
    raw = pd.DataFrame(
        {
            "date": pd.date_range("2024-01-02", periods=5, freq="B"),
            "open": [10.0, 10.0, 10.0, 11.0, 12.0],
            "high": [10.5, 10.5, 10.5, 11.5, 12.5],
            "low": [9.5, 9.5, 9.5, 10.5, 11.5],
            "close": [10.0, 10.0, 10.5, 11.0, 12.0],
            "volume": [10000] * 5,
            "amount": [100000, 100000, 105000, 110000, 120000],
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


def test_close_signal_executes_next_open() -> None:
    bars = sample_bars().iloc[:4].reset_index(drop=True)
    signal = pd.Series([0, 1, 1, 0])

    result = run_backtest(
        bars,
        signal,
        initial_cash=10_000,
        fee=FeeModel(commission_rate=0.001, minimum_commission=0, stamp_duty_rate=0),
        rules=MarketRules(board_lot=100, slippage_bps=0),
    )

    assert result.trades.iloc[0]["date"] == bars.iloc[2]["date"]
    assert result.trades.iloc[0]["price"] == bars.iloc[2]["open"]
    assert result.trades.iloc[0]["side"] == "buy"


def test_sell_cost_includes_market_tax() -> None:
    bars = sample_bars()
    signal = pd.Series([0, 1, 1, 0, 0])

    result = run_backtest(
        bars,
        signal,
        initial_cash=10_000,
        fee=FeeModel(commission_rate=0, minimum_commission=0, stamp_duty_rate=0.001),
        rules=MarketRules(board_lot=100, slippage_bps=0),
    )

    sell = result.trades[result.trades["side"] == "sell"].iloc[0]
    assert sell["fees"] == pytest.approx(sell["gross"] * 0.001)


def test_backtest_rejects_short_signal() -> None:
    signal = pd.Series([0, -1, -1, 0, 0])

    with pytest.raises(ValueError, match="long/cash"):
        run_backtest(sample_bars(), signal, 10_000, FeeModel(), MarketRules())
