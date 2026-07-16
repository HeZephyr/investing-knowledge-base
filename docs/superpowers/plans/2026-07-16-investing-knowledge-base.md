# A 股与港股理财知识库 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 建成一个 Obsidian 友好、来源可追溯、能获取免费 A/HK 日线数据并运行无未来函数回测的中文理财知识库第一版。

**Architecture:** 仓库以不可变 `raw`、LLM 维护 `wiki`、可再生 `output` 为主层；Python 包将数据提供商、标准化、校验、回测与报告拆成独立模块。所有外部事实通过来源卡引用，行情缓存与第三方源码缓存不进入 Git。

**Tech Stack:** Python 3.11+、pandas、NumPy、PyArrow、Typer、Pydantic、PyYAML、Matplotlib、AKShare、BaoStock、pytest、Ruff、Markdown、Obsidian、Git/GitHub。

---

## 文件职责图

```text
README.md / wiki/dashboard.md       用户入口与学习导航
AGENTS.md                           摄取、查询、维护、量化纪律
raw/**                              来源卡、合法快照、外部仓库档案
wiki/**                             结构化中文知识与双向链接
src/investkb/sources.py             来源卡解析与审计
src/investkb/data/models.py         标准行情数据契约
src/investkb/data/providers.py      AKShare/BaoStock 适配边界
src/investkb/data/store.py          Parquet 缓存与复现清单
src/investkb/validation/market.py   行情质量规则
src/investkb/metrics.py             绩效与风险指标
src/investkb/backtest/engine.py     次日成交、费用与持仓状态机
src/investkb/strategies.py          无状态信号函数
src/investkb/reporting.py           Markdown/CSV/PNG 报告
src/investkb/cli.py                 统一命令行入口
tests/**                            固定夹具与核心正确性测试
```

## Phase 1：仓库、Obsidian 与治理

### Task 1：项目骨架与开发环境

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `.python-version`
- Create: `.obsidian/app.json`
- Create: `.obsidian/appearance.json`
- Create: `.obsidian/core-plugins.json`
- Create: `src/investkb/__init__.py`
- Test: `tests/test_package.py`

- [x] **Step 1: 写包导入失败测试**

```python
def test_package_exposes_version() -> None:
    import investkb
    assert investkb.__version__ == "0.1.0"
```

- [x] **Step 2: 运行测试并确认失败**

Run: `python -m pytest tests/test_package.py -q`
Expected: FAIL，提示无法导入 `investkb`。

- [x] **Step 3: 建立最小包、依赖与工具配置**

```toml
[project]
name = "investkb"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["pandas>=2.2", "numpy>=2", "pyarrow>=17", "pydantic>=2.8", "pyyaml>=6", "typer>=0.12", "matplotlib>=3.9"]

[project.optional-dependencies]
data = ["akshare>=1.17", "baostock>=0.8.9"]
dev = ["pytest>=8", "pytest-cov>=5", "ruff>=0.6"]

[project.scripts]
investkb = "investkb.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py311"
```

`src/investkb/__init__.py`：

```python
__version__ = "0.1.0"
```

`.gitignore` 必须忽略 `.venv/`、`data/cache/`、`data/reference-repos/`、`__pycache__/`、`.pytest_cache/`、`.ruff_cache/`、`*.parquet` 和 Obsidian 工作区状态文件。

- [x] **Step 4: 创建虚拟环境、安装并运行测试**

Run: `python3 -m venv .venv && .venv/bin/pip install -e '.[dev,data]' && .venv/bin/pytest -q`
Expected: PASS。

- [x] **Step 5: 提交骨架**

Run: `git add .gitignore .python-version .obsidian pyproject.toml src tests && git commit -m "build: scaffold investkb project"`

### Task 2：README、AGENTS 与目录入口

**Files:**
- Create: `README.md`
- Create: `AGENTS.md`
- Create: `wiki/dashboard.md`
- Create: `wiki/index.md`
- Create: `wiki/log.md`
- Create: `raw/README.md`
- Create: `output/README.md`
- Test: `tests/test_repository_docs.py`

- [x] **Step 1: 写入口文档契约测试**

