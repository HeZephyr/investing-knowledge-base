from __future__ import annotations

from datetime import datetime, timezone

import pytest

from investkb.company import (
    CompanyResearchError,
    FilingFact,
    cash_conversion_metrics,
    fully_diluted_shares,
    normalized_multiples,
    reconcile_statements,
    reverse_dcf_growth,
    scenario_valuation,
    select_point_in_time_facts,
)
from investkb.coverage import load_coverage


def _time(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day, tzinfo=timezone.utc)


def test_point_in_time_facts_use_latest_filing_available_then() -> None:
    facts = [
        FilingFact("revenue", "2023", 100, _time(2024, 2, 1), "original"),
        FilingFact("revenue", "2023", 96, _time(2024, 8, 1), "restatement"),
        FilingFact("revenue", "2024", 120, _time(2025, 2, 1), "next-year"),
    ]
    early = select_point_in_time_facts(facts, decision_at=_time(2024, 6, 30))
    late = select_point_in_time_facts(facts, decision_at=_time(2024, 12, 31))
    assert early[("revenue", "2023")].value == 100
    assert early[("revenue", "2023")].accession == "original"
    assert late[("revenue", "2023")].value == 96
    assert ("revenue", "2024") not in late


def test_point_in_time_rejects_naive_decision_timestamp() -> None:
    with pytest.raises(CompanyResearchError, match="timezone"):
        select_point_in_time_facts([], decision_at=datetime(2024, 1, 1))


def test_three_statement_reconciliation_checks_both_identities() -> None:
    result = reconcile_statements(
        assets=500,
        liabilities=300,
        equity=200,
        opening_cash=50,
        cash_from_operations=80,
        cash_from_investing=-40,
        cash_from_financing=-10,
        fx_effect=2,
        closing_cash=82,
    )
    assert result == {"balance_sheet_gap": 0.0, "cash_flow_gap": 0.0}


@pytest.mark.parametrize("closing_cash", [81, 83])
def test_three_statement_reconciliation_fails_closed(closing_cash: float) -> None:
    with pytest.raises(CompanyResearchError, match="cash-flow identity"):
        reconcile_statements(
            assets=500,
            liabilities=300,
            equity=200,
            opening_cash=50,
            cash_from_operations=80,
            cash_from_investing=-40,
            cash_from_financing=-10,
            fx_effect=2,
            closing_cash=closing_cash,
        )


def test_cash_conversion_uses_average_balances_and_capex() -> None:
    metrics = cash_conversion_metrics(
        revenue=1_000,
        cost_of_goods_sold=600,
        receivables_open=90,
        receivables_close=110,
        inventory_open=100,
        inventory_close=140,
        payables_open=70,
        payables_close=90,
        cash_from_operations=150,
        capital_expenditure=60,
        days=365,
    )
    assert metrics["dso_days"] == pytest.approx(36.5)
    assert metrics["dio_days"] == pytest.approx(73.0)
    assert metrics["dpo_days"] == pytest.approx(48.67, abs=0.01)
    assert metrics["cash_conversion_cycle_days"] == pytest.approx(60.83, abs=0.01)
    assert metrics["free_cash_flow"] == 90


def test_cash_conversion_rejects_nonpositive_sales_or_cost() -> None:
    with pytest.raises(CompanyResearchError, match="positive"):
        cash_conversion_metrics(0, 1, 1, 1, 1, 1, 1, 1, 1, 1)


def test_fully_diluted_shares_applies_treasury_stock_method() -> None:
    shares = fully_diluted_shares(
        basic_shares=100,
        restricted_stock_units=4,
        option_shares=10,
        option_exercise_price=20,
        average_market_price=50,
    )
    assert shares["incremental_option_shares"] == pytest.approx(6)
    assert shares["fully_diluted_shares"] == pytest.approx(110)
    assert fully_diluted_shares(100, 0, 10, 60, 50)["incremental_option_shares"] == 0


def test_reverse_dcf_recovers_implied_growth() -> None:
    growth = reverse_dcf_growth(
        enterprise_value=3_631.64,
        revenue=1_000,
        free_cash_flow_margin=0.20,
        discount_rate=0.10,
        terminal_growth=0.03,
        forecast_years=5,
    )
    assert growth == pytest.approx(0.08, abs=0.001)


def test_reverse_dcf_rejects_infeasible_value() -> None:
    with pytest.raises(CompanyResearchError, match="not bracketed"):
        reverse_dcf_growth(100_000, 1_000, 0.2, 0.1, 0.03, 5)


def test_scenario_valuation_requires_complete_probabilities() -> None:
    result = scenario_valuation(
        scenarios=[
            {"name": "bear", "probability": 0.25, "enterprise_value": 700},
            {"name": "base", "probability": 0.50, "enterprise_value": 1_000},
            {"name": "bull", "probability": 0.25, "enterprise_value": 1_500},
        ],
        net_debt=100,
        diluted_shares=100,
    )
    assert result["weighted_enterprise_value"] == pytest.approx(1_050)
    assert result["weighted_equity_value_per_share"] == pytest.approx(9.5)
    with pytest.raises(CompanyResearchError, match="sum to 1"):
        scenario_valuation([{"name": "only", "probability": 0.9, "enterprise_value": 1}], 0, 1)


def test_normalized_multiples_leave_loss_denominators_undefined() -> None:
    result = normalized_multiples(
        enterprise_value=1_000,
        equity_value=800,
        revenue=500,
        ebitda=-20,
        net_income=-10,
    )
    assert result == {"ev_to_revenue": 2.0, "ev_to_ebitda": None, "price_to_earnings": None}


def test_company_research_chain_has_stage_appropriate_evidence() -> None:
    manifest = load_coverage("config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}
    ids = (
        "company-disclosure",
        "company-point-in-time",
        "company-three-statements",
        "company-reconciliation",
        "company-revenue",
        "company-earnings-quality",
        "company-cash-conversion",
        "company-capital-allocation",
        "company-governance",
        "company-dilution",
        "company-reverse-dcf",
        "company-scenarios",
        "company-comparables",
    )
    for requirement_id in ids:
        requirement = requirements[requirement_id]
        assert requirement.status == "validated"
        assert not requirement.gap
        assert requirement.evidence
