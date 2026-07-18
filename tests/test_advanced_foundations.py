from __future__ import annotations

import numpy as np
import pytest

from investkb.advanced_foundations import (
    FoundationError,
    cohens_d,
    normal_power_two_sample,
    ols_hc1_diagnostics,
    seeded_bootstrap_mean,
)


def test_cohens_d_uses_pooled_sample_standard_deviation() -> None:
    assert cohens_d([1, 2, 3], [2, 3, 4]) == pytest.approx(-1.0)


@pytest.mark.parametrize(
    ("first", "second", "message"),
    [
        ([1], [2, 3], "two observations"),
        ([1, 1], [1, 1], "variance"),
        ([1, np.inf], [2, 3], "finite"),
    ],
)
def test_cohens_d_rejects_invalid_samples(first: list[float], second: list[float], message: str) -> None:
    with pytest.raises(FoundationError, match=message):
        cohens_d(first, second)


def test_normal_power_increases_with_sample_size() -> None:
    small = normal_power_two_sample(effect_size=0.4, n_per_group=20, alpha=0.05)
    large = normal_power_two_sample(effect_size=0.4, n_per_group=100, alpha=0.05)
    assert 0 < small < large < 1


@pytest.mark.parametrize(
    ("effect_size", "n_per_group", "alpha", "message"),
    [
        (0.0, 20, 0.05, "effect_size"),
        (0.4, 1, 0.05, "n_per_group"),
        (0.4, 20, 0.0, "alpha"),
        (np.nan, 20, 0.05, "finite"),
    ],
)
def test_normal_power_rejects_impossible_inputs(
    effect_size: float, n_per_group: int, alpha: float, message: str
) -> None:
    with pytest.raises(FoundationError, match=message):
        normal_power_two_sample(effect_size, n_per_group, alpha)


def test_ols_hc1_reports_residual_leverage_error_and_influence() -> None:
    x = np.arange(1.0, 9.0)
    design = np.column_stack([np.ones_like(x), x])
    response = 1.0 + 2.0 * x
    response[-1] += 12.0

    result = ols_hc1_diagnostics(design, response)

    assert result["coefficients"].shape == (2,)
    assert result["residuals"].shape == (8,)
    assert result["hc1_standard_errors"].shape == (2,)
    assert np.all(np.isfinite(result["hc1_standard_errors"]))
    assert np.sum(result["leverage"]) == pytest.approx(2.0)
    assert int(np.argmax(result["cooks_distance"])) == 7


def test_ols_hc1_rejects_bad_shapes_and_singular_designs() -> None:
    with pytest.raises(FoundationError, match="two-dimensional"):
        ols_hc1_diagnostics([1, 2, 3], [1, 2, 3])
    singular = np.array([[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]])
    with pytest.raises(FoundationError, match="rank"):
        ols_hc1_diagnostics(singular, [1, 2, 3])
    with pytest.raises(FoundationError, match="more observations"):
        ols_hc1_diagnostics(np.eye(2), [1, 2])


def test_seeded_bootstrap_is_reproducible_without_global_state() -> None:
    values = [1.0, 2.0, 4.0, 8.0]
    first = seeded_bootstrap_mean(values, resamples=20, seed=20260718)
    second = seeded_bootstrap_mean(values, resamples=20, seed=20260718)
    different = seeded_bootstrap_mean(values, resamples=20, seed=7)
    assert first.shape == (20,)
    assert np.array_equal(first, second)
    assert not np.array_equal(first, different)


@pytest.mark.parametrize("seed", [None, True, 1.5])
def test_seeded_bootstrap_requires_an_explicit_integer_seed(seed: object) -> None:
    with pytest.raises(FoundationError, match="seed"):
        seeded_bootstrap_mean([1, 2, 3], resamples=10, seed=seed)  # type: ignore[arg-type]


def test_seeded_bootstrap_rejects_invalid_data_and_counts() -> None:
    with pytest.raises(FoundationError, match="finite"):
        seeded_bootstrap_mean([1, np.nan], resamples=10, seed=1)
    with pytest.raises(FoundationError, match="resamples"):
        seeded_bootstrap_mean([1, 2], resamples=0, seed=1)