```python
from pathlib import Path

def test_required_repository_entrypoints_exist() -> None:
    for path in ["README.md", "AGENTS.md", "wiki/dashboard.md", "wiki/index.md", "wiki/log.md", "raw/README.md", "output/README.md"]:
        assert Path(path).is_file(), path

def test_readme_links_learning_dashboard() -> None:
    assert "wiki/dashboard.md" in Path("README.md").read_text()
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/test_repository_docs.py -q`
Expected: FAIL，列出缺失入口文件。

- [x] **Step 3: 写清用户与代理工作流**

README 必须包含风险声明、目录说明、Obsidian 打开方式、5 分钟开始、安装命令、首个数据命令、首个回测命令和学习入口。AGENTS 必须包含 Raw 不可变规则、来源等级、摄取/查询/lint 流程、引用规则、TDD、数据质量、禁止未来函数、报告必备字段和日志格式。

日志格式固定为：

```markdown
## [YYYY-MM-DD] ingest|query|lint|research | 标题
- changed: [[页面]]
- sources: raw-id
- result: 一句话结果
```

- [x] **Step 4: 运行文档测试**

Run: `.venv/bin/pytest tests/test_repository_docs.py -q`
Expected: PASS。

- [x] **Step 5: 提交治理文档**

Run: `git add README.md AGENTS.md raw output wiki tests/test_repository_docs.py && git commit -m "docs: add Obsidian and agent workflows"`

## Phase 2：Raw 与 Wiki

### Task 3：来源卡格式与审计器

**Files:**
- Create: `src/investkb/sources.py`
- Create: `tests/test_sources.py`
- Create: `raw/source-catalog.md`
- Create: `raw/repositories/catalog.md`

- [x] **Step 1: 写来源卡审计失败测试**

```python
from pathlib import Path
from investkb.sources import audit_source_card

def test_source_card_requires_traceability(tmp_path: Path) -> None:
    card = tmp_path / "bad.md"
    card.write_text("---\nid: x\ntitle: X\n---\n")
    errors = audit_source_card(card)
    assert "url" in errors
    assert "retrieved" in errors
    assert "source_grade" in errors
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/test_sources.py -q`
Expected: FAIL，提示 `investkb.sources` 不存在。

- [x] **Step 3: 实现 YAML frontmatter 审计**

```python
REQUIRED = {"id", "title", "publisher", "url", "retrieved", "source_grade", "markets", "usage"}

def audit_source_card(path: Path) -> list[str]:
    metadata = parse_frontmatter(path.read_text(encoding="utf-8"))
    return sorted(REQUIRED - metadata.keys())
```

解析器必须拒绝没有成对 `---` 的文件，并把 YAML 根节点非字典视为格式错误。

- [x] **Step 4: 运行测试与 lint**

Run: `.venv/bin/pytest tests/test_sources.py -q && .venv/bin/ruff check src tests`
Expected: PASS。

- [x] **Step 5: 提交来源契约**

Run: `git add src/investkb/sources.py tests/test_sources.py raw && git commit -m "feat: add auditable source cards"`

### Task 4：首批官方与开源 Raw

**Files:**
- Create: `raw/official/mainland/*.md`
- Create: `raw/official/hong-kong/*.md`
- Create: `raw/books-and-papers/*.md`
- Create: `raw/repositories/cards/*.md`
- Create: `raw/repositories/manifest.yaml`
- Create: `scripts/snapshot_reference_repo.sh`
- Test: `tests/test_raw_collection.py`

- [x] **Step 1: 写覆盖面和许可证测试**

```python
from pathlib import Path
from investkb.sources import audit_source_card

def test_raw_collection_has_minimum_coverage() -> None:
    cards = list(Path("raw").glob("**/*.md"))
    source_cards = [p for p in cards if p.name not in {"README.md", "catalog.md", "source-catalog.md"}]
    assert len(source_cards) >= 30
    assert all(not audit_source_card(path) for path in source_cards)

def test_reference_repo_cards_record_license_and_commit() -> None:
    for path in Path("raw/repositories/cards").glob("*.md"):
        text = path.read_text()
        assert "license:" in text
        assert "pinned_commit:" in text
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/test_raw_collection.py -q`
Expected: FAIL，来源数量不足。

- [x] **Step 3: 建立不少于 30 张首批来源卡**

