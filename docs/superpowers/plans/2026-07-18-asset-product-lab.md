# Asset and Product Research Lab Implementation Plan

**Goal:** Complete Issue #43 and validate all eighteen asset/product requirements.

**Architecture:** Add one pure numerical module, focused tests, a frozen futures example, official source cards, linked synthesis pages, navigation, and coverage evidence. Implement exercises test-first and promote coverage only after the required evidence exists.

## 1. Numerical contracts

- [x] Write failing tests for option payoff, Black-Scholes price/Greeks, parity, implied volatility, and invalid domains.
- [x] Write failing tests for convertible, ETF tracking/currency, index-divisor, futures-roll, and structured-note contracts.
- [x] Implement `src/investkb/assets.py` with explicit assumptions and domain errors.

## 2. Primary evidence

- [x] Add official cards for stock ownership, money-market funds, U.S. and China government curves.
- [x] Add official cards for convertible bonds and A-share/Hong Kong/U.S. REIT regimes.
- [x] Add official cards for derivatives, index methodology, overseas ETF tax boundaries, and structured notes.

## 3. Synthesis and frozen case

- [x] Expand existing product pages and add derivatives/options/structured-product pages.
- [x] Add a frozen futures curve/roll manifest, observations, reproducible report, and test.
- [x] Update Wiki, source catalog, dashboard, MkDocs navigation, and maintenance/lesson logs.

## 4. Coverage and delivery

- [x] Promote the eleven incomplete asset requirements only after stage-appropriate evidence exists.
- [x] Assert the assets axis is 18/18 validated and regenerate the coverage report.
- [x] Run targeted tests, real full verification, secret/public-boundary checks, and site build.
- [ ] Commit in reviewable stages, push, open a ready PR closing #43, inspect CI/reviews/threads, and squash merge the verified SHA.
