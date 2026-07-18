"""Deterministic numerical exercises for the advanced foundations curriculum."""

from __future__ import annotations

from collections.abc import Hashable, Mapping
from statistics import NormalDist
from typing import Any, Sequence

import numpy as np
from numpy.typing import NDArray


class FoundationError(ValueError):
    """Raised when an educational numerical contract is not identifiable."""


def _finite_vector(values: Sequence[float], *, name: str, minimum: int = 1) -> NDArray[np.float64]:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1:
        raise FoundationError(f"{name} must be one-dimensional")
    if array.size < minimum:
        raise FoundationError(f"{name} needs at least {minimum} observations")
    if not np.all(np.isfinite(array)):
        raise FoundationError(f"{name} must contain only finite observations")
    return array


def cohens_d(first: Sequence[float], second: Sequence[float]) -> float:
    """Return equal-variance Cohen's d using pooled sample variance."""

    first_array = _finite_vector(first, name="first sample", minimum=2)
    second_array = _finite_vector(second, name="second sample", minimum=2)
    degrees_of_freedom = first_array.size + second_array.size - 2
    pooled_variance = (
        (first_array.size - 1) * np.var(first_array, ddof=1)
        + (second_array.size - 1) * np.var(second_array, ddof=1)
    ) / degrees_of_freedom
    if not np.isfinite(pooled_variance) or pooled_variance <= 0:
        raise FoundationError("pooled variance must be positive")
    return float((np.mean(first_array) - np.mean(second_array)) / np.sqrt(pooled_variance))


def normal_power_two_sample(effect_size: float, n_per_group: int, alpha: float = 0.05) -> float:
    """Approximate two-sided power for two equal-sized independent groups."""

    if not np.isfinite(effect_size) or not np.isfinite(alpha):
        raise FoundationError("effect_size and alpha must be finite")
    if effect_size == 0:
        raise FoundationError("effect_size must be non-zero")
    if isinstance(n_per_group, bool) or not isinstance(n_per_group, (int, np.integer)):
        raise FoundationError("n_per_group must be an integer")
    if n_per_group < 2:
        raise FoundationError("n_per_group must be at least 2")
    if not 0 < alpha < 1:
        raise FoundationError("alpha must be between 0 and 1")

    normal = NormalDist()
    critical = normal.inv_cdf(1 - alpha / 2)
    noncentrality = abs(effect_size) * np.sqrt(n_per_group / 2)
    power = normal.cdf(-critical - noncentrality) + 1 - normal.cdf(critical - noncentrality)
    return float(power)


def ols_hc1_diagnostics(
    design: Sequence[Sequence[float]], response: Sequence[float]
) -> dict[str, NDArray[np.float64]]:
    """Fit full-rank OLS and return HC1, leverage, residual, and influence diagnostics."""

    matrix = np.asarray(design, dtype=float)
    if matrix.ndim != 2:
        raise FoundationError("design must be a two-dimensional matrix")
    if not np.all(np.isfinite(matrix)):
        raise FoundationError("design must contain only finite observations")
    target = _finite_vector(response, name="response")
    observations, parameters = matrix.shape
    if target.size != observations:
        raise FoundationError("response length must match design observations")
    if observations <= parameters:
        raise FoundationError("design needs more observations than parameters")
    if np.linalg.matrix_rank(matrix) < parameters:
        raise FoundationError("design matrix must have full column rank")

    cross_product_inverse = np.linalg.inv(matrix.T @ matrix)
    coefficients = cross_product_inverse @ matrix.T @ target
    residuals = target - matrix @ coefficients
    leverage = np.einsum("ij,jk,ik->i", matrix, cross_product_inverse, matrix)

    meat = matrix.T @ (matrix * residuals[:, None] ** 2)
    hc1_covariance = (
        observations
        / (observations - parameters)
        * (cross_product_inverse @ meat @ cross_product_inverse)
    )
    hc1_standard_errors = np.sqrt(np.maximum(np.diag(hc1_covariance), 0.0))

    residual_variance = float(residuals @ residuals / (observations - parameters))
    if residual_variance <= np.finfo(float).eps:
        cooks_distance = np.zeros(observations, dtype=float)
    else:
        denominator = np.maximum(1.0 - leverage, np.finfo(float).eps) ** 2
        cooks_distance = residuals**2 / (parameters * residual_variance) * leverage / denominator

    return {
        "coefficients": coefficients,
        "residuals": residuals,
        "leverage": leverage,
        "hc1_standard_errors": hc1_standard_errors,
        "cooks_distance": cooks_distance,
    }


def seeded_bootstrap_mean(
    values: Sequence[float], *, resamples: int, seed: int
) -> NDArray[np.float64]:
    """Return bootstrap means from a local generator with an explicit integer seed."""

    observations = _finite_vector(values, name="values")
    if isinstance(resamples, bool) or not isinstance(resamples, (int, np.integer)) or resamples < 1:
        raise FoundationError("resamples must be a positive integer")
    if isinstance(seed, bool) or not isinstance(seed, (int, np.integer)):
        raise FoundationError("seed must be an explicit integer")
    generator = np.random.default_rng(int(seed))
    samples = generator.choice(observations, size=(int(resamples), observations.size), replace=True)
    return np.mean(samples, axis=1)


def grouped_table_summary(
    rows: Sequence[Mapping[str, Any]], *, group_key: str, value_key: str
) -> list[dict[str, Any]]:
    """Return first-seen group counts and means from explicit row mappings."""

    if not rows:
        raise FoundationError("rows must contain at least one record")
    groups: dict[Hashable, list[float]] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, Mapping):
            raise FoundationError(f"row {index} must be a mapping")
        if group_key not in row:
            raise FoundationError(f"row {index} is missing group_key {group_key}")
        if value_key not in row:
            raise FoundationError(f"row {index} is missing value_key {value_key}")
        group = row[group_key]
        if not isinstance(group, Hashable):
            raise FoundationError(f"row {index} group must be hashable")
        value = row[value_key]
        if isinstance(value, bool):
            raise FoundationError(f"row {index} value must be numeric and finite")
        try:
            numeric = float(value)
        except (TypeError, ValueError) as exc:
            raise FoundationError(f"row {index} value must be numeric and finite") from exc
        if not np.isfinite(numeric):
            raise FoundationError(f"row {index} value must be finite")
        groups.setdefault(group, []).append(numeric)
    return [
        {"group": group, "count": len(values), "mean": float(np.mean(values))}
        for group, values in groups.items()
    ]
