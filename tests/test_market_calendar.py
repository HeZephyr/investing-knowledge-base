from __future__ import annotations

from datetime import datetime, timezone

import pytest

from investkb.market_calendar import (
    CalendarError,
    MarketSession,
    compare_calendars,
    normalize_sessions,
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
            [same, MarketSession("XNYS", _utc(20, 19), _utc(21, 1))]
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
