"""Explicit, offline-testable adapter for free global daily data."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import hashlib
from importlib import import_module
import math
from typing import Any, Iterable

import pandas as pd

from investkb.data.models import normalize_bars
from investkb.data.providers import DataUnavailableError

ACTION_COLUMNS = [
    "market",
    "symbol",
    "ex_date",
    "action_type",
    "value",
    "currency",
    "provider",
    "retrieved_at",
]


@dataclass(frozen=True)
class GlobalInstrument:
    """Explicit mapping from a canonical instrument to one provider symbol."""

    market: str
    symbol: str
    provider_symbol: str
    currency: str
    exchange_timezone: str

    def __post_init__(self) -> None:
        values = (
            self.market,
            self.symbol,
            self.provider_symbol,
            self.currency,
            self.exchange_timezone,
        )
        if not all(isinstance(value, str) and value.strip() for value in values):
            raise ValueError("global instrument fields must be non-empty strings")


def _digest(frame: pd.DataFrame) -> str:
    normalized = frame.copy()
    for column in normalized.columns:
        if pd.api.types.is_datetime64_any_dtype(normalized[column]):
            normalized[column] = normalized[column].astype(str)
    payload = normalized.to_json(orient="records", date_format="iso", double_precision=15)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class YFinanceProvider:
    """Normalize yfinance convenience data without treating it as an official source."""

    def __init__(
        self,
        client: Any | None,
        instruments: Iterable[GlobalInstrument],
        *,
        retrieved_at: datetime | None = None,
        timeout: int = 10,
    ) -> None:
        self.client = client or import_module("yfinance")
        instrument_list = list(instruments)
        self.instruments = {(item.market, item.symbol): item for item in instrument_list}
        if len(self.instruments) != len(instrument_list):
            raise ValueError("duplicate global instrument mapping")
        self.retrieved_at = retrieved_at or datetime.now(timezone.utc)
        if self.retrieved_at.tzinfo is None:
            raise ValueError("retrieved_at must include a timezone")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.timeout = timeout

    def instrument(self, market: str, symbol: str) -> GlobalInstrument:
        try:
            return self.instruments[(market, symbol)]
        except KeyError as exc:
            raise ValueError(f"instrument not registered: {market}/{symbol}") from exc

    @staticmethod
    def _dates(index: pd.Index, instrument: GlobalInstrument) -> pd.Series:
        if not isinstance(index, pd.DatetimeIndex):
            try:
                index = pd.DatetimeIndex(pd.to_datetime(index, errors="raise"))
            except Exception as exc:
                raise DataUnavailableError("provider dates are not parseable") from exc
        if index.tz is not None:
            index = index.tz_convert(instrument.exchange_timezone).tz_localize(None)
        return pd.Series(index.normalize(), index=range(len(index)))

    @staticmethod
    def _validate_prices(frame: pd.DataFrame) -> None:
        prices = frame[["open", "high", "low", "close"]]
        if prices.isna().any().any() or (prices <= 0).any().any():
            raise DataUnavailableError("provider OHLC contains missing or non-positive values")
        invalid = (frame["high"] < prices[["open", "close", "low"]].max(axis=1)) | (
            frame["low"] > prices[["open", "close", "high"]].min(axis=1)
        )
        if invalid.any():
            raise DataUnavailableError("provider OHLC relationships are invalid")
        if frame["volume"].isna().any() or (frame["volume"] < 0).any():
            raise DataUnavailableError("provider volume contains missing or negative values")
        if frame["date"].duplicated().any():
            raise DataUnavailableError("provider returned duplicate trading dates")

    def daily_bars(
        self, market: str, symbol: str, start: date, end: date, adjustment: str
    ) -> pd.DataFrame:
        if start > end:
            raise ValueError("start must not be after end")
        if adjustment not in {"none", "adjusted"}:
            raise ValueError("adjustment must be none or adjusted")
        instrument = self.instrument(market, symbol)
        request = {
            "provider_symbol": instrument.provider_symbol,
            "start": start.isoformat(),
            "end_inclusive": end.isoformat(),
            "adjustment": adjustment,
        }
        try:
            response = self.client.download(
                instrument.provider_symbol,
                start=start.isoformat(),
                end=(end + timedelta(days=1)).isoformat(),
                auto_adjust=adjustment == "adjusted",
                actions=False,
                progress=False,
                timeout=self.timeout,
                multi_level_index=False,
            )
        except Exception as exc:
            raise DataUnavailableError(
                f"yfinance download failed: {type(exc).__name__}: {exc}"
            ) from exc
        if not isinstance(response, pd.DataFrame) or response.empty:
            raise DataUnavailableError(f"yfinance returned empty data for {market}/{symbol}")
        if isinstance(response.columns, pd.MultiIndex):
            raise DataUnavailableError("yfinance returned ambiguous multi-level columns")
        required = {"Open", "High", "Low", "Close", "Volume"}
        missing = sorted(required - set(response.columns))
        if missing:
            raise DataUnavailableError(f"yfinance columns changed; missing: {', '.join(missing)}")
        mapped = pd.DataFrame(
            {
                "date": self._dates(response.index, instrument),
                "open": pd.to_numeric(response["Open"], errors="raise").to_numpy(),
                "high": pd.to_numeric(response["High"], errors="raise").to_numpy(),
                "low": pd.to_numeric(response["Low"], errors="raise").to_numpy(),
                "close": pd.to_numeric(response["Close"], errors="raise").to_numpy(),
                "volume": pd.to_numeric(response["Volume"], errors="raise").to_numpy(),
                "amount": float("nan"),
            }
        )
        mapped = mapped[(mapped["date"].dt.date >= start) & (mapped["date"].dt.date <= end)]
        if mapped.empty:
            raise DataUnavailableError(f"yfinance returned no rows in range for {market}/{symbol}")
        self._validate_prices(mapped)
        bars = normalize_bars(
            mapped,
            market,
            symbol,
            instrument.currency,
            "yfinance",
            adjustment,
            retrieved_at=self.retrieved_at,
        )
        bars.attrs["provenance"] = {
            "provider": "yfinance",
            "endpoint": "download",
            **request,
            "retrieved_at": self.retrieved_at.astimezone(timezone.utc).isoformat(),
            "rows": len(bars),
            "sha256": _digest(bars),
        }
        return bars

    def company_actions(self, market: str, symbol: str, start: date, end: date) -> pd.DataFrame:
        if start > end:
            raise ValueError("start must not be after end")
        instrument = self.instrument(market, symbol)
        try:
            response = self.client.Ticker(instrument.provider_symbol).actions
        except Exception as exc:
            raise DataUnavailableError(
                f"yfinance actions failed: {type(exc).__name__}: {exc}"
            ) from exc
        if not isinstance(response, pd.DataFrame):
            raise DataUnavailableError("yfinance actions response is not a table")
        missing = sorted({"Dividends", "Stock Splits"} - set(response.columns))
        if missing:
            raise DataUnavailableError(
                f"yfinance action columns changed; missing: {', '.join(missing)}"
            )
        rows: list[dict[str, Any]] = []
        dates = (
            self._dates(response.index, instrument)
            if not response.empty
            else pd.Series(dtype="datetime64[ns]")
        )
        for offset, (_, source) in enumerate(response.iterrows()):
            ex_date = dates.iloc[offset]
            if not start <= ex_date.date() <= end:
                continue
            try:
                dividend = float(source["Dividends"])
                split = float(source["Stock Splits"])
            except (TypeError, ValueError) as exc:
                raise DataUnavailableError(
                    "yfinance action values must be numeric, finite, and non-negative"
                ) from exc
            if not all(math.isfinite(value) and value >= 0 for value in (dividend, split)):
                raise DataUnavailableError(
                    "yfinance action values must be numeric, finite, and non-negative"
                )
            if dividend:
                rows.append(
                    {
                        "market": market,
                        "symbol": symbol,
                        "ex_date": ex_date,
                        "action_type": "cash_dividend",
                        "value": dividend,
                        "currency": instrument.currency,
                        "provider": "yfinance",
                        "retrieved_at": pd.Timestamp(self.retrieved_at).tz_convert("UTC"),
                    }
                )
            if split:
                rows.append(
                    {
                        "market": market,
                        "symbol": symbol,
                        "ex_date": ex_date,
                        "action_type": "stock_split",
                        "value": split,
                        "currency": None,
                        "provider": "yfinance",
                        "retrieved_at": pd.Timestamp(self.retrieved_at).tz_convert("UTC"),
                    }
                )
        actions = pd.DataFrame(rows, columns=ACTION_COLUMNS).sort_values(
            ["ex_date", "action_type"], ignore_index=True
        )
        actions.attrs["provenance"] = {
            "provider": "yfinance",
            "endpoint": "Ticker.actions",
            "provider_symbol": instrument.provider_symbol,
            "start": start.isoformat(),
            "end_inclusive": end.isoformat(),
            "retrieved_at": self.retrieved_at.astimezone(timezone.utc).isoformat(),
            "rows": len(actions),
            "sha256": _digest(actions),
        }
        return actions
