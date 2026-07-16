from datetime import date

import pandas as pd
import pytest

from investkb.data.providers import AKShareProvider, BaoStockProvider, DataUnavailableError

START = date(2024, 1, 1)
END = date(2024, 1, 31)


class FakeAKShare:
    def stock_zh_a_hist(self, **kwargs):
        assert kwargs["symbol"] == "600000"
        return pd.DataFrame(
            {
                "日期": ["2024-01-02"],
                "开盘": [3.5],
                "最高": [3.6],
                "最低": [3.4],
                "收盘": [3.55],
                "成交量": [100],
                "成交额": [35500],
            }
        )

    def fund_etf_hist_em(self, **kwargs):
        assert kwargs["symbol"] == "510300"
        return pd.DataFrame(
            {
                "日期": ["2024-01-02"],
                "开盘": [3.5],
                "最高": [3.6],
                "最低": [3.4],
                "收盘": [3.55],
                "成交量": [100],
                "成交额": [35500],
            }
        )

    def fund_open_fund_info_em(self, **kwargs):
        assert kwargs["symbol"] == "000001"
        return pd.DataFrame(
            {
                "净值日期": ["2023-12-29", "2024-01-02", "2024-02-01"],
                "单位净值": [1.0, 1.01, 1.02],
                "日增长率": [0.0, 1.0, 0.99],
            }
        )


class EmptyAKShare:
    def stock_hk_hist(self, **kwargs):
        return pd.DataFrame()


class FallbackAKShare:
    def stock_hk_hist(self, **kwargs):
        raise ConnectionError("primary endpoint unavailable")

    def stock_hk_daily(self, **kwargs):
        return pd.DataFrame(
            {
                "date": ["2023-12-29", "2024-01-02", "2024-02-01"],
                "open": [290.0, 292.0, 300.0],
                "high": [295.0, 296.0, 305.0],
                "low": [288.0, 290.0, 298.0],
                "close": [294.0, 295.0, 303.0],
                "volume": [100, 120, 130],
                "amount": [29_400, 35_400, 39_390],
            }
        )


class ETFFallbackAKShare:
    def fund_etf_hist_em(self, **kwargs):
        raise ConnectionError("primary ETF endpoint unavailable")

    def fund_etf_hist_sina(self, **kwargs):
        assert kwargs["symbol"] == "sh510300"
        return pd.DataFrame(
            {
                "date": ["2023-12-29", "2024-01-02", "2024-02-01"],
                "open": [3.4, 3.5, 3.6],
                "high": [3.5, 3.6, 3.7],
                "low": [3.3, 3.4, 3.5],
                "close": [3.45, 3.55, 3.65],
                "volume": [100, 120, 130],
                "amount": [345, 426, 474],
            }
        )


def test_akshare_cn_adapter_maps_vendor_columns() -> None:
    bars = AKShareProvider(client=FakeAKShare()).daily_bars("CN", "600000", START, END, "qfq")

    assert bars.iloc[0]["provider"] == "akshare"
    assert bars.iloc[0]["symbol"] == "600000"
    assert bars.iloc[0]["currency"] == "CNY"


def test_akshare_cn_etf_routes_to_fund_interface() -> None:
    bars = AKShareProvider(client=FakeAKShare()).daily_bars("CN", "510300", START, END, "qfq")

    assert bars.iloc[0]["symbol"] == "510300"
    assert bars.iloc[0]["close"] == 3.55


def test_cn_etf_falls_back_to_sina_interface_and_filters_dates() -> None:
    bars = AKShareProvider(client=ETFFallbackAKShare()).daily_bars(
        "CN", "510300", START, END, "none"
    )

    assert bars["date"].dt.date.tolist() == [date(2024, 1, 2)]
    assert bars.iloc[0]["adjustment"] == ""


def test_open_end_fund_nav_has_separate_nav_contract() -> None:
    nav = AKShareProvider(client=FakeAKShare()).fund_nav("000001", START, END)

    assert nav.columns.tolist() == [
        "fund_code",
        "date",
        "unit_nav",
        "daily_growth_pct",
        "provider",
        "retrieved_at",
    ]
    assert nav["date"].dt.date.tolist() == [date(2024, 1, 2)]


def test_provider_rejects_empty_response() -> None:
    with pytest.raises(DataUnavailableError, match="empty"):
        AKShareProvider(client=EmptyAKShare()).daily_bars("HK", "00700", START, END, "qfq")


def test_hk_provider_falls_back_to_daily_interface_and_filters_dates() -> None:
    bars = AKShareProvider(client=FallbackAKShare()).daily_bars("HK", "00700", START, END, "qfq")

    assert bars["date"].dt.date.tolist() == [date(2024, 1, 2)]


class FakeResult:
    error_code = "0"
    error_msg = "success"
    fields = ["date", "open", "high", "low", "close", "volume", "amount"]

    def __init__(self):
        self.rows = [["2024-01-02", "10", "11", "9", "10.5", "100", "1050"]]

    def next(self):
        return bool(self.rows)

    def get_row_data(self):
        return self.rows.pop(0)


class FakeBaoStock:
    def login(self):
        return type("Login", (), {"error_code": "0", "error_msg": "success"})()

    def logout(self):
        return None

    def query_history_k_data_plus(self, code, fields, **kwargs):
        assert code == "sh.600000"
        return FakeResult()


def test_baostock_maps_a_share_response() -> None:
    bars = BaoStockProvider(client=FakeBaoStock()).daily_bars("CN", "600000", START, END, "qfq")

    assert bars.iloc[0]["provider"] == "baostock"
    assert bars.iloc[0]["close"] == 10.5


def test_baostock_rejects_reversed_date_range() -> None:
    with pytest.raises(ValueError, match="start"):
        BaoStockProvider(client=FakeBaoStock()).daily_bars("CN", "600000", END, START, "qfq")