官方来源至少覆盖证监会、上交所、深交所、北交所、中基协、港交所、香港证监会、投委会；开源来源至少覆盖 ExploreFinance、AKShare、BaoStock、Qlib、RQAlpha、Backtesting.py、Pyfolio/Empyrical、Awesome Quant。每张卡写来源摘要、可采用内容、限制、关联 Wiki 主题；未知许可证使用 `license: NOASSERTION` 和 `usage: link-and-analyze-only`。

- [x] **Step 4: 实现安全浅克隆脚本并审计**

脚本接口：

```bash
scripts/snapshot_reference_repo.sh <https-url> <commit> <target-name>
```

它只允许 `https://github.com/` URL，目标固定在 `data/reference-repos/`，执行 `git clone --filter=blob:none --no-checkout` 后 checkout 固定 commit，拒绝空 commit 或含 `/..` 的目标名。

Run: `.venv/bin/pytest tests/test_raw_collection.py -q && .venv/bin/python -c 'from pathlib import Path; from investkb.sources import audit_source_card; cards=list(Path("raw").glob("**/*.md")); errors={str(p): audit_source_card(p) for p in cards if p.name not in {"README.md", "catalog.md", "source-catalog.md"}}; assert not any(errors.values()), errors; print(len(errors), "source cards audited")'`
Expected: PASS，输出来源卡总数和零错误。

- [x] **Step 5: 提交首批 Raw**

Run: `git add raw scripts tests/test_raw_collection.py && git commit -m "docs: curate initial official and open-source raw corpus"`

### Task 5：Wiki 知识网络与 lint

**Files:**
- Create: `src/investkb/wiki.py`
- Create: `tests/test_wiki.py`
- Create: `wiki/markets/*.md`
- Create: `wiki/products/*.md`
- Create: `wiki/concepts/*.md`
- Create: `wiki/risk/*.md`
- Create: `wiki/quant/*.md`
- Create: `wiki/glossary/*.md`
- Create: `wiki/learning-path.md`

- [x] **Step 1: 写断链、孤儿页与来源引用测试**

```python
from investkb.wiki import lint_wiki

def test_wiki_has_no_broken_links_or_missing_sources() -> None:
    report = lint_wiki("wiki", "raw")
    assert report.broken_links == []
    assert report.missing_sources == []
    assert report.orphans == []
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/test_wiki.py -q`
Expected: FAIL，提示 Wiki lint 未实现或页面缺失。

- [x] **Step 3: 实现双链与来源 lint**

扫描 `[[页面]]`，按文件 stem 与 frontmatter aliases 建索引；忽略代码围栏；检查 `sources` 中的 ID 存在于 Raw；`dashboard`、`index`、`log` 不判为孤儿。

- [x] **Step 4: 建立不少于 35 个首批 Wiki 页面**

必须覆盖学习路线、A/HK 市场差异、订单与费用、股票/指数/ETF/基金、财报三表、估值、分散、回撤、行为偏差、收益率、复权、基准、未来函数、幸存者偏差、过拟合、样本外和交易成本。每页包含统一 frontmatter、相关双链和 Raw 来源 ID。

Run: `.venv/bin/pytest tests/test_wiki.py -q && .venv/bin/python -c 'from investkb.wiki import lint_wiki; r=lint_wiki("wiki", "raw"); assert not (r.broken_links or r.missing_sources or r.orphans), r; print("wiki lint passed")'`
Expected: PASS，零断链、零缺来源、零关键孤儿页。

- [x] **Step 5: 提交 Wiki 基线**

Run: `git add src/investkb/wiki.py tests/test_wiki.py wiki && git commit -m "docs: build beginner A-share and HK wiki"`

## Phase 3：免费数据与质量控制

### Task 6：标准行情契约与 Parquet 存储

**Files:**
- Create: `src/investkb/data/models.py`
- Create: `src/investkb/data/store.py`
- Create: `tests/data/test_models.py`
- Create: `tests/data/test_store.py`

- [x] **Step 1: 写标准化与往返测试**

