from __future__ import annotations

from datetime import datetime, timezone

import pytest
import pandas as pd

import investkb.market_calendar as market_calendar
from investkb.market_calendar import (
    CalendarError,
    MarketSession,
    compare_calendars,
    normalize_sessions,
    smoke_exchange_calendars,
)


def _utc(day: int, hour: int) -> datetime:
    return datetime(2026, 7, day, hour, tzinfo=timezone.utc)


def test_normalize_sessions_orders_markets_and_preserves_timezone() -> None:
    sessions = [
        MarketSession("XNYS", _utc(20, 13), _utc(20, 20)),
        MarketSession("XHKG", _utc(20, 1), _utc(20, 8)),
    ]
    assert normalize_sessions(sessions) == [
        {
            "market": "XHKG",
            "session_date": "2026-07-20",
            "opens_at": "2026-07-20T01:00:00+00:00",
            "closes_at": "2026-07-20T08:00:00+00:00",
        },
        {
            "market": "XNYS",
            "session_date": "2026-07-20",
            "opens_at": "2026-07-20T13:00:00+00:00",
            "closes_at": "2026-07-20T20:00:00+00:00",
        },
    ]


def test_market_session_rejects_naive_reversed_duplicate_and_overlap() -> None:
    with pytest.raises(CalendarError, match="timezone-aware"):
        MarketSession("XNYS", datetime(2026, 7, 20, 13), datetime(2026, 7, 20, 20))
    with pytest.raises(CalendarError, match="after"):
        MarketSession("XNYS", _utc(20, 20), _utc(20, 13))
    same = MarketSession("XNYS", _utc(20, 13), _utc(20, 20))
    with pytest.raises(CalendarError, match="duplicate"):
        normalize_sessions([same, same])
    with pytest.raises(CalendarError, match="overlap"):
        normalize_sessions(
            [
                MarketSession("XNYS", _utc(20, 13), _utc(21, 2)),
                MarketSession("XNYS", _utc(21, 1), _utc(21, 8)),
            ]
        )


def test_compare_calendars_reports_missing_unexpected_and_changed_sessions() -> None:
    expected = [
        MarketSession("XHKG", _utc(20, 1), _utc(20, 8)),
        MarketSession("XNYS", _utc(20, 13), _utc(20, 20)),
        MarketSession("XNYS", _utc(21, 13), _utc(21, 20)),
    ]
    observed = [
        MarketSession("XHKG", _utc(20, 1), _utc(20, 9)),
        MarketSession("XNYS", _utc(21, 13), _utc(21, 20)),
        MarketSession("XLON", _utc(22, 7), _utc(22, 15)),
    ]
    assert compare_calendars(expected, observed) == {
        "missing": ["XNYS:2026-07-20"],
        "unexpected": ["XLON:2026-07-22"],
        "changed": ["XHKG:2026-07-20"],
        "matches": False,
    }


def test_compare_calendars_is_clean_for_equivalent_inputs() -> None:
    sessions = [MarketSession("XNYS", _utc(20, 13), _utc(20, 20))]
    assert compare_calendars(sessions, list(reversed(sessions))) == {
        "missing": [],
        "unexpected": [],
        "changed": [],
        "matches": True,
    }


def test_exchange_calendar_adapter_uses_naive_labels_and_aware_session_times(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeCalendar:
        def sessions_in_range(self, start: pd.Timestamp, end: pd.Timestamp):
            assert start.tz is None
            assert end.tz is None
            return [pd.Timestamp("2026-07-20")]

        def session_open(self, label: pd.Timestamp) -> pd.Timestamp:
            return pd.Timestamp(f"{label.date()} 13:30", tz="UTC")

        def session_close(self, label: pd.Timestamp) -> pd.Timestamp:
            return pd.Timestamp(f"{label.date()} 20:00", tz="UTC")

    class FakeExchangeCalendars:
        @staticmethod
        def get_calendar(market: str) -> FakeCalendar:
            assert market == "XNYS"
            return FakeCalendar()

    monkeypatch.setattr(market_calendar, "import_module", lambda _: FakeExchangeCalendars())
    assert smoke_exchange_calendars(["XNYS"]) == {"XNYS": 1}
