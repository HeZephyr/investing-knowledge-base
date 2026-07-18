from __future__ import annotations

import math

import pytest

from investkb.assets import (
    AssetModelError,
    black_scholes,
    convertible_metrics,
    cross_currency_return,
    futures_roll_decomposition,
    implied_volatility,
    index_divisor_after_rebalance,
    option_payoff,
    structured_note_redemption,
    tracking_statistics,
)


def test_option_payoff_preserves_right_obligation_and_premium() -> None:
    call = option_payoff("call", spot=120, strike=100, premium=6, position="long")
    put = option_payoff("put", spot=80, strike=100, premium=5, position="long")
    short_call = option_payoff("call", spot=120, strike=100, premium=6, position="short")

    assert call == {"intrinsic": 20.0, "premium_cash_flow": -6.0, "net_payoff": 14.0}
    assert put["net_payoff"] == pytest.approx(15.0)
    assert short_call["net_payoff"] == pytest.approx(-14.0)


def test_black_scholes_matches_reference_values_and_put_call_parity() -> None:
    call = black_scholes("call", spot=100, strike=100, years=1, rate=0.05, volatility=0.20)
    put = black_scholes("put", spot=100, strike=100, years=1, rate=0.05, volatility=0.20)

    assert call.price == pytest.approx(10.4506, abs=1e-4)
    assert put.price == pytest.approx(5.5735, abs=1e-4)
    assert call.price - put.price == pytest.approx(100 - 100 * math.exp(-0.05), abs=1e-9)
    assert call.delta == pytest.approx(0.6368, abs=1e-4)
    assert put.delta == pytest.approx(-0.3632, abs=1e-4)
    assert call.gamma == pytest.approx(put.gamma)
    assert call.vega == pytest.approx(put.vega)


def test_implied_volatility_recovers_input_and_rejects_no_arbitrage_violation() -> None:
    observed = black_scholes("call", 100, 105, 0.75, 0.03, 0.27, dividend_yield=0.01).price
    solved = implied_volatility(
        "call", observed, 100, 105, 0.75, 0.03, dividend_yield=0.01
    )
    assert solved == pytest.approx(0.27, abs=1e-8)

    with pytest.raises(AssetModelError, match="bounds"):
        implied_volatility("call", 200, 100, 100, 1, 0.02)


def test_convertible_metrics_separate_equity_option_and_bond_floor() -> None:
    result = convertible_metrics(
        face_value=100,
        conversion_price=20,
        stock_price=22,
        market_price=118,
        bond_floor=94,
    )
    assert result == {
        "conversion_ratio": 5.0,
        "conversion_value": 110.0,
        "conversion_premium": pytest.approx(8 / 110),
        "premium_over_bond_floor": pytest.approx(24 / 94),
        "floor_shortfall": 0.0,
    }


def test_fund_tracking_and_currency_returns_are_explicit() -> None:
    stats = tracking_statistics(
        fund_returns=[0.01, -0.01, 0.02],
        benchmark_returns=[0.012, -0.008, 0.019],
        periods_per_year=12,
    )
    active = [-0.002, -0.002, 0.001]
    assert stats["annualized_tracking_difference"] == pytest.approx(sum(active) / 3 * 12)
    assert stats["annualized_tracking_error"] == pytest.approx(
        pytest.importorskip("numpy").std(active, ddof=1) * math.sqrt(12)
    )
    assert cross_currency_return(local_return=0.10, fx_return=-0.05) == pytest.approx(0.045)


def test_index_divisor_preserves_level_across_non_market_change() -> None:
    result = index_divisor_after_rebalance(
        old_market_value=1_000,
        old_divisor=10,
        new_market_value=1_200,
    )
    assert result == {
        "index_level_before": 100.0,
        "new_divisor": 12.0,
        "index_level_after": 100.0,
    }


def test_futures_roll_decomposition_does_not_call_curve_gap_a_return() -> None:
    result = futures_roll_decomposition(
        old_entry=100,
        old_exit=105,
        new_entry=108,
        new_exit=110,
    )
    assert result["old_contract_return"] == pytest.approx(0.05)
    assert result["curve_gap_at_roll"] == pytest.approx(108 / 105 - 1)
    assert result["new_contract_return"] == pytest.approx(110 / 108 - 1)
    assert result["chained_investor_return"] == pytest.approx(1.05 * (110 / 108) - 1)


def test_structured_note_redemption_captures_barrier_cap_and_issuer_recovery() -> None:
    protected = structured_note_redemption(
        [100, 95, 110], principal=1_000, barrier_ratio=0.70, participation=1.0, cap=0.15
    )
    knocked_in = structured_note_redemption(
        [100, 65, 80], principal=1_000, barrier_ratio=0.70, participation=1.0, cap=0.15
    )
    defaulted = structured_note_redemption(
        [100, 110],
        principal=1_000,
        barrier_ratio=0.70,
        participation=1.0,
        cap=0.15,
        issuer_recovery=0.40,
    )

    assert protected == {"barrier_breached": False, "contractual_redemption": 1_100.0, "redemption_after_issuer_credit": 1_100.0}
    assert knocked_in["barrier_breached"] is True
    assert knocked_in["contractual_redemption"] == pytest.approx(800.0)
    assert defaulted["contractual_redemption"] == pytest.approx(1_100.0)
    assert defaulted["redemption_after_issuer_credit"] == pytest.approx(440.0)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: option_payoff("swap", 100, 100), "option_type"),
        (lambda: black_scholes("call", 0, 100, 1, 0.02, 0.2), "spot"),
        (lambda: black_scholes("call", 100, 100, 0, 0.02, 0.2), "years"),
        (lambda: black_scholes("call", 100, 100, 1, 0.02, 0), "volatility"),
        (lambda: convertible_metrics(100, 0, 10, 90, 80), "conversion_price"),
        (lambda: tracking_statistics([0.1], [0.1], 12), "at least two"),
        (lambda: tracking_statistics([0.1, 0.2], [0.1], 12), "equal length"),
        (lambda: cross_currency_return(-1.1, 0), "greater than -1"),
        (lambda: index_divisor_after_rebalance(100, 0, 100), "old_divisor"),
        (lambda: futures_roll_decomposition(100, 0, 101, 102), "old_exit"),
        (lambda: structured_note_redemption([], 100, 0.7, 1, 0.2), "path"),
        (lambda: structured_note_redemption([100, 90], 100, 1.2, 1, 0.2), "barrier"),
    ],
)
def test_asset_models_reject_ambiguous_or_impossible_inputs(call, message: str) -> None:
    with pytest.raises(AssetModelError, match=message):
        call()