```python
def test_bar_frame_normalizes_columns(sample_bars):
    frame = normalize_bars(sample_bars, market="CN", symbol="510300", currency="CNY", provider="fixture", adjustment="qfq")
    assert list(frame.columns) == EXPECTED_BAR_COLUMNS
    assert str(frame["date"].dtype).startswith("datetime64")

def test_parquet_round_trip(tmp_path, normalized_bars):
    store = ParquetStore(tmp_path)
    manifest = store.write_bars(normalized_bars)
    assert store.read_bars("CN", "510300").equals(normalized_bars)
    assert manifest.sha256
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/data/test_models.py tests/data/test_store.py -q`
Expected: FAIL，模块不存在。

- [x] **Step 3: 实现确定性 schema 与原子写入**

字段固定为 `market,symbol,date,open,high,low,close,volume,amount,currency,adjustment,provider,retrieved_at`；按 `market/symbol/year.parquet` 分区，先写临时文件再原子替换；manifest 记录参数、行数、日期范围、版本与 SHA-256。

- [x] **Step 4: 运行测试**

Run: `.venv/bin/pytest tests/data -q`
Expected: PASS。

- [x] **Step 5: 提交数据契约**

Run: `git add src/investkb/data tests/data && git commit -m "feat: add normalized market data store"`

### Task 7：AKShare 与 BaoStock 适配器

**Files:**
- Create: `src/investkb/data/providers.py`
- Create: `tests/data/test_providers.py`
- Create: `configs/providers.yaml`

- [x] **Step 1: 写依赖注入的适配测试**

```python
def test_akshare_cn_adapter_maps_vendor_columns(fake_akshare):
    bars = AKShareProvider(client=fake_akshare).daily_bars("CN", "510300", date(2024, 1, 1), date(2024, 1, 31), "qfq")
    assert bars.iloc[0]["provider"] == "akshare"
    assert bars.iloc[0]["symbol"] == "510300"

def test_provider_rejects_empty_response(fake_empty_akshare):
    with pytest.raises(DataUnavailableError, match="empty"):
        AKShareProvider(client=fake_empty_akshare).daily_bars("HK", "00700", START, END, "qfq")
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/data/test_providers.py -q`
Expected: FAIL，适配器不存在。

- [x] **Step 3: 实现提供商协议和显式错误**

`MarketDataProvider.daily_bars(market, symbol, start, end, adjustment)` 返回标准 frame；CN/HK 路由到已核验的 AKShare 接口，BaoStock 只接受 CN；捕获上游异常并保留原异常类型和接口名，不返回空 frame。

- [x] **Step 4: 跑离线测试与标记的网络 smoke test**

Run: `.venv/bin/pytest tests/data/test_providers.py -q`
Expected: PASS。

Run: `.venv/bin/pytest -m network -q`
Expected: 在网络可用时抓取一只 A 股 ETF 和一只港股；接口不可用时给出可诊断失败而非伪造数据。

- [x] **Step 5: 提交数据适配器**

Run: `git add src/investkb/data/providers.py tests/data/test_providers.py configs/providers.yaml && git commit -m "feat: add free A-share and HK data adapters"`

### Task 8：行情质量校验

**Files:**
- Create: `src/investkb/validation/market.py`
- Create: `tests/validation/test_market.py`
- Create: `configs/validation.yaml`

- [x] **Step 1: 写坏数据夹具测试**

```python
@pytest.mark.parametrize("mutation,code", [
    ("duplicate", "duplicate-key"),
    ("negative", "non-positive-price"),
    ("bad_ohlc", "ohlc-inconsistent"),
    ("unsorted", "date-order"),
])
def test_validate_bars_reports_structured_issues(good_bars, mutation, code):
    issues = validate_bars(mutate(good_bars, mutation))
    assert code in {issue.code for issue in issues}
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/validation/test_market.py -q`
Expected: FAIL，校验器不存在。

- [x] **Step 3: 实现结构化校验问题**

每个问题包含 `code,severity,row,message`；error 阻止落地/回测，warning 进入 manifest。实现主键、日期顺序、OHLC、正价格、非负成交量、缺口、极端跳变与复权连续性规则。

- [x] **Step 4: 运行校验测试**

Run: `.venv/bin/pytest tests/validation -q`
Expected: PASS。

- [x] **Step 5: 提交质量规则**

Run: `git add src/investkb/validation tests/validation configs/validation.yaml && git commit -m "feat: validate market data quality"`

## Phase 4：回测、报告与端到端体验

