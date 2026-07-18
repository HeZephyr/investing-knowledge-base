"""Pure educational contracts for market execution mechanics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import math
from typing import Sequence


class MarketOperationError(ValueError):
    """Raised when a market operation is impossible or underspecified."""


def _positive(value: float, name: str) -> float:
    if isinstance(value, bool) or not math.isfinite(value) or value <= 0:
        raise MarketOperationError(f"{name} must be finite and positive")
    return float(value)


@dataclass(frozen=True)
class MarketRule:
    market: str
    currency: str
    timezone: str
    effective_from: date
    tick_size: float
    lot_size: int
    price_limit_pct: float | None = None

    def __post_init__(self) -> None:
        if not self.market or not self.currency or not self.timezone:
            raise MarketOperationError("market, currency, and timezone are required")
        _positive(self.tick_size, "tick_size")
        if (
            isinstance(self.lot_size, bool)
            or not isinstance(self.lot_size, int)
            or self.lot_size < 1
        ):
            raise MarketOperationError("lot_size must be a positive integer")
        if self.price_limit_pct is not None and (
            not math.isfinite(self.price_limit_pct) or not 0 < self.price_limit_pct < 100
        ):
            raise MarketOperationError("price_limit_pct must be between 0 and 100")


@dataclass(frozen=True)
class FeeRule:
    name: str
    rate: float = 0.0
    minimum: float = 0.0
    fixed: float = 0.0
    side: str = "both"
    decimal_places: int = 2

    def __post_init__(self) -> None:
        if not self.name:
            raise MarketOperationError("fee name is required")
        for value, name in ((self.rate, "rate"), (self.minimum, "minimum"), (self.fixed, "fixed")):
            if isinstance(value, bool) or not math.isfinite(value) or value < 0:
                raise MarketOperationError(f"fee {name} must be finite and non-negative")
        if self.side not in {"buy", "sell", "both"}:
            raise MarketOperationError("fee side must be buy, sell, or both")
        if (
            isinstance(self.decimal_places, bool)
            or not isinstance(self.decimal_places, int)
            or not 0 <= self.decimal_places <= 8
        ):
            raise MarketOperationError("decimal_places must be an integer between 0 and 8")


@dataclass(frozen=True)
class CorporateAction:
    action_type: str
    effective_date: date
    ratio: float | None = None
    cash_per_share: float | None = None
    subscription_price: float | None = None

    def __post_init__(self) -> None:
        if self.action_type not in {
            "split",
            "reverse_split",
            "cash_dividend",
            "rights",
            "delisting",
        }:
            raise MarketOperationError("unknown corporate action_type")
        if self.action_type in {"split", "reverse_split", "rights"}:
            if self.ratio is None:
                raise MarketOperationError("corporate action ratio is required")
            _positive(self.ratio, "corporate action ratio")
        if self.action_type == "cash_dividend":
            if self.cash_per_share is None:
                raise MarketOperationError("cash_per_share is required")
            _positive(self.cash_per_share, "cash_per_share")
        if self.action_type == "rights":
            if self.subscription_price is None:
                raise MarketOperationError("subscription_price is required")
            _positive(self.subscription_price, "subscription_price")


def _aligned(value: float, increment: float) -> bool:
    quotient = Decimal(str(value)) / Decimal(str(increment))
    return quotient == quotient.to_integral_value()


def validate_order(
    rule: MarketRule,
    *,
    price: float,
    quantity: int,
    side: str,
    order_type: str,
    trade_date: date,
    reference_price: float | None = None,
    suspended: bool = False,
) -> dict[str, object]:
    """Validate a simplified order against one effective-dated market rule."""

    price = _positive(price, "price")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise MarketOperationError("quantity must be a positive integer")
    if side not in {"buy", "sell"}:
        raise MarketOperationError("side must be buy or sell")
    if order_type not in {"limit", "market"}:
        raise MarketOperationError("order_type must be limit or market")
    if trade_date < rule.effective_from:
        raise MarketOperationError("trade_date is before the rule effective date")
    if suspended:
        raise MarketOperationError("security is suspended")
    if not _aligned(price, rule.tick_size):
        raise MarketOperationError("price is not aligned to tick_size")
    if quantity % rule.lot_size:
        raise MarketOperationError("quantity is not aligned to lot_size")
    if rule.price_limit_pct is not None:
        if reference_price is None:
            raise MarketOperationError("reference_price is required for a price limit")
        reference = _positive(reference_price, "reference_price")
        boundary = rule.price_limit_pct / 100
        if price < reference * (1 - boundary) - 1e-12 or price > reference * (1 + boundary) + 1e-12:
            raise MarketOperationError("price is outside the price limit")
    return {
        "market": rule.market,
        "currency": rule.currency,
        "timezone": rule.timezone,
        "price": price,
        "quantity": quantity,
        "side": side,
        "order_type": order_type,
        "trade_date": trade_date.isoformat(),
    }


def _round_money(value: float, places: int) -> float:
    quantum = Decimal(1).scaleb(-places)
    return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP))


def calculate_fees(
    notional: float, *, side: str, currency: str, rules: Sequence[FeeRule]
) -> dict[str, object]:
    """Calculate an explicit side-aware fee breakdown."""

    notional = _positive(notional, "notional")
    if side not in {"buy", "sell"}:
        raise MarketOperationError("side must be buy or sell")
    if not currency:
        raise MarketOperationError("currency is required")
    names = [rule.name for rule in rules]
    if len(names) != len(set(names)):
        raise MarketOperationError("fee rule names must be unique")
    components: dict[str, float] = {}
    for rule in rules:
        if rule.side not in {"both", side}:
            components[rule.name] = 0.0
            continue
        amount = max(notional * rule.rate, rule.minimum) + rule.fixed
        components[rule.name] = _round_money(amount, rule.decimal_places)
    return {
        "currency": currency,
        "components": components,
        "total": _round_money(sum(components.values()), 2),
    }


def quoted_spread(bid: float, ask: float) -> dict[str, float]:
    """Return absolute and midpoint-relative quoted spread."""

    bid = _positive(bid, "bid")
    ask = _positive(ask, "ask")
    if ask <= bid:
        raise MarketOperationError("quotes are crossed or locked")
    midpoint = (bid + ask) / 2
    spread = ask - bid
    return {
        "midpoint": midpoint,
        "absolute_spread": spread,
        "spread_bps": spread / midpoint * 10_000,
    }


def walk_order_book(
    levels: Sequence[tuple[float, int]],
    *,
    side: str,
    quantity: int,
    benchmark_price: float | None = None,
) -> dict[str, float | int]:
    """Walk displayed depth without extrapolating beyond supplied levels."""

    if side not in {"buy", "sell"}:
        raise MarketOperationError("side must be buy or sell")
    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise MarketOperationError("quantity must be a positive integer")
    if not levels:
        raise MarketOperationError("levels must not be empty")
    validated: list[tuple[float, int]] = []
    for price, available in levels:
        price = _positive(price, "level price")
        if isinstance(available, bool) or not isinstance(available, int) or available <= 0:
            raise MarketOperationError("level quantity must be a positive integer")
        validated.append((price, available))
    prices = [price for price, _ in validated]
    if side == "buy" and prices != sorted(prices):
        raise MarketOperationError("buy levels must be in ascending price order")
    if side == "sell" and prices != sorted(prices, reverse=True):
        raise MarketOperationError("sell levels must be in descending price order")

    remaining = quantity
    notional = 0.0
    for price, available in validated:
        filled = min(remaining, available)
        notional += filled * price
        remaining -= filled
        if remaining == 0:
            break
    filled_quantity = quantity - remaining
    average_price = notional / filled_quantity
    result: dict[str, float | int] = {
        "filled_quantity": filled_quantity,
        "unfilled_quantity": remaining,
        "average_price": average_price,
    }
    if benchmark_price is not None:
        benchmark = _positive(benchmark_price, "benchmark_price")
        direction = 1 if side == "buy" else -1
        result["implementation_shortfall_bps"] = (
            direction * (average_price / benchmark - 1) * 10_000
        )
    return result


def apply_corporate_action(
    *,
    quantity: int,
    total_cost_basis: float,
    action: CorporateAction,
    as_of: date,
) -> dict[str, object]:
    """Apply one effective corporate action without inventing market prices."""

    if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
        raise MarketOperationError("quantity must be a positive integer")
    if (
        isinstance(total_cost_basis, bool)
        or not math.isfinite(total_cost_basis)
        or total_cost_basis < 0
    ):
        raise MarketOperationError("total_cost_basis must be finite and non-negative")
    if as_of < action.effective_date:
        raise MarketOperationError("corporate action is not effective as of the requested date")

    result: dict[str, object] = {
        "status": "active",
        "quantity": quantity,
        "total_cost_basis": float(total_cost_basis),
        "cost_basis_per_share": float(total_cost_basis / quantity),
        "cash": 0.0,
    }
    if action.action_type in {"split", "reverse_split"}:
        assert action.ratio is not None
        new_quantity = quantity * action.ratio
        if not float(new_quantity).is_integer():
            raise MarketOperationError("corporate action creates a fractional quantity")
        integer_quantity = int(new_quantity)
        if integer_quantity < 1:
            raise MarketOperationError("corporate action leaves no whole shares")
        result["quantity"] = integer_quantity
        result["cost_basis_per_share"] = float(total_cost_basis / integer_quantity)
    elif action.action_type == "cash_dividend":
        assert action.cash_per_share is not None
        result["cash"] = float(quantity * action.cash_per_share)
    elif action.action_type == "rights":
        assert action.ratio is not None and action.subscription_price is not None
        entitlement = quantity * action.ratio
        if not float(entitlement).is_integer():
            raise MarketOperationError("rights action creates a fractional entitlement")
        result["rights_entitlement"] = int(entitlement)
        result["subscription_cash_required"] = float(entitlement * action.subscription_price)
    elif action.action_type == "delisting":
        result["status"] = "delisted"
        result["price_series_terminated"] = True
    return result


def settlement_date(trade_date: date, *, sessions: Sequence[date], lag: int) -> date:
    """Advance T+N over an explicit ordered set of eligible market sessions."""

    if isinstance(lag, bool) or not isinstance(lag, int) or lag < 0:
        raise MarketOperationError("settlement lag must be a non-negative integer")
    ordered = list(sessions)
    if len(ordered) != len(set(ordered)):
        raise MarketOperationError("sessions must be unique")
    if ordered != sorted(ordered):
        raise MarketOperationError("sessions must be in ascending order")
    try:
        start = ordered.index(trade_date)
    except ValueError as exc:
        raise MarketOperationError("trade_date must be an eligible session") from exc
    target = start + lag
    if target >= len(ordered):
        raise MarketOperationError("session horizon is insufficient for settlement lag")
    return ordered[target]
