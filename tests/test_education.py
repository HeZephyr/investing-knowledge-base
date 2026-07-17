from __future__ import annotations

import math

import pytest

from investkb.education import (
    bond_price,
    bonferroni_threshold,
    discrete_moments,
    effective_annual_rate,
    future_value,
    macaulay_duration,
    mean_confidence_interval,
    present_value,
    rolling_origin_splits,
    simple_ols,
)


def test_compounding_and_discounting_match_hand_calculation() -> None:
    assert future_value(1000, 0.10, 2) == pytest.approx(1210)
    assert present_value(1210, 0.10, 2) == pytest.approx(1000)
    assert effective_annual_rate(0.12, 12) == pytest.approx((1.01**12) - 1)


def test_discrete_moments_match_two_state_return_example() -> None:
    mean, variance = discrete_moments([-0.10, 0.20], [0.4, 0.6])

    assert mean == pytest.approx(0.08)
    assert variance == pytest.approx(0.0216)


def test_mean_confidence_interval_uses_sample_standard_error() -> None:
    estimate, lower, upper = mean_confidence_interval([1.0, 2.0, 3.0], z_score=1.96)

    margin = 1.96 / math.sqrt(3)
    assert estimate == pytest.approx(2.0)
    assert lower == pytest.approx(2.0 - margin)
    assert upper == pytest.approx(2.0 + margin)


def test_bonferroni_threshold_discloses_number_of_tests() -> None:
    assert bonferroni_threshold(0.05, 20) == pytest.approx(0.0025)


def test_simple_ols_matches_exact_line() -> None:
    result = simple_ols([1.0, 2.0, 3.0], [3.0, 5.0, 7.0])

    assert result.intercept == pytest.approx(1.0)
    assert result.slope == pytest.approx(2.0)
    assert result.r_squared == pytest.approx(1.0)


def test_rolling_origin_splits_never_train_on_future_observations() -> None:
    splits = rolling_origin_splits(9, min_train_size=4, test_size=2, step=2)

    assert splits == (
        ((0, 1, 2, 3), (4, 5)),
        ((0, 1, 2, 3, 4, 5), (6, 7)),
    )
    assert all(max(train) < min(test) for train, test in splits)


def test_bond_price_and_duration_match_two_year_annual_coupon() -> None:
    price = bond_price(100, coupon_rate=0.05, yield_to_maturity=0.05, years=2)
    duration = macaulay_duration(
        100, coupon_rate=0.05, yield_to_maturity=0.05, years=2
    )

    expected_duration = ((1 * 5 / 1.05) + (2 * 105 / 1.05**2)) / 100
    assert price == pytest.approx(100)
    assert duration == pytest.approx(expected_duration)


@pytest.mark.parametrize(
    ("call", "match"),
    [
        (lambda: future_value(100, -1.0, 1), "rate"),
        (lambda: present_value(float("nan"), 0.05, 1), "finite"),
        (lambda: effective_annual_rate(0.05, 0), "positive integer"),
        (lambda: discrete_moments([1, 2], [0.2, 0.2]), "sum to 1"),
        (lambda: discrete_moments([1], [-1]), "nonnegative"),
        (lambda: mean_confidence_interval([1]), "at least two"),
        (lambda: bonferroni_threshold(1.5, 3), "between 0 and 1"),
        (lambda: simple_ols([1, 1], [2, 3]), "variation"),
        (lambda: rolling_origin_splits(5, 5), "room for a test"),
        (lambda: bond_price(100, 0.05, -1.0, 2), "yield"),
    ],
)
def test_education_functions_reject_misleading_inputs(call, match: str) -> None:
    with pytest.raises(ValueError, match=match):
        call()