### Task 9：绩效指标

**Files:**
- Create: `src/investkb/metrics.py`
- Create: `tests/test_metrics.py`

- [x] **Step 1: 写手算指标测试**

```python
def test_max_drawdown_from_known_equity_curve():
    equity = pd.Series([100.0, 120.0, 90.0, 108.0])
    assert max_drawdown(equity) == pytest.approx(-0.25)

def test_metrics_reject_too_short_series():
    with pytest.raises(ValueError, match="two observations"):
        performance_summary(pd.Series([1.0]))
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/test_metrics.py -q`
Expected: FAIL。

- [x] **Step 3: 实现指标并明确年化口径**

实现 total return、CAGR、annualized volatility、max drawdown、Sharpe、Sortino、Calmar、win rate；默认 252 个交易日，无风险利率作为显式参数；零波动返回 `None` 而非无穷大。

- [x] **Step 4: 运行测试**

Run: `.venv/bin/pytest tests/test_metrics.py -q`
Expected: PASS。

- [x] **Step 5: 提交指标**

Run: `git add src/investkb/metrics.py tests/test_metrics.py && git commit -m "feat: add transparent performance metrics"`

### Task 10：无未来函数回测引擎

**Files:**
- Create: `src/investkb/backtest/models.py`
- Create: `src/investkb/backtest/engine.py`
- Create: `tests/backtest/test_engine.py`
- Create: `configs/markets.yaml`

- [x] **Step 1: 写次日成交与费用测试**

```python
def test_close_signal_executes_next_open(sample_bars):
    signal = pd.Series([0, 1, 1, 0], index=sample_bars.index)
    result = run_backtest(sample_bars, signal, initial_cash=10_000, fee=FeeModel(commission_rate=0.001, minimum_commission=0, stamp_duty_rate=0))
    assert result.trades.iloc[0]["date"] == sample_bars.iloc[2]["date"]
    assert result.trades.iloc[0]["price"] == sample_bars.iloc[2]["open"]

def test_sell_cost_includes_market_tax(sample_bars):
    result = run_round_trip(sample_bars, FeeModel(commission_rate=0, minimum_commission=0, stamp_duty_rate=0.001))
    assert result.trades.iloc[-1]["fees"] > 0
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/backtest/test_engine.py -q`
Expected: FAIL。

- [x] **Step 3: 实现逐日状态机**

收盘信号只在下一可交易日开盘执行；处理现金、整手、佣金最低额、卖出税、滑点、停牌/零成交量；输出 equity、positions、orders、trades 和 assumptions。第一版只允许 long/cash，拒绝负仓位和杠杆。

- [x] **Step 4: 运行回测测试**

Run: `.venv/bin/pytest tests/backtest -q`
Expected: PASS，手算现金和持仓完全一致。

- [x] **Step 5: 提交引擎**

Run: `git add src/investkb/backtest tests/backtest configs/markets.yaml && git commit -m "feat: add next-session daily backtester"`

### Task 11：策略、报告和模板

**Files:**
- Create: `src/investkb/strategies.py`
- Create: `src/investkb/reporting.py`
- Create: `tests/test_strategies.py`
- Create: `tests/test_reporting.py`
- Create: `output/templates/*.md`
- Create: `configs/strategies/*.yaml`

- [x] **Step 1: 写信号不偷看和报告字段测试**

```python
def test_moving_average_signal_uses_only_current_and_past_prices(prices):
    original = moving_average_signal(prices, fast=2, slow=3)
    changed = prices.copy(); changed.iloc[-1] *= 100
    revised = moving_average_signal(changed, fast=2, slow=3)
    pd.testing.assert_series_equal(original.iloc[:-1], revised.iloc[:-1])

def test_report_contains_reproducibility_sections(tmp_path, backtest_result):
    path = build_report(backtest_result, tmp_path)
    text = path.read_text()
    for heading in ["数据", "假设", "费用", "基准", "结果", "限制", "复现命令"]:
        assert heading in text
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/test_strategies.py tests/test_reporting.py -q`
Expected: FAIL。

- [x] **Step 3: 实现基准、均线、定投与报告**

