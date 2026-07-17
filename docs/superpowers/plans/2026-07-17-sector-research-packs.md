# Sector Research Packs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build auditable Raw → Wiki → Output research packs for energy, financials, and consumer sectors, raising their coverage requirements from `missing` to `reviewed` without presenting macro data as stock recommendations.

**Architecture:** Six official source cards establish provenance and revision limits; three sector Wiki pages translate the sources into business and financial mechanisms; three sector evidence-card templates pre-register historical-time research. Repository contract tests enforce structure and reachability, while the existing coverage engine records only evidence-backed status changes.

**Tech Stack:** Markdown/YAML, Python 3.11+, pytest, `investkb` source/Wiki/coverage auditors, MkDocs Material, Git/GitHub Actions.

---

### Task 1: Add failing sector-pack contracts

**Files:**
- Create: `tests/test_sector_research_packs.py`

- [ ] **Step 1: Write the failing Raw-card contract**

Define a parametrized test for these exact paths and IDs:

```python
RAW_CARDS = {
    "raw/official/united-states/eia-open-data.md": "raw-us-eia-open-data",
    "raw/official/global/opec-annual-statistical-bulletin.md": "raw-global-opec-asb",
    "raw/official/global/bis-basel-framework.md": "raw-global-bis-basel-framework",
    "raw/official/united-states/fdic-bankfind-call-reports.md": "raw-us-fdic-bankfind-call-reports",
    "raw/official/united-states/census-monthly-retail-trade.md": "raw-us-census-monthly-retail-trade",
    "raw/official/mainland/nbs-retail-sales-methodology.md": "raw-cn-nbs-retail-sales-methodology",
}
```

For each card, parse frontmatter, require retrieval date `2026-07-17`, grade A, `link-and-summarize`, and non-empty sections `权威性与用途`, `更新频率与字段`, `许可与使用边界`, `利益冲突`, `历史修订`, `局限与失效条件`.

- [ ] **Step 2: Write the failing Wiki and Output contracts**

Require Wiki files `wiki/sectors/能源.md`, `wiki/sectors/金融.md`, and `wiki/sectors/消费.md`. Each must have its two expected Raw IDs and non-empty sections `定义与边界`, `产业链与商业模式`, `指标树与时序`, `财务映射`, `估值`, `跨市场差异`, `反例与失败模式`, `研究检查清单`, `来源说明`.

Require Output files `output/templates/能源周期证据卡.md`, `output/templates/银行资产负债表证据卡.md`, and `output/templates/消费单位经济证据卡.md`. Each must contain `数据截止日`, `历史可得日`, `内容 SHA-256`, `基准`, `预设失效条件`, `替代解释`, and a fenced `bash` reproduction block.

- [ ] **Step 3: Write failing reachability and coverage assertions**

Require all three Wiki links in `wiki/index.md` and `wiki/dashboard.md`, all three templates in `output/README.md`, and all three pages in `mkdocs.yml`. Load `config/knowledge-coverage.yaml` and assert energy, financials and consumer are `reviewed` with `synthesis`, `source`, and `template` evidence. Keep `sector-framework` at `reviewed` until a later frozen-data application proves the generic framework.

- [ ] **Step 4: Run the focused test and verify RED**

Run: `.venv/bin/pytest tests/test_sector_research_packs.py -q`

Expected: FAIL because the six Raw cards, three Wiki pages and three templates do not yet exist.

- [ ] **Step 5: Commit the RED contracts**

```bash
git add tests/test_sector_research_packs.py
git commit -m "test(sectors): define research pack contracts"
```

### Task 2: Add six official Raw source cards

**Files:**
- Create: `raw/official/united-states/eia-open-data.md`
- Create: `raw/official/global/opec-annual-statistical-bulletin.md`
- Create: `raw/official/global/bis-basel-framework.md`
- Create: `raw/official/united-states/fdic-bankfind-call-reports.md`
- Create: `raw/official/united-states/census-monthly-retail-trade.md`
- Create: `raw/official/mainland/nbs-retail-sales-methodology.md`

- [ ] **Step 1: Add energy cards**

Use canonical URLs `https://www.eia.gov/opendata/documentation.php` and `https://www.opec.org/opec_web/en/publications/202.htm` (fall back to the canonical OPEC publication landing page if this route redirects). Record EIA API-key requirements without a key, public-domain reuse with attribution, API version drift, weekly/monthly/annual frequencies, units and revision risk. Treat OPEC as producer-published statistics with incentive conflict; summarize only and do not redistribute its PDF/data.

