"""按市场、证券和年份保存 Parquet，并生成复现清单。"""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd

from investkb.data.models import EXPECTED_BAR_COLUMNS


@dataclass(frozen=True)
class DataManifest:
    market: str
    symbol: str
    rows: int
    start: str
    end: str
    provider: str
    adjustment: str
    sha256: str
    request: dict[str, Any]


class ParquetStore:
    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)

    def _directory(self, market: str, symbol: str) -> Path:
        return self.root / market / symbol

    def write_bars(self, bars: pd.DataFrame, request: dict[str, Any] | None = None) -> DataManifest:
        if bars.empty:
            raise ValueError("cannot store empty bars")
        if list(bars.columns) != EXPECTED_BAR_COLUMNS:
            raise ValueError("bars do not match EXPECTED_BAR_COLUMNS")
        market_values = bars["market"].unique()
        symbol_values = bars["symbol"].unique()
        if len(market_values) != 1 or len(symbol_values) != 1:
            raise ValueError("one write must contain exactly one market and symbol")

        market, symbol = str(market_values[0]), str(symbol_values[0])
        directory = self._directory(market, symbol)
        directory.mkdir(parents=True, exist_ok=True)
        for year, partition in bars.groupby(bars["date"].dt.year, sort=True):
            destination = directory / f"{year}.parquet"
            if destination.exists():
                existing = pd.read_parquet(destination)
                if set(existing["adjustment"]) != set(partition["adjustment"]):
                    raise ValueError("cannot mix adjustment modes in one symbol store")
                partition = (
                    pd.concat([existing, partition], ignore_index=True)
                    .drop_duplicates(["market", "symbol", "date"], keep="last")
                    .sort_values("date")
                    .reset_index(drop=True)
                )
            with tempfile.NamedTemporaryFile(
                dir=directory, suffix=".parquet", delete=False
            ) as handle:
                temporary = Path(handle.name)
            try:
                partition.reset_index(drop=True).to_parquet(temporary, index=False)
                os.replace(temporary, destination)
            finally:
                temporary.unlink(missing_ok=True)

        files = sorted(directory.glob("*.parquet"))
        digest = hashlib.sha256()
        for path in files:
            digest.update(path.name.encode("utf-8"))
            digest.update(path.read_bytes())
        stored = pd.concat([pd.read_parquet(path) for path in files], ignore_index=True)

        manifest = DataManifest(
            market=market,
            symbol=symbol,
            rows=len(stored),
            start=stored["date"].min().date().isoformat(),
            end=stored["date"].max().date().isoformat(),
            provider=",".join(sorted(set(stored["provider"].astype(str)))),
            adjustment=str(stored["adjustment"].iloc[0]),
            sha256=digest.hexdigest(),
            request=request or {},
        )
        manifest_path = directory / "manifest.json"
        with tempfile.NamedTemporaryFile(
            dir=directory, mode="w", encoding="utf-8", delete=False
        ) as handle:
            json.dump(asdict(manifest), handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
            temporary_manifest = Path(handle.name)
        os.replace(temporary_manifest, manifest_path)
        return manifest

    def read_bars(self, market: str, symbol: str) -> pd.DataFrame:
        files = sorted(self._directory(market, symbol).glob("*.parquet"))
        if not files:
            raise FileNotFoundError(f"no stored bars for {market}/{symbol}")
        return pd.concat([pd.read_parquet(path) for path in files], ignore_index=True)[
            EXPECTED_BAR_COLUMNS
        ]
