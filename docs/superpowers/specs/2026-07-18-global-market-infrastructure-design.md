# Global market infrastructure design

## Objective

Complete the market axis with reusable, deterministic contracts for order validation, fees, microstructure, settlement, corporate actions, and trading calendars, backed by effective-dated official sources for mainland China, Hong Kong/Stock Connect, the United States, and the United Kingdom.

## Architecture

`src/investkb/market_operations.py` owns pure market-mechanics functions. Market differences arrive as explicit rule mappings with market, currency, timezone, effective date, tick/lot, limits, settlement lag, and fee components; the module does not fetch rules or place orders. `src/investkb/market_calendar.py` normalises explicit sessions and compares a checked fixture with an observed read-only calendar. A dedicated scheduled workflow runs credential-free smoke checks and never rewrites the repository.

## Contracts

- Order validation checks positive finite price/quantity, tick and lot alignment, side/order type, reference-price bands, suspension and effective-date chronology. A limit price is an instruction boundary, not an execution guarantee.
- Fees distinguish rate, minimum, fixed-per-order, sell-only, and rounded components. Results preserve a component breakdown and currency; no generic fee table silently spans jurisdictions or dates.
- Microstructure calculations return quoted spread, midpoint, depth-limited average execution price, implementation shortfall, and unfilled quantity. They reject crossed/unsorted books and never extrapolate beyond displayed depth.
- Corporate actions transform quantity and cost basis for splits/reverse splits, cash dividends, and rights only from explicit effective records. Delisting terminates the price series instead of forward-filling it.
- Settlement advances by eligible business sessions rather than calendar days and records market/timezone/lag. The educational contract does not model every custody or failed-settlement remedy.
- Calendar normalisation rejects duplicate/naive/overlapping sessions. Comparison reports missing, unexpected, and changed sessions; a scheduled failure is evidence of drift, not permission to auto-correct history.

## Source and content boundaries

Current rules use primary regulator, exchange, clearing, tax, or investor-education pages with retrieval and effective-date notes. Stock Connect coverage separates northbound/southbound, quota, holiday eligibility, settlement currency, taxes, beneficial ownership, and corporate actions. UK coverage separates FCA disclosure/conduct, LSE venue rules, CREST/Euroclear settlement, and HMRC tax. Cross-market tables are research maps, not broker instructions.

## Failure boundaries

Impossible prices, quantities, ticks, lots, dates, fee rates, books, action ratios, settlement calendars, and timezone-naive sessions fail closed. No Cookie, Token, personal holdings, broker API, order routing, or automated trading enters public code or workflows. Rules after the retrieval/effective date require re-verification.
