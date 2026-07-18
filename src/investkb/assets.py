"""Offline educational contracts for asset and product mechanics.

The functions expose assumptions and reject invalid domains. They are not live
prices, product recommendations, tax advice, or order-execution components.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from statistics import stdev
from typing import Sequence


class AssetModelError(ValueError):
    """Raised when an asset-model input is impossible or underspecified."""


def _finite(value: float, name: str) -> float:
    if isinstance(value, bool):
        raise AssetModelError(f"{name} must be finite")
    number = float(value)
    if not math.isfinite(number):
        raise AssetModelError(f"{name} must be finite")
    return number


def _positive(value: float, name: str) -> float:
    number = _finite(value, name)
    if number <= 0:
        raise AssetModelError(f"{name} must be positive")
    return number


def _nonnegative(value: float, name: str) -> float:
    number = _finite(value, name)
    if number < 0:
        raise AssetModelError(f"{name} must be non-negative")
    return number


def _option_type(value: str) -> str:
    if value not in {"call", "put"}:
        raise AssetModelError("option_type must be call or put")
    return value


def option_payoff(
    option_type: str,
    spot: float,
    strike: float,
    premium: float = 0.0,
    position: str = "long",
) -> dict[str, float]:
    """Return expiry payoff, keeping intrinsic value and premium separate."""

    option_type = _option_type(option_type)
    spot = _nonnegative(spot, "spot")
    strike = _positive(strike, "strike")
    premium = _finite(premium, "premium")
    if premium < 0:
        raise AssetModelError("premium must be non-negative")
    if position not in {"long", "short"}:
        raise AssetModelError("position must be long or short")
    intrinsic = max(spot - strike, 0.0) if option_type == "call" else max(strike - spot, 0.0)
    direction = 1.0 if position == "long" else -1.0
    premium_cash_flow = -direction * premium
    return {
        "intrinsic": intrinsic,
        "premium_cash_flow": premium_cash_flow,
        "net_payoff": direction * intrinsic + premium_cash_flow,
    }


def _normal_cdf(value: float) -> float:
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def _normal_pdf(value: float) -> float:
    return math.exp(-0.5 * value * value) / math.sqrt(2.0 * math.pi)


@dataclass(frozen=True)
class BlackScholesResult:
    """European option result under constant-rate lognormal assumptions."""

    price: float
    delta: float
    gamma: float
    vega: float
    theta: float
    rho: float


def black_scholes(
    option_type: str,
    spot: float,
    strike: float,
    years: float,
    rate: float,
    volatility: float,
    dividend_yield: float = 0.0,
) -> BlackScholesResult:
    """Price a European option and return textbook continuous-time Greeks."""

    option_type = _option_type(option_type)
    spot = _positive(spot, "spot")
    strike = _positive(strike, "strike")
    years = _positive(years, "years")
    rate = _finite(rate, "rate")
    volatility = _positive(volatility, "volatility")
    dividend_yield = _finite(dividend_yield, "dividend_yield")

    root_t = math.sqrt(years)
    d1 = (
        math.log(spot / strike) + (rate - dividend_yield + 0.5 * volatility * volatility) * years
    ) / (volatility * root_t)
    d2 = d1 - volatility * root_t
    spot_pv = spot * math.exp(-dividend_yield * years)
    strike_pv = strike * math.exp(-rate * years)
    density = _normal_pdf(d1)
    gamma = math.exp(-dividend_yield * years) * density / (spot * volatility * root_t)
    vega = spot_pv * density * root_t

    if option_type == "call":
        price = spot_pv * _normal_cdf(d1) - strike_pv * _normal_cdf(d2)
        delta = math.exp(-dividend_yield * years) * _normal_cdf(d1)
        theta = (
            -spot_pv * density * volatility / (2 * root_t)
            - rate * strike_pv * _normal_cdf(d2)
            + dividend_yield * spot_pv * _normal_cdf(d1)
        )
        rho = years * strike_pv * _normal_cdf(d2)
    else:
        price = strike_pv * _normal_cdf(-d2) - spot_pv * _normal_cdf(-d1)
        delta = math.exp(-dividend_yield * years) * (_normal_cdf(d1) - 1)
        theta = (
            -spot_pv * density * volatility / (2 * root_t)
            + rate * strike_pv * _normal_cdf(-d2)
            - dividend_yield * spot_pv * _normal_cdf(-d1)
        )
        rho = -years * strike_pv * _normal_cdf(-d2)
    return BlackScholesResult(price, delta, gamma, vega, theta, rho)


def implied_volatility(
    option_type: str,
    observed_price: float,
    spot: float,
    strike: float,
    years: float,
    rate: float,
    dividend_yield: float = 0.0,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 200,
) -> float:
    """Invert Black-Scholes by bounded bisection after no-arbitrage checks."""

    option_type = _option_type(option_type)
    observed = _positive(observed_price, "observed_price")
    spot = _positive(spot, "spot")
    strike = _positive(strike, "strike")
    years = _positive(years, "years")
    rate = _finite(rate, "rate")
    dividend_yield = _finite(dividend_yield, "dividend_yield")
    tolerance = _positive(tolerance, "tolerance")
    if (
        isinstance(max_iterations, bool)
        or not isinstance(max_iterations, int)
        or max_iterations < 1
    ):
        raise AssetModelError("max_iterations must be a positive integer")

    spot_pv = spot * math.exp(-dividend_yield * years)
    strike_pv = strike * math.exp(-rate * years)
    if option_type == "call":
        lower_bound, upper_bound = max(spot_pv - strike_pv, 0.0), spot_pv
    else:
        lower_bound, upper_bound = max(strike_pv - spot_pv, 0.0), strike_pv
    if observed < lower_bound - tolerance or observed > upper_bound + tolerance:
        raise AssetModelError("observed_price violates European no-arbitrage bounds")

    low, high = 1e-9, 5.0
    high_price = black_scholes(option_type, spot, strike, years, rate, high, dividend_yield).price
    if observed > high_price + tolerance:
        raise AssetModelError("observed_price needs volatility above the supported bounds")
    for _ in range(max_iterations):
        middle = (low + high) / 2
        price = black_scholes(option_type, spot, strike, years, rate, middle, dividend_yield).price
        if abs(price - observed) <= tolerance:
            return middle
        if price < observed:
            low = middle
        else:
            high = middle
    raise AssetModelError("implied volatility did not converge")


def convertible_metrics(
    face_value: float,
    conversion_price: float,
    stock_price: float,
    market_price: float,
    bond_floor: float,
) -> dict[str, float]:
    """Separate a convertible's equity parity from its estimated bond floor."""

    face = _positive(face_value, "face_value")
    conversion_price = _positive(conversion_price, "conversion_price")
    stock_price = _positive(stock_price, "stock_price")
    market_price = _positive(market_price, "market_price")
    bond_floor = _positive(bond_floor, "bond_floor")
    ratio = face / conversion_price
    conversion_value = ratio * stock_price
    return {
        "conversion_ratio": ratio,
        "conversion_value": conversion_value,
        "conversion_premium": market_price / conversion_value - 1,
        "premium_over_bond_floor": market_price / bond_floor - 1,
        "floor_shortfall": max(bond_floor - market_price, 0.0),
    }


