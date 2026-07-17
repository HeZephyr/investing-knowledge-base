# Research Streams Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close Issue #9 with three traceable public research-source cards, a cross-stream evidence matrix, and a reusable empirical-evidence template.

**Architecture:** Keep source-specific facts and terms in append-safe Raw cards, synthesize only cited claims in one Wiki method page, and put reusable reproduction requirements in an Output template. Content-contract tests enforce provenance, conflicts, licensing, limitations, data frequency, point-in-time risk, and index reachability.

**Tech Stack:** Markdown/YAML frontmatter, Python 3.11+, pytest, Ruff, MkDocs Material, existing `investkb` Raw/Wiki/publication audits.

---

### Task 1: Add failing content-contract tests

**Files:**
- Modify: `tests/test_raw_collection.py`
- Modify: `tests/test_global_scope.py`

- [ ] **Step 1: Write the failing Raw-card test**

Append this test to `tests/test_raw_collection.py`:

```python
def test_research_stream_cards_disclose_provenance_conflicts_and_limits() -> None:
    expected = {
        "shiller-yale-financial-markets.md": "raw-expert-shiller-yale-financial-markets",
        "aqr-data-library.md": "raw-research-aqr-data-library",
        "gmo-research-library.md": "raw-expert-gmo-research-library",
    }
    card_root = Path("raw/experts/cards")

    for filename, source_id in expected.items():
        path = card_root / filename
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text)
        assert metadata["id"] == source_id
        assert metadata["retrieved"].isoformat() == "2026-07-17"
        assert metadata["license"]
        for section in ("利益冲突", "许可与条款", "局限与失效条件"):
            assert f"## {section}" in text

    aqr = (card_root / "aqr-data-library.md").read_text(encoding="utf-8")
    for disclosure in ("字段与频率", "月度", "日度", "假设组合", "时间偏差"):
        assert disclosure in aqr
```

- [ ] **Step 2: Write the failing reachability test**

Append this test to `tests/test_global_scope.py`:

```python
def test_research_evidence_matrix_and_output_template_are_reachable() -> None:
    matrix = ROOT / "wiki/methods/投资研究证据矩阵.md"
    template = ROOT / "output/templates/实证证据卡.md"
    index = (ROOT / "wiki/index.md").read_text(encoding="utf-8")
    dashboard = (ROOT / "wiki/dashboard.md").read_text(encoding="utf-8")
    output_index = (ROOT / "output/README.md").read_text(encoding="utf-8")

    assert matrix.is_file()
    assert template.is_file()
    assert "[[投资研究证据矩阵]]" in index
    assert "[[投资研究证据矩阵]]" in dashboard
    assert "实证证据卡" in output_index
```

- [ ] **Step 3: Run the focused tests and verify RED**

Run:

```bash
.venv/bin/pytest -q tests/test_raw_collection.py tests/test_global_scope.py
```

Expected: failure because `raw/experts/cards/shiller-yale-financial-markets.md` and `wiki/methods/投资研究证据矩阵.md` do not exist.

- [ ] **Step 4: Commit the failing tests**

```bash
git add tests/test_raw_collection.py tests/test_global_scope.py
git commit -m "test: define research stream content contracts"
```

### Task 2: Add the three Raw source cards

**Files:**
- Create: `raw/experts/cards/shiller-yale-financial-markets.md`
- Create: `raw/experts/cards/aqr-data-library.md`
- Create: `raw/experts/cards/gmo-research-library.md`
- Modify: `raw/experts/catalog.md`
- Modify: `raw/source-catalog.md`

- [ ] **Step 1: Create the Yale card**

Use this frontmatter and section contract, followed by concise Chinese summaries of the verified official pages:

```markdown
---
id: raw-expert-shiller-yale-financial-markets
title: Robert Shiller — Financial Markets (ECON 252, 2011)
publisher: Open Yale Courses, Yale University
url: https://oyc.yale.edu/economics/econ-252
retrieved: 2026-07-17
source_grade: C
markets: [全球, 美股]
usage: link-and-summarize
license: CC-BY-NC-SA-3.0-US
---
# Shiller / Yale《金融市场》

## 原始材料与范围

## 更新频率与数据

## 利益冲突

## 许可与条款

## 局限与失效条件
```

