"""Timezone-aware market-session contracts and credential-free smoke checks."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from importlib import import_module
import json
from typing import Sequence

import pandas as pd


class CalendarError(ValueError):
    """Raised when a market calendar is ambiguous or internally inconsistent."""


@dataclass(frozen=True)
class MarketSession:
    market: str
    opens_at: datetime
    closes_at: datetime

    def __post_init__(self) -> None:
        if not self.market:
            raise CalendarError("market is required")
        if self.opens_at.tzinfo is None or self.closes_at.tzinfo is None:
            raise CalendarError("session timestamps must be timezone-aware")
        if self.closes_at <= self.opens_at:
            raise CalendarError("closes_at must be after opens_at")

    @property
    def identity(self) -> tuple[str, str]:
        return self.market, self.opens_at.date().isoformat()


def _validated(sessions: Sequence[MarketSession]) -> list[MarketSession]:
    ordered = sorted(sessions, key=lambda item: (item.market, item.opens_at))
    identities = [session.identity for session in ordered]
    if len(identities) != len(set(identities)):
        raise CalendarError("calendar contains a duplicate market session date")
    previous_by_market: dict[str, MarketSession] = {}
    for session in ordered:
        previous = previous_by_market.get(session.market)
        if previous is not None and previous.closes_at > session.opens_at:
            raise CalendarError("calendar contains overlapping sessions")
        previous_by_market[session.market] = session
    return ordered


def normalize_sessions(sessions: Sequence[MarketSession]) -> list[dict[str, str]]:
    """Return deterministic serialisable records after structural validation."""

    return [
        {
            "market": session.market,
            "session_date": session.identity[1],
            "opens_at": session.opens_at.isoformat(),
            "closes_at": session.closes_at.isoformat(),
        }
        for session in _validated(sessions)
    ]


def compare_calendars(
    expected: Sequence[MarketSession], observed: Sequence[MarketSession]
) -> dict[str, object]:
    """Compare two session sets without mutating or auto-correcting either one."""

    expected_map = {session.identity: session for session in _validated(expected)}
    observed_map = {session.identity: session for session in _validated(observed)}
    missing_keys = sorted(expected_map.keys() - observed_map.keys())
    unexpected_keys = sorted(observed_map.keys() - expected_map.keys())
    changed_keys = sorted(
        key
        for key in expected_map.keys() & observed_map.keys()
        if (
            expected_map[key].opens_at != observed_map[key].opens_at
            or expected_map[key].closes_at != observed_map[key].closes_at
        )
    )

    def labels(keys: Sequence[tuple[str, str]]) -> list[str]:
        return [f"{market}:{session_date}" for market, session_date in keys]

    result = {
        "missing": labels(missing_keys),
        "unexpected": labels(unexpected_keys),
        "changed": labels(changed_keys),
    }
    result["matches"] = not any(result.values())
    return result


def smoke_exchange_calendars(markets: Sequence[str]) -> dict[str, int]:
    """Read upcoming sessions from exchange_calendars without credentials or writes."""

    if not markets:
        raise CalendarError("at least one market is required")
    exchange_calendars = import_module("exchange_calendars")
    today = pd.Timestamp.now(tz="UTC").tz_localize(None).normalize()
    start = today - pd.Timedelta(days=7)
    end = today + pd.Timedelta(days=30)
    counts: dict[str, int] = {}
    for market in markets:
        calendar = exchange_calendars.get_calendar(market)
        labels = calendar.sessions_in_range(start, end)
        if len(labels) == 0:
            raise CalendarError(f"calendar returned no sessions: {market}")
        sessions = [
            MarketSession(
                market,
                calendar.session_open(label).to_pydatetime(),
                calendar.session_close(label).to_pydatetime(),
            )
            for label in labels
        ]
        normalize_sessions(sessions)
        counts[market] = len(sessions)
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only market calendar smoke check")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--markets", default="XSHG,XHKG,XNYS,XLON")
    args = parser.parse_args()
    if not args.smoke:
        parser.error("--smoke is required")
    markets = [market.strip() for market in args.markets.split(",") if market.strip()]
    print(json.dumps(smoke_exchange_calendars(markets), sort_keys=True))


if __name__ == "__main__":
    main()
