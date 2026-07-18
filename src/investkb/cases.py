"""Validate small, immutable public-data snapshots used by research cases."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlparse

import pandas as pd
import yaml


REQUIRED_COLUMNS = (
    "series",
    "period",
    "value",
    "unit",
    "available_at",
    "source_url",
    "provider",
)


class CaseSnapshotError(ValueError):
    """A frozen case snapshot cannot be trusted or reproduced."""


@dataclass(frozen=True)
class CaseSnapshot:
    case_id: str
    rows: int
    sha256: str
    providers: tuple[str, ...]
    available_at_max: datetime
    decision_at: datetime
    observations: pd.DataFrame


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CaseSnapshotError(f"{label} must be a mapping")
    return value


def _text(mapping: dict[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise CaseSnapshotError(f"manifest field {key} must be non-empty text")
    return value.strip()


def _string_list(mapping: dict[str, Any], key: str) -> tuple[str, ...]:
    value = mapping.get(key)
    if not isinstance(value, list) or not value:
        raise CaseSnapshotError(f"manifest field {key} must be a non-empty list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise CaseSnapshotError(f"manifest field {key} contains an invalid value")
    return tuple(item.strip() for item in value)


def _decision_timestamp(value: str | date | datetime) -> datetime:
    if isinstance(value, str):
        try:
            parsed_date = date.fromisoformat(value)
        except ValueError as exc:
            raise CaseSnapshotError("decision_date must be ISO YYYY-MM-DD") from exc
        return datetime.combine(parsed_date, time.max, tzinfo=timezone.utc)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            raise CaseSnapshotError("decision datetime must include a timezone")
        return value.astimezone(timezone.utc)
    if isinstance(value, date):
        return datetime.combine(value, time.max, tzinfo=timezone.utc)
    raise CaseSnapshotError("decision_date has an unsupported type")


def _safe_snapshot_path(manifest_path: Path, relative: str) -> Path:
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or pure.suffix.lower() != ".csv":
        raise CaseSnapshotError("snapshot must be a relative CSV path without traversal")
    return manifest_path.parent / Path(*pure.parts)


def load_case_snapshot(
    manifest_path: str | Path, *, decision_date: str | date | datetime
) -> CaseSnapshot:
    """Load and validate one offline case snapshot without network access."""

    path = Path(manifest_path)
    try:
        payload = _mapping(yaml.safe_load(path.read_text(encoding="utf-8")), "manifest")
    except (OSError, yaml.YAMLError) as exc:
        raise CaseSnapshotError(f"cannot read manifest: {exc}") from exc

    case_id = _text(payload, "case_id")
    snapshot_path = _safe_snapshot_path(path, _text(payload, "snapshot"))
    expected_sha = _text(payload, "snapshot_sha256").lower()
    if len(expected_sha) != 64 or any(char not in "0123456789abcdef" for char in expected_sha):
        raise CaseSnapshotError("snapshot_sha256 must be a 64-character SHA-256")

    try:
        raw = snapshot_path.read_bytes()
    except OSError as exc:
        raise CaseSnapshotError(f"cannot read snapshot: {exc}") from exc
    actual_sha = hashlib.sha256(raw).hexdigest()
    if actual_sha != expected_sha:
        raise CaseSnapshotError(
            f"SHA-256 mismatch for {snapshot_path.name}: expected {expected_sha}, got {actual_sha}"
        )

    try:
        frame = pd.read_csv(snapshot_path, dtype={"series": "string", "period": "string"})
    except Exception as exc:
        raise CaseSnapshotError(f"cannot parse snapshot CSV: {exc}") from exc
    if frame.empty:
        raise CaseSnapshotError("snapshot has no observations")
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in frame.columns]
    if missing_columns:
        raise CaseSnapshotError(f"missing required columns: {', '.join(missing_columns)}")
    if frame[list(REQUIRED_COLUMNS)].isna().any().any():
        raise CaseSnapshotError("missing required observation value")

    primary_key = _string_list(payload, "primary_key")
    unknown_key_columns = [column for column in primary_key if column not in frame.columns]
    if unknown_key_columns:
        raise CaseSnapshotError(f"primary key references unknown columns: {unknown_key_columns}")
    if frame.duplicated(list(primary_key), keep=False).any():
        raise CaseSnapshotError("duplicate primary key in snapshot")

    allowed_units = set(_string_list(payload, "allowed_units"))
    actual_units = set(frame["unit"].astype(str))
    unknown_units = sorted(actual_units - allowed_units)
    if unknown_units:
        raise CaseSnapshotError(f"unknown unit in snapshot: {', '.join(unknown_units)}")

    values = pd.to_numeric(frame["value"], errors="coerce")
    if values.isna().any() or any(not math.isfinite(float(value)) for value in values):
        raise CaseSnapshotError("missing or non-finite numeric value")
    frame = frame.copy()
    frame["value"] = values.astype(float)

    available = pd.to_datetime(frame["available_at"], utc=True, errors="coerce")
    if available.isna().any():
        raise CaseSnapshotError("available_at must be an ISO timestamp with timezone")
    decision_at = _decision_timestamp(decision_date)
    available_max = available.max().to_pydatetime()
    if available_max > decision_at:
        raise CaseSnapshotError("observation available_at is after decision date")
    frame["available_at"] = available

    invalid_urls = [
        value
        for value in frame["source_url"].astype(str)
        if urlparse(value).scheme != "https" or not urlparse(value).netloc
    ]
    if invalid_urls:
        raise CaseSnapshotError("source_url must use an absolute HTTPS URL")
    providers = tuple(sorted(set(frame["provider"].astype(str))))
    if not providers or any(not provider.strip() for provider in providers):
        raise CaseSnapshotError("provider must be non-empty")

    return CaseSnapshot(
        case_id=case_id,
        rows=len(frame),
        sha256=actual_sha,
        providers=providers,
        available_at_max=available_max,
        decision_at=decision_at,
        observations=frame,
    )


def _series(snapshot: CaseSnapshot, name: str) -> dict[str, float]:
    selected = snapshot.observations.loc[
        snapshot.observations["series"].astype(str) == name, ["period", "value"]
    ]
    if selected.empty:
        raise CaseSnapshotError(f"required series is missing: {name}")
    return {str(row.period): float(row.value) for row in selected.itertuples(index=False)}


def _growth(current: float, previous: float) -> float:
    if previous == 0:
        raise CaseSnapshotError("growth denominator cannot be zero")
    return (current / previous - 1.0) * 100.0


def _same_direction(left: float, right: float) -> bool:
    return (left > 0 and right > 0) or (left < 0 and right < 0) or (left == right == 0)


def _energy_metrics(snapshot: CaseSnapshot) -> dict[str, Any]:
    wti = _series(snapshot, "wti_annual_average")
    cash = _series(snapshot, "xom_operating_cash_flow")
    gaps: dict[str, float] = {}
    matches = 0
    for year, previous in (("2023", "2022"), ("2024", "2023")):
        wti_growth = _growth(wti[year], wti[previous])
        cash_growth = _growth(cash[year], cash[previous])
        gaps[year] = round(abs(wti_growth - cash_growth), 2)
        matches += int(_same_direction(wti_growth, cash_growth))
    return {
        "case_id": "energy",
        "direction_matches": matches,
        "growth_gap_percentage_points": gaps,
        "hypothesis_supported": matches == 2 and all(gap <= 5 for gap in gaps.values()),
    }


def _bank_metrics(snapshot: CaseSnapshot) -> dict[str, Any]:
    assets = _series(snapshot, "svb_assets")
    deposits = _series(snapshot, "svb_deposits")
    equity = _series(snapshot, "svb_equity")
    failure = _series(snapshot, "svb_failure")
    start_ratio = equity["2021-Q4"] / assets["2021-Q4"] * 100
    end_ratio = equity["2022-Q4"] / assets["2022-Q4"] * 100
    deposit_change = _growth(deposits["2022-Q4"], deposits["2021-Q4"])
    failed = failure["2023-03-10"] == 1
    return {
        "case_id": "bank",
        "equity_to_assets_2021_q4_pct": round(start_ratio, 2),
        "equity_to_assets_2022_q4_pct": round(end_ratio, 2),
        "deposit_change_pct": round(deposit_change, 2),
        "failed": failed,
        "hypothesis_supported": not (end_ratio >= start_ratio and deposit_change < 0 and failed),
    }


def _consumer_metrics(snapshot: CaseSnapshot) -> dict[str, Any]:
    macro = _series(snapshot, "us_retail_monthly_average")
    target = _series(snapshot, "target_revenue")
    walmart = _series(snapshot, "walmart_revenue")
    target_mismatches = 0
    walmart_matches = 0
    for year, previous, walmart_year, walmart_previous in (
        ("2023", "2022", "FY2024", "FY2023"),
        ("2024", "2023", "FY2025", "FY2024"),
    ):
        macro_growth = _growth(macro[year], macro[previous])
        target_growth = _growth(target[year], target[previous])
        walmart_growth = _growth(walmart[walmart_year], walmart[walmart_previous])
        target_mismatches += int(not _same_direction(macro_growth, target_growth))
        walmart_matches += int(_same_direction(macro_growth, walmart_growth))
    return {
        "case_id": "consumer",
        "target_direction_mismatches": target_mismatches,
        "walmart_direction_matches": walmart_matches,
        "hypothesis_supported": target_mismatches == 0,
    }


def _healthcare_metrics(snapshot: CaseSnapshot) -> dict[str, Any]:
    approval = _series(snapshot, "fda_accelerated_approval")["2021-06-07"] == 1
    restricted = _series(snapshot, "cms_restricted_coverage")["2022-04-07"] == 1
    writeoff = _series(snapshot, "biogen_aduhelm_inventory_writeoff")["2022"]
    return {
        "case_id": "healthcare",
        "accelerated_approval": approval,
        "coverage_restricted": restricted,
        "inventory_writeoff_usd_millions": writeoff,
        "hypothesis_supported": approval and not restricted and writeoff == 0,
    }


def _internet_metrics(snapshot: CaseSnapshot) -> dict[str, Any]:
    dap = _series(snapshot, "meta_family_dap")
    revenue = _series(snapshot, "meta_revenue")
    dap_growth = _growth(dap["2024"], dap["2023"])
    revenue_growth = _growth(revenue["2024"], revenue["2023"])
    impressions_growth = _series(snapshot, "meta_ad_impressions_growth")["2024"]
    price_growth = _series(snapshot, "meta_average_price_per_ad_growth")["2024"]
    gap = abs(revenue_growth - dap_growth)
    return {
        "case_id": "internet",
        "dap_growth_pct": round(dap_growth, 2),
        "revenue_growth_pct": round(revenue_growth, 2),
        "growth_gap_percentage_points": round(gap, 2),
        "ad_impressions_growth_pct": impressions_growth,
        "average_price_per_ad_growth_pct": price_growth,
        "hypothesis_supported": gap <= 5 and impressions_growth == 0 and price_growth == 0,
    }


def _memory_metrics(snapshot: CaseSnapshot) -> dict[str, Any]:
    revenue = _series(snapshot, "micron_revenue")
    margin = _series(snapshot, "micron_gross_margin_pct")
    inventory = _series(snapshot, "micron_inventory")
    capex = _series(snapshot, "micron_capex_net")
    write_down = _series(snapshot, "micron_inventory_write_down")
    revenue_growth = _growth(revenue["FY2024"], revenue["FY2023"])
    inventory_change = _growth(inventory["FY2024"], inventory["FY2023"])
    margin_change = margin["FY2024"] - margin["FY2023"]
    recovered = revenue_growth > 20 and margin_change > 10
    return {
        "case_id": "memory",
        "revenue_growth_pct": round(revenue_growth, 2),
        "inventory_change_pct": round(inventory_change, 2),
        "gross_margin_change_pp": round(margin_change, 2),
        "capex_change_pct": round(_growth(capex["FY2024"], capex["FY2023"]), 2),
        "fy2023_inventory_write_down_usd_millions": write_down["FY2023"],
        "dram_asp_increased": _series(snapshot, "dram_asp_direction")["Q4-FY2024"] > 0,
        "nand_asp_increased": _series(snapshot, "nand_asp_direction")["Q4-FY2024"] > 0,
        "hypothesis_supported": not (recovered and inventory_change > 0),
    }


def case_metrics(snapshot: CaseSnapshot) -> dict[str, Any]:
    """Return deterministic, pre-registered metrics for a known frozen case."""

    calculators = {
        "energy": _energy_metrics,
        "bank": _bank_metrics,
        "consumer": _consumer_metrics,
        "healthcare": _healthcare_metrics,
        "internet": _internet_metrics,
        "memory": _memory_metrics,
    }
    try:
        calculator = calculators[snapshot.case_id]
    except KeyError as exc:
        raise CaseSnapshotError(f"unknown case_id: {snapshot.case_id}") from exc
    return calculator(snapshot)


def main() -> None:
    """Validate a snapshot and print its deterministic metrics as JSON."""

    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--decision-date", required=True)
    args = parser.parse_args()
    snapshot = load_case_snapshot(args.manifest, decision_date=args.decision_date)
    payload = {
        "case_id": snapshot.case_id,
        "rows": snapshot.rows,
        "sha256": snapshot.sha256,
        "providers": snapshot.providers,
        "metrics": case_metrics(snapshot),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
