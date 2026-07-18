from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from investkb.cases import CaseSnapshotError, case_metrics, load_case_snapshot
from investkb.coverage import load_coverage


ROOT = Path(__file__).parents[1]
CASE_NAMES = ("energy", "bank", "consumer")


@pytest.mark.parametrize("case_name", CASE_NAMES)
def test_frozen_case_snapshot_is_verified_and_reproducible(case_name: str) -> None:
    root = ROOT / "raw/cases" / case_name
    snapshot = load_case_snapshot(root / "manifest.yaml", decision_date="2026-07-17")

    assert snapshot.rows >= 6
    assert len(snapshot.sha256) == 64
    assert snapshot.providers
    assert snapshot.available_at_max <= snapshot.decision_at
    assert not snapshot.observations.isna().any().any()
    metrics = case_metrics(snapshot)
    assert metrics["case_id"] == case_name
    assert metrics["hypothesis_supported"] is False

    config = yaml.safe_load(
        (ROOT / "config/cases" / f"{case_name}.yaml").read_text(encoding="utf-8")
    )
    assert config["case_id"] == case_name
    assert config["decision_date"].isoformat() == "2026-07-17"
    assert config["attempts"] == 1

    report = (ROOT / "output/cases" / f"{case_name}.md").read_text(encoding="utf-8")
    for phrase in (
        "预注册命题",
        "预设成功标准",
        "预设失效条件",
        "替代解释",
        "来源事实",
        "计算结果",
        "负结果",
        "SHA-256",
        "首次可得日",
        "离线复现",
    ):
        assert phrase in report


def test_case_cli_reproduces_metrics_without_network() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "investkb.cases",
            "raw/cases/bank/manifest.yaml",
            "--decision-date",
            "2026-07-17",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["metrics"]["deposit_change_pct"] == -8.39
    assert payload["metrics"]["hypothesis_supported"] is False

    source = (ROOT / "src/investkb/cases.py").read_text(encoding="utf-8")
    for module in ("requests", "urllib.request", "http.client", "socket"):
        assert module not in source


def test_energy_case_preserves_partial_support_and_magnitude_failure() -> None:
    snapshot = load_case_snapshot(
        ROOT / "raw/cases/energy/manifest.yaml", decision_date="2026-07-17"
    )
    metrics = case_metrics(snapshot)
    assert metrics["direction_matches"] == 2
    assert metrics["growth_gap_percentage_points"]["2023"] == pytest.approx(9.65, abs=0.01)
    assert metrics["growth_gap_percentage_points"]["2024"] == pytest.approx(0.59, abs=0.01)


def test_bank_case_falsifies_simple_capital_ratio_sufficiency() -> None:
    snapshot = load_case_snapshot(ROOT / "raw/cases/bank/manifest.yaml", decision_date="2026-07-17")
    metrics = case_metrics(snapshot)
    assert metrics["equity_to_assets_2022_q4_pct"] > metrics["equity_to_assets_2021_q4_pct"]
    assert metrics["deposit_change_pct"] == pytest.approx(-8.39, abs=0.01)
    assert metrics["failed"] is True


def test_consumer_case_keeps_company_divergence() -> None:
    snapshot = load_case_snapshot(
        ROOT / "raw/cases/consumer/manifest.yaml", decision_date="2026-07-17"
    )
    metrics = case_metrics(snapshot)
    assert metrics["target_direction_mismatches"] == 2
    assert metrics["walmart_direction_matches"] == 2


def _write_snapshot(tmp_path: Path, rows: list[str], *, sha256: str | None = None) -> Path:
    manifest = tmp_path / "manifest.yaml"
    observations = tmp_path / "observations.csv"
    content = "series,period,value,unit,available_at,source_url,provider\n" + "\n".join(rows) + "\n"
    observations.write_text(content, encoding="utf-8")
    digest = sha256 or hashlib.sha256(content.encode()).hexdigest()
    manifest.write_text(
        "case_id: bad\n"
        "snapshot: observations.csv\n"
        f'snapshot_sha256: "{digest}"\n'
        "primary_key: [series, period]\n"
        "allowed_units: [USD]\n",
        encoding="utf-8",
    )
    return manifest


def test_snapshot_rejects_bad_hash(tmp_path: Path) -> None:
    manifest = _write_snapshot(
        tmp_path,
        ["x,2025-Q1,1,USD,2026-01-01T00:00:00Z,https://example.invalid/x,fixture"],
        sha256="0" * 64,
    )
    with pytest.raises(CaseSnapshotError, match="SHA-256"):
        load_case_snapshot(manifest, decision_date="2026-07-17")


@pytest.mark.parametrize(
    ("rows", "message"),
    [
        (
            [
                "x,2025-Q1,1,USD,2026-01-01T00:00:00Z,https://example.invalid/x,fixture",
                "x,2025-Q1,2,USD,2026-01-02T00:00:00Z,https://example.invalid/x,fixture",
            ],
            "duplicate primary key",
        ),
        (
            ["x,2025-Q1,1,USD,2026-07-18T00:00:00Z,https://example.invalid/x,fixture"],
            "after decision date",
        ),
        (
            ["x,2025-Q1,1,shares,2026-01-01T00:00:00Z,https://example.invalid/x,fixture"],
            "unknown unit",
        ),
        (
            ["x,2025-Q1,,USD,2026-01-01T00:00:00Z,https://example.invalid/x,fixture"],
            "missing",
        ),
    ],
)
def test_snapshot_rejects_invalid_observations(
    tmp_path: Path, rows: list[str], message: str
) -> None:
    manifest = _write_snapshot(tmp_path, rows)
    with pytest.raises(CaseSnapshotError, match=message):
        load_case_snapshot(manifest, decision_date="2026-07-17")


def test_case_coverage_requires_source_report_and_test_evidence() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}
    for case_name in CASE_NAMES:
        requirement = requirements[f"sector-{case_name}-case"]
        assert requirement.stage == "case-validated"
        assert requirement.status == "validated"
        assert {item.kind for item in requirement.evidence} == {"source", "report", "test"}
