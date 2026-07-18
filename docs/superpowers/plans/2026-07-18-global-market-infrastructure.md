# Global Market Infrastructure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete Issue #41 and validate all sixteen market-axis requirements.

**Architecture:** Add two focused pure-Python modules: market operations for orders, fees, books, settlement, and actions; market calendar for session normalisation and drift comparison. Keep current rules in source cards and synthesis pages, while a least-privilege schedule only executes read-only smoke contracts.

**Tech Stack:** Python 3.11/3.12, NumPy/Pandas, pytest, YAML, GitHub Actions, Markdown/MkDocs/Obsidian.

---

### Task 1: Order, fee, and microstructure contracts

**Files:**
- Create: `tests/test_market_operations.py`
- Create: `src/investkb/market_operations.py`

- [ ] Write failing tests for tick/lot/reference-band/suspension/effective-date validation and exact component fee rounding.
- [ ] Run the focused test and confirm the import fails for the missing module.
- [ ] Commit the red contract.
- [ ] Implement `validate_order`, `calculate_fees`, `quoted_spread`, and `walk_order_book` as pure functions.
- [ ] Run focused tests and Ruff; reject crossed/unsorted books, invalid rates, and implicit currency while reporting insufficient depth as unfilled quantity.

### Task 2: Corporate actions and settlement

**Files:**
- Modify: `tests/test_market_operations.py`
- Modify: `src/investkb/market_operations.py`

- [ ] Add failing fixtures for forward/reverse splits, cash dividends, rights, delisting, eligible-session T+N, and impossible chronology.
- [ ] Implement point-in-time `apply_corporate_action` and `settlement_date` without forward-filling delisted securities.
- [ ] Verify cost-basis conservation where applicable and explicit cash/rights outputs.
- [ ] Run focused tests and commit.

### Task 3: Calendar contract and scheduled monitor

**Files:**
- Create: `tests/test_market_calendar.py`
- Create: `src/investkb/market_calendar.py`
- Create: `.github/workflows/market-calendar-smoke.yml`
- Modify: `tests/test_github_workflows.py`

- [ ] Write failing tests for timezone-aware ordered sessions, duplicates, overlaps, missing/unexpected/changed comparisons, and workflow least privilege/schedule.
- [ ] Implement session normalisation and deterministic drift reports.
- [ ] Add a credential-free, read-only, rate-limited schedule plus manual dispatch; it must not commit or place orders.
- [ ] Run calendar/workflow tests and commit.

### Task 4: Current primary sources and synthesis

**Files:**
- Add official cards for FCA/LSE/HMRC/Euroclear, SEC/FINRA/DTCC, mainland exchanges/CSDC, and HKEX Stock Connect.
- Create: `wiki/markets/英国市场.md`
- Create: `wiki/markets/市场微观结构.md`
- Create: `wiki/markets/清算结算与托管.md`
- Create: `wiki/markets/公司行动与退市.md`
- Modify: A-share, US, Stock Connect, fees, global market, indexes, dashboard, and MkDocs navigation.

- [ ] Verify every dynamic URL, retrieval date, effective-date boundary, jurisdiction, timezone, currency, and reuse limit.
- [ ] Build cross-market maps without presenting them as current broker instructions.
- [ ] Link code exercises, failure examples, and falsification checks from synthesis pages.
- [ ] Run source audit and Wiki lint.

### Task 5: Coverage and full delivery

**Files:**
- Modify: `config/knowledge-coverage.yaml`
- Modify: coverage report, README, source catalog, log, lessons, indexes, and implementation plan.

- [ ] Promote all eight market requirements only after stage-appropriate evidence exists and assert markets 16/16.
- [ ] Run `./scripts/verify.sh` through tests, sources, Wiki, coverage, privacy, strict Pages, and offline demo.
- [ ] Commit, push, create a ready PR closing #41, wait for CI/PR Policy, inspect comments/reviews/threads, and squash merge with expected head SHA.
