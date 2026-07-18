from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from investkb.coverage import load_coverage
from investkb.sectors import (
    IndustryClassification,
    SectorModelError,
    backlog_bridge,
    capacity_utilization,
    insurance_underwriting_metrics,
    mining_unit_economics,
    property_project_bridge,
    real_estate_credit_metrics,
    reserve_roll_forward,
    semiconductor_output,
    solvency_coverage,
)


ROOT = Path(__file__).parents[1]


def test_insurance_metrics_keep_underwriting_reserves_and_capital_separate() -> None:
    underwriting = insurance_underwriting_metrics(1_000, incurred_claims=620, expenses=280)
    reserve = reserve_roll_forward(500, incurred_claims=620, claims_paid=580, closing_reserve=550)
    solvency = solvency_coverage(eligible_capital=180, required_capital=120)

    assert underwriting == {
        "loss_ratio": 0.62,
        "expense_ratio": 0.28,
        "combined_ratio": 0.90,
        "underwriting_result": 100.0,
    }
    assert reserve == {"expected_closing_reserve": 540.0, "unexplained_development": 10.0}
    assert solvency == {"coverage_ratio": 1.5, "capital_buffer": 60.0}


def test_semiconductor_output_exposes_each_yield_stage() -> None:
    result = semiconductor_output(
        wafer_starts=1_000,
        gross_dies_per_wafer=500,
        fab_yield=0.80,
        package_test_yield=0.95,
    )
    assert result == {
        "gross_dies": 500_000.0,
        "good_dies_after_fab": 400_000.0,
        "shippable_units": 380_000.0,
        "end_to_end_yield": 0.76,
    }


def test_industrial_backlog_and_capacity_do_not_treat_orders_as_revenue() -> None:
    bridge = backlog_bridge(
        opening_backlog=1_000,
        bookings=400,
        revenue_recognized=350,
        adjustments=-10,
        closing_backlog=1_040,
    )
    assert bridge == {
        "expected_closing_backlog": 1_040.0,
        "reconciliation_gap": 0.0,
        "book_to_bill": pytest.approx(400 / 350),
    }
    assert capacity_utilization(actual_output=80, practical_capacity=100) == pytest.approx(0.8)


def test_property_bridge_and_credit_metrics_reconcile_cash_and_financing() -> None:
    project = property_project_bridge(
        opening_cash=100,
        presales_collected=300,
        other_inflows=50,
        land_cost=80,
        construction_cost=180,
        interest_paid=20,
        taxes_paid=10,
        closing_cash=160,
    )
    credit = real_estate_credit_metrics(debt=500, cash=100, ebitda=120, interest_expense=40)
    assert project == {"expected_closing_cash": 160.0, "reconciliation_gap": 0.0}
    assert credit == {
        "net_debt": 400.0,
        "net_debt_to_ebitda": pytest.approx(400 / 120),
        "interest_coverage": 3.0,
    }


def test_mining_bridge_converts_grade_recovery_and_payability_into_unit_cost() -> None:
    result = mining_unit_economics(
        ore_tonnes=1_000_000,
        grade=0.01,
        recovery_rate=0.90,
        payable_rate=0.95,
        cash_cost=42_750_000,
    )
    assert result == {
        "contained_metal_tonnes": 10_000.0,
        "recovered_metal_tonnes": 9_000.0,
        "payable_metal_tonnes": 8_550.0,
        "cash_cost_per_payable_tonne": 5_000.0,
    }


def test_classification_preserves_scheme_revision_activity_and_effective_date() -> None:
    record = IndustryClassification(
        scheme="ISIC",
        revision="Rev.5",
        code="2610",
        primary_activity="Manufacture of electronic components and boards",
        effective_from=date(2025, 1, 1),
    )
    assert record.code == "2610"
    assert record.revision == "Rev.5"


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: insurance_underwriting_metrics(0, 1, 1), "earned_premium"),
        (lambda: reserve_roll_forward(10, -1, 1, 10), "incurred_claims"),
        (lambda: solvency_coverage(10, 0), "required_capital"),
        (lambda: semiconductor_output(10, 10, 1.1, 0.9), "fab_yield"),
        (lambda: backlog_bridge(10, 10, 0, 0, 20), "revenue_recognized"),
        (lambda: capacity_utilization(101, 100), "cannot exceed"),
        (lambda: property_project_bridge(1, 1, 1, 1, 1, 1, 1, -1), "closing_cash"),
        (lambda: real_estate_credit_metrics(1, 2, 0, 1), "ebitda"),
        (lambda: mining_unit_economics(1, 0, 0.9, 0.9, 1), "grade"),
        (
            lambda: IndustryClassification("", "Rev.5", "1", "activity", date(2025, 1, 1)),
            "required",
        ),
    ],
)
def test_sector_models_reject_ambiguous_or_impossible_inputs(call, message: str) -> None:
    with pytest.raises(SectorModelError, match=message):
        call()


def test_all_sector_requirements_have_stage_appropriate_evidence() -> None:
    manifest = load_coverage(ROOT / "config/knowledge-coverage.yaml")
    sectors = [item for item in manifest.requirements if item.axis == "sectors"]
    assert len(sectors) == 18
    assert all(item.status == "validated" and not item.gap for item in sectors)
