# Coverage Taxonomy v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the coarse 42-item coverage manifest with a schema-v2, 100+ atomic capability taxonomy that distinguishes content, exercises, empirical cases, and live maintenance.

**Architecture:** Keep one versioned YAML as the authority. Add `stage` to every requirement, enforce stage-specific evidence combinations only for validated capabilities, expand from five to eight knowledge axes, and render both axis and stage summaries. Migrate existing evidence conservatively and add missing capabilities rather than manufacturing completion.

**Tech Stack:** Python 3.11+, dataclasses, PyYAML, pytest, Markdown, Typer CLI, MkDocs Material, GitHub Actions.

---

### Task 1: Define schema-v2 behavior with failing tests

**Files:**
- Modify: `tests/test_coverage.py`

- [ ] **Step 1: Upgrade fixture builders to schema v2**

Add a `stage: str = "content-ready"` parameter to `_requirement`, include it in the returned mapping, and write fixture manifests with `schema_version: 2`. Update the valid-manifest assertion to expect version 2.

- [ ] **Step 2: Add unknown-stage and v1 rejection tests**

Add tests asserting `load_coverage` rejects schema v1 and `validate_coverage` returns `unknown stage: invented` for an invalid stage.

- [ ] **Step 3: Add stage-specific validated evidence tests**

Create one test per stage using real temporary files:

```python
STAGE_EVIDENCE = {
    "content-ready": {"source", "synthesis"},
    "exercise-tested": {"implementation", "test"},
    "case-validated": {"source", "report", "test"},
    "maintenance-live": {"workflow", "test"},
}
```

For each stage, first provide an incomplete subset and assert validation says `validated stage <stage> requires one of`; then provide the complete set and assert no stage error. Also prove `exercise-tested` accepts the alternative `synthesis + test` combination.

- [ ] **Step 4: Add report stage-summary test**

Assert the deterministic report contains `## 分能力阶段状态`, all four stage labels, and a `阶段` column in the per-item table.

- [ ] **Step 5: Add repository taxonomy contract**

Require the real manifest to have at least 100 requirements, exactly the eight axes `foundations`, `markets`, `assets`, `sectors`, `company`, `methods`, `portfolio`, `engineering`, and all four stages.

- [ ] **Step 6: Run RED**

Run: `.venv/bin/pytest tests/test_coverage.py -q`

Expected: FAIL because the loader only accepts schema v1, requirements have no stage, and reports have no stage table.

- [ ] **Step 7: Commit RED tests**

```bash
git add tests/test_coverage.py
git commit -m "test(coverage): define taxonomy v2 contracts"
```

### Task 2: Implement schema-v2 parsing, validation and reporting

**Files:**
- Modify: `src/investkb/coverage.py`

- [ ] **Step 1: Add axis and stage constants**

Replace axes with:

```python
ALLOWED_AXES = (
    "foundations", "markets", "assets", "sectors",
    "company", "methods", "portfolio", "engineering",
)
ALLOWED_STAGES = (
    "content-ready", "exercise-tested", "case-validated", "maintenance-live"
)
```

Add Chinese labels and stage evidence alternatives:

```python
STAGE_EVIDENCE_OPTIONS = {
    "content-ready": (frozenset({"source", "synthesis"}),),
    "exercise-tested": (
        frozenset({"synthesis", "test"}),
        frozenset({"implementation", "test"}),
    ),
    "case-validated": (frozenset({"source", "report", "test"}),),
    "maintenance-live": (frozenset({"workflow", "test"}),),
}
```

- [ ] **Step 2: Parse schema and stage**

Require root `schema_version == 2`, add `stage` to `CoverageRequirement`, and preserve it in loaded objects and any internal `CoverageManifest` construction.

- [ ] **Step 3: Enforce stage evidence only at validated**

Reject unknown stages. For validated requirements, require at least one evidence option to be a subset of actual evidence kinds, require empty gap, and keep existing path/date/kind checks. Incomplete statuses still require a non-empty gap.

- [ ] **Step 4: Render axis and stage summaries**

Keep status-weight scoring. Add a second deterministic table grouped by stage, include stage labels in the detailed table, and update the warning to say validated proves only the declared atomic stage.

- [ ] **Step 5: Run unit tests GREEN**

Run: `.venv/bin/pytest tests/test_coverage.py -q`

Expected: fixture tests pass; the real-manifest 100+ test remains RED until migration.

- [ ] **Step 6: Commit implementation**

```bash
git add src/investkb/coverage.py
git commit -m "feat(coverage): enforce capability stages"
```

### Task 3: Migrate to a 135-capability manifest

**Files:**
- Replace: `config/knowledge-coverage.yaml`

- [ ] **Step 1: Create 25 foundations capabilities**

Cover arithmetic/ratios, compounding, discounting, probability, distributions, sampling, estimation, hypothesis tests, effect sizes, multiple testing, regression, time series, causal inference, accounting and company finance. Pair content and exercise requirements where execution matters. Mark unsupported items missing; existing accounting Wiki may provide reviewed synthesis but not validated content without an admitted source.

- [ ] **Step 2: Create 15 markets and 15 assets capabilities**