State that the course was recorded in Spring 2011, includes 23 lectures on risk management, institutions, and behavioral finance, is static educational material, and cannot establish current market rules. Record that most Yale-authored material is CC BY-NC-SA 3.0 US while third-party material is excluded.

- [ ] **Step 2: Create the AQR card**

Use this exact frontmatter and section contract:

```markdown
---
id: raw-research-aqr-data-library
title: AQR Data Library
publisher: AQR Capital Management, LLC
url: https://www.aqr.com/Insights/Datasets/About-the-AQR-Data-Library
retrieved: 2026-07-17
source_grade: B
markets: [全球, 美股]
usage: link-and-analyze-only
license: NOASSERTION
---
# AQR Data Library

## 原始材料与范围

## 更新频率与数据

### 字段与频率

## 利益冲突

## 许可与条款

## 局限与失效条件
```

Record paper-linked hypothetical portfolio return series, long-only excess returns and long/short premia, monthly and selected daily frequency, frozen paper samples versus updated extensions, the April 30, 2026 QMJ monthly/daily examples, AQR's requested citation, no stated reusable data license, manager product incentives, schema/method revision risk, publication and time bias, implementation costs, shorting, and capacity.

- [ ] **Step 3: Create the GMO card**

Use this exact frontmatter and section contract:

```markdown
---
id: raw-expert-gmo-research-library
title: GMO Research Library
publisher: GMO LLC
url: https://www.gmo.com/
retrieved: 2026-07-17
source_grade: C
markets: [全球, 美股]
usage: link-and-summarize
license: NOASSERTION
---
# GMO Research Library

## 原始材料与范围

## 更新频率与数据

## 利益冲突

## 许可与条款

## 局限与失效条件
```

Record the library filters, seven-year forecast stream, valuation and mean-reversion focus, asset-manager incentives, personal/informational-use terms, public-reproduction and deep-link restrictions, proprietary-model limits, forecast versioning, and unknown timing of mean reversion. Keep only the GMO website root in public frontmatter; do not deep-link the research library.

- [ ] **Step 4: Update both Raw catalogs**

Add one bullet per new card to `raw/experts/catalog.md`, including the non-endorsement and data-use boundaries. Add a short Issue #9 batch paragraph to `raw/source-catalog.md` naming Yale, AQR, and GMO and stating that downloadable series are not redistributed.

- [ ] **Step 5: Run the Raw audit and focused test**

```bash
.venv/bin/python -m investkb.cli sources audit raw
.venv/bin/pytest -q tests/test_raw_collection.py
```

Expected: source audit passes with 57 cards; the Raw-card test passes.

- [ ] **Step 6: Commit the Raw layer**

```bash
git add raw/experts/cards raw/experts/catalog.md raw/source-catalog.md
git commit -m "content: add behavioral factor and valuation sources"
```

### Task 3: Add Wiki synthesis and Output template

**Files:**
- Create: `wiki/methods/投资研究证据矩阵.md`
- Create: `output/templates/实证证据卡.md`
- Modify: `wiki/methods/公开投资框架.md`
- Modify: `wiki/index.md`
- Modify: `wiki/dashboard.md`
- Modify: `wiki/log.md`
- Modify: `output/README.md`

- [ ] **Step 1: Create the matrix Wiki page**

Start with this frontmatter and required structure:

```markdown
---
title: 投资研究证据矩阵
aliases: [跨流派证据矩阵, 研究流派矩阵]
category: methods
markets: [全球, 美股]
level: intermediate
status: seed
sources: [raw-expert-shiller-yale-financial-markets, raw-research-aqr-data-library, raw-expert-gmo-research-library, raw-research-kenneth-french-data-library]
updated: 2026-07-17
---

# 投资研究证据矩阵

## 如何使用

## 跨流派矩阵

## 从观点到可证伪问题

## 数据时点与实施约束

## 失效条件

## 检查清单

## 相关页面
```

The matrix must compare valuation, quality, momentum, behavior, and macro/asset allocation across Yale/Shiller, AQR, GMO, and the existing Kenneth French source. Explicitly label source facts, testable inferences, unavailable/proprietary fields, costs, look-ahead risk, and falsification conditions. Link to `[[估值]]`, `[[因子研究]]`, `[[行为偏差]]`, `[[样本外测试]]`, `[[换手与交易成本]]`, `[[基准]]`, and `[[数据质量]]`.

