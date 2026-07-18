# Company research lab design

## Objective

Turn the company-research axis into a beginner-safe chain of testable calculations. The lab separates facts available at a decision time, accounting identities, operating diagnostics, per-share dilution, and valuation assumptions.

## Boundaries

- Pure Python and offline fixtures; no brokerage, scraping session, Cookie, or live order path.
- Point-in-time selection never uses a filing published after the decision timestamp. Later restatements replace earlier facts only for later decisions.
- Accounting reconciliation fails closed when balance-sheet or cash-flow identities exceed tolerance.
- Valuation functions return model-implied values, not target prices or recommendations.
- Undefined multiples for negative denominators remain missing instead of becoming persuasive negative ratios.

## Public API

- `FilingFact` and `select_point_in_time_facts`: latest filed version by metric and period as of a timezone-aware decision time.
- `reconcile_statements`: validate assets = liabilities + equity and opening cash + CFO + CFI + CFF + FX = closing cash.
- `cash_conversion_metrics`: DSO, DIO, DPO, CCC and FCF with average-balance denominators.
- `fully_diluted_shares`: basic shares plus RSUs and treasury-stock-method incremental option shares.
- `reverse_dcf_growth`: bisection solver for the constant revenue growth implied by enterprise value.
- `scenario_valuation`: validate probabilities and calculate probability-weighted equity value per share.
- `normalized_multiples`: calculate comparable EV/revenue, EV/EBITDA and P/E with explicit undefined fields.

## Verification

Tests cover future filings, timezone errors, restatements, broken identities, zero/negative denominators, out-of-the-money options, infeasible DCF prices, invalid probabilities, and loss-making comparables.
