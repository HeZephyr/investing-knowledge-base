from datetime import date, datetime, timezone

import pandas as pd
import pytest

from investkb.data.global_provider import (
    ACTION_COLUMNS,
    GlobalInstrument,
    YFinanceProvider,
)
from investkb.data.providers import DataUnavailableError


START = date(2024, 1, 1)
END = date(2024, 1, 31)
STAMP = datetime(2026, 7, 18, 9, 0, tzinfo=timezone.utc)


class FakeTicker:
    @property
    def actions(self) -> pd.DataFrame:
        return pd.DataFrame(
            {"Dividends": [0.24, 0.0], "Stock Splits": [0.0, 4.0]},
            index=pd.to_datetime(["2024-01-05", "2024-01-20"]).tz_localize("America/New_York"),
        )


class FakeYFinance:
    def download(self, ticker, **kwargs):
        assert ticker == "AAPL"
        assert kwargs["auto_adjust"] is False
        assert kwargs["timeout"] == 10
        return pd.DataFrame(
            {
                "Open": [185.0, 187.0],
                "High": [188.0, 190.0],
                "Low": [184.0, 186.0],
                "Close": [187.0, 189.0],
                "Adj Close": [186.5, 188.5],
                "Volume": [1_000, 1_200],
            },
            index=pd.to_datetime(["2024-01-02", "2024-01-03"]),
        )

    def Ticker(self, ticker):
        assert ticker == "AAPL"
        return FakeTicker()


def registry() -> list[GlobalInstrument]:
    return [
        GlobalInstrument("US", "AAPL", "AAPL", "USD", "America/New_York"),
        GlobalInstrument("KR", "005930", "005930.KS", "KRW", "Asia/Seoul"),
    ]


def test_yfinance_adapter_normalizes_unadjusted_bars_and_provenance() -> None:
    bars = YFinanceProvider(FakeYFinance(), registry(), retrieved_at=STAMP).daily_bars(
        "US", "AAPL", START, END, "none"
    )

    assert bars["market"].unique().tolist() == ["US"]
    assert bars["symbol"].unique().tolist() == ["AAPL"]
    assert bars["currency"].unique().tolist() == ["USD"]
    assert bars["close"].tolist() == [187.0, 189.0]
    assert bars["amount"].isna().all()
    assert bars.attrs["provenance"]["provider_symbol"] == "AAPL"
    assert bars.attrs["provenance"]["rows"] == 2
    assert len(bars.attrs["provenance"]["sha256"]) == 64


def test_company_actions_keep_dividends_and_splits_separate() -> None:
    actions = YFinanceProvider(FakeYFinance(), registry(), retrieved_at=STAMP).company_actions(
        "US", "AAPL", START, END
    )

    assert actions.columns.tolist() == ACTION_COLUMNS
    assert actions["action_type"].tolist() == ["cash_dividend", "stock_split"]
    assert actions["value"].tolist() == [0.24, 4.0]
    assert actions.iloc[0]["currency"] == "USD"
    assert pd.isna(actions.iloc[1]["currency"])
    assert len(actions.attrs["provenance"]["sha256"]) == 64


def test_registry_never_guesses_korean_provider_symbol() -> None:
    provider = YFinanceProvider(FakeYFinance(), registry(), retrieved_at=STAMP)

    assert provider.instrument("KR", "005930").provider_symbol == "005930.KS"
    with pytest.raises(ValueError, match="not registered"):
        provider.instrument("KR", "000660")


class BrokenYFinance(FakeYFinance):
    def download(self, ticker, **kwargs):
        return pd.DataFrame(
            {"Open": [10.0], "High": [9.0], "Low": [8.0], "Close": [11.0], "Volume": [1]},
            index=pd.to_datetime(["2024-01-02"]),
        )


@pytest.mark.parametrize("adjustment", ["qfq", "hfq", "mystery"])
def test_global_provider_rejects_ambiguous_adjustment_modes(adjustment: str) -> None:
    with pytest.raises(ValueError, match="adjustment"):
        YFinanceProvider(FakeYFinance(), registry()).daily_bars(
            "US", "AAPL", START, END, adjustment
        )


def test_global_provider_fails_closed_on_invalid_ohlc() -> None:
    with pytest.raises(DataUnavailableError, match="OHLC"):
        YFinanceProvider(BrokenYFinance(), registry()).daily_bars("US", "AAPL", START, END, "none")
