import pandas as pd
import pytest

from investkb.metrics import max_drawdown, performance_summary


def test_max_drawdown_from_known_equity_curve() -> None:
    equity = pd.Series([100.0, 120.0, 90.0, 108.0])

    assert max_drawdown(equity) == pytest.approx(-0.25)


def test_metrics_reject_too_short_series() -> None:
    with pytest.raises(ValueError, match="two observations"):
        performance_summary(pd.Series([1.0]))


def test_performance_summary_uses_compounded_total_return() -> None:
    summary = performance_summary(pd.Series([100.0, 110.0, 99.0]), annualization=2)

    assert summary["total_return"] == pytest.approx(-0.01)
    assert summary["max_drawdown"] == pytest.approx(-0.10)
    assert summary["win_rate"] == pytest.approx(0.5)
