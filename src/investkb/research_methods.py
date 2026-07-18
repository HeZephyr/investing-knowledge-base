"""Deterministic research-method exercises with explicit time and evidence boundaries."""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from typing import Any, Mapping, Sequence

import numpy as np


class ResearchMethodError(ValueError):
    """A research method input violates chronology, evidence, or numeric assumptions."""


def _positive_int(name: str, value: int, *, allow_zero: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ResearchMethodError(f"{name} must be an integer")
    minimum = 0 if allow_zero else 1
    if value < minimum:
        raise ResearchMethodError(f"{name} must be >= {minimum}")
    return value


def _array(values: Sequence[float], name: str, *, minimum: int = 1) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.ndim != 1 or array.size < minimum or not np.isfinite(array).all():
        raise ResearchMethodError(f"{name} must be a finite one-dimensional series")
    return array


def walk_forward_splits(
    observations: int,
    *,
    train_size: int,
    test_size: int,
    step: int,
    embargo: int = 0,
    expanding: bool = True,
) -> list[tuple[int, int, int, int]]:
    """Return chronological half-open train/test ranges with an explicit embargo."""

    total = _positive_int("observations", observations)
    train = _positive_int("train_size", train_size)
    test = _positive_int("test_size", test_size)
    stride = _positive_int("step", step)
    gap = _positive_int("embargo", embargo, allow_zero=True)
    if train + gap + test > total:
        raise ResearchMethodError("train, embargo, and test windows do not fit observations")
    splits: list[tuple[int, int, int, int]] = []
    train_start = 0
    train_end = train
    while train_end + gap + test <= total:
        test_start = train_end + gap
        splits.append((train_start, train_end, test_start, test_start + test))
        train_end += stride
        if not expanding:
            train_start += stride
    return splits


def _aware_timestamp(name: str, value: Any) -> datetime:
    if isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ResearchMethodError(f"{name} must be an ISO timestamp") from exc
    elif isinstance(value, datetime):
        parsed = value
    else:
        raise ResearchMethodError(f"{name} must be a timestamp")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ResearchMethodError(f"{name} must include timezone")
    return parsed


def validate_preregistration(
    registration: Mapping[str, Any], *, result_available_at: datetime
) -> dict[str, Any]:
    """Validate and hash an immutable research preregistration."""

    required = (
        "hypothesis",
        "success_condition",
        "failure_condition",
        "dataset",
        "window",
        "method",
        "costs",
        "alternative_explanations",
        "registered_at",
    )
    missing: list[str] = []
    for field in required:
        value = registration.get(field)
        if field == "alternative_explanations":
            if (
                not isinstance(value, list)
                or not value
                or any(not str(item).strip() for item in value)
            ):
                missing.append(field)
        elif field == "registered_at":
            if value is None:
                missing.append(field)
        elif not isinstance(value, str) or not value.strip():
            missing.append(field)
    if missing:
        raise ResearchMethodError(f"preregistration missing: {', '.join(missing)}")
    registered = _aware_timestamp("registered_at", registration["registered_at"])
    result_time = _aware_timestamp("result_available_at", result_available_at)
    if registered >= result_time:
        raise ResearchMethodError("registered_at must be before result_available_at")
    normalized = dict(registration)
    normalized["registered_at"] = registered.isoformat()
    encoded = json.dumps(
        normalized, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode()
    return {"registration": normalized, "sha256": hashlib.sha256(encoded).hexdigest()}


def autocorrelation(values: Sequence[float], *, lag: int) -> float:
    """Calculate the conventional demeaned sample autocorrelation at one lag."""

    series = _array(values, "values", minimum=2)
    lag = _positive_int("lag", lag)
    if lag >= series.size:
        raise ResearchMethodError("lag must be smaller than the series length")
    demeaned = series - series.mean()
    denominator = float(demeaned @ demeaned)
    if denominator == 0:
        raise ResearchMethodError("autocorrelation is undefined for a constant series")
    return float(demeaned[lag:] @ demeaned[:-lag] / denominator)


def random_walk_errors(values: Sequence[float]) -> list[float]:
    """Return one-step errors from the prior-observation forecast baseline."""

    series = _array(values, "values", minimum=2)
    return np.diff(series).tolist()


def ewma_volatility(
    returns: Sequence[float], *, decay: float = 0.94, annualization: int = 252
) -> float:
    """Return the final annualised EWMA volatility estimate."""

    series = _array(returns, "returns")
    decay = float(decay)
    if not math.isfinite(decay) or not 0 < decay < 1:
        raise ResearchMethodError("decay must be between 0 and 1")
    annualization = _positive_int("annualization", annualization)
    variance = float(series[0] ** 2)
    for value in series[1:]:
        variance = decay * variance + (1 - decay) * float(value**2)
    return math.sqrt(variance * annualization)


def event_study(
    asset_returns: Sequence[float],
    market_returns: Sequence[float],
    *,
    estimation_window: tuple[int, int],
    event_window: tuple[int, int],
) -> dict[str, Any]:
    """Estimate a market model and calculate event-window abnormal returns and CAR."""

    asset = _array(asset_returns, "asset_returns", minimum=4)
    market = _array(market_returns, "market_returns", minimum=4)
    if asset.shape != market.shape:
        raise ResearchMethodError("asset and market returns must have matching lengths")
    est_start, est_end = estimation_window
    event_start, event_end = event_window
    if not (0 <= est_start < est_end <= event_start < event_end <= asset.size):
        raise ResearchMethodError("estimation and event windows violate chronology")
    if est_end - est_start < 3:
        raise ResearchMethodError("estimation window requires at least three observations")
    x = market[est_start:est_end]
    y = asset[est_start:est_end]
    centered = x - x.mean()
    denominator = float(centered @ centered)
    if denominator == 0:
        raise ResearchMethodError("market variance must be positive in the estimation window")
    beta = float(centered @ (y - y.mean()) / denominator)
    alpha = float(y.mean() - beta * x.mean())
    abnormal = asset[event_start:event_end] - (alpha + beta * market[event_start:event_end])
    return {
        "alpha": alpha,
        "beta": beta,
        "abnormal_returns": abnormal.tolist(),
        "cumulative_abnormal_return": float(abnormal.sum()),
    }


def validate_event_windows(events: Sequence[int], *, pre: int, post: int) -> list[tuple[int, int]]:
    """Build half-open event windows and reject overlapping observations."""

    pre = _positive_int("pre", pre, allow_zero=True)
    post = _positive_int("post", post, allow_zero=True)
    if not events:
        raise ResearchMethodError("events must not be empty")
    normalized = sorted(_positive_int("event", event, allow_zero=True) for event in events)
    if len(set(normalized)) != len(normalized):
        raise ResearchMethodError("events must be unique")
    windows = [(event - pre, event + post + 1) for event in normalized]
    if any(start < 0 for start, _ in windows):
        raise ResearchMethodError("event window cannot start before zero")
    for previous, current in zip(windows, windows[1:]):
        if current[0] < previous[1]:
            raise ResearchMethodError("event windows overlap")
    return windows