- [ ] **Step 2: Add financial cards**

Use `https://www.bis.org/basel_framework/` and `https://banks.data.fdic.gov/bankfind-suite/`. Record that Basel is a global minimum framework whose local implementation differs and has effective-date versions. Record FDIC quarterly Call Report coverage, 1,100+ fields, field definitions, institution identifier/history, revisions, US-only scope, and public API/bulk availability.

- [ ] **Step 3: Add consumer cards**

Use `https://www.census.gov/retail/data.html` and `https://www.stats.gov.cn/zs/tjws/zytjzbqs/shxfp/202410/t20241025_1957174.html`. Record nominal versus real sales, seasonal adjustment, advance/preliminary/final revision, samples and industry classifications. Explicitly state that aggregate retail sales do not identify any listed company’s revenue.

- [ ] **Step 4: Run Raw audits**

Run: `.venv/bin/pytest tests/test_sector_research_packs.py::test_sector_raw_cards_disclose_provenance_and_limits tests/test_raw_collection.py -q`

Expected: Raw-card contract passes; remaining sector-pack tests still fail because Wiki and Output are absent.

- [ ] **Step 5: Commit Raw cards**

```bash
git add raw/official
git commit -m "data(sectors): catalog official sector sources"
```

### Task 3: Synthesize three sector Wiki pages

**Files:**
- Create: `wiki/sectors/能源.md`
- Create: `wiki/sectors/金融.md`
- Create: `wiki/sectors/消费.md`
- Modify: `wiki/sectors/周期行业研究.md`

- [ ] **Step 1: Write the energy page**

Cover upstream/midstream/downstream, demand in physical units, production/spare capacity/inventory, spot versus futures and differentials, lifting/finding/refining costs, reserves, capex and free cash flow. Connect each metric to income statement, balance sheet and cash flow, and distinguish global commodity exposure from A/HK/US company exposure.

- [ ] **Step 2: Write the financials page**

Separate banks, insurers and brokers. For banks, define earning assets, funding, NIM, credit cost, NPL/coverage, CET1/RWA, liquidity and duration gap. Explain why deposits are operating inputs rather than ordinary debt and why P/B requires ROE, capital and loss-cycle context. Identify local regulatory implementation as a required source for company work.

- [ ] **Step 3: Write the consumer page**

Separate staples/discretionary and brands/retailers/platform channels. Define volume-price-mix, same-store sales, store cohort maturity, gross margin bridge, inventory/markdowns, returns, customer acquisition and working capital. Separate nominal macro sales from real volume and company revenue.

- [ ] **Step 4: Strengthen the generic sector framework**

Add an industry-type decision tree and links to the three applications. Preserve `status: seed` in page frontmatter if the current Wiki status vocabulary expects it; coverage status remains the authoritative `reviewed` state. Add a warning that a template is not validated until frozen-data cases include failed hypotheses.

- [ ] **Step 5: Run Wiki lint and focused contracts**

Run: `.venv/bin/python -m investkb.cli wiki lint && .venv/bin/pytest tests/test_sector_research_packs.py -q`

Expected: Wiki contracts pass; template/reachability/coverage assertions remain RED.

- [ ] **Step 6: Commit the synthesis**

```bash
git add wiki/sectors
git commit -m "docs(sectors): synthesize three industry frameworks"
```

### Task 4: Add pre-registered sector evidence cards

**Files:**
- Create: `output/templates/能源周期证据卡.md`
- Create: `output/templates/银行资产负债表证据卡.md`
- Create: `output/templates/消费单位经济证据卡.md`

- [ ] **Step 1: Add energy evidence fields**

Require thesis and falsifier; EIA/OPEC vintage and retrieval; inventory, production, spare capacity, curve and company exposure; price/FX/cost bridge; capex lag; benchmark; historical availability; sensitivity and reproduction command.

- [ ] **Step 2: Add banking evidence fields**

Require entity/perimeter and reporting currency; Call Report/filing period and public date; NIM, deposit beta/mix, duration, NPL/charge-offs/provisions, CET1/RWA; restatement mapping; peer benchmark; stress loss and reproduction command.

- [ ] **Step 3: Add consumer evidence fields**

