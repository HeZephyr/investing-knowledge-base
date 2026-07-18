from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from investkb.cases import case_metrics, load_case_snapshot
from investkb.coverage import load_coverage


ROOT = Path(__file__).parents[1]
CASES = ("healthcare", "internet", "memory")

SOURCE_GROUPS = {
    "healthcare": (
        "raw/official/united-states/fda-clinical-endpoints.md",
        "raw/official/united-states/clinicaltrials-gov-api.md",
        "raw/official/united-states/cms-amyloid-coverage.md",
        "raw/official/china/nmpa-drug-registration.md",
        "raw/official/hong-kong/hkex-biotech-chapter-18a.md",
        "raw/official/korea/mfds-drug-approval.md",
    ),
    "internet": (
        "raw/official/united-states/ftc-platform-data-practices.md",
        "raw/official/europe/eu-digital-markets-act.md",
        "raw/official/china/samr-platform-antitrust.md",
        "raw/official/global/meta-platform-metrics.md",
    ),
    "memory": (
        "raw/official/global/jedec-memory-standards.md",
        "raw/official/global/micron-memory-results.md",
        "raw/official/korea/korean-memory-disclosures.md",
    ),
}

WIKI_PAGES = {
    "healthcare": "wiki/sectors/医药医疗.md",
    "internet": "wiki/sectors/互联网平台.md",
    "memory": "wiki/sectors/存储半导体.md",
}


@pytest.mark.parametrize("case_name", CASES)
def test_sector_system_has_primary_sources_framework_and_frozen_case(case_name: str) -> None:
    sources = SOURCE_GROUPS[case_name]
    assert len(sources) >= 2
    grade_a = 0
    for relative in sources:
        text = (ROOT / relative).read_text(encoding="utf-8")
        assert "source_grade:" in text
        grade_a += int("source_grade: A" in text)
        assert "usage: link-and-summarize" in text
        assert "不能" in text or "不可" in text
    assert grade_a >= 2

    wiki = (ROOT / WIKI_PAGES[case_name]).read_text(encoding="utf-8")
    for phrase in (
        "证据链",
        "跨市场",
        "预注册证据卡",
        "失效条件",
        "公司映射",
        "红旗",
        "冻结案例",
    ):
        assert phrase in wiki
    for market in ("A股", "港股", "美股", "韩国"):
        assert market in wiki

    snapshot = load_case_snapshot(
        ROOT / f"raw/cases/{case_name}/manifest.yaml", decision_date="2026-07-17"
    )
    metrics = case_metrics(snapshot)
    assert snapshot.rows >= 3
    assert metrics["case_id"] == case_name
    assert metrics["hypothesis_supported"] is False

    config = yaml.safe_load((ROOT / f"config/cases/{case_name}.yaml").read_text(encoding="utf-8"))
    assert config["attempts"] == 1
    assert config["decision_date"].isoformat() == "2026-07-17"

    report = (ROOT / f"output/cases/{case_name}.md").read_text(encoding="utf-8")
    for phrase in ("预注册命题", "正向证据", "负结果", "失败复盘", "SHA-256", "离线复现"):
        assert phrase in report


def test_healthcare_case_keeps_approval_coverage_and_demand_separate() -> None:
    snapshot = load_case_snapshot(
        ROOT / "raw/cases/healthcare/manifest.yaml", decision_date="2026-07-17"
    )
    metrics = case_metrics(snapshot)
    assert metrics["accelerated_approval"] is True
    assert metrics["coverage_restricted"] is True
    assert metrics["inventory_writeoff_usd_millions"] == pytest.approx(275.0)


def test_internet_case_decomposes_users_price_and_impressions() -> None:
    snapshot = load_case_snapshot(
        ROOT / "raw/cases/internet/manifest.yaml", decision_date="2026-07-17"
    )
    metrics = case_metrics(snapshot)
    assert metrics["dap_growth_pct"] == pytest.approx(5.02, abs=0.01)
    assert metrics["revenue_growth_pct"] == pytest.approx(21.94, abs=0.01)
    assert metrics["ad_impressions_growth_pct"] == 11.0
    assert metrics["average_price_per_ad_growth_pct"] == 10.0


def test_memory_case_rejects_absolute_inventory_as_required_turn_signal() -> None:
    snapshot = load_case_snapshot(
        ROOT / "raw/cases/memory/manifest.yaml", decision_date="2026-07-17"
    )
    metrics = case_metrics(snapshot)
    assert metrics["inventory_change_pct"] == pytest.approx(5.82, abs=0.01)
    assert metrics["revenue_growth_pct"] == pytest.approx(61.59, abs=0.01)
    assert metrics["gross_margin_change_pp"] == pytest.approx(31.5, abs=0.01)
    assert metrics["fy2023_inventory_write_down_usd_millions"] == 1831.0


def test_coverage_promotes_only_complete_new_sector_evidence() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}
    for case_name in CASES:
        content = requirements[f"sector-{case_name}-content"]
        case = requirements[f"sector-{case_name}-case"]
        assert content.status == "validated"
        assert case.status == "validated"
        assert {item.kind for item in case.evidence} == {"source", "report", "test"}
