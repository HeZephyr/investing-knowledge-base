from __future__ import annotations

from datetime import date

import numpy as np
import pytest

from investkb.coverage import load_coverage
from investkb.portfolio import (
    PortfolioLabError,
    allocation_diagnostics,
    brinson_attribution,
    liquidity_diagnostics,
    rebalance_plan,
    reverse_stress_shock,
    risk_contributions,
    stress_loss,
    validate_decision_journal,
    validate_ips,
)


def test_ips_requires_constraints_and_future_review() -> None:
    result = validate_ips(
        {
            "objective": "preserve purchasing power and learn",
            "horizon_years": 10,
            "emergency_reserve_months": 12,
            "max_equity_weight": 0.70,
            "max_single_asset_weight": 0.35,
            "decision_date": "2026-07-17",
            "next_review_date": "2027-07-17",
        },
        as_of=date(2026, 7, 17),
    )
    assert result["review_interval_days"] == 365
    with pytest.raises(PortfolioLabError, match="review"):
        validate_ips(
            {**result["policy"], "next_review_date": "2026-01-01"}, as_of=date(2026, 7, 17)
        )


def test_allocation_diagnostics_measure_concentration() -> None:
    result = allocation_diagnostics(
        {"equity": 0.5, "bond": 0.3, "gold": 0.2},
        expected_returns={"equity": 0.07, "bond": 0.03, "gold": 0.02},
    )
    assert result["herfindahl_index"] == pytest.approx(0.38)
    assert result["effective_holdings"] == pytest.approx(2.6316, abs=0.0001)
    assert result["expected_return"] == pytest.approx(0.048)


def test_weight_validation_rejects_leverage_and_missing_labels() -> None:
    with pytest.raises(PortfolioLabError, match="sum to 1"):
        allocation_diagnostics({"equity": 0.8, "bond": 0.5})
    with pytest.raises(PortfolioLabError, match="labels"):
        allocation_diagnostics({"equity": 1.0}, expected_returns={"bond": 0.03})


def test_rebalance_plan_uses_cash_flow_and_charges_turnover() -> None:
    result = rebalance_plan(
        {"equity": 60, "bond": 30, "gold": 10},
        {"equity": 0.5, "bond": 0.3, "gold": 0.2},
        cash_flow=10,
        fee_bps=20,
    )
    assert result["trades"] == pytest.approx({"equity": -5, "bond": 3, "gold": 12})
    assert result["one_way_turnover"] == pytest.approx(10 / 110)
    assert result["gross_traded_value"] == pytest.approx(20)
    assert result["estimated_cost"] == pytest.approx(0.04)
    assert result["post_cost_value"] == pytest.approx(109.96)


def test_liquidity_diagnostics_use_participation_cap() -> None:
    result = liquidity_diagnostics(
        positions={"liquid": 1_000_000, "thin": 600_000},
        average_daily_value={"liquid": 5_000_000, "thin": 200_000},
        participation_rate=0.10,
        max_days=20,
    )
    assert result["days_to_liquidate"]["liquid"] == pytest.approx(2)
    assert result["days_to_liquidate"]["thin"] == pytest.approx(30)
    assert result["breaches"] == ["thin"]


def test_risk_contributions_reconcile_and_reject_bad_covariance() -> None:
    result = risk_contributions([0.6, 0.4], np.array([[0.04, 0.006], [0.006, 0.01]]))
    assert result["portfolio_volatility"] == pytest.approx(0.13740, abs=0.00001)
    assert sum(result["component_contributions"]) == pytest.approx(result["portfolio_volatility"])
    assert sum(result["contribution_shares"]) == pytest.approx(1)
    with pytest.raises(PortfolioLabError, match="symmetric"):
        risk_contributions([0.5, 0.5], np.array([[1, 2], [0, 1]]))


def test_stress_and_reverse_stress_keep_loss_sign_explicit() -> None:
    weights = {"equity": 0.5, "bond": 0.3, "gold": 0.2}
    assert stress_loss(weights, {"equity": -0.30, "bond": -0.05, "gold": 0.10}) == pytest.approx(
        -0.145
    )
    assert reverse_stress_shock(
        weights, known_shocks={"bond": -0.05, "gold": 0.10}, solve_asset="equity", target_loss=-0.20
    ) == pytest.approx(-0.41)


def test_brinson_attribution_reconciles_active_return() -> None:
    result = brinson_attribution(
        portfolio_weights=[0.6, 0.4],
        benchmark_weights=[0.5, 0.5],
        portfolio_returns=[0.12, 0.02],
        benchmark_returns=[0.10, 0.03],
    )
    assert result["portfolio_return"] == pytest.approx(0.08)
    assert result["benchmark_return"] == pytest.approx(0.065)
    assert result["active_return"] == pytest.approx(0.015)
    assert result["allocation"] + result["selection"] + result["interaction"] == pytest.approx(
        0.015
    )


def test_decision_journal_scores_process_not_outcome() -> None:
    journal = {
        "decision_date": "2026-07-17",
        "thesis": "public educational allocation hypothesis",
        "base_rate": "historical range with source",
        "success_condition": "measurable objective",
        "failure_condition": "precommitted invalidation",
        "horizon": "12 months",
        "size_limit": "paper portfolio only",
        "evidence": ["source-a", "source-b"],
    }
    result = validate_decision_journal(journal)
    assert result == {"complete": True, "completeness_score": 1.0, "missing_fields": []}
    incomplete = validate_decision_journal({"decision_date": "2026-07-17"})
    assert incomplete["complete"] is False
    assert "thesis" in incomplete["missing_fields"]


def test_portfolio_axis_has_stage_appropriate_evidence() -> None:
    manifest = load_coverage("config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}
    for requirement_id in (
        "portfolio-ips",
        "portfolio-goals",
        "portfolio-allocation",
        "portfolio-diversification",
        "portfolio-position-sizing",
        "portfolio-rebalancing",
        "portfolio-liquidity",
        "portfolio-stress",
        "portfolio-risk-budget",
        "portfolio-benchmark",
        "portfolio-attribution",
        "portfolio-decision-journal",
    ):
        requirement = requirements[requirement_id]
        assert requirement.status == "validated"
        assert requirement.evidence
        assert not requirement.gap
