# Foundations Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete Issue #39 with tested statistical foundations and authoritative mathematics, economics, accounting, and market-history curricula.

**Architecture:** Add one pure Python foundations module and one focused test module. Reuse existing public frozen-data replication and three-statement reconciliation evidence where it already proves a requirement; add source cards and synthesis pages for content-ready capabilities.

**Tech Stack:** Python 3.11/3.12, NumPy, pytest, YAML coverage manifest, Markdown/MkDocs/Obsidian.

---

### Task 1: Effect size, power, and robust regression contracts

**Files:**
- Create: `tests/test_advanced_foundations.py`
- Create: `src/investkb/advanced_foundations.py`

- [ ] Test a known pooled-standard-deviation effect size, monotonic power, invalid inputs, full-rank OLS diagnostics, leverage, HC1 errors, influence, and singular rejection.
- [ ] Run `.venv/bin/pytest -q tests/test_advanced_foundations.py` and confirm import failure.
- [ ] Commit the red contract before production implementation.
- [ ] Implement the smallest validated numerical functions and rerun focused tests and Ruff.

### Task 2: Explicit stochastic reproducibility

**Files:**
- Modify: `tests/test_advanced_foundations.py`
- Modify: `src/investkb/advanced_foundations.py`

- [ ] Test equal results for equal seeds, different results for different seeds, output size, non-finite data, invalid resample counts, and missing/bool seed rejection.
- [ ] Verify the test fails before implementation.
- [ ] Implement a local `numpy.random.Generator` bootstrap without touching global random state.
- [ ] Connect the exercise to the checked dependency and interpreter environment.

### Task 3: Authoritative sources and curriculum

**Files:**
- Create source cards under `raw/courses`, `raw/books-and-papers`, and `raw/official/united-states`.
- Create foundation pages for mathematics, economics, monetary transmission, and crisis history.
- Modify hypothesis, regression, accounting, accrual, replication, index, and navigation pages.

- [ ] Verify current primary/open textbook URLs and record retrieval, license, scope, and local-use boundaries.
- [ ] Add worked examples, falsification questions, and misuse warnings rather than source-only link lists.
- [ ] Link every new page from the Wiki index and MkDocs navigation.
- [ ] Run source audit and Wiki lint.

### Task 4: Replication, accounting, and coverage evidence

**Files:**
- Modify: `config/knowledge-coverage.yaml`
- Modify: `tests/test_advanced_foundations.py`
- Modify reports, source catalog, dashboard, log, lessons, and README.

- [ ] Reuse the frozen public evidence-case implementation/test for paper reproduction and the tested company reconciliation for accounting.
- [ ] Promote all twelve incomplete foundation requirements only after stage-appropriate evidence exists.
- [ ] Assert all twenty foundation requirements are validated and have no gap.
- [ ] Regenerate reports and public indexes.

### Task 5: Verification and delivery

- [ ] Run `./scripts/verify.sh` and require all tests, source checks, Wiki lint, coverage, privacy audit, strict MkDocs, and offline demo to pass.
- [ ] Commit and push `codex/foundations-lab`, open a PR closing #39, wait for CI and PR Policy, inspect comments/reviews/threads, and squash merge with expected head SHA.
