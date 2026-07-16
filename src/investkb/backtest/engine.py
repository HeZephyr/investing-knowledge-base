"""透明的逐日日线回测状态机。"""

from __future__ import annotations

import pandas as pd

from investkb.backtest.models import BacktestResult, FeeModel, MarketRules
from investkb.validation.market import validate_bars

TRADE_COLUMNS = ["date", "side", "quantity", "price", "gross", "fees", "cash_after"]


def _buy_quantity(cash: float, price: float, fee: FeeModel, board_lot: int) -> int:
    lots = int(cash // (price * board_lot))
    while lots > 0:
        quantity = lots * board_lot
        gross = quantity * price
        if gross + fee.calculate("buy", gross) <= cash:
            return quantity
        lots -= 1
    return 0


def run_backtest(
    bars: pd.DataFrame,
    signal: pd.Series,
    initial_cash: float,
    fee: FeeModel,
    rules: MarketRules,
) -> BacktestResult:
    """收盘信号在下一条可交易 bar 的开盘执行，只允许 long/cash。"""
    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")
    if rules.board_lot <= 0:
        raise ValueError("board_lot must be positive")
    if len(signal) != len(bars):
        raise ValueError("signal length must match bars")
    if signal.isna().any() or not set(signal.unique()) <= {0, 1}:
        raise ValueError("signal must contain long/cash targets 1 or 0")
    errors = [issue for issue in validate_bars(bars) if issue.severity == "error"]
    if errors:
        raise ValueError(f"bars failed validation: {errors[0].code}")

    cash = float(initial_cash)
    shares = 0
    trades: list[dict] = []
    positions: list[dict] = []
    slip = rules.slippage_bps / 10_000.0

    for index, row in bars.reset_index(drop=True).iterrows():
        target = int(signal.iloc[index - 1]) if index > 0 else 0
        can_trade = float(row["volume"]) > 0
        if can_trade and target == 1 and shares == 0:
            price = float(row["open"]) * (1.0 + slip)
            quantity = _buy_quantity(cash, price, fee, rules.board_lot)
            if quantity:
                gross = quantity * price
                fees = fee.calculate("buy", gross)
                cash -= gross + fees
                shares += quantity
                trades.append(
                    {
                        "date": row["date"],
                        "side": "buy",
                        "quantity": quantity,
                        "price": price,
                        "gross": gross,
                        "fees": fees,
                        "cash_after": cash,
                    }
                )
        elif can_trade and target == 0 and shares > 0:
            price = float(row["open"]) * (1.0 - slip)
            quantity = shares
            gross = quantity * price
            fees = fee.calculate("sell", gross)
            cash += gross - fees
            shares = 0
            trades.append(
                {
                    "date": row["date"],
                    "side": "sell",
                    "quantity": quantity,
                    "price": price,
                    "gross": gross,
                    "fees": fees,
                    "cash_after": cash,
                }
            )
        positions.append(
            {
                "date": row["date"],
                "shares": shares,
                "cash": cash,
                "equity": cash + shares * float(row["close"]),
            }
        )

    positions_frame = pd.DataFrame(positions)
    trades_frame = pd.DataFrame(trades, columns=TRADE_COLUMNS)
    equity = positions_frame.set_index("date")["equity"].rename("equity")
    assumptions = {
        "execution": "previous close signal executes at next tradable open",
        "positioning": "long/cash; no leverage or shorting",
        "board_lot": rules.board_lot,
        "slippage_bps": rules.slippage_bps,
        "commission_rate": fee.commission_rate,
        "minimum_commission": fee.minimum_commission,
        "stamp_duty_rate": fee.stamp_duty_rate,
    }
    return BacktestResult(equity, positions_frame, trades_frame.copy(), trades_frame, assumptions)