- [ ] **Step 2: Create the empirical-evidence template**

Use these exact sections:

```markdown
# 实证证据卡（运行前填写）

## 命题与预注册
- 可证伪命题：
- 预设成功标准：
- 预设失效条件：

## 来源与许可
- Raw 来源 ID 与版本：
- 发布者利益冲突：
- 许可/条款与允许用途：
- 禁止再分发的原始材料：

## 数据谱系
- provider / endpoint / 参数：
- 抓取时间 / 数据截止日：
- 字段 / 频率 / 单位 / 时区：
- 行数 / 内容 SHA-256：
- 历史时点、修订与幸存者处理：

## 研究设计
- 基准 / 费用 / 滑点 / 不可成交：
- 信号可得时点 / 成交时点：
- 训练 / 验证 / 样本外：
- 参数敏感性与尝试次数：

## 结果与限制
- 来源事实：
- 计算结果：
- 推断：
- 局限、冲突与替代解释：

## 复现
```bash
# 写出可从公开输入重建结果的完整命令；不要填写 Cookie、Token 或本地私人路径。
```
```

- [ ] **Step 3: Update indexes and append-only log**

Add `[[投资研究证据矩阵]]` to the methods sections of `wiki/index.md`, `wiki/dashboard.md`, and `wiki/methods/公开投资框架.md`. Add `实证证据卡` to the templates list in `output/README.md`. Append:

```markdown
## [2026-07-17] ingest | 行为、因子与估值研究流
- changed: [[投资研究证据矩阵]], [[公开投资框架]]
- sources: raw-expert-shiller-yale-financial-markets, raw-research-aqr-data-library, raw-expert-gmo-research-library
- result: 建立跨流派可证伪矩阵与许可安全的实证证据模板，不再分发第三方原始数据。
```

- [ ] **Step 4: Run focused tests and Wiki lint**

```bash
.venv/bin/pytest -q tests/test_global_scope.py tests/test_wiki.py tests/test_site.py
.venv/bin/python -m investkb.cli wiki lint
```

Expected: all tests pass; Wiki lint reports no broken links, missing sources, or orphan pages.

- [ ] **Step 5: Commit Wiki and Output layers**

```bash
git add wiki output/README.md output/templates/实证证据卡.md
git commit -m "docs: add cross-stream evidence matrix"
```

### Task 4: Validate and publish through PR

**Files:**
- Modify only if verification finds an in-scope defect.

- [ ] **Step 1: Run every local gate**

```bash
.venv/bin/ruff check src tests
.venv/bin/ruff format --check src tests
.venv/bin/pytest -q
.venv/bin/python -m investkb.cli sources audit raw
.venv/bin/python -m investkb.cli wiki lint
.venv/bin/python -m investkb.publication
tmp="$(mktemp -d)" && (cd "$tmp" && /Users/zephyr/mycode/investing-knowledge-base/.venv/bin/python -m investkb.cli demo backtest --offline && test -s output/reports/demo/report.md && test -s output/reports/demo/equity.png)
.venv/bin/python -m investkb.site
.venv/bin/mkdocs build --strict
```

Expected: Ruff clean, all tests pass, 57 source cards pass, Wiki lint and public boundary pass, offline report artifacts are non-empty, and MkDocs strict build succeeds.

- [ ] **Step 2: Inspect the public diff**

```bash
git status -sb
git diff --check origin/main...HEAD
git diff --stat origin/main...HEAD
git log --oneline origin/main..HEAD
```

Confirm there are no credentials, personal data, caches, third-party source copies, or unindexed pages.

- [ ] **Step 3: Push the topic branch**

```bash
git push -u origin codex/issue-9-research-streams
```

- [ ] **Step 4: Open the pull request**

Create a ready-for-review PR titled `content: add empirical behavioral and valuation research streams` with `Closes #9`, source dates, conflict and license boundaries, tests, risks, and public-boundary checks in the body. Add `codex` and `codex-automation` labels when available.

- [ ] **Step 5: Wait for required checks and verify Pages scope**

Confirm every required PR check is successful. Do not merge. Because Pages deploys only from `main`, verify the current production page remains healthy now and record that the new content will deploy only after reviewed merge.
