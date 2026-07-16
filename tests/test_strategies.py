import pandas as pd

from investkb.strategies import buy_and_hold_signal, moving_average_signal


def test_moving_average_signal_uses_only_current_and_past_prices() -> None:
    prices = pd.Series([10.0, 11.0, 12.0, 11.0, 13.0, 14.0])
    original = moving_average_signal(prices, fast=2, slow=3)
    changed = prices.copy()
    changed.iloc[-1] *= 100
    revised = moving_average_signal(changed, fast=2, slow=3)

    pd.testing.assert_series_equal(original.iloc[:-1], revised.iloc[:-1])


def test_buy_and_hold_waits_for_next_session_execution() -> None:
    signal = buy_and_hold_signal(4)

    assert signal.tolist() == [1, 1, 1, 1]
