"""Synthetic offline fixture; it cannot place an order."""


def paper_trade_example() -> str:
    return "backtest transaction_cost slippage lookahead"