def tracking_statistics(
    fund_returns: Sequence[float],
    benchmark_returns: Sequence[float],
    periods_per_year: int,
) -> dict[str, float]:
    """Annualize mean active return and sample volatility of active return."""

    if len(fund_returns) != len(benchmark_returns):
        raise AssetModelError("fund_returns and benchmark_returns must have equal length")
    if len(fund_returns) < 2:
        raise AssetModelError("returns must contain at least two observations")
    if (
        isinstance(periods_per_year, bool)
        or not isinstance(periods_per_year, int)
        or periods_per_year < 1
    ):
        raise AssetModelError("periods_per_year must be a positive integer")
    active = [
        _finite(fund, "fund return") - _finite(benchmark, "benchmark return")
        for fund, benchmark in zip(fund_returns, benchmark_returns, strict=True)
    ]
    return {
        "annualized_tracking_difference": sum(active) / len(active) * periods_per_year,
        "annualized_tracking_error": stdev(active) * math.sqrt(periods_per_year),
    }


def cross_currency_return(local_return: float, fx_return: float) -> float:
    """Compound asset return with the investor-currency change per local currency."""

    local = _finite(local_return, "local_return")
    fx = _finite(fx_return, "fx_return")
    if local < -1 or fx < -1:
        raise AssetModelError("local_return and fx_return must be at least -1")
    return (1 + local) * (1 + fx) - 1


def index_divisor_after_rebalance(
    old_market_value: float, old_divisor: float, new_market_value: float
) -> dict[str, float]:
    """Adjust the divisor so a non-market constituent change does not move the index."""

    old_value = _positive(old_market_value, "old_market_value")
    old_divisor = _positive(old_divisor, "old_divisor")
    new_value = _positive(new_market_value, "new_market_value")
    level = old_value / old_divisor
    new_divisor = new_value / level
    return {
        "index_level_before": level,
        "new_divisor": new_divisor,
        "index_level_after": new_value / new_divisor,
    }


def futures_roll_decomposition(
    old_entry: float, old_exit: float, new_entry: float, new_exit: float
) -> dict[str, float]:
    """Separate held-contract returns from the quoted curve gap at a roll."""

    old_entry = _positive(old_entry, "old_entry")
    old_exit = _positive(old_exit, "old_exit")
    new_entry = _positive(new_entry, "new_entry")
    new_exit = _positive(new_exit, "new_exit")
    first = old_exit / old_entry - 1
    second = new_exit / new_entry - 1
    return {
        "old_contract_return": first,
        "curve_gap_at_roll": new_entry / old_exit - 1,
        "new_contract_return": second,
        "chained_investor_return": (1 + first) * (1 + second) - 1,
    }


def structured_note_redemption(
    reference_path: Sequence[float],
    principal: float,
    barrier_ratio: float,
    participation: float,
    cap: float,
    issuer_recovery: float = 1.0,
) -> dict[str, float | bool]:
    """Evaluate one disclosed barrier note payoff, then apply issuer recovery."""

    if not reference_path:
        raise AssetModelError("reference path must not be empty")
    initial = _positive(reference_path[0], "initial reference value")
    path = [initial] + [_nonnegative(value, "reference path value") for value in reference_path[1:]]
    principal = _positive(principal, "principal")
    barrier = _finite(barrier_ratio, "barrier_ratio")
    participation = _finite(participation, "participation")
    cap = _finite(cap, "cap")
    recovery = _finite(issuer_recovery, "issuer_recovery")
    if not 0 < barrier <= 1:
        raise AssetModelError("barrier_ratio must be between 0 and 1")
    if participation < 0 or cap < 0:
        raise AssetModelError("participation and cap must be non-negative")
    if not 0 <= recovery <= 1:
        raise AssetModelError("issuer_recovery must be between 0 and 1")

    terminal_ratio = path[-1] / initial
    breached = min(path) / initial <= barrier
    if breached and terminal_ratio < 1:
        contractual = principal * terminal_ratio
    else:
        upside = min(max(terminal_ratio - 1, 0.0) * participation, cap)
        contractual = principal * (1 + upside)
    return {
        "barrier_breached": breached,
        "contractual_redemption": contractual,
        "redemption_after_issuer_credit": contractual * recovery,
    }
