# 知识库覆盖审计

- 清单日期：2026-07-18
- 仓库就绪度，不是预期收益：**98.7%**
- 需求总数：135

> v2 基线变更：清单从粗主题升级为原子能力；分母扩大导致的分数下降不表示成果被删除。
> validated 只证明所声明的原子阶段满足证据组合；不保证投资收益，也不替代其他阶段。

## 分轴状态

| 维度 | missing | seed | reviewed | validated | 就绪度 |
|---|---:|---:|---:|---:|---:|
| 基础学科 | 0 | 0 | 0 | 20 | 100.0% |
| 市场 | 0 | 0 | 0 | 16 | 100.0% |
| 资产与产品 | 0 | 0 | 0 | 18 | 100.0% |
| 行业 | 0 | 0 | 0 | 18 | 100.0% |
| 公司研究 | 0 | 0 | 0 | 16 | 100.0% |
| 研究方法 | 0 | 0 | 0 | 18 | 100.0% |
| 组合与风控 | 0 | 0 | 0 | 14 | 100.0% |
| 工程与维护 | 1 | 1 | 0 | 13 | 88.3% |

## 分能力阶段状态

| 阶段 | 含义 | missing | seed | reviewed | validated | 就绪度 |
|---|---|---:|---:|---:|---:|---:|
| `content-ready` | 内容就绪 | 0 | 0 | 0 | 73 | 100.0% |
| `exercise-tested` | 练习已测 | 1 | 1 | 0 | 43 | 96.1% |
| `case-validated` | 案例验证 | 0 | 0 | 0 | 11 | 100.0% |
| `maintenance-live` | 维护在线 | 0 | 0 | 0 | 6 | 100.0% |

## 逐项证据与缺口

