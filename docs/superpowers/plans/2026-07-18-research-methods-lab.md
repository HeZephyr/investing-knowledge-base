# Research Methods Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete Issue #37 with tested chronological research contracts and sourced method guidance.

**Architecture:** Add one pure Python method module and one focused test module. Reuse existing point-in-time, fee, factor-case, and decision-journal evidence where it already proves the requirement; add Wiki/source evidence only for content-ready capabilities.

**Tech Stack:** Python 3.11/3.12, NumPy, pytest, YAML coverage manifest, Markdown/MkDocs/Obsidian.

---

### Task 1: Chronological and preregistration contracts

**Files:**
- Create: `tests/test_research_methods.py`
- Create: `src/investkb/research_methods.py`

- [ ] Write tests asserting exact expanding/rolling split ranges, embargo separation, canonical hash stability, missing-field rejection, and registration-before-results.
- [ ] Run `.venv/bin/pytest -q tests/test_research_methods.py` and confirm import failure.
- [ ] Implement `walk_forward_splits` and `validate_preregistration` with explicit validation.
- [ ] Re-run the focused tests and confirm the new group passes.
- [ ] Commit the red contract separately before production implementation.

### Task 2: Time-series diagnostics

**Files:**
- Modify: `tests/test_research_methods.py`
- Modify: `src/investkb/research_methods.py`

- [ ] Test lag-one autocorrelation, prior-value forecast errors, EWMA annualised volatility, invalid lag, and invalid lambda.
- [ ] Verify the new tests fail because the functions are missing.
- [ ] Implement demeaned autocorrelation, random-walk errors, and the EWMA recursion over squared returns.
- [ ] Run focused tests and Ruff checks.

### Task 3: Event-study engine

**Files:**
- Modify: `tests/test_research_methods.py`
- Modify: `src/investkb/research_methods.py`

- [ ] Test a known alpha/beta fixture, abnormal returns/CAR, estimation/event chronology, zero market variance, and overlapping event windows.
- [ ] Verify failure before implementation.
- [ ] Implement OLS market-model estimation, abnormal-return calculation, and `validate_event_windows`.
- [ ] Run focused tests and confirm attribution values and errors.

### Task 4: Sources and synthesis

**Files:**
- Create: `raw/books-and-papers/causal-inference-what-if.md`
- Create: `raw/books-and-papers/event-studies-economics-finance.md`
- Create: `wiki/methods/因果推断与识别.md`
- Create: `wiki/methods/研究预注册与证据等级.md`
- Create: `wiki/quant/事件研究.md`
- Modify: factor, survivorship, out-of-sample, time-series, evidence-matrix, behavior, and navigation pages.

- [ ] Add link-and-summarize source cards with license/use boundaries.
- [ ] Explain DAG exchangeability/positivity/consistency, matching limits, parallel trends, exclusion restrictions, and event-window contamination.
- [ ] Add worked offline examples and link every new page from Wiki and MkDocs navigation.
- [ ] Run source audit and Wiki lint.

### Task 5: Coverage and full verification

**Files:**
- Modify: `config/knowledge-coverage.yaml`
- Modify: `output/reports/knowledge-coverage.md`
- Modify: `README.md`, `raw/source-catalog.md`, `wiki/log.md`, `wiki/methods/经验与失败教训.md`

- [ ] Promote all eleven incomplete method requirements only after stage-appropriate evidence exists.
- [ ] Add a coverage test for every method requirement and regenerate the report.
- [ ] Run `./scripts/verify.sh`; expect all tests, 100+ sources, Wiki lint, coverage, privacy scan, strict site, and offline demo to pass.
- [ ] Commit, push `codex/research-methods-lab`, open a PR closing #37, wait for CI/Policy, inspect comments/reviews/threads, and squash merge with expected head SHA.
