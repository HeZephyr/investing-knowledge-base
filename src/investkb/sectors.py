"""Hand-checkable operating bridges for cross-industry research."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import math


class SectorModelError(ValueError):
    """Raised when an industry bridge has impossible or ambiguous inputs."""


def _finite(value: float, name: str) -> float:
    if isinstance(value, bool):
        raise SectorModelError(f"{name} must be finite")
    number = float(value)
    if not math.isfinite(number):
        raise SectorModelError(f"{name} must be finite")
    return number


def _nonnegative(value: float, name: str) -> float:
    number = _finite(value, name)
    if number < 0:
        raise SectorModelError(f"{name} must be non-negative")
    return number


def _positive(value: float, name: str) -> float:
    number = _finite(value, name)
    if number <= 0:
        raise SectorModelError(f"{name} must be positive")
    return number


def _unit_interval(value: float, name: str, *, allow_zero: bool = True) -> float:
    number = _finite(value, name)
    lower_ok = number >= 0 if allow_zero else number > 0
    if not lower_ok or number > 1:
        boundary = "between 0 and 1" if allow_zero else "greater than 0 and at most 1"
        raise SectorModelError(f"{name} must be {boundary}")
    return number


def insurance_underwriting_metrics(
    earned_premium: float, incurred_claims: float, expenses: float
) -> dict[str, float]:
    """Separate loss, expense, combined ratios and underwriting result."""

    premium = _positive(earned_premium, "earned_premium")
    claims = _nonnegative(incurred_claims, "incurred_claims")
    expenses = _nonnegative(expenses, "expenses")
    return {
        "loss_ratio": claims / premium,
        "expense_ratio": expenses / premium,
        "combined_ratio": (claims + expenses) / premium,
        "underwriting_result": premium - claims - expenses,
    }


def reserve_roll_forward(
    opening_reserve: float,
    current_accident_year_incurred: float,
    prior_period_development: float,
    claims_paid: float,
    other_movements: float,
    closing_reserve: float,
) -> dict[str, float]:
    """Reconcile claims reserves with development and other movements explicit."""

    opening = _nonnegative(opening_reserve, "opening_reserve")
    current = _nonnegative(current_accident_year_incurred, "current_accident_year_incurred")
    development = _finite(prior_period_development, "prior_period_development")
    paid = _nonnegative(claims_paid, "claims_paid")
    other = _finite(other_movements, "other_movements")
    closing = _nonnegative(closing_reserve, "closing_reserve")
    expected = opening + current + development - paid + other
    if expected < 0:
        raise SectorModelError("reserve movements imply a negative closing reserve")
    return {
        "expected_closing_reserve": expected,
        "reconciliation_gap": closing - expected,
    }


def solvency_coverage(eligible_capital: float, required_capital: float) -> dict[str, float]:
    """Report regulatory-capital coverage without mixing it with accounting equity."""

    eligible = _nonnegative(eligible_capital, "eligible_capital")
    required = _positive(required_capital, "required_capital")
    return {"coverage_ratio": eligible / required, "capital_buffer": eligible - required}


def semiconductor_output(
    wafer_starts: float,
    gross_dies_per_wafer: float,
    fab_yield: float,
    package_test_yield: float,
) -> dict[str, float]:
    """Bridge wafer starts through fabrication and package/test yield."""

    wafers = _nonnegative(wafer_starts, "wafer_starts")
    dies = _positive(gross_dies_per_wafer, "gross_dies_per_wafer")
    fab = _unit_interval(fab_yield, "fab_yield")
    package = _unit_interval(package_test_yield, "package_test_yield")
    gross = wafers * dies
    good = gross * fab
    shippable = good * package
    return {
        "gross_dies": gross,
        "good_dies_after_fab": good,
        "shippable_units": shippable,
        "end_to_end_yield": fab * package,
    }


def backlog_bridge(
    opening_backlog: float,
    bookings: float,
    revenue_recognized: float,
    adjustments: float,
    closing_backlog: float,
) -> dict[str, float]:
    """Reconcile backlog while keeping bookings distinct from recognized revenue."""

    opening = _nonnegative(opening_backlog, "opening_backlog")
    bookings = _nonnegative(bookings, "bookings")
    revenue = _positive(revenue_recognized, "revenue_recognized")
    adjustments = _finite(adjustments, "adjustments")
    closing = _nonnegative(closing_backlog, "closing_backlog")
    expected = opening + bookings - revenue + adjustments
    if expected < 0:
        raise SectorModelError("backlog bridge implies a negative closing balance")
    return {
        "expected_closing_backlog": expected,
        "reconciliation_gap": closing - expected,
        "book_to_bill": bookings / revenue,
    }


def capacity_utilization(actual_output: float, practical_capacity: float) -> float:
    """Return output divided by explicitly defined practical capacity."""

    actual = _nonnegative(actual_output, "actual_output")
    capacity = _positive(practical_capacity, "practical_capacity")
    return actual / capacity


def property_project_bridge(
    opening_cash: float,
    presales_collected: float,
    other_inflows: float,
    land_cost: float,
    construction_cost: float,
    interest_paid: float,
    taxes_paid: float,
    closing_cash: float,
) -> dict[str, float]:
    """Reconcile a simplified project cash bridge without treating presales as profit."""

    opening = _nonnegative(opening_cash, "opening_cash")
    presales = _nonnegative(presales_collected, "presales_collected")
    inflows = _nonnegative(other_inflows, "other_inflows")
    costs = sum(
        (
            _nonnegative(land_cost, "land_cost"),
            _nonnegative(construction_cost, "construction_cost"),
            _nonnegative(interest_paid, "interest_paid"),
            _nonnegative(taxes_paid, "taxes_paid"),
        )
    )
    closing = _nonnegative(closing_cash, "closing_cash")
    cash_before_financing = opening + presales + inflows - costs
    shortfall = max(0.0, -cash_before_financing)
    expected = cash_before_financing + shortfall
    return {
        "cash_before_required_financing": cash_before_financing,
        "funding_shortfall": shortfall,
        "expected_closing_cash": expected,
        "reconciliation_gap": closing - expected,
    }


def real_estate_credit_metrics(
    debt: float, cash: float, ebitda: float, interest_expense: float
) -> dict[str, float]:
    """Report simplified leverage diagnostics with explicit denominator limits."""

    debt = _nonnegative(debt, "debt")
    cash = _nonnegative(cash, "cash")
    ebitda = _positive(ebitda, "ebitda")
    interest = _positive(interest_expense, "interest_expense")
    net_debt = debt - cash
    return {
        "net_debt": net_debt,
        "net_debt_to_ebitda": net_debt / ebitda,
        "interest_coverage": ebitda / interest,
    }


def mining_unit_economics(
    ore_tonnes: float,
    grade_fraction: float,
    recovery_rate: float,
    payable_rate: float,
    cash_cost: float,
) -> dict[str, float]:
    """Bridge ore through dimensionless grade fraction, recovery, and payability."""

    ore = _positive(ore_tonnes, "ore_tonnes")
    grade = _unit_interval(grade_fraction, "grade_fraction", allow_zero=False)
    recovery = _unit_interval(recovery_rate, "recovery_rate", allow_zero=False)
    payable = _unit_interval(payable_rate, "payable_rate", allow_zero=False)
    cost = _nonnegative(cash_cost, "cash_cost")
    contained = ore * grade
    recovered = contained * recovery
    payable_metal = recovered * payable
    return {
        "contained_metal_tonnes": contained,
        "recovered_metal_tonnes": recovered,
        "payable_metal_tonnes": payable_metal,
        "cash_cost_per_payable_tonne": cost / payable_metal,
    }


@dataclass(frozen=True)
class IndustryClassification:
    """One versioned classification label for a primary economic activity."""

    scheme: str
    revision: str
    code: str
    primary_activity: str
    mapping_effective_from: date

    def __post_init__(self) -> None:
        if not all(
            isinstance(value, str) and value.strip()
            for value in (self.scheme, self.revision, self.code, self.primary_activity)
        ):
            raise SectorModelError("scheme, revision, code, and primary_activity are required")
        if not isinstance(self.mapping_effective_from, date):
            raise SectorModelError("mapping_effective_from must be a date")
