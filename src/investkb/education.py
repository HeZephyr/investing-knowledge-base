"""可手算复核的金融与统计教学原语。

这些函数服务于学习和测试，不是交易信号、定价服务或投资建议。
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable

import numpy as np


def _finite(value: float, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _positive_integer(value: int, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{label} must be a positive integer")
    return value


def _compounding_inputs(
    amount: float,
    annual_rate: float,
    periods: float,
    compounds_per_period: int,
) -> tuple[float, float, float, int]:
    amount = _finite(amount, "amount")
    annual_rate = _finite(annual_rate, "annual rate")
    periods = _finite(periods, "periods")
    frequency = _positive_integer(compounds_per_period, "compounds_per_period")
    if periods < 0:
        raise ValueError("periods must be nonnegative")
    if 1 + annual_rate / frequency <= 0:
        raise ValueError("annual rate is outside the compounding domain")
    return amount, annual_rate, periods, frequency


def future_value(
    principal: float,
    annual_rate: float,
    periods: float,
    compounds_per_period: int = 1,
) -> float:
    """Return compound future value for a nominal annual rate."""
    principal, annual_rate, periods, frequency = _compounding_inputs(
        principal, annual_rate, periods, compounds_per_period
    )
    return principal * (1 + annual_rate / frequency) ** (periods * frequency)


def present_value(
    future_cash_flow: float,
    annual_rate: float,
    periods: float,
    compounds_per_period: int = 1,
) -> float:
    """Discount one future cash flow using a nominal annual rate."""
    future_cash_flow, annual_rate, periods, frequency = _compounding_inputs(
        future_cash_flow, annual_rate, periods, compounds_per_period
    )
    return future_cash_flow / (1 + annual_rate / frequency) ** (periods * frequency)


def effective_annual_rate(nominal_rate: float, compounds_per_year: int) -> float:
    """Convert a nominal annual rate into an effective annual rate."""
    nominal_rate = _finite(nominal_rate, "nominal rate")
    frequency = _positive_integer(compounds_per_year, "compounds_per_year")
    if 1 + nominal_rate / frequency <= 0:
        raise ValueError("nominal rate is outside the compounding domain")
    return (1 + nominal_rate / frequency) ** frequency - 1


def _one_dimensional(values: Iterable[float], label: str) -> np.ndarray:
    array = np.asarray(tuple(values), dtype=float)
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{label} must be a nonempty one-dimensional sequence")
    if not np.isfinite(array).all():
        raise ValueError(f"{label} must contain only finite values")
    return array


def discrete_moments(
    values: Iterable[float], probabilities: Iterable[float]
) -> tuple[float, float]:
    """Return population mean and variance for a discrete distribution."""
    outcomes = _one_dimensional(values, "values")
    weights = _one_dimensional(probabilities, "probabilities")
    if outcomes.size != weights.size:
        raise ValueError("values and probabilities must have equal length")
    if (weights < 0).any():
        raise ValueError("probabilities must be nonnegative")
    if not math.isclose(float(weights.sum()), 1.0, rel_tol=1e-9, abs_tol=1e-12):
        raise ValueError("probabilities must sum to 1")
    mean = float(np.dot(outcomes, weights))
    variance = float(np.dot((outcomes - mean) ** 2, weights))
    return mean, variance


def mean_confidence_interval(
    values: Iterable[float], *, z_score: float = 1.96
) -> tuple[float, float, float]:
    """Return mean and a normal-approximation interval using sample standard error."""
    sample = _one_dimensional(values, "values")
    if sample.size < 2:
        raise ValueError("values must contain at least two observations")
    z_score = _finite(z_score, "z_score")
    if z_score <= 0:
        raise ValueError("z_score must be positive")
    estimate = float(sample.mean())
    standard_error = float(sample.std(ddof=1) / math.sqrt(sample.size))
    margin = z_score * standard_error
    return estimate, estimate - margin, estimate + margin


def bonferroni_threshold(family_alpha: float, number_of_tests: int) -> float:
    """Return the per-test alpha for Bonferroni family-wise error control."""
    family_alpha = _finite(family_alpha, "family_alpha")
    if not 0 < family_alpha < 1:
        raise ValueError("family_alpha must be between 0 and 1")
    tests = _positive_integer(number_of_tests, "number_of_tests")
    return family_alpha / tests


@dataclass(frozen=True)
class OLSResult:
    """Small, explicit result for one-regressor ordinary least squares."""

    intercept: float
    slope: float
    r_squared: float


def simple_ols(x: Iterable[float], y: Iterable[float]) -> OLSResult:
    """Fit an intercept and one slope without implying causal interpretation."""
    predictor = _one_dimensional(x, "x")
    response = _one_dimensional(y, "y")
    if predictor.size != response.size:
        raise ValueError("x and y must have equal length")
    if predictor.size < 2:
        raise ValueError("x and y must contain at least two observations")
    centered_x = predictor - predictor.mean()
    sum_squares_x = float(np.dot(centered_x, centered_x))
    if sum_squares_x <= 0:
        raise ValueError("x must contain variation")
    centered_y = response - response.mean()
    slope = float(np.dot(centered_x, centered_y) / sum_squares_x)
    intercept = float(response.mean() - slope * predictor.mean())
    residuals = response - (intercept + slope * predictor)
    total_sum_squares = float(np.dot(centered_y, centered_y))
    if total_sum_squares <= 0:
        raise ValueError("y must contain response variation for R-squared")
    r_squared = 1 - float(np.dot(residuals, residuals)) / total_sum_squares
    return OLSResult(intercept=intercept, slope=slope, r_squared=r_squared)


def rolling_origin_splits(
    number_of_observations: int,
    min_train_size: int,
    test_size: int = 1,
    step: int = 1,
) -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    """Create expanding-window splits whose test observations are always later."""
    observations = _positive_integer(number_of_observations, "number_of_observations")
    minimum = _positive_integer(min_train_size, "min_train_size")
    test_size = _positive_integer(test_size, "test_size")
    step = _positive_integer(step, "step")
    if minimum + test_size > observations:
        raise ValueError("number_of_observations must leave room for a test window")
    splits = []
    for train_end in range(minimum, observations - test_size + 1, step):
        train = tuple(range(train_end))
        test = tuple(range(train_end, train_end + test_size))
        splits.append((train, test))
    return tuple(splits)


def _bond_cash_flows(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years: float,
    payments_per_year: int,
) -> tuple[np.ndarray, np.ndarray, float]:
    face = _finite(face_value, "face value")
    coupon_rate = _finite(coupon_rate, "coupon rate")
    yield_to_maturity = _finite(yield_to_maturity, "yield")
    years = _finite(years, "years")
    frequency = _positive_integer(payments_per_year, "payments_per_year")
    if face <= 0 or coupon_rate < 0 or years <= 0:
        raise ValueError("face value and years must be positive; coupon rate must be nonnegative")
    if 1 + yield_to_maturity / frequency <= 0:
        raise ValueError("yield is outside the discounting domain")
    raw_periods = years * frequency
    periods = round(raw_periods)
    if not math.isclose(raw_periods, periods, abs_tol=1e-12):
        raise ValueError("years must align with payments_per_year")
    times = np.arange(1, periods + 1, dtype=float)
    cash_flows = np.full(periods, face * coupon_rate / frequency, dtype=float)
    cash_flows[-1] += face
    discount = (1 + yield_to_maturity / frequency) ** times
    return times / frequency, cash_flows / discount, face


def bond_price(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years: float,
    payments_per_year: int = 1,
) -> float:
    """Price fixed coupon cash flows at one flat yield."""
    _, present_values, _ = _bond_cash_flows(
        face_value, coupon_rate, yield_to_maturity, years, payments_per_year
    )
    return float(present_values.sum())


def macaulay_duration(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years: float,
    payments_per_year: int = 1,
) -> float:
    """Return Macaulay duration in years for fixed coupon cash flows."""
    times, present_values, _ = _bond_cash_flows(
        face_value, coupon_rate, yield_to_maturity, years, payments_per_year
    )
    price = float(present_values.sum())
    return float(np.dot(times, present_values) / price)


def modified_duration(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years: float,
    payments_per_year: int = 1,
) -> float:
    """Return modified duration for a parallel change in one flat nominal yield."""
    frequency = _positive_integer(payments_per_year, "payments_per_year")
    macaulay = macaulay_duration(
        face_value, coupon_rate, yield_to_maturity, years, frequency
    )
    yield_to_maturity = _finite(yield_to_maturity, "yield")
    return macaulay / (1 + yield_to_maturity / frequency)


def bond_convexity(
    face_value: float,
    coupon_rate: float,
    yield_to_maturity: float,
    years: float,
    payments_per_year: int = 1,
) -> float:
    """Return traditional fixed-cash-flow convexity for one flat nominal yield."""
    frequency = _positive_integer(payments_per_year, "payments_per_year")
    times, present_values, _ = _bond_cash_flows(
        face_value, coupon_rate, yield_to_maturity, years, frequency
    )
    yield_to_maturity = _finite(yield_to_maturity, "yield")
    periods = times * frequency
    price = float(present_values.sum())
    scale = frequency**2 * (1 + yield_to_maturity / frequency) ** 2
    weights = periods * (periods + 1) / scale
    return float(np.dot(weights, present_values) / price)


def yield_to_maturity(
    face_value: float,
    coupon_rate: float,
    market_price: float,
    years: float,
    payments_per_year: int = 1,
    *,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> float:
    """Solve one flat nominal YTM by bounded bisection for fixed coupon cash flows."""
    price = _finite(market_price, "market price")
    if price <= 0:
        raise ValueError("market price must be positive")
    frequency = _positive_integer(payments_per_year, "payments_per_year")
    tolerance = _finite(tolerance, "tolerance")
    iterations = _positive_integer(max_iterations, "max_iterations")
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    def difference(rate: float) -> float:
        return bond_price(face_value, coupon_rate, rate, years, frequency) - price

    lower = -0.95 * frequency
    upper = 1.0
    lower_difference = difference(lower)
    upper_difference = difference(upper)
    while upper_difference > 0 and upper < 1024:
        upper *= 2
        upper_difference = difference(upper)
    if lower_difference < 0 or upper_difference > 0:
        raise ValueError("market price does not bracket a finite yield")

    for _ in range(iterations):
        midpoint = (lower + upper) / 2
        midpoint_difference = difference(midpoint)
        if abs(midpoint_difference) <= tolerance or upper - lower <= tolerance:
            return midpoint
        if midpoint_difference > 0:
            lower = midpoint
        else:
            upper = midpoint
    raise ValueError("yield solver did not converge")


def expected_credit_loss(
    exposure: float, default_probability: float, recovery_rate: float
) -> float:
    """Return exposure × probability of default × loss given default."""
    exposure = _finite(exposure, "exposure")
    probability = _finite(default_probability, "default probability")
    recovery = _finite(recovery_rate, "recovery rate")
    if exposure < 0:
        raise ValueError("exposure must be nonnegative")
    if not 0 <= probability <= 1:
        raise ValueError("default probability must be between 0 and 1")
    if not 0 <= recovery <= 1:
        raise ValueError("recovery rate must be between 0 and 1")
    return exposure * probability * (1 - recovery)


def annualized_futures_basis(spot: float, futures: float, days_to_expiry: int) -> float:
    """Return simple annualized futures-minus-spot basis; not an expected return."""
    spot = _finite(spot, "spot")
    futures = _finite(futures, "futures")
    days = _positive_integer(days_to_expiry, "days_to_expiry")
    if spot <= 0:
        raise ValueError("spot must be positive")
    if futures <= 0:
        raise ValueError("futures must be positive")
    return (futures / spot - 1) * 365 / days


def commodity_roll_yield(near_contract: float, next_contract: float) -> float:
    """Return a one-roll price-only proxy, near / next - 1, before costs."""
    near = _finite(near_contract, "near contract")
    next_price = _finite(next_contract, "next contract")
    if near <= 0 or next_price <= 0:
        raise ValueError("contract prices must be positive")
    return near / next_price - 1