| ID | 维度 | 阶段 | 要求 | 状态 | 最后核验 | 证据 | 缺口 |
|---|---|---|---|---|---|---|---|
| `asset-bond-math` | 资产与产品 | `exercise-tested` | 债券定价、久期与凸性 | validated | 2026-07-17 | `synthesis:wiki/products/债券.md`<br>`implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | — |
| `asset-cash` | 资产与产品 | `content-ready` | 现金与货币基金 | validated | 2026-07-18 | `synthesis:wiki/products/货币基金.md`<br>`source:raw/official/united-states/sec-money-market-funds.md` | — |
| `asset-commodities` | 资产与产品 | `content-ready` | 大宗商品现货与期货曲线 | validated | 2026-07-17 | `source:raw/official/united-states/cftc-futures-basics.md`<br>`source:raw/official/united-states/eia-open-data.md`<br>`synthesis:wiki/assets/大宗商品.md` | — |
| `asset-convertible` | 资产与产品 | `content-ready` | 可转债条款与风险 | validated | 2026-07-18 | `synthesis:wiki/products/可转债.md`<br>`source:raw/official/mainland/sse-convertible-bonds.md`<br>`implementation:src/investkb/assets.py`<br>`test:tests/test_assets.py` | — |
| `asset-credit-bonds` | 资产与产品 | `content-ready` | 信用债、评级与违约 | validated | 2026-07-17 | `source:raw/official/united-states/sec-bond-bulletins.md`<br>`source:raw/official/global/bis-debt-statistics.md`<br>`synthesis:wiki/products/债券.md` | — |
| `asset-derivatives` | 资产与产品 | `content-ready` | 衍生品权利义务与保证金 | validated | 2026-07-18 | `synthesis:wiki/products/衍生品.md`<br>`source:raw/official/united-states/cftc-derivatives-framework.md` | — |
| `asset-equity` | 资产与产品 | `content-ready` | 股票所有权与现金流权利 | validated | 2026-07-18 | `synthesis:wiki/products/股票.md`<br>`source:raw/official/united-states/sec-stocks-ownership.md` | — |
| `asset-etf` | 资产与产品 | `content-ready` | ETF 结构、交易与跟踪误差 | validated | 2026-07-17 | `synthesis:wiki/products/ETF.md`<br>`source:raw/official/mainland/sse-etf.md` | — |
| `asset-futures` | 资产与产品 | `content-ready` | 期货合约、交割与保证金 | validated | 2026-07-18 | `source:raw/official/united-states/cftc-derivatives-framework.md`<br>`synthesis:wiki/assets/大宗商品.md`<br>`report:output/cases/futures-roll.md`<br>`test:tests/test_assets.py` | — |
| `asset-fx` | 资产与产品 | `content-ready` | 外汇报价与汇率风险 | validated | 2026-07-17 | `synthesis:wiki/concepts/汇率风险.md`<br>`source:raw/official/global/fred-exchange-rates.md` | — |
| `asset-gold` | 资产与产品 | `content-ready` | 黄金定价与基准 | validated | 2026-07-17 | `synthesis:wiki/assets/黄金.md`<br>`source:raw/official/global/lbma-gold-benchmark.md` | — |
| `asset-government-bonds` | 资产与产品 | `content-ready` | 国债与收益率曲线 | validated | 2026-07-18 | `source:raw/official/united-states/us-treasury-yield-curve.md`<br>`source:raw/official/mainland/chinabond-government-curve.md`<br>`synthesis:wiki/products/债券.md` | — |
| `asset-index` | 资产与产品 | `content-ready` | 指数编制与基准治理 | validated | 2026-07-18 | `synthesis:wiki/products/指数.md`<br>`source:raw/official/global/sp-index-mathematics.md`<br>`implementation:src/investkb/assets.py`<br>`test:tests/test_assets.py` | — |
| `asset-mutual-fund` | 资产与产品 | `content-ready` | 公募基金结构与费用 | validated | 2026-07-17 | `synthesis:wiki/products/公募基金.md`<br>`source:raw/official/mainland/csrc-fund-law.md` | — |
| `asset-options-math` | 资产与产品 | `exercise-tested` | 期权收益、希腊字母与波动率 | validated | 2026-07-18 | `synthesis:wiki/products/期权与波动率.md`<br>`implementation:src/investkb/assets.py`<br>`test:tests/test_assets.py` | — |
| `asset-overseas-etf` | 资产与产品 | `content-ready` | 海外 ETF 与跨币种暴露 | validated | 2026-07-18 | `synthesis:wiki/products/海外ETF.md`<br>`source:raw/official/united-states/irs-overseas-etf-taxes.md`<br>`source:raw/official/united-states/irs-nonresident-estate-tax.md`<br>`implementation:src/investkb/assets.py`<br>`test:tests/test_assets.py` | — |
| `asset-reit` | 资产与产品 | `content-ready` | REIT 结构与现金流 | validated | 2026-07-18 | `synthesis:wiki/products/REIT.md`<br>`source:raw/official/mainland/sse-infrastructure-reits.md`<br>`source:raw/official/hong-kong/hkex-reits.md`<br>`source:raw/official/united-states/sec-reits.md` | — |
| `asset-structured-products` | 资产与产品 | `content-ready` | 结构化产品与路径依赖 | validated | 2026-07-18 | `synthesis:wiki/products/结构化产品.md`<br>`source:raw/official/united-states/sec-structured-notes.md`<br>`implementation:src/investkb/assets.py`<br>`test:tests/test_assets.py` | — |
| `company-capital-allocation` | 公司研究 | `content-ready` | 资本配置与再投资回报 | validated | 2026-07-17 | `source:raw/experts/cards/damodaran-valuation.md`<br>`synthesis:wiki/company/资本配置治理与稀释.md` | — |
| `company-case-negative` | 公司研究 | `case-validated` | 公司研究负结果与放弃案例 | validated | 2026-07-17 | `source:raw/cases/healthcare/manifest.yaml`<br>`report:output/cases/company-negative.md`<br>`test:tests/test_public_evidence_cases.py` | — |
| `company-case-positive` | 公司研究 | `case-validated` | 公司研究正结果冻结案例 | validated | 2026-07-17 | `source:raw/cases/company-positive/manifest.yaml`<br>`report:output/cases/company-positive.md`<br>`test:tests/test_public_evidence_cases.py` | — |
| `company-cash-conversion` | 公司研究 | `exercise-tested` | 营运资本与现金转换 | validated | 2026-07-17 | `implementation:src/investkb/company.py`<br>`test:tests/test_company_research.py` | — |
| `company-comparables` | 公司研究 | `content-ready` | 可比公司与估值倍数 | validated | 2026-07-17 | `source:raw/experts/cards/damodaran-valuation.md`<br>`synthesis:wiki/company/估值实验室.md` | — |
| `company-dilution` | 公司研究 | `exercise-tested` | 股权激励、增发与稀释计算 | validated | 2026-07-17 | `implementation:src/investkb/company.py`<br>`test:tests/test_company_research.py` | — |
| `company-disclosure` | 公司研究 | `content-ready` | 法定披露与公告检索 | validated | 2026-07-17 | `source:raw/official/united-states/investor-edgar-research.md`<br>`synthesis:wiki/company/法定披露与历史时点.md` | — |
| `company-earnings-quality` | 公司研究 | `content-ready` | 盈利质量与应计分析 | validated | 2026-07-17 | `source:raw/official/global/ifrs-ias-7.md`<br>`synthesis:wiki/concepts/盈利质量.md` | — |
| `company-governance` | 公司研究 | `content-ready` | 治理、激励与关联交易 | validated | 2026-07-17 | `source:raw/official/united-states/sec-edgar.md`<br>`synthesis:wiki/company/资本配置治理与稀释.md` | — |
| `company-point-in-time` | 公司研究 | `exercise-tested` | 按当时可得信息重建公司档案 | validated | 2026-07-17 | `implementation:src/investkb/company.py`<br>`test:tests/test_company_research.py` | — |
| `company-reconciliation` | 公司研究 | `exercise-tested` | 三表重建与勾稽练习 | validated | 2026-07-17 | `implementation:src/investkb/company.py`<br>`test:tests/test_company_research.py` | — |
| `company-revenue` | 公司研究 | `content-ready` | 收入确认与合同经济 | validated | 2026-07-17 | `source:raw/official/global/ifrs-15.md`<br>`synthesis:wiki/company/收入确认与合同经济.md` | — |
| `company-reverse-dcf` | 公司研究 | `exercise-tested` | 反向 DCF 与市场隐含预期 | validated | 2026-07-17 | `implementation:src/investkb/company.py`<br>`test:tests/test_company_research.py` | — |
| `company-scenarios` | 公司研究 | `exercise-tested` | 多情景估值与敏感性 | validated | 2026-07-17 | `implementation:src/investkb/company.py`<br>`test:tests/test_company_research.py` | — |
| `company-three-statements` | 公司研究 | `content-ready` | 三表结构与勾稽关系 | validated | 2026-07-17 | `source:raw/official/global/ifrs-ias-1.md`<br>`synthesis:wiki/concepts/财务三表.md` | — |
| `company-valuation-content` | 公司研究 | `content-ready` | 绝对与相对估值框架 | validated | 2026-07-17 | `synthesis:wiki/concepts/估值.md`<br>`source:raw/experts/cards/damodaran-valuation.md` | — |
| `engineering-audit-plugin` | 工程与维护 | `exercise-tested` | 第三方仓库与 Skill 供应链审计插件 | validated | 2026-07-17 | `implementation:plugins/investing-research/scripts/audit_repository.py`<br>`implementation:plugins/investing-research/skills/audit-finance-skills/SKILL.md`<br>`test:tests/test_investing_research_plugin.py`<br>`test:tests/test_finance_skill_audit.py` | — |
| `engineering-ci` | 工程与维护 | `maintenance-live` | 多版本 CI 与保护检查 | validated | 2026-07-17 | `workflow:.github/workflows/ci.yml`<br>`test:tests/test_github_workflows.py` | — |
| `engineering-coverage` | 工程与维护 | `exercise-tested` | 机器可审计覆盖报告 | validated | 2026-07-17 | `implementation:src/investkb/coverage.py`<br>`test:tests/test_coverage.py` | — |
| `engineering-data-adapters` | 工程与维护 | `exercise-tested` | A股、港股与基金免费数据适配 | validated | 2026-07-17 | `implementation:src/investkb/data/providers.py`<br>`test:tests/data/test_providers.py` | — |
| `engineering-dependencies` | 工程与维护 | `maintenance-live` | 依赖更新与兼容性守护 | validated | 2026-07-17 | `workflow:.github/dependabot.yml`<br>`test:tests/test_github_workflows.py` | — |
| `engineering-global-data` | 工程与维护 | `exercise-tested` | 美股、韩国与全球免费数据适配 | seed | 2026-07-17 | `source:raw/repositories/cards/yfinance.md` | 缺标准化适配器、公司行动和离线契约测试 |
| `engineering-link-health` | 工程与维护 | `maintenance-live` | 来源链接健康检查 | validated | 2026-07-17 | `workflow:.github/workflows/link-check.yml`<br>`test:tests/test_github_workflows.py` | — |
| `engineering-maintenance-skill` | 工程与维护 | `exercise-tested` | 可复用知识库维护 Skill | validated | 2026-07-17 | `implementation:skills/maintain-investing-knowledge-base/SKILL.md`<br>`test:tests/test_knowledge_skill.py` | — |
| `engineering-offline-store` | 工程与维护 | `exercise-tested` | 离线数据缓存与可重复运行 | validated | 2026-07-17 | `implementation:src/investkb/data/store.py`<br>`test:tests/data/test_store.py` | — |
| `engineering-pages` | 工程与维护 | `maintenance-live` | 可搜索互动 GitHub Pages | validated | 2026-07-17 | `workflow:.github/workflows/pages.yml`<br>`test:tests/test_site.py` | — |
| `engineering-private-research` | 工程与维护 | `exercise-tested` | 私人观察池、持仓与决策日志 | missing | 2026-07-17 | — | 用户暂无持仓；需在本地 private 层建立不公开的投资政策与观察池 |
| `engineering-provider-monitoring` | 工程与维护 | `maintenance-live` | 免费数据源定时烟测 | validated | 2026-07-17 | `workflow:.github/workflows/provider-smoke.yml`<br>`test:tests/test_github_workflows.py` | — |
| `engineering-public-boundary` | 工程与维护 | `exercise-tested` | 公开与私人边界 | validated | 2026-07-17 | `implementation:src/investkb/publication.py`<br>`test:tests/test_public_boundary.py` | — |
| `engineering-reporting` | 工程与维护 | `exercise-tested` | 可复现研究报告生成 | validated | 2026-07-17 | `implementation:src/investkb/reporting.py`<br>`test:tests/test_reporting.py` | — |
| `engineering-source-lineage` | 工程与维护 | `exercise-tested` | Raw 来源谱系审计 | validated | 2026-07-17 | `implementation:src/investkb/sources.py`<br>`test:tests/test_sources.py` | — |
| `foundation-accounting-accrual` | 基础学科 | `content-ready` | 权责发生制与会计判断 | validated | 2026-07-18 | `source:raw/official/global/ifrs-15.md`<br>`synthesis:wiki/concepts/盈利质量.md`<br>`test:tests/test_company_research.py` | — |
| `foundation-accounting-statements` | 基础学科 | `content-ready` | 会计恒等式与三张报表 | validated | 2026-07-18 | `source:raw/official/global/ifrs-ias-1.md`<br>`synthesis:wiki/concepts/财务三表.md`<br>`test:tests/test_company_research.py` | — |
| `foundation-calculus` | 基础学科 | `content-ready` | 投资所需微积分与优化 | validated | 2026-07-18 | `source:raw/courses/mit-calculus.md`<br>`synthesis:wiki/foundations/投资数学与优化.md` | — |
| `foundation-compounding` | 基础学科 | `exercise-tested` | 复利、贴现与年化换算 | validated | 2026-07-17 | `implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | — |
| `foundation-corporate-finance` | 基础学科 | `content-ready` | 公司金融基础 | validated | 2026-07-17 | `source:raw/courses/mit-finance-theory.md`<br>`synthesis:wiki/foundations/公司金融基础.md` | — |
| `foundation-distributions` | 基础学科 | `content-ready` | 常见分布与厚尾 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/概率与收益分布.md` | — |
| `foundation-estimation` | 基础学科 | `exercise-tested` | 点估计、区间估计与不确定性 | validated | 2026-07-17 | `implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | — |
| `foundation-hypothesis` | 基础学科 | `exercise-tested` | 假设检验、效应量与多重检验 | validated | 2026-07-18 | `synthesis:wiki/foundations/假设检验与多重比较.md`<br>`implementation:src/investkb/advanced_foundations.py`<br>`test:tests/test_advanced_foundations.py` | — |
| `foundation-linear-algebra` | 基础学科 | `content-ready` | 投资所需线性代数 | validated | 2026-07-18 | `source:raw/courses/mit-linear-algebra.md`<br>`synthesis:wiki/foundations/投资数学与优化.md` | — |
| `foundation-macroeconomics` | 基础学科 | `content-ready` | 宏观经济账户与周期 | validated | 2026-07-18 | `source:raw/official/united-states/bea-national-accounts.md`<br>`synthesis:wiki/foundations/宏观账户周期与货币传导.md` | — |
| `foundation-market-history` | 基础学科 | `content-ready` | 金融史与市场危机 | validated | 2026-07-18 | `source:raw/official/united-states/federal-reserve-history-crises.md`<br>`synthesis:wiki/foundations/金融危机与机制复盘.md` | — |
| `foundation-microeconomics` | 基础学科 | `content-ready` | 微观经济与产业组织 | validated | 2026-07-18 | `source:raw/books-and-papers/openstax-principles-economics.md`<br>`synthesis:wiki/foundations/微观经济与产业组织.md` | — |
| `foundation-monetary-policy` | 基础学科 | `content-ready` | 货币政策与利率传导 | validated | 2026-07-18 | `source:raw/official/united-states/federal-reserve-monetary-policy.md`<br>`synthesis:wiki/foundations/宏观账户周期与货币传导.md` | — |
| `foundation-probability` | 基础学科 | `content-ready` | 概率与条件概率 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/概率与收益分布.md` | — |
| `foundation-random-variables` | 基础学科 | `content-ready` | 随机变量与期望方差 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/概率与收益分布.md` | — |
| `foundation-reading-papers` | 基础学科 | `exercise-tested` | 阅读论文与复现实证 | validated | 2026-07-18 | `synthesis:wiki/foundations/论文阅读与复现.md`<br>`implementation:src/investkb/evidence_cases.py`<br>`test:tests/test_public_evidence_cases.py` | — |
| `foundation-regression` | 基础学科 | `exercise-tested` | 线性回归与诊断 | validated | 2026-07-18 | `synthesis:wiki/foundations/回归与诊断.md`<br>`implementation:src/investkb/advanced_foundations.py`<br>`test:tests/test_advanced_foundations.py` | — |
| `foundation-sampling` | 基础学科 | `content-ready` | 抽样、选择偏差与误差 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/抽样与估计.md` | — |
| `foundation-statistical-coding` | 基础学科 | `exercise-tested` | Python 统计计算基础 | validated | 2026-07-18 | `implementation:src/investkb/advanced_foundations.py`<br>`test:tests/test_advanced_foundations.py`<br>`report:pyproject.toml` | — |
| `foundation-tvm` | 基础学科 | `content-ready` | 货币时间价值 | validated | 2026-07-17 | `source:raw/books-and-papers/openstax-principles-finance.md`<br>`synthesis:wiki/foundations/复利与贴现.md` | — |
| `market-calendar-monitor` | 市场 | `maintenance-live` | 全球交易日历持续校验 | validated | 2026-07-18 | `workflow:.github/workflows/market-calendar-smoke.yml`<br>`test:tests/test_market_calendar.py` | — |
| `market-cn-execution` | 市场 | `exercise-tested` | A 股订单、涨跌停与结算练习 | validated | 2026-07-18 | `implementation:src/investkb/market_operations.py`<br>`test:tests/test_market_operations.py` | — |
| `market-cn-rules` | 市场 | `content-ready` | A 股交易与披露规则 | validated | 2026-07-17 | `synthesis:wiki/markets/A股市场.md`<br>`source:raw/official/mainland/sse-trading-rules.md` | — |
| `market-corporate-actions` | 市场 | `exercise-tested` | 分红、拆并股、配股与退市处理 | validated | 2026-07-18 | `implementation:src/investkb/market_operations.py`<br>`test:tests/test_market_operations.py` | — |
| `market-cross-border` | 市场 | `content-ready` | 沪深港通与跨境访问 | validated | 2026-07-18 | `source:raw/official/hong-kong/hkex-stock-connect-operations.md`<br>`synthesis:wiki/markets/沪深港通.md` | — |
| `market-emerging-rules` | 市场 | `content-ready` | 新兴市场访问框架 | validated | 2026-07-17 | `source:raw/official/global/imf-areaer.md`<br>`source:raw/official/global/world-bank-gfdd.md`<br>`synthesis:wiki/markets/新兴市场访问.md` | — |
| `market-europe-rules` | 市场 | `content-ready` | 欧盟主要市场与 UCITS | validated | 2026-07-17 | `source:raw/official/europe/esma-trading.md`<br>`source:raw/official/europe/eu-investment-funds-ucits.md`<br>`synthesis:wiki/markets/欧盟市场.md` | — |
| `market-hk-fees` | 市场 | `content-ready` | 港股费用与风险 | validated | 2026-07-17 | `synthesis:wiki/markets/交易费用.md`<br>`source:raw/official/hong-kong/hkex-transaction-fees.md` | — |
| `market-hk-rules` | 市场 | `content-ready` | 港股交易与披露规则 | validated | 2026-07-17 | `synthesis:wiki/markets/港股市场.md`<br>`source:raw/official/hong-kong/hkex-trading-rules.md` | — |
| `market-japan-rules` | 市场 | `content-ready` | 日本交易与披露规则 | validated | 2026-07-17 | `source:raw/official/japan/jpx-trading-clearing.md`<br>`source:raw/official/japan/fsa-edinet.md`<br>`synthesis:wiki/markets/日本市场.md` | — |
| `market-korea-rules` | 市场 | `content-ready` | 韩国交易与披露规则 | validated | 2026-07-17 | `synthesis:wiki/markets/韩国股市.md`<br>`source:raw/official/korea/krx-investment-guide.md` | — |
| `market-microstructure` | 市场 | `content-ready` | 市场微观结构 | validated | 2026-07-18 | `source:raw/official/united-states/sec-execution-settlement.md`<br>`synthesis:wiki/markets/市场微观结构.md` | — |
| `market-settlement` | 市场 | `content-ready` | 清算、结算与托管 | validated | 2026-07-18 | `source:raw/official/united-states/dtcc-clearing-custody.md`<br>`synthesis:wiki/markets/清算结算与托管.md` | — |
| `market-uk-rules` | 市场 | `content-ready` | 英国交易与披露规则 | validated | 2026-07-18 | `source:raw/official/united-kingdom/fca-markets-disclosure.md`<br>`synthesis:wiki/markets/英国市场.md` | — |
| `market-us-disclosure` | 市场 | `content-ready` | 美股披露与投资者保护 | validated | 2026-07-17 | `synthesis:wiki/markets/美股市场.md`<br>`source:raw/official/united-states/sec-edgar.md` | — |
| `market-us-execution` | 市场 | `exercise-tested` | 美股订单执行、费用与公司行动 | validated | 2026-07-18 | `implementation:src/investkb/market_operations.py`<br>`test:tests/test_market_operations.py` | — |
| `method-backtest` | 研究方法 | `exercise-tested` | 无未来函数日线回测 | validated | 2026-07-17 | `implementation:src/investkb/backtest/engine.py`<br>`test:tests/backtest/test_engine.py` | — |
| `method-behavior-lessons` | 研究方法 | `content-ready` | 行为偏差、经验与失败教训 | validated | 2026-07-18 | `source:raw/experts/cards/shiller-yale-financial-markets.md`<br>`synthesis:wiki/risk/行为偏差.md` | — |
| `method-causal-inference` | 研究方法 | `content-ready` | 因果推断与识别假设 | validated | 2026-07-18 | `source:raw/books-and-papers/causal-inference-what-if.md`<br>`synthesis:wiki/methods/因果推断与识别.md` | — |
| `method-costs` | 研究方法 | `exercise-tested` | 换手、费用、滑点与冲击成本 | validated | 2026-07-18 | `implementation:src/investkb/backtest/engine.py`<br>`test:tests/backtest/test_engine.py` | — |
| `method-data-quality` | 研究方法 | `exercise-tested` | 数据质量与历史时点校验 | validated | 2026-07-17 | `synthesis:wiki/quant/数据质量.md`<br>`test:tests/validation/test_market.py` | — |
| `method-event-study` | 研究方法 | `exercise-tested` | 事件研究与公告反应 | validated | 2026-07-18 | `implementation:src/investkb/research_methods.py`<br>`test:tests/test_research_methods.py` | — |
| `method-evidence-matrix` | 研究方法 | `content-ready` | 跨流派证据矩阵 | validated | 2026-07-18 | `source:raw/experts/cards/aqr-data-library.md`<br>`synthesis:wiki/methods/投资研究证据矩阵.md` | — |
| `method-factor-content` | 研究方法 | `content-ready` | 因子定义、组合与风险调整 | validated | 2026-07-18 | `source:raw/experts/cards/kenneth-french-data-library.md`<br>`synthesis:wiki/quant/因子研究.md` | — |
| `method-factor-replication` | 研究方法 | `case-validated` | 公开因子冻结复现 | validated | 2026-07-17 | `source:raw/cases/factor-strategy/manifest.yaml`<br>`report:output/cases/factor-replication.md`<br>`test:tests/test_public_evidence_cases.py` | — |
| `method-lookahead` | 研究方法 | `exercise-tested` | 未来函数识别与防护 | validated | 2026-07-18 | `implementation:src/investkb/company.py`<br>`test:tests/test_company_research.py` | — |
| `method-negative-results` | 研究方法 | `case-validated` | 无效策略与负结果复现 | validated | 2026-07-17 | `source:raw/cases/factor-strategy/manifest.yaml`<br>`report:output/cases/negative-strategy.md`<br>`test:tests/test_public_evidence_cases.py` | — |
| `method-out-of-sample` | 研究方法 | `exercise-tested` | 样本外、滚动与走步验证 | validated | 2026-07-18 | `implementation:src/investkb/research_methods.py`<br>`test:tests/test_research_methods.py` | — |
| `method-overfitting` | 研究方法 | `content-ready` | 回测过拟合与选择偏差 | validated | 2026-07-17 | `synthesis:wiki/quant/过拟合.md`<br>`source:raw/books-and-papers/backtest-overfitting.md` | — |
| `method-preregistration` | 研究方法 | `exercise-tested` | 研究预注册与假设锁定 | validated | 2026-07-18 | `implementation:src/investkb/research_methods.py`<br>`test:tests/test_research_methods.py` | — |
| `method-return-metrics` | 研究方法 | `exercise-tested` | 收益率、年化与复权计算 | validated | 2026-07-17 | `implementation:src/investkb/metrics.py`<br>`test:tests/test_metrics.py` | — |
| `method-risk-metrics` | 研究方法 | `exercise-tested` | 波动率、回撤与风险指标 | validated | 2026-07-17 | `synthesis:wiki/risk/最大回撤.md`<br>`test:tests/test_metrics.py` | — |
| `method-survivorship` | 研究方法 | `content-ready` | 幸存者偏差与退市样本 | validated | 2026-07-18 | `source:raw/books-and-papers/shumway-delisting-bias.md`<br>`synthesis:wiki/quant/幸存者偏差.md` | — |
| `method-time-series` | 研究方法 | `exercise-tested` | 金融时间序列建模 | validated | 2026-07-18 | `implementation:src/investkb/research_methods.py`<br>`test:tests/test_research_methods.py` | — |
| `portfolio-allocation` | 组合与风控 | `exercise-tested` | 战略与战术资产配置 | validated | 2026-07-17 | `implementation:src/investkb/portfolio.py`<br>`test:tests/test_portfolio_lab.py` | — |
| `portfolio-attribution` | 组合与风控 | `exercise-tested` | 绩效归因与费用后评价 | validated | 2026-07-17 | `implementation:src/investkb/portfolio.py`<br>`test:tests/test_portfolio_lab.py` | — |
| `portfolio-benchmark` | 组合与风控 | `content-ready` | 基准选择与主动风险 | validated | 2026-07-17 | `source:raw/books-and-papers/sharpe-mutual-fund-performance.md`<br>`synthesis:wiki/portfolio/基准与绩效归因.md` | — |
| `portfolio-decision-journal` | 组合与风控 | `exercise-tested` | 决策日志与过程评分 | validated | 2026-07-17 | `implementation:src/investkb/portfolio.py`<br>`test:tests/test_portfolio_lab.py` | — |
| `portfolio-diversification` | 组合与风控 | `content-ready` | 分散化与相关性失稳 | validated | 2026-07-17 | `source:raw/books-and-papers/markowitz-portfolio-selection.md`<br>`synthesis:wiki/concepts/分散化.md` | — |
| `portfolio-drawdown` | 组合与风控 | `exercise-tested` | 最大回撤与恢复期 | validated | 2026-07-17 | `synthesis:wiki/risk/最大回撤.md`<br>`test:tests/test_metrics.py` | — |
| `portfolio-goals` | 组合与风控 | `content-ready` | 目标、期限与约束 | validated | 2026-07-17 | `source:raw/official/united-states/investor-asset-allocation.md`<br>`synthesis:wiki/portfolio/投资政策与目标.md` | — |
| `portfolio-ips` | 组合与风控 | `exercise-tested` | 投资政策书与治理 | validated | 2026-07-17 | `implementation:src/investkb/portfolio.py`<br>`test:tests/test_portfolio_lab.py` | — |
| `portfolio-liquidity` | 组合与风控 | `content-ready` | 流动性、容量与变现风险 | validated | 2026-07-17 | `source:raw/official/united-states/sec-fund-liquidity-risk.md`<br>`synthesis:wiki/risk/流动性风险.md` | — |
| `portfolio-position-sizing` | 组合与风控 | `content-ready` | 仓位、容量与风险承受 | validated | 2026-07-17 | `source:raw/official/united-states/investor-asset-allocation.md`<br>`synthesis:wiki/risk/仓位管理.md` | — |
| `portfolio-public-case` | 组合与风控 | `case-validated` | 公开多资产组合冻结案例 | validated | 2026-07-17 | `source:raw/cases/portfolio-public/manifest.yaml`<br>`report:output/cases/portfolio-public.md`<br>`test:tests/test_public_evidence_cases.py` | — |
| `portfolio-rebalancing` | 组合与风控 | `exercise-tested` | 再平衡规则与成本权衡 | validated | 2026-07-17 | `implementation:src/investkb/portfolio.py`<br>`test:tests/test_portfolio_lab.py` | — |
| `portfolio-risk-budget` | 组合与风控 | `exercise-tested` | 风险预算与贡献分解 | validated | 2026-07-17 | `implementation:src/investkb/portfolio.py`<br>`test:tests/test_portfolio_lab.py` | — |
| `portfolio-stress` | 组合与风控 | `exercise-tested` | 情景分析与压力测试 | validated | 2026-07-17 | `implementation:src/investkb/portfolio.py`<br>`test:tests/test_portfolio_lab.py` | — |
| `sector-bank-case` | 行业 | `case-validated` | 银行资产负债表冻结案例 | validated | 2026-07-17 | `source:raw/cases/bank/manifest.yaml`<br>`report:output/cases/bank.md`<br>`test:tests/test_frozen_sector_cases.py` | — |
| `sector-consumer-case` | 行业 | `case-validated` | 消费单位经济冻结案例 | validated | 2026-07-17 | `source:raw/cases/consumer/manifest.yaml`<br>`report:output/cases/consumer.md`<br>`test:tests/test_frozen_sector_cases.py` | — |
| `sector-consumer-content` | 行业 | `content-ready` | 消费量价、渠道与单位经济 | validated | 2026-07-17 | `synthesis:wiki/sectors/消费.md`<br>`source:raw/official/united-states/census-monthly-retail-trade.md` | — |
| `sector-energy-case` | 行业 | `case-validated` | 能源周期冻结数据案例 | validated | 2026-07-17 | `source:raw/cases/energy/manifest.yaml`<br>`report:output/cases/energy.md`<br>`test:tests/test_frozen_sector_cases.py` | — |
| `sector-energy-content` | 行业 | `content-ready` | 能源供需、成本曲线与公司传导 | validated | 2026-07-17 | `synthesis:wiki/sectors/能源.md`<br>`source:raw/official/united-states/eia-open-data.md` | — |
| `sector-financial-content` | 行业 | `content-ready` | 银行、保险与券商分析 | validated | 2026-07-17 | `synthesis:wiki/sectors/金融.md`<br>`source:raw/official/global/bis-basel-framework.md` | — |
| `sector-framework` | 行业 | `content-ready` | 可复用行业研究框架 | validated | 2026-07-18 | `synthesis:wiki/sectors/周期行业研究.md`<br>`source:raw/official/global/un-isic-rev5.md`<br>`implementation:src/investkb/sectors.py`<br>`test:tests/test_sectors.py` | — |
| `sector-healthcare-case` | 行业 | `case-validated` | 医药公司冻结数据案例 | validated | 2026-07-17 | `source:raw/cases/healthcare/manifest.yaml`<br>`report:output/cases/healthcare.md`<br>`test:tests/test_health_internet_memory.py` | — |
| `sector-healthcare-content` | 行业 | `content-ready` | 医药研发、支付与监管 | validated | 2026-07-17 | `synthesis:wiki/sectors/医药医疗.md`<br>`source:raw/official/united-states/fda-clinical-endpoints.md`<br>`source:raw/official/china/nmpa-drug-registration.md` | — |
| `sector-industrials` | 行业 | `content-ready` | 工业、资本品与订单周期 | validated | 2026-07-18 | `synthesis:wiki/sectors/工业与资本品.md`<br>`source:raw/official/united-states/census-m3-orders.md`<br>`implementation:src/investkb/sectors.py`<br>`test:tests/test_sectors.py` | — |
| `sector-insurance-content` | 行业 | `content-ready` | 保险负债、准备金与投资端 | validated | 2026-07-18 | `synthesis:wiki/sectors/金融.md`<br>`source:raw/official/global/ifrs-17-insurance-contracts.md`<br>`source:raw/official/global/iais-insurance-capital-standard.md`<br>`implementation:src/investkb/sectors.py`<br>`test:tests/test_sectors.py` | — |
| `sector-internet-case` | 行业 | `case-validated` | 互联网平台冻结数据案例 | validated | 2026-07-17 | `source:raw/cases/internet/manifest.yaml`<br>`report:output/cases/internet.md`<br>`test:tests/test_health_internet_memory.py` | — |
| `sector-internet-content` | 行业 | `content-ready` | 互联网平台网络效应与变现 | validated | 2026-07-17 | `synthesis:wiki/sectors/互联网平台.md`<br>`source:raw/official/united-states/ftc-platform-data-practices.md`<br>`source:raw/official/europe/eu-digital-markets-act.md` | — |
| `sector-materials-mining` | 行业 | `content-ready` | 材料与矿业成本曲线 | validated | 2026-07-18 | `synthesis:wiki/sectors/材料与矿业.md`<br>`source:raw/official/united-states/usgs-mineral-summaries-2026.md`<br>`source:raw/official/united-states/sec-mining-subpart-1300.md`<br>`implementation:src/investkb/sectors.py`<br>`test:tests/test_sectors.py` | — |
| `sector-memory-case` | 行业 | `case-validated` | 存储周期冻结数据案例 | validated | 2026-07-17 | `source:raw/cases/memory/manifest.yaml`<br>`report:output/cases/memory.md`<br>`test:tests/test_health_internet_memory.py` | — |
| `sector-memory-content` | 行业 | `content-ready` | 存储半导体供需与技术代际 | validated | 2026-07-17 | `synthesis:wiki/sectors/存储半导体.md`<br>`source:raw/official/global/jedec-memory-standards.md` | — |
| `sector-real-estate` | 行业 | `content-ready` | 地产开发、运营与融资 | validated | 2026-07-18 | `synthesis:wiki/sectors/地产开发与运营.md`<br>`source:raw/official/united-states/census-housing-construction.md`<br>`source:raw/official/global/ifrs-15.md`<br>`source:raw/official/global/ifrs-ias-7.md`<br>`implementation:src/investkb/sectors.py`<br>`test:tests/test_sectors.py` | — |
| `sector-technology-hardware` | 行业 | `content-ready` | 硬件与半导体产业链 | validated | 2026-07-18 | `synthesis:wiki/sectors/硬件与半导体产业链.md`<br>`source:raw/official/united-states/nist-semiconductor-supply-chain.md`<br>`source:raw/official/global/tsmc-2025-20f.md`<br>`implementation:src/investkb/sectors.py`<br>`test:tests/test_sectors.py` | — |