策略只返回目标仓位或信号，不接触资金状态；报告生成 `report.md`、`metrics.csv`、`equity.csv`、`trades.csv` 和 `equity.png`。模板至少包含投资政策书、公司分析、基金分析、回测计划、交易前检查和复盘。

- [x] **Step 4: 运行测试**

Run: `.venv/bin/pytest tests/test_strategies.py tests/test_reporting.py -q`
Expected: PASS。

- [x] **Step 5: 提交策略与输出**

Run: `git add src/investkb/strategies.py src/investkb/reporting.py tests output/templates configs/strategies && git commit -m "feat: add beginner strategies and reproducible reports"`

### Task 12：CLI、教程与端到端验收

**Files:**
- Create: `src/investkb/cli.py`
- Create: `tests/test_cli.py`
- Create: `notebooks/README.md`
- Create: `notebooks/01_认识收益与风险.ipynb`
- Create: `notebooks/02_获取并检查行情.ipynb`
- Create: `notebooks/03_第一个无未来函数回测.ipynb`
- Create: `scripts/verify.sh`
- Modify: `README.md`
- Modify: `wiki/log.md`

- [x] **Step 1: 写 CLI 端到端测试**

```python
def test_cli_help_and_offline_demo(runner):
    assert runner.invoke(app, ["--help"]).exit_code == 0
    result = runner.invoke(app, ["demo", "backtest", "--offline"])
    assert result.exit_code == 0
    assert Path("output/reports/demo/report.md").exists()
```

- [x] **Step 2: 运行测试并确认失败**

Run: `.venv/bin/pytest tests/test_cli.py -q`
Expected: FAIL。

- [x] **Step 3: 实现统一 CLI**

命令必须包含：

```text
investkb sources audit [PATH]
investkb wiki lint
investkb data fetch MARKET SYMBOL --start --end --adjustment
investkb data validate MARKET SYMBOL
investkb backtest run CONFIG
investkb demo backtest --offline
```

离线 demo 使用提交到 `tests/fixtures/` 的小型合成行情，不冒充真实市场数据；网络命令将 provider 和抓取时间写入 manifest。

- [x] **Step 4: 创建编号教程并运行全量验证**

Run: `scripts/verify.sh`
Expected: Ruff 通过、全部 pytest 通过、Raw 审计通过、Wiki lint 通过、离线报告生成成功。

- [x] **Step 5: 提交端到端版本**

Run: `git add README.md wiki/log.md src/investkb/cli.py tests notebooks scripts/verify.sh && git commit -m "feat: deliver end-to-end investing knowledge base"`

### Task 13：GitHub 私有仓库与最终验收

**Files:**
- Modify: `README.md`
- Create: `docs/verification/first-release.md`

- [x] **Step 1: 检查敏感信息和大文件**

Run: `git status --short && git ls-files | rg '(^data/cache|\.env$|reference-repos|\.parquet$)'`
Expected: 工作树干净；第二个命令无输出。

- [x] **Step 2: 运行最终验证并记录环境**

Run: `scripts/verify.sh && .venv/bin/python -V && git log --oneline --decorate -15`
Expected: 所有检查 PASS；把版本、测试数、Raw/Wiki 数量和已知限制写入验证报告。

- [x] **Step 3: 创建同名 GitHub 私有仓库**

优先使用已安装 GitHub 连接器；若不可用，安装并使用 GitHub CLI。仓库名固定 `investing-knowledge-base`，visibility 固定 `private`，禁止用 `public` 作为降级策略。

- [x] **Step 4: 关联、推送并核验可见性**

Run: `git remote -v && git push -u origin main`
Expected: 推送成功；远程 API/连接器返回 `private: true`，默认分支为 `main`。

- [x] **Step 5: 提交最终验证报告（若第 2 步产生变更）**

Run: `git add docs/verification/first-release.md README.md && git commit -m "docs: record first release verification" && git push`
Expected: 本地与远程 main 一致。

## 自检结果

- 设计稿 1–12 节均映射到上述 Task 1–13。
- 第一版边界保持为日线/周线、研究与回测，不包含实盘和分钟级。
- Raw、Wiki、数据、回测均有独立测试和阶段提交。
- 类型命名统一：标准行情为 bar frame，策略返回 signal/target，回测输出 result。
- 未保留占位实现；网络不稳定由离线夹具和显式 smoke test 分离。
