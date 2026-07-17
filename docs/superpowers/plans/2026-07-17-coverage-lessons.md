# Auditable Coverage and Lessons System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make repository completion and accumulated lessons machine-verifiable without presenting page count as investment readiness.

**Architecture:** Parse a versioned YAML requirement manifest into immutable records, validate evidence and promotion rules, render a deterministic public Markdown report, and expose both validation and report generation through Typer. Store operational and research lessons in a linked Wiki ledger and reusable Output template.

**Tech Stack:** Python 3.11 dataclasses, PyYAML, Typer, pytest, Markdown/YAML, existing CI and MkDocs.

---

### Task 1: Define coverage behavior with failing tests

**Files:**
- Create: `tests/test_coverage.py`

- [ ] Write tests using a temporary manifest and evidence files for: valid parsing; duplicate ID; unknown status; future verification date; missing evidence; `validated` with fewer than two evidence kinds; weighted score; deterministic Markdown rendering.
- [ ] Use the public API `load_coverage(path, root, today)`, `validate_coverage(manifest, root, today)`, `coverage_score(manifest)` and `render_coverage_report(manifest)` imported from `investkb.coverage`.
- [ ] Run `.venv/bin/pytest -q tests/test_coverage.py` and confirm collection fails because `investkb.coverage` does not exist.
- [ ] Commit with `test: define auditable coverage contracts`.

The test fixture must use this shape:

```yaml
schema_version: 1
as_of: 2026-07-17
requirements:
  - id: market-cn-rules
    axis: markets
    title: A 股市场规则
    status: validated
    verified: 2026-07-17
    evidence:
      - path: wiki/markets/A股市场.md
        kind: synthesis
      - path: tests/test_global_scope.py
        kind: test
    gap: ""
```

### Task 2: Implement parser, validation, score and renderer

**Files:**
- Create: `src/investkb/coverage.py`
- Test: `tests/test_coverage.py`

- [ ] Add frozen dataclasses `Evidence`, `CoverageRequirement`, and `CoverageManifest`.
- [ ] Parse YAML with `yaml.safe_load`; reject a non-mapping root, unsupported schema, invalid date, non-list requirements and malformed evidence with `CoverageFormatError`.
- [ ] Validate allowed axes `{markets, assets, sectors, methods, engineering}`, states `{missing, seed, reviewed, validated}`, unique IDs, dates no later than `today`, and all evidence paths relative to `root`.
- [ ] Require evidence counts by state: missing=0 allowed, seed>=1, reviewed>=1, validated>=2 distinct kinds. Require a non-empty gap for every non-validated requirement and an empty gap for validated.
- [ ] Score with weights missing=0, seed=0.25, reviewed=0.65, validated=1.0 and return a percentage rounded to one decimal.
- [ ] Render a deterministic Chinese Markdown report with overall readiness, a per-axis table, state counts, every requirement and every non-empty gap. Label the score as repository readiness, not investment return.
- [ ] Run focused tests until green, then Ruff, and commit `feat: add evidence-backed coverage model`.

### Task 3: Add repository manifest, CLI and generated report

**Files:**
- Create: `config/knowledge-coverage.yaml`
- Modify: `src/investkb/cli.py`
- Modify: `tests/test_cli.py`
- Create: `output/reports/knowledge-coverage.md`
- Modify: `.github/workflows/ci.yml`

- [ ] Add a failing CLI test asserting `coverage validate` succeeds on the repository manifest and `coverage report --output` writes the same bytes as the committed report.
- [ ] Add `coverage_app` with `validate` and `report` commands. Catch `CoverageFormatError`, print every validation failure, and exit 1.
- [ ] Populate requirements across all five axes from actual current evidence. Use honest `missing`, `seed`, `reviewed`, and `validated` states; include Japan/Europe/emerging markets, broader assets and sectors as explicit gaps.
- [ ] Generate and commit the report with `.venv/bin/python -m investkb.cli coverage report --output output/reports/knowledge-coverage.md`.
- [ ] Add `.venv`-independent CI command `python -m investkb.cli coverage validate` to the knowledge-integrity job.
- [ ] Run focused CLI/coverage tests and commit `feat: publish auditable knowledge coverage report`.

### Task 4: Add lessons ledger and incident template

**Files:**
- Create: `wiki/methods/经验与失败教训.md`
- Create: `output/templates/研究事故与教训.md`
- Modify: `wiki/index.md`
- Modify: `wiki/dashboard.md`
- Modify: `wiki/log.md`
- Modify: `docs/INDEX.md`
- Modify: `output/README.md`
- Modify: `mkdocs.yml`
- Modify: `tests/test_global_scope.py`

- [ ] Add a failing reachability test requiring the Wiki page, Output template, inbound links from index/dashboard, and these seven headings: 事件、证据、根因、影响、修复、预防、复验.
- [ ] Create the Wiki ledger with initial lessons: exact Action-version assertion failure; GMO deep-link restriction; AQR historical revisions/time bias; SSE next_seq/noop heartbeat versus payload; negative-result retention. Separate observed evidence from inference and do not include session material.
- [ ] Create the reusable incident template with severity, event timeline, evidence, root cause, impact, repair, prevention, regression test/manual re-verification, and public/private classification.
- [ ] Link both artifacts through indexes, Output README and MkDocs navigation; append the maintenance log.
- [ ] Run focused tests and Wiki lint, then commit `docs: add experience and failure lessons ledger`.

### Task 5: Full verification, review and PR

**Files:**
- Modify only for in-scope verification defects.

- [ ] Run Ruff lint/format, all pytest, coverage validate/report byte comparison, Raw audit, Wiki lint, publication audit, offline backtest, site generation and MkDocs strict build.
- [ ] Inspect `git diff --check origin/main...HEAD`, public secret terms, generated files and commit history.
- [ ] Push `codex/coverage-lessons`, open a ready PR closing #11, wait for every required check, self-review against the design, fix all important findings, and squash merge.
- [ ] Verify Pages deployment and the live coverage/lessons pages after merge.
