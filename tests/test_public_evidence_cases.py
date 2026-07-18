from __future__ import annotations

from pathlib import Path

import pytest

from investkb.cases import case_metrics, load_case_snapshot
from investkb.coverage import load_coverage
from investkb.evidence_cases import EvidenceCaseError, evidence_metrics


ROOT = Path(__file__).parents[1]


def _snapshot(name: str):
    return load_case_snapshot(
        ROOT / f"raw/cases/{name}/manifest.yaml", decision_date="2026-07-17"
    )


def test_company_positive_case_reconciles_growth_margin_cash_and_shares() -> None:
    metrics = evidence_metrics(_snapshot("company-positive"), analysis="company")
    assert metrics["hypothesis_supported"] is True
    assert metrics["revenue_growth_pct"] == pytest.approx(41.07, abs=0.01)
    assert metrics["operating_margin_change_pp"] == pytest.approx(17.35, abs=0.01)
    assert metrics["fcf_margin_change_pp"] == pytest.approx(15.86, abs=0.01)
    assert metrics["diluted_share_change_pct"] == pytest.approx(-3.26, abs=0.01)
    assert metrics["fcf_per_diluted_share_growth_pct"] == pytest.approx(192.08, abs=0.01)


def test_company_negative_case_explicitly_abandons_only_the_failed_thesis() -> None:
    metrics = case_metrics(_snapshot("healthcare"))
    assert metrics["hypothesis_supported"] is False
    report = (ROOT / "output/cases/company-negative.md").read_text(encoding="utf-8")
    for phrase in ("放弃原命题", "abandon_original_thesis=true", "不等于放弃整家公司", "重新研究条件"):
        assert phrase in report


def test_public_factor_replication_preserves_arithmetic_and_geometric_results() -> None:
    metrics = evidence_metrics(_snapshot("factor-strategy"), analysis="factor")
    assert metrics["hypothesis_supported"] is True
    assert metrics["hml_arithmetic_mean_pct"] == pytest.approx(1.95, abs=0.01)
    assert metrics["hml_compound_return_pct"] == pytest.approx(7.97, abs=0.01)
    assert metrics["hml_positive_years"] == 14
    assert metrics["years"] == 26


def test_preregistered_contrarian_strategy_fails_after_costs() -> None:
    metrics = evidence_metrics(
        _snapshot("factor-strategy"), analysis="negative_strategy", fee_bps=10
    )
    assert metrics["hypothesis_supported"] is False
    assert metrics["strategy_cagr_pct"] == pytest.approx(3.91, abs=0.01)
    assert metrics["benchmark_cagr_pct"] == pytest.approx(9.16, abs=0.01)
    assert metrics["strategy_cumulative_return_pct"] == pytest.approx(160.97, abs=0.01)
    assert metrics["benchmark_cumulative_return_pct"] == pytest.approx(794.55, abs=0.01)
    assert metrics["invested_years"] == 6
    assert metrics["position_changes"] == 8


def test_public_multi_asset_case_rebalances_and_charges_turnover() -> None:
    metrics = evidence_metrics(_snapshot("portfolio-public"), analysis="portfolio", fee_bps=10)
    assert metrics["hypothesis_supported"] is True
    assert metrics["portfolio_cumulative_return_pct"] == pytest.approx(61.66, abs=0.01)
    assert metrics["portfolio_cagr_pct"] == pytest.approx(8.33, abs=0.01)
    assert metrics["benchmark_cumulative_return_pct"] == pytest.approx(16.04, abs=0.01)
    assert metrics["annual_volatility_pct"] == pytest.approx(11.33, abs=0.01)
    assert metrics["max_drawdown_pct"] == pytest.approx(-5.36, abs=0.01)
    assert metrics["fee_bps"] == 10


@pytest.mark.parametrize("fee_bps", [-1, 10_001])
def test_public_case_rejects_impossible_fee(fee_bps: int) -> None:
    with pytest.raises(EvidenceCaseError, match="fee_bps"):
        evidence_metrics(_snapshot("portfolio-public"), analysis="portfolio", fee_bps=fee_bps)


@pytest.mark.parametrize(
    "name",
    ("company-positive", "company-negative", "factor-replication", "negative-strategy", "portfolio-public"),
)
def test_public_case_reports_keep_preregistration_provenance_and_limits(name: str) -> None:
    report = (ROOT / f"output/cases/{name}.md").read_text(encoding="utf-8")
    for phrase in (
        "预注册命题",
        "预设成功标准",
        "预设失效条件",
        "来源事实",
        "计算结果",
        "SHA-256",
        "局限",
        "离线复现",
    ):
        assert phrase in report


def test_remaining_case_coverage_has_source_report_and_test() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}
    ids = (
        "company-case-positive",
        "company-case-negative",
        "method-factor-replication",
        "method-negative-results",
        "portfolio-public-case",
    )
    for requirement_id in ids:
        requirement = requirements[requirement_id]
        assert requirement.status == "validated"
        assert {evidence.kind for evidence in requirement.evidence} == {
            "source",
            "report",
            "test",
        }
