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
