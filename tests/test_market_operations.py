from __future__ import annotations

from datetime import date

import pytest

from investkb.market_operations import (
    CorporateAction,
    FeeRule,
    MarketOperationError,
    MarketRule,
    apply_corporate_action,
    calculate_fees,
    quoted_spread,
    settlement_date,
    validate_order,
    walk_order_book,
)


def _cn_rule() -> MarketRule:
    return MarketRule(
        market="CN",
        currency="CNY",
        timezone="Asia/Shanghai",
        effective_from=date(2026, 1, 1),
        tick_size=0.01,
        lot_size=100,
        price_limit_pct=10.0,
    )


def test_validate_order_enforces_market_rule_and_returns_explicit_context() -> None:
    result = validate_order(
        _cn_rule(),
        price=11.0,
        quantity=200,
        side="buy",
        order_type="limit",
        trade_date=date(2026, 7, 18),
        reference_price=10.0,
    )
    assert result == {
        "market": "CN",
        "currency": "CNY",
        "timezone": "Asia/Shanghai",
        "price": 11.0,
        "quantity": 200,
        "side": "buy",
        "order_type": "limit",
        "trade_date": "2026-07-18",
    }


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"price": 10.005}, "tick"),
        ({"quantity": 150}, "lot"),
        ({"price": 11.01}, "price limit"),
        ({"suspended": True}, "suspended"),
        ({"trade_date": date(2025, 12, 31)}, "effective"),
        ({"side": "hold"}, "side"),
        ({"order_type": "magic"}, "order_type"),
    ],
)
def test_validate_order_rejects_impossible_or_inactive_orders(
    overrides: dict[str, object], message: str
) -> None:
    inputs: dict[str, object] = {
        "price": 10.0,
        "quantity": 100,
        "side": "buy",
        "order_type": "limit",
        "trade_date": date(2026, 7, 18),
        "reference_price": 10.0,
    }
    inputs.update(overrides)
    with pytest.raises(MarketOperationError, match=message):
        validate_order(_cn_rule(), **inputs)  # type: ignore[arg-type]


def test_calculate_fees_preserves_side_specific_rounded_components() -> None:
    rules = [
        FeeRule("commission", rate=0.0003, minimum=5.0),
        FeeRule("venue", fixed=1.25),
        FeeRule("stamp", rate=0.001, side="sell"),
    ]
    buy = calculate_fees(10_000, side="buy", currency="CNY", rules=rules)
    sell = calculate_fees(10_000, side="sell", currency="CNY", rules=rules)
    assert buy == {
        "currency": "CNY",
        "components": {"commission": 5.0, "venue": 1.25, "stamp": 0.0},
        "total": 6.25,
    }
    assert sell["components"] == {"commission": 5.0, "venue": 1.25, "stamp": 10.0}
    assert sell["total"] == 16.25


def test_calculate_fees_rejects_invalid_notional_rules_and_currency() -> None:
    with pytest.raises(MarketOperationError, match="notional"):
        calculate_fees(0, side="buy", currency="CNY", rules=[])
    with pytest.raises(MarketOperationError, match="currency"):
        calculate_fees(100, side="buy", currency="", rules=[])
    with pytest.raises(MarketOperationError, match="rate"):
        FeeRule("broken", rate=-0.1)


def test_quoted_spread_reports_midpoint_and_basis_points() -> None:
    result = quoted_spread(9.9, 10.1)
    assert result["midpoint"] == pytest.approx(10.0)
    assert result["absolute_spread"] == pytest.approx(0.2)
    assert result["spread_bps"] == pytest.approx(200.0)
    with pytest.raises(MarketOperationError, match="crossed"):
        quoted_spread(10.1, 10.0)


def test_walk_order_book_reports_average_shortfall_and_unfilled_depth() -> None:
    complete = walk_order_book(
        [(10.0, 100), (10.1, 100)], side="buy", quantity=150, benchmark_price=9.9
    )
    assert complete["filled_quantity"] == 150
    assert complete["unfilled_quantity"] == 0
    assert complete["average_price"] == pytest.approx((10 * 100 + 10.1 * 50) / 150)
    assert complete["implementation_shortfall_bps"] == pytest.approx(
        (complete["average_price"] / 9.9 - 1) * 10_000
    )

    partial = walk_order_book(
        [(10.0, 100), (10.1, 100)], side="buy", quantity=250, benchmark_price=9.9
    )
    assert partial["filled_quantity"] == 200
    assert partial["unfilled_quantity"] == 50