Markets cover global comparison, A/HK/US/Korea/Japan/Europe/emerging rules, connect access, sessions/orders, settlement/custody, fees/taxes, disclosure and corporate actions. Assets cover equity, funds/ETF, bonds, cash, FX, gold, commodities, REIT, convertibles and derivatives, with separate exercises/cases where appropriate.

- [ ] **Step 3: Create 15 sectors and 15 company capabilities**

Sectors split content and cases for generic framework, memory, energy, financials, consumer, healthcare and internet plus cross-sector comparison. Company capabilities cover ownership, business model, filings, three statements, reconciliation, revenue recognition, working capital, earnings quality, capital allocation, governance, valuation, reverse valuation and frozen-data company cases.

- [ ] **Step 4: Create 18 methods and 14 portfolio capabilities**

Methods cover provenance, data quality, adjustment, returns, benchmark, empirical design, backtest content/exercise/case, factor content/case, behavior, decision logs, replication, robustness, negative results and out-of-sample work. Portfolio covers IPS, diversification, allocation, optimization, constraints, rebalancing, risk metrics, drawdown, performance attribution, FX hedging, liquidity, costs and governance.

- [ ] **Step 5: Create 18 engineering capabilities**

Cover source lineage, A/HK adapters, global adapters, schemas, caching, credential isolation, private/public split, CI, Pages, publication, monitoring, link health, coverage, maintenance Skill, plugin packaging, notebooks, reports and automation. Mark maintenance-live validated only where workflow+test evidence exists.

- [ ] **Step 6: Validate count and honest migration**

Run a read-only Python one-liner through the project module to print axis/stage/status counts. Require exactly 135 unique IDs, eight non-empty axes and four non-empty stages. Confirm no `case-validated` item is validated without a frozen public report.

- [ ] **Step 7: Run coverage tests GREEN**

Run: `.venv/bin/pytest tests/test_coverage.py -q && .venv/bin/python -m investkb.cli coverage validate`

Expected: PASS and the new score is lower than v1’s 60.4%.

- [ ] **Step 8: Commit migration**

```bash
git add config/knowledge-coverage.yaml
git commit -m "data(coverage): expand to 135 capabilities"
```

### Task 4: Regenerate the report and document the new completion model

**Files:**
- Regenerate: `output/reports/knowledge-coverage.md`
- Modify: `README.md`
- Modify: `AGENTS.md`
- Modify: `docs/INDEX.md`
- Modify: `skills/maintain-investing-knowledge-base/SKILL.md`
- Modify: `wiki/methods/经验与失败教训.md`
- Modify: `wiki/log.md`
- Modify: `site/index.md`
- Modify: `tests/test_knowledge_skill.py`

- [ ] **Step 1: Update public explanations**

Explain eight axes, four stages, the 135-capability denominator and why score decline is a correction. State that page count and Star count are discovery signals only.

- [ ] **Step 2: Update governance and Skill**

Require every new coverage entry to declare a stage; validated must meet stage evidence. Require repository/plugin/book/paper work to map to at least one atomic capability without upgrading unrelated stages.

- [ ] **Step 3: Record the lesson**

Add an experience entry with event, evidence, root cause, impact, repair, prevention and verification: coarse requirements made readiness look high; v2 increased denominator and separated content/exercise/case/maintenance.

- [ ] **Step 4: Update Skill tests first if wording is contract behavior**

Add assertions for `stage`, `content-ready`, `exercise-tested`, `case-validated`, and `maintenance-live`, observe RED, then update Skill and rerun GREEN.

- [ ] **Step 5: Regenerate twice and compare**

```bash
.venv/bin/python -m investkb.cli coverage report --output output/reports/knowledge-coverage.md
cp output/reports/knowledge-coverage.md /tmp/coverage-v2.md
.venv/bin/python -m investkb.cli coverage report --output output/reports/knowledge-coverage.md
cmp /tmp/coverage-v2.md output/reports/knowledge-coverage.md
```

- [ ] **Step 6: Commit docs/report**

```bash
git add README.md AGENTS.md docs/INDEX.md skills/maintain-investing-knowledge-base wiki site/index.md tests/test_knowledge_skill.py output/reports/knowledge-coverage.md
git commit -m "docs(coverage): explain capability maturity v2"
```

### Task 5: Verify and publish through Issue #16

**Files:**
- Modify only if verification finds an in-scope defect.

- [ ] **Step 1: Run complete local verification**

Run: `scripts/verify.sh`

Expected: Ruff check/format, all tests, 63+ Raw cards, Wiki lint, schema-v2 coverage, publication, strict MkDocs and offline report pass.

- [ ] **Step 2: Self-review migration**

Check all 135 IDs are unique, every existing evidence path is real, validated stage rules are satisfied, no missing capability has fake evidence, and the report score/count equals the CLI output. Inspect the public diff for secrets and private paths.

- [ ] **Step 3: Push and open a ready PR**

Push `codex/coverage-taxonomy-v2`. Open PR `feat(coverage): expand to capability taxonomy v2`, include `Closes #16`, v1/v2 denominator and score, stage rules, tests and known gaps.

- [ ] **Step 4: Wait and merge**

Wait for Python 3.11/3.12, Raw/Wiki/coverage, offline report, strict site, public boundary and PR policy. Fix failures by TDD, then squash merge and confirm Pages renders the stage table.
