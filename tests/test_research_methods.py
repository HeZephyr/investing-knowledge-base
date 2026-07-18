from __future__ import annotations

from datetime import datetime, timezone

import numpy as np
import pytest

from investkb.coverage import load_coverage
from investkb.research_methods import (
    ResearchMethodError,
    autocorrelation,
    event_study,
    ewma_volatility,
    random_walk_errors,
    validate_event_windows,
    validate_preregistration,
    walk_forward_splits,
)


def _utc(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day, tzinfo=timezone.utc)


def test_walk_forward_splits_keep_embargo_and_chronology() -> None:
    expanding = walk_forward_splits(20, train_size=8, test_size=3, step=3, embargo=1)
    assert expanding == [(0, 8, 9, 12), (0, 11, 12, 15), (0, 14, 15, 18)]
    rolling = walk_forward_splits(
        20, train_size=8, test_size=3, step=3, embargo=1, expanding=False
    )
    assert rolling == [(0, 8, 9, 12), (3, 11, 12, 15), (6, 14, 15, 18)]
    assert all(train_end + 1 <= test_start for _, train_end, test_start, _ in expanding)


def test_walk_forward_rejects_impossible_sizes() -> None:
    with pytest.raises(ResearchMethodError, match="fit"):
        walk_forward_splits(10, train_size=8, test_size=3, step=1, embargo=1)


def test_preregistration_hash_is_canonical_and_before_results() -> None:
    registration = {
        "hypothesis": "annual factor mean is positive",
        "success_condition": "arithmetic mean > 0",
        "failure_condition": "arithmetic mean <= 0",
        "dataset": "frozen public annual factors",
        "window": "2000-2025",
        "method": "arithmetic mean and compound return",
        "costs": "not applicable to descriptive replication",
        "alternative_explanations": ["sample window", "data vintage"],
        "registered_at": "2026-07-16T12:00:00+00:00",
    }
    first = validate_preregistration(registration, result_available_at=_utc(2026, 7, 17))
    reordered = validate_preregistration(
        dict(reversed(list(registration.items()))), result_available_at=_utc(2026, 7, 17)
    )
    assert first["sha256"] == reordered["sha256"]
    assert len(first["sha256"]) == 64
    with pytest.raises(ResearchMethodError, match="before"):
        validate_preregistration(
            {**registration, "registered_at": "2026-07-18T00:00:00+00:00"},
            result_available_at=_utc(2026, 7, 17),
        )


def test_preregistration_rejects_missing_failure_condition() -> None:
    with pytest.raises(ResearchMethodError, match="failure_condition"):
        validate_preregistration(
            {"hypothesis": "incomplete", "registered_at": "2026-07-16T00:00:00+00:00"},
            result_available_at=_utc(2026, 7, 17),
        )


def test_time_series_diagnostics_have_explicit_baselines() -> None:
    values = [1.0, 2.0, 3.0, 4.0]
    assert autocorrelation(values, lag=1) == pytest.approx(0.25)
    assert random_walk_errors(values) == pytest.approx([1.0, 1.0, 1.0])
    volatility = ewma_volatility([0.01, -0.02, 0.03], decay=0.94, annualization=252)
    expected_variance = 0.01**2
    for value in (-0.02, 0.03):
        expected_variance = 0.94 * expected_variance + 0.06 * value**2
    assert volatility == pytest.approx(np.sqrt(expected_variance * 252))


@pytest.mark.parametrize("lag", [0, 4])
def test_autocorrelation_rejects_invalid_lag(lag: int) -> None:
    with pytest.raises(ResearchMethodError, match="lag"):
        autocorrelation([1, 2, 3, 4], lag=lag)


def test_ewma_rejects_invalid_decay() -> None:
    with pytest.raises(ResearchMethodError, match="decay"):
        ewma_volatility([0.1, 0.2], decay=1.0)


def test_event_study_recovers_market_model_and_car() -> None:
    market = np.array([-0.03, -0.01, 0.00, 0.01, 0.02, 0.03, -0.02, 0.01])
    asset = 0.001 + 1.2 * market
    asset[6:] += np.array([0.02, -0.005])
    result = event_study(
        asset,
        market,
        estimation_window=(0, 6),
        event_window=(6, 8),
    )
    assert result["alpha"] == pytest.approx(0.001)
    assert result["beta"] == pytest.approx(1.2)
    assert result["abnormal_returns"] == pytest.approx([0.02, -0.005])
    assert result["cumulative_abnormal_return"] == pytest.approx(0.015)


def test_event_study_rejects_zero_variance_market() -> None:
    with pytest.raises(ResearchMethodError, match="variance"):
        event_study([0, 0, 0, 0], [1, 1, 1, 1], estimation_window=(0, 3), event_window=(3, 4))


def test_event_windows_reject_overlap() -> None:
    assert validate_event_windows([10, 30], pre=2, post=3) == [(8, 14), (28, 34)]
    with pytest.raises(ResearchMethodError, match="overlap"):
        validate_event_windows([10, 14], pre=2, post=3)


def test_method_axis_has_stage_appropriate_evidence() -> None:
    manifest = load_coverage("config/knowledge-coverage.yaml")
    requirements = {item.id: item for item in manifest.requirements}
    for requirement_id in (
        "method-lookahead",
        "method-survivorship",
        "method-costs",
        "method-out-of-sample",
        "method-factor-content",
        "method-evidence-matrix",
        "method-preregistration",
        "method-causal-inference",
        "method-time-series",
        "method-event-study",
        "method-behavior-lessons",
    ):
        requirement = requirements[requirement_id]
        assert requirement.status == "validated"
        assert requirement.evidence
        assert not requirement.gap