def test_walk_order_book_rejects_unsorted_or_invalid_levels() -> None:
    with pytest.raises(MarketOperationError, match="ascending"):
        walk_order_book([(10.1, 100), (10.0, 100)], side="buy", quantity=100)
    with pytest.raises(MarketOperationError, match="quantity"):
        walk_order_book([(10.0, 0)], side="buy", quantity=100)


def test_split_and_reverse_split_conserve_total_cost_basis() -> None:
    split = apply_corporate_action(
        quantity=100,
        total_cost_basis=1_000,
        action=CorporateAction("split", date(2026, 7, 1), ratio=2.0),
        as_of=date(2026, 7, 1),
    )
    assert split == {
        "status": "active",
        "quantity": 200,
        "total_cost_basis": 1_000.0,
        "cost_basis_per_share": 5.0,
        "cash": 0.0,
    }
    reverse = apply_corporate_action(
        quantity=200,
        total_cost_basis=1_000,
        action=CorporateAction("reverse_split", date(2026, 7, 2), ratio=0.5),
        as_of=date(2026, 7, 2),
    )
    assert reverse["quantity"] == 100
    assert reverse["cost_basis_per_share"] == 10.0


def test_dividend_rights_and_delisting_have_distinct_outputs() -> None:
    dividend = apply_corporate_action(
        quantity=100,
        total_cost_basis=1_000,
        action=CorporateAction("cash_dividend", date(2026, 7, 1), cash_per_share=0.3),
        as_of=date(2026, 7, 1),
    )
    assert dividend["cash"] == pytest.approx(30.0)
    assert dividend["quantity"] == 100

    rights = apply_corporate_action(
        quantity=100,
        total_cost_basis=1_000,
        action=CorporateAction("rights", date(2026, 7, 1), ratio=0.2, subscription_price=4.0),
        as_of=date(2026, 7, 1),
    )
    assert rights["rights_entitlement"] == 20
    assert rights["subscription_cash_required"] == pytest.approx(80.0)
    assert rights["quantity"] == 100

    delisted = apply_corporate_action(
        quantity=100,
        total_cost_basis=1_000,
        action=CorporateAction("delisting", date(2026, 7, 1)),
        as_of=date(2026, 7, 1),
    )
    assert delisted["status"] == "delisted"
    assert delisted["price_series_terminated"] is True


def test_corporate_actions_reject_future_or_fractional_results() -> None:
    with pytest.raises(MarketOperationError, match="not effective"):
        apply_corporate_action(
            quantity=100,
            total_cost_basis=1_000,
            action=CorporateAction("split", date(2026, 7, 2), ratio=2),
            as_of=date(2026, 7, 1),
        )
    with pytest.raises(MarketOperationError, match="fractional"):
        apply_corporate_action(
            quantity=101,
            total_cost_basis=1_000,
            action=CorporateAction("reverse_split", date(2026, 7, 1), ratio=0.5),
            as_of=date(2026, 7, 1),
        )


def test_settlement_advances_over_eligible_sessions() -> None:
    sessions = [date(2026, 7, 17), date(2026, 7, 20), date(2026, 7, 21)]
    assert settlement_date(date(2026, 7, 17), sessions=sessions, lag=2) == date(2026, 7, 21)
    assert settlement_date(date(2026, 7, 17), sessions=sessions, lag=0) == date(2026, 7, 17)


def test_settlement_rejects_non_session_duplicates_and_insufficient_horizon() -> None:
    sessions = [date(2026, 7, 17), date(2026, 7, 20)]
    with pytest.raises(MarketOperationError, match="trade_date"):
        settlement_date(date(2026, 7, 18), sessions=sessions, lag=1)
    with pytest.raises(MarketOperationError, match="unique"):
        settlement_date(date(2026, 7, 17), sessions=[sessions[0], sessions[0]], lag=1)
    with pytest.raises(MarketOperationError, match="horizon"):
        settlement_date(date(2026, 7, 17), sessions=sessions, lag=2)
