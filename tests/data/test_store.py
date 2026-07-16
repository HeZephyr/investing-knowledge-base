from datetime import datetime, timezone

import pandas as pd

from investkb.data.models import normalize_bars
from investkb.data.store import ParquetStore
from tests.data.test_models import raw_bars


def test_parquet_round_trip_and_manifest(tmp_path) -> None:
    bars = normalize_bars(
        raw_bars(),
        "CN",
        "510300",
        "CNY",
        "fixture",
        "qfq",
        retrieved_at=datetime(2026, 7, 16, tzinfo=timezone.utc),
    )
    store = ParquetStore(tmp_path)

    manifest = store.write_bars(bars, request={"start": "2024-01-01"})
    restored = store.read_bars("CN", "510300")

    assert restored.equals(bars)
    assert len(manifest.sha256) == 64
    assert manifest.rows == 2
    assert manifest.request == {"start": "2024-01-01"}


def test_incremental_write_preserves_existing_dates_and_manifest_describes_full_store(
    tmp_path,
) -> None:
    first = normalize_bars(
        raw_bars().iloc[[0]],
        "CN",
        "510300",
        "CNY",
        "fixture",
        "qfq",
        retrieved_at=datetime(2026, 7, 15, tzinfo=timezone.utc),
    )
    second_raw = pd.DataFrame(
        {
            "date": ["2024-01-03"],
            "open": [10.5],
            "high": [11.0],
            "low": [10.2],
            "close": [10.8],
            "volume": [1200],
            "amount": [12800],
        }
    )
    second = normalize_bars(
        second_raw,
        "CN",
        "510300",
        "CNY",
        "fixture",
        "qfq",
        retrieved_at=datetime(2026, 7, 16, tzinfo=timezone.utc),
    )
    store = ParquetStore(tmp_path)
    store.write_bars(first)

    manifest = store.write_bars(second)

    assert store.read_bars("CN", "510300")["date"].dt.strftime("%Y-%m-%d").tolist() == [
        "2024-01-02",
        "2024-01-03",
    ]
    assert manifest.rows == 2
    assert manifest.start == "2024-01-02"
