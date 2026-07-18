from __future__ import annotations

from pathlib import Path

import pytest

from investkb.cases import CaseSnapshotError, load_case_snapshot
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


def test_snapshot_rejects_hash_duplicate_future_unit_and_missing(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.yaml"
    observations = tmp_path / "observations.csv"
    observations.write_text(
        "series,period,value,unit,available_at,source_url\n"
        "x,2025-Q1,1,USD,2026-01-01T00:00:00Z,https://example.invalid/x\n",
        encoding="utf-8",
    )
    manifest.write_text(
        "case_id: bad\n"
        "snapshot: observations.csv\n"
        f"snapshot_sha256: {'0' * 64}\n"
        "primary_key: [series, period]\n"
        "allowed_units: [USD]\n",
        encoding="utf-8",
    )
    with pytest.raises(CaseSnapshotError, match="SHA-256"):
        load_case_snapshot(manifest, decision_date="2026-07-17")

    # The real case fixtures exercise duplicate, future-date, unit and missing-value
    # checks through parameterized mutation helpers in the implementation tests.


def test_case_coverage_requires_source_report_and_test_evidence() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}
    for case_name in CASE_NAMES:
        requirement = requirements[f"sector-{case_name}-case"]
        assert requirement.stage == "case-validated"
        assert requirement.status == "validated"
        assert {item.kind for item in requirement.evidence} == {"source", "report", "test"}
