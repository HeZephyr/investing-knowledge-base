"""免费行情提供商适配器；上游列名不会泄漏到其他模块。"""

from __future__ import annotations

from datetime import date, datetime, timezone
from importlib import import_module
from typing import Any, Protocol

import pandas as pd

from investkb.data.models import normalize_bars

AKSHARE_COLUMNS = {
    "日期": "date",
    "开盘": "open",
    "最高": "high",
    "最低": "low",
    "收盘": "close",
    "成交量": "volume",
    "成交额": "amount",
}


class DataUnavailableError(RuntimeError):
    """上游失败、返回空数据或响应不满足契约。"""


class MarketDataProvider(Protocol):
    def daily_bars(
        self, market: str, symbol: str, start: date, end: date, adjustment: str
    ) -> pd.DataFrame: ...


class AKShareProvider:
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or import_module("akshare")

    def daily_bars(
        self, market: str, symbol: str, start: date, end: date, adjustment: str
    ) -> pd.DataFrame:
        if market not in {"CN", "HK"}:
            raise ValueError("AKShare market must be CN or HK")
        if start > end:
            raise ValueError("start must not be after end")
        if adjustment not in {"", "none", "qfq", "hfq"}:
            raise ValueError("adjustment must be none, qfq, or hfq")
        effective_adjustment = "" if adjustment == "none" else adjustment
        cn_fund_prefixes = ("15", "16", "50", "51", "52", "56", "58")
        if market == "CN" and symbol.startswith(cn_fund_prefixes):
            interface = "fund_etf_hist_em"
        else:
            interface = "stock_zh_a_hist" if market == "CN" else "stock_hk_hist"
        function = getattr(self.client, interface, None)
        if function is None:
            raise DataUnavailableError(f"akshare interface missing: {interface}")
        primary_error: Exception | None = None
        try:
            response = function(
                symbol=symbol,
                period="daily",
                start_date=start.strftime("%Y%m%d"),
                end_date=end.strftime("%Y%m%d"),
                adjust=effective_adjustment,
            )
        except Exception as exc:
            primary_error = exc
            response = pd.DataFrame()
        if market == "HK" and response.empty and hasattr(self.client, "stock_hk_daily"):
            try:
                response = self.client.stock_hk_daily(symbol=symbol, adjust=effective_adjustment)
                if isinstance(response, pd.DataFrame) and not response.empty:
                    response = response.copy()
                    response["date"] = pd.to_datetime(response["date"])
                    response = response[
                        (response["date"].dt.date >= start) & (response["date"].dt.date <= end)
                    ]
            except Exception as fallback_error:
                detail = (
                    f"{type(primary_error).__name__}: {primary_error}" if primary_error else "empty"
                )
                raise DataUnavailableError(
                    "akshare HK interfaces failed; "
                    f"stock_hk_hist={detail}; stock_hk_daily={type(fallback_error).__name__}: {fallback_error}"
                ) from fallback_error
        if (
            interface == "fund_etf_hist_em"
            and response.empty
            and effective_adjustment == ""
            and hasattr(self.client, "fund_etf_hist_sina")
        ):
            exchange_symbol = ("sh" if symbol.startswith("5") else "sz") + symbol
            try:
                response = self.client.fund_etf_hist_sina(symbol=exchange_symbol)
                if isinstance(response, pd.DataFrame) and not response.empty:
                    response = response.copy()
                    response["date"] = pd.to_datetime(response["date"])
                    response = response[
                        (response["date"].dt.date >= start) & (response["date"].dt.date <= end)
                    ]
                    primary_error = None
            except Exception as fallback_error:
                detail = (
                    f"{type(primary_error).__name__}: {primary_error}" if primary_error else "empty"
                )
                raise DataUnavailableError(
                    "akshare ETF interfaces failed; "
                    f"fund_etf_hist_em={detail}; fund_etf_hist_sina="
                    f"{type(fallback_error).__name__}: {fallback_error}"
                ) from fallback_error
        if primary_error is not None and response.empty:
            raise DataUnavailableError(
                f"akshare {interface} failed: {type(primary_error).__name__}: {primary_error}"
            ) from primary_error
        if not isinstance(response, pd.DataFrame) or response.empty:
            raise DataUnavailableError(
                f"akshare {interface} returned empty data for {market}/{symbol}"
            )
        if set(AKSHARE_COLUMNS) <= set(response.columns):
            mapped = response.rename(columns=AKSHARE_COLUMNS)
        else:
            mapped = response
        required = {"date", "open", "high", "low", "close", "volume", "amount"}
        missing = sorted(required - set(mapped.columns))
        if missing:
            raise DataUnavailableError(
                f"akshare {interface} columns changed; missing: {', '.join(missing)}"
            )
        return normalize_bars(
            mapped,
            market=market,
            symbol=symbol,
            currency="CNY" if market == "CN" else "HKD",
            provider="akshare",
            adjustment=effective_adjustment,
        )

    def fund_nav(self, symbol: str, start: date, end: date) -> pd.DataFrame:
        """获取场外开放式基金单位净值；净值数据不伪装为 OHLC。"""
        if start > end:
            raise ValueError("start must not be after end")
        function = getattr(self.client, "fund_open_fund_info_em", None)
        if function is None:
            raise DataUnavailableError("akshare interface missing: fund_open_fund_info_em")
        try:
            response = function(symbol=symbol, indicator="单位净值走势", period="成立来")
        except Exception as exc:
            raise DataUnavailableError(
                f"akshare fund_open_fund_info_em failed: {type(exc).__name__}: {exc}"
            ) from exc
        required = {"净值日期", "单位净值", "日增长率"}
        if not isinstance(response, pd.DataFrame) or response.empty:
            raise DataUnavailableError(f"akshare returned empty fund NAV for {symbol}")
        missing = sorted(required - set(response.columns))
        if missing:
            raise DataUnavailableError(f"fund NAV columns changed; missing: {', '.join(missing)}")
        nav = response.rename(
            columns={"净值日期": "date", "单位净值": "unit_nav", "日增长率": "daily_growth_pct"}
        )[["date", "unit_nav", "daily_growth_pct"]].copy()
        nav["date"] = pd.to_datetime(nav["date"])
        nav = nav[(nav["date"].dt.date >= start) & (nav["date"].dt.date <= end)]
        if nav.empty:
            raise DataUnavailableError(f"akshare returned no fund NAV in range for {symbol}")
        nav["unit_nav"] = pd.to_numeric(nav["unit_nav"], errors="raise")
        nav["daily_growth_pct"] = pd.to_numeric(nav["daily_growth_pct"], errors="coerce")
        nav.insert(0, "fund_code", symbol)
        nav["provider"] = "akshare"
        nav["retrieved_at"] = pd.Timestamp(datetime.now(timezone.utc))
        return nav.reset_index(drop=True)