Require channel/geography/category, store cohort and same-store definition; price/volume/mix; gross margin, markdown/returns, inventory and working capital; CPI/FX/acquisition effects; peer benchmark; failure condition and reproduction command.

- [ ] **Step 4: Verify template contract**

Run: `.venv/bin/pytest tests/test_sector_research_packs.py -q`

Expected: only index and coverage assertions remain RED.

- [ ] **Step 5: Commit templates**

```bash
git add output/templates
git commit -m "docs(sectors): add preregistered evidence cards"
```

### Task 5: Integrate navigation, lessons and coverage

**Files:**
- Modify: `raw/source-catalog.md`
- Modify: `wiki/index.md`
- Modify: `wiki/dashboard.md`
- Modify: `output/README.md`
- Modify: `mkdocs.yml`
- Modify: `wiki/methods/经验与失败教训.md`
- Modify: `wiki/log.md`
- Modify: `config/knowledge-coverage.yaml`
- Regenerate: `output/reports/knowledge-coverage.md`

- [ ] **Step 1: Update curated indexes and site navigation**

Add the three sectors and templates to all required entrypoints. Update the Raw catalog count and describe the six official sector sources. Keep Obsidian links canonical and MkDocs paths explicit.

- [ ] **Step 2: Record reusable failures**

Append lessons covering: macro aggregate growth is not a company revenue proxy; advance/revised series create historical-time leakage; producer or regulator data has scope/incentive boundaries; and cross-jurisdiction Basel labels do not imply identical capital definitions. Each lesson must include failure, consequence, prevention and regression evidence.

- [ ] **Step 3: Update coverage honestly**

For `sector-energy`, `sector-financials`, and `sector-consumer`, set `status: reviewed`, list one Wiki, one Raw card and one sector template, and keep a gap for a frozen-data company/time-series case. Do not promote `sector-framework`; change its gap to require three completed frozen-data cases with positive and negative outcomes.

- [ ] **Step 4: Regenerate and validate coverage**

Run:

```bash
.venv/bin/python -m investkb.cli coverage validate
.venv/bin/python -m investkb.cli coverage report --output output/reports/knowledge-coverage.md
cp output/reports/knowledge-coverage.md /tmp/sector-coverage.md
.venv/bin/python -m investkb.cli coverage report --output output/reports/knowledge-coverage.md
cmp /tmp/sector-coverage.md output/reports/knowledge-coverage.md
```

Expected: all commands exit 0 and the two reports are byte-identical.

- [ ] **Step 5: Run focused contracts GREEN**

Run: `.venv/bin/pytest tests/test_sector_research_packs.py tests/test_coverage.py tests/test_wiki.py tests/test_site.py -q`

Expected: PASS.

- [ ] **Step 6: Commit integration**

```bash
git add raw/source-catalog.md wiki output/README.md output/reports/knowledge-coverage.md mkdocs.yml config/knowledge-coverage.yaml
git commit -m "docs(sectors): integrate research packs and lessons"
```

### Task 6: Verify, review and publish through PR

**Files:**
- Modify only if verification exposes an in-scope defect.

- [ ] **Step 1: Run the complete local gate**

Run: `scripts/verify.sh`

Expected: Ruff, full Pytest, coverage, Raw/Wiki integrity, public boundary, offline report and strict site build all pass.

- [ ] **Step 2: Audit the public diff**

Run:

```bash
git diff --check origin/main...HEAD
git diff --stat origin/main...HEAD
git grep -nEi 'cookie|authorization:|api[_-]?key\s*[:=]|token\s*[:=]' origin/main..HEAD -- . ':!docs/superpowers/**'
git status --short
```

Expected: no whitespace error, no credential material, and a clean worktree.

- [ ] **Step 3: Self-review against Issue #15**

Verify every acceptance item using current files and test output. Correct any unsupported claim before publication; do not count empty templates as completed empirical cases.

- [ ] **Step 4: Push and open the PR**

Push `codex/sector-research-packs`. Open a ready PR titled `docs(sectors): add energy financials and consumer research packs`, link `Closes #15`, list sources/retrieval date, coverage change, tests, residual gaps and public/private audit.

- [ ] **Step 5: Wait for all required checks and merge**

Inspect Python 3.11, Python 3.12, Raw and Wiki integrity, Offline backtest report, Strict static site build, Public/private boundary and PR policy. Fix failures through additional commits. Squash merge only when all are green, then confirm `origin/main` and GitHub Pages contain the merged content.