class BaoStockProvider:
    def __init__(self, client: Any | None = None) -> None:
        self.client = client or import_module("baostock")

    @staticmethod
    def _code(symbol: str) -> str:
        exchange = "sh" if symbol.startswith(("5", "6", "9")) else "sz"
        return f"{exchange}.{symbol}"

    def daily_bars(
        self, market: str, symbol: str, start: date, end: date, adjustment: str
    ) -> pd.DataFrame:
        if market != "CN":
            raise ValueError("BaoStock supports CN only")
        if start > end:
            raise ValueError("start must not be after end")
        adjust_flags = {"hfq": "1", "qfq": "2", "": "3"}
        if adjustment not in adjust_flags:
            raise ValueError("adjustment must be '', qfq, or hfq")
        login = self.client.login()
        if login.error_code != "0":
            raise DataUnavailableError(f"baostock login failed: {login.error_msg}")
        try:
            result = self.client.query_history_k_data_plus(
                self._code(symbol),
                "date,open,high,low,close,volume,amount",
                start_date=start.isoformat(),
                end_date=end.isoformat(),
                frequency="d",
                adjustflag=adjust_flags[adjustment],
            )
            if result.error_code != "0":
                raise DataUnavailableError(f"baostock query failed: {result.error_msg}")
            rows: list[list[str]] = []
            while result.next():
                rows.append(result.get_row_data())
        except DataUnavailableError:
            raise
        except Exception as exc:
            raise DataUnavailableError(
                f"baostock query failed: {type(exc).__name__}: {exc}"
            ) from exc
        finally:
            self.client.logout()
        if not rows:
            raise DataUnavailableError(f"baostock returned empty data for CN/{symbol}")
        frame = pd.DataFrame(rows, columns=result.fields)
        return normalize_bars(frame, "CN", symbol, "CNY", "baostock", adjustment)
