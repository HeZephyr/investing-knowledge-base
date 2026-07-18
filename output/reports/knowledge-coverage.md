# 知识库覆盖审计

- 清单日期：2026-07-17
- 仓库就绪度，不是预期收益：**75.4%**
- 需求总数：135

> v2 基线变更：清单从粗主题升级为原子能力；分母扩大导致的分数下降不表示成果被删除。
> validated 只证明所声明的原子阶段满足证据组合；不保证投资收益，也不替代其他阶段。

## 分轴状态

| 维度 | missing | seed | reviewed | validated | 就绪度 |
|---|---:|---:|---:|---:|---:|
| 基础学科 | 6 | 0 | 6 | 8 | 59.5% |
| 市场 | 7 | 0 | 1 | 8 | 54.1% |
| 资产与产品 | 3 | 0 | 8 | 7 | 67.8% |
| 行业 | 4 | 0 | 2 | 12 | 73.9% |
| 公司研究 | 0 | 0 | 0 | 16 | 100.0% |
| 研究方法 | 2 | 1 | 8 | 7 | 69.2% |
| 组合与风控 | 0 | 0 | 0 | 14 | 100.0% |
| 工程与维护 | 1 | 1 | 0 | 13 | 88.3% |

## 分能力阶段状态

| 阶段 | 含义 | missing | seed | reviewed | validated | 就绪度 |
|---|---|---:|---:|---:|---:|---:|
| `content-ready` | 内容就绪 | 16 | 0 | 17 | 40 | 69.9% |
| `exercise-tested` | 练习已测 | 6 | 2 | 8 | 29 | 77.1% |
| `case-validated` | 案例验证 | 0 | 0 | 0 | 11 | 100.0% |
| `maintenance-live` | 维护在线 | 1 | 0 | 0 | 5 | 83.3% |

## 逐项证据与缺口

| ID | 维度 | 阶段 | 要求 | 状态 | 最后核验 | 证据 | 缺口 |
|---|---|---|---|---|---|---|---|
| `asset-bond-math` | 资产与产品 | `exercise-tested` | 债券定价、久期与凸性 | validated | 2026-07-17 | `synthesis:wiki/products/债券.md`<br>`implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | — |
| `asset-cash` | 资产与产品 | `content-ready` | 现金与货币基金 | reviewed | 2026-07-17 | `synthesis:wiki/products/货币基金.md` | 缺收益来源、流动性和信用风险官方来源 |
| `asset-commodities` | 资产与产品 | `content-ready` | 大宗商品现货与期货曲线 | validated | 2026-07-17 | `source:raw/official/united-states/cftc-futures-basics.md`<br>`source:raw/official/united-states/eia-open-data.md`<br>`synthesis:wiki/assets/大宗商品.md` | — |
| `asset-convertible` | 资产与产品 | `content-ready` | 可转债条款与风险 | reviewed | 2026-07-17 | `synthesis:wiki/products/可转债.md` | 缺赎回、转股、信用与估值来源 |
| `asset-credit-bonds` | 资产与产品 | `content-ready` | 信用债、评级与违约 | validated | 2026-07-17 | `source:raw/official/united-states/sec-bond-bulletins.md`<br>`source:raw/official/global/bis-debt-statistics.md`<br>`synthesis:wiki/products/债券.md` | — |
| `asset-derivatives` | 资产与产品 | `content-ready` | 衍生品权利义务与保证金 | missing | 2026-07-17 | — | 缺期权、期货、互换的统一框架 |
| `asset-equity` | 资产与产品 | `content-ready` | 股票所有权与现金流权利 | reviewed | 2026-07-17 | `synthesis:wiki/products/股票.md` | 缺公司法和市场官方来源 |
| `asset-etf` | 资产与产品 | `content-ready` | ETF 结构、交易与跟踪误差 | validated | 2026-07-17 | `synthesis:wiki/products/ETF.md`<br>`source:raw/official/mainland/sse-etf.md` | — |
| `asset-futures` | 资产与产品 | `content-ready` | 期货合约、交割与保证金 | reviewed | 2026-07-17 | `source:raw/official/united-states/cftc-futures-basics.md`<br>`synthesis:wiki/assets/大宗商品.md` | 已有通用合约、交割、保证金与连续合约框架；仍缺逐品种交易所规格和冻结合约链案例 |
| `asset-fx` | 资产与产品 | `content-ready` | 外汇报价与汇率风险 | validated | 2026-07-17 | `synthesis:wiki/concepts/汇率风险.md`<br>`source:raw/official/global/fred-exchange-rates.md` | — |
| `asset-gold` | 资产与产品 | `content-ready` | 黄金定价与基准 | validated | 2026-07-17 | `synthesis:wiki/assets/黄金.md`<br>`source:raw/official/global/lbma-gold-benchmark.md` | — |
| `asset-government-bonds` | 资产与产品 | `content-ready` | 国债与收益率曲线 | reviewed | 2026-07-17 | `source:raw/courses/mit-finance-theory.md`<br>`synthesis:wiki/foundations/债券与利率基础.md` | 已有债券入门；仍缺主要市场官方曲线来源和市场制度 |
| `asset-index` | 资产与产品 | `content-ready` | 指数编制与基准治理 | reviewed | 2026-07-17 | `synthesis:wiki/products/指数.md`<br>`synthesis:wiki/concepts/基准.md` | 缺指数公司方法论和调整案例 |
| `asset-mutual-fund` | 资产与产品 | `content-ready` | 公募基金结构与费用 | validated | 2026-07-17 | `synthesis:wiki/products/公募基金.md`<br>`source:raw/official/mainland/csrc-fund-law.md` | — |
| `asset-options-math` | 资产与产品 | `exercise-tested` | 期权收益、希腊字母与波动率 | missing | 2026-07-17 | — | 缺收益图、定价实现和边界测试 |
| `asset-overseas-etf` | 资产与产品 | `content-ready` | 海外 ETF 与跨币种暴露 | reviewed | 2026-07-17 | `synthesis:wiki/products/海外ETF.md` | 缺税务、遗产税、预扣税和产品来源 |
| `asset-reit` | 资产与产品 | `content-ready` | REIT 结构与现金流 | reviewed | 2026-07-17 | `synthesis:wiki/products/REIT.md` | 缺 A股、港股和美股制度对比 |
| `asset-structured-products` | 资产与产品 | `content-ready` | 结构化产品与路径依赖 | missing | 2026-07-17 | — | 缺条款拆解、发行人信用和压力情景 |
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
| `foundation-accounting-accrual` | 基础学科 | `content-ready` | 权责发生制与会计判断 | reviewed | 2026-07-17 | `synthesis:wiki/concepts/盈利质量.md` | 缺准则来源和应计项目拆解练习 |
| `foundation-accounting-statements` | 基础学科 | `content-ready` | 会计恒等式与三张报表 | reviewed | 2026-07-17 | `synthesis:wiki/concepts/财务三表.md` | 缺准则来源、练习与勾稽案例 |
| `foundation-calculus` | 基础学科 | `content-ready` | 投资所需微积分与优化 | missing | 2026-07-17 | — | 缺导数、凸性和约束优化基础 |
| `foundation-compounding` | 基础学科 | `exercise-tested` | 复利、贴现与年化换算 | validated | 2026-07-17 | `implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | — |
| `foundation-corporate-finance` | 基础学科 | `content-ready` | 公司金融基础 | validated | 2026-07-17 | `source:raw/courses/mit-finance-theory.md`<br>`synthesis:wiki/foundations/公司金融基础.md` | — |
| `foundation-distributions` | 基础学科 | `content-ready` | 常见分布与厚尾 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/概率与收益分布.md` | — |
| `foundation-estimation` | 基础学科 | `exercise-tested` | 点估计、区间估计与不确定性 | validated | 2026-07-17 | `implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | — |
| `foundation-hypothesis` | 基础学科 | `exercise-tested` | 假设检验、效应量与多重检验 | reviewed | 2026-07-17 | `synthesis:wiki/foundations/假设检验与多重比较.md`<br>`implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | 已测 Bonferroni；仍缺效应量、功效和依赖检验练习 |
| `foundation-linear-algebra` | 基础学科 | `content-ready` | 投资所需线性代数 | missing | 2026-07-17 | — | 缺向量、矩阵、协方差与优化基础 |
| `foundation-macroeconomics` | 基础学科 | `content-ready` | 宏观经济账户与周期 | missing | 2026-07-17 | — | 缺国民账户、通胀、就业和周期框架 |
| `foundation-market-history` | 基础学科 | `content-ready` | 金融史与市场危机 | missing | 2026-07-17 | — | 缺跨市场危机时间线与机制复盘 |
| `foundation-microeconomics` | 基础学科 | `content-ready` | 微观经济与产业组织 | missing | 2026-07-17 | — | 缺供需、弹性、竞争结构和定价权体系 |
| `foundation-monetary-policy` | 基础学科 | `content-ready` | 货币政策与利率传导 | missing | 2026-07-17 | — | 缺央行工具、收益率曲线和资产价格传导 |
| `foundation-probability` | 基础学科 | `content-ready` | 概率与条件概率 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/概率与收益分布.md` | — |
| `foundation-random-variables` | 基础学科 | `content-ready` | 随机变量与期望方差 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/概率与收益分布.md` | — |
| `foundation-reading-papers` | 基础学科 | `exercise-tested` | 阅读论文与复现实证 | reviewed | 2026-07-17 | `synthesis:wiki/foundations/论文阅读与复现.md`<br>`test:tests/test_foundations_curriculum.py` | 已有阅读合同；仍缺一篇论文的公开冻结数据复现练习 |
| `foundation-regression` | 基础学科 | `exercise-tested` | 线性回归与诊断 | reviewed | 2026-07-17 | `synthesis:wiki/foundations/回归与诊断.md`<br>`implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | 已测一元 OLS；仍缺稳健误差、残差和影响点诊断练习 |
| `foundation-sampling` | 基础学科 | `content-ready` | 抽样、选择偏差与误差 | validated | 2026-07-17 | `source:raw/books-and-papers/openintro-statistics.md`<br>`synthesis:wiki/foundations/抽样与估计.md` | — |
| `foundation-statistical-coding` | 基础学科 | `exercise-tested` | Python 统计计算基础 | reviewed | 2026-07-17 | `implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | 已测数组与确定性纯函数；仍缺表格、随机种子和环境锁定练习 |
| `foundation-tvm` | 基础学科 | `content-ready` | 货币时间价值 | validated | 2026-07-17 | `source:raw/books-and-papers/openstax-principles-finance.md`<br>`synthesis:wiki/foundations/复利与贴现.md` | — |
| `market-calendar-monitor` | 市场 | `maintenance-live` | 全球交易日历持续校验 | missing | 2026-07-17 | — | 缺免费来源、离线契约和定时监控 |
| `market-cn-execution` | 市场 | `exercise-tested` | A 股订单、涨跌停与结算练习 | missing | 2026-07-17 | — | 缺订单状态机、费用和异常交易练习 |
| `market-cn-rules` | 市场 | `content-ready` | A 股交易与披露规则 | validated | 2026-07-17 | `synthesis:wiki/markets/A股市场.md`<br>`source:raw/official/mainland/sse-trading-rules.md` | — |
| `market-corporate-actions` | 市场 | `exercise-tested` | 分红、拆并股、配股与退市处理 | missing | 2026-07-17 | — | 缺跨市场公司行动数据模型和测试 |
| `market-cross-border` | 市场 | `content-ready` | 沪深港通与跨境访问 | reviewed | 2026-07-17 | `synthesis:wiki/markets/沪深港通.md` | 缺额度、假日、币种、税费和公司行动官方来源 |
| `market-emerging-rules` | 市场 | `content-ready` | 新兴市场访问框架 | validated | 2026-07-17 | `source:raw/official/global/imf-areaer.md`<br>`source:raw/official/global/world-bank-gfdd.md`<br>`synthesis:wiki/markets/新兴市场访问.md` | — |
| `market-europe-rules` | 市场 | `content-ready` | 欧盟主要市场与 UCITS | validated | 2026-07-17 | `source:raw/official/europe/esma-trading.md`<br>`source:raw/official/europe/eu-investment-funds-ucits.md`<br>`synthesis:wiki/markets/欧盟市场.md` | — |
| `market-hk-fees` | 市场 | `content-ready` | 港股费用与风险 | validated | 2026-07-17 | `synthesis:wiki/markets/交易费用.md`<br>`source:raw/official/hong-kong/hkex-transaction-fees.md` | — |
| `market-hk-rules` | 市场 | `content-ready` | 港股交易与披露规则 | validated | 2026-07-17 | `synthesis:wiki/markets/港股市场.md`<br>`source:raw/official/hong-kong/hkex-trading-rules.md` | — |
| `market-japan-rules` | 市场 | `content-ready` | 日本交易与披露规则 | validated | 2026-07-17 | `source:raw/official/japan/jpx-trading-clearing.md`<br>`source:raw/official/japan/fsa-edinet.md`<br>`synthesis:wiki/markets/日本市场.md` | — |
| `market-korea-rules` | 市场 | `content-ready` | 韩国交易与披露规则 | validated | 2026-07-17 | `synthesis:wiki/markets/韩国股市.md`<br>`source:raw/official/korea/krx-investment-guide.md` | — |
| `market-microstructure` | 市场 | `content-ready` | 市场微观结构 | missing | 2026-07-17 | — | 缺价差、深度、冲击成本和价格发现体系 |
| `market-settlement` | 市场 | `content-ready` | 清算、结算与托管 | missing | 2026-07-17 | — | 缺各市场结算周期、失败与托管风险 |
| `market-uk-rules` | 市场 | `content-ready` | 英国交易与披露规则 | missing | 2026-07-17 | — | 缺 FCA、LSE 与税费来源 |
| `market-us-disclosure` | 市场 | `content-ready` | 美股披露与投资者保护 | validated | 2026-07-17 | `synthesis:wiki/markets/美股市场.md`<br>`source:raw/official/united-states/sec-edgar.md` | — |
| `market-us-execution` | 市场 | `exercise-tested` | 美股订单执行、费用与公司行动 | missing | 2026-07-17 | — | 缺官方规则、费用计算和公司行动测试 |
| `method-backtest` | 研究方法 | `exercise-tested` | 无未来函数日线回测 | validated | 2026-07-17 | `implementation:src/investkb/backtest/engine.py`<br>`test:tests/backtest/test_engine.py` | — |
| `method-behavior-lessons` | 研究方法 | `content-ready` | 行为偏差、经验与失败教训 | reviewed | 2026-07-17 | `synthesis:wiki/risk/行为偏差.md`<br>`source:raw/experts/cards/shiller-yale-financial-markets.md`<br>`synthesis:wiki/methods/经验与失败教训.md` | 缺预承诺练习与真实决策日志复盘 |
| `method-causal-inference` | 研究方法 | `content-ready` | 因果推断与识别假设 | missing | 2026-07-17 | — | 缺 DAG、匹配、双重差分和工具变量体系 |
| `method-costs` | 研究方法 | `exercise-tested` | 换手、费用、滑点与冲击成本 | reviewed | 2026-07-17 | `synthesis:wiki/quant/换手与交易成本.md` | 缺分市场费用模型和冲击成本测试 |
| `method-data-quality` | 研究方法 | `exercise-tested` | 数据质量与历史时点校验 | validated | 2026-07-17 | `synthesis:wiki/quant/数据质量.md`<br>`test:tests/validation/test_market.py` | — |
| `method-event-study` | 研究方法 | `exercise-tested` | 事件研究与公告反应 | missing | 2026-07-17 | — | 缺事件窗、基准模型、重叠事件和测试 |
| `method-evidence-matrix` | 研究方法 | `content-ready` | 跨流派证据矩阵 | reviewed | 2026-07-17 | `synthesis:wiki/methods/投资研究证据矩阵.md` | 缺论文层级、外部效度和更新日期审计 |
| `method-factor-content` | 研究方法 | `content-ready` | 因子定义、组合与风险调整 | reviewed | 2026-07-17 | `synthesis:wiki/quant/因子研究.md`<br>`source:raw/experts/cards/kenneth-french-data-library.md` | 缺完整因子谱系和口径比较 |
| `method-factor-replication` | 研究方法 | `case-validated` | 公开因子冻结复现 | validated | 2026-07-17 | `source:raw/cases/factor-strategy/manifest.yaml`<br>`report:output/cases/factor-replication.md`<br>`test:tests/test_public_evidence_cases.py` | — |
| `method-lookahead` | 研究方法 | `exercise-tested` | 未来函数识别与防护 | reviewed | 2026-07-17 | `synthesis:wiki/quant/未来函数.md` | 缺专门的披露时点与特征滞后测试 |
| `method-negative-results` | 研究方法 | `case-validated` | 无效策略与负结果复现 | validated | 2026-07-17 | `source:raw/cases/factor-strategy/manifest.yaml`<br>`report:output/cases/negative-strategy.md`<br>`test:tests/test_public_evidence_cases.py` | — |
| `method-out-of-sample` | 研究方法 | `exercise-tested` | 样本外、滚动与走步验证 | reviewed | 2026-07-17 | `synthesis:wiki/quant/样本外测试.md` | 缺时间切分实现和测试 |
| `method-overfitting` | 研究方法 | `content-ready` | 回测过拟合与选择偏差 | validated | 2026-07-17 | `synthesis:wiki/quant/过拟合.md`<br>`source:raw/books-and-papers/backtest-overfitting.md` | — |
| `method-preregistration` | 研究方法 | `exercise-tested` | 研究预注册与假设锁定 | seed | 2026-07-17 | `template:output/templates/实证证据卡.md` | 缺示例、机器校验和一次真实使用 |
| `method-return-metrics` | 研究方法 | `exercise-tested` | 收益率、年化与复权计算 | validated | 2026-07-17 | `implementation:src/investkb/metrics.py`<br>`test:tests/test_metrics.py` | — |
| `method-risk-metrics` | 研究方法 | `exercise-tested` | 波动率、回撤与风险指标 | validated | 2026-07-17 | `synthesis:wiki/risk/最大回撤.md`<br>`test:tests/test_metrics.py` | — |
| `method-survivorship` | 研究方法 | `content-ready` | 幸存者偏差与退市样本 | reviewed | 2026-07-17 | `synthesis:wiki/quant/幸存者偏差.md` | 缺权威来源和含退市样本案例 |
| `method-time-series` | 研究方法 | `exercise-tested` | 金融时间序列建模 | reviewed | 2026-07-17 | `synthesis:wiki/foundations/时间序列与预测.md`<br>`implementation:src/investkb/education.py`<br>`test:tests/test_education.py` | 已测滚动起点切分；仍缺平稳性、自相关、基线预测和波动模型练习 |
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
| `sector-framework` | 行业 | `content-ready` | 可复用行业研究框架 | reviewed | 2026-07-17 | `synthesis:wiki/sectors/周期行业研究.md` | 缺通用官方分类来源和跨行业练习 |
| `sector-healthcare-case` | 行业 | `case-validated` | 医药公司冻结数据案例 | validated | 2026-07-17 | `source:raw/cases/healthcare/manifest.yaml`<br>`report:output/cases/healthcare.md`<br>`test:tests/test_health_internet_memory.py` | — |
| `sector-healthcare-content` | 行业 | `content-ready` | 医药研发、支付与监管 | validated | 2026-07-17 | `synthesis:wiki/sectors/医药医疗.md`<br>`source:raw/official/united-states/fda-clinical-endpoints.md`<br>`source:raw/official/china/nmpa-drug-registration.md` | — |
| `sector-industrials` | 行业 | `content-ready` | 工业、资本品与订单周期 | missing | 2026-07-17 | — | 缺订单、积压、产能和售后经济体系 |
| `sector-insurance-content` | 行业 | `content-ready` | 保险负债、准备金与投资端 | reviewed | 2026-07-17 | `synthesis:wiki/sectors/金融.md` | 缺偿付能力与会计准则官方来源 |
| `sector-internet-case` | 行业 | `case-validated` | 互联网平台冻结数据案例 | validated | 2026-07-17 | `source:raw/cases/internet/manifest.yaml`<br>`report:output/cases/internet.md`<br>`test:tests/test_health_internet_memory.py` | — |
| `sector-internet-content` | 行业 | `content-ready` | 互联网平台网络效应与变现 | validated | 2026-07-17 | `synthesis:wiki/sectors/互联网平台.md`<br>`source:raw/official/united-states/ftc-platform-data-practices.md`<br>`source:raw/official/europe/eu-digital-markets-act.md` | — |
| `sector-materials-mining` | 行业 | `content-ready` | 材料与矿业成本曲线 | missing | 2026-07-17 | — | 缺品位、回收率、资本开支和成本曲线体系 |
| `sector-memory-case` | 行业 | `case-validated` | 存储周期冻结数据案例 | validated | 2026-07-17 | `source:raw/cases/memory/manifest.yaml`<br>`report:output/cases/memory.md`<br>`test:tests/test_health_internet_memory.py` | — |
| `sector-memory-content` | 行业 | `content-ready` | 存储半导体供需与技术代际 | validated | 2026-07-17 | `synthesis:wiki/sectors/存储半导体.md`<br>`source:raw/official/global/jedec-memory-standards.md` | — |
| `sector-real-estate` | 行业 | `content-ready` | 地产开发、运营与融资 | missing | 2026-07-17 | — | 缺销售、土地、杠杆和区域供需体系 |
| `sector-technology-hardware` | 行业 | `content-ready` | 硬件与半导体产业链 | missing | 2026-07-17 | — | 缺晶圆、封测、设备和终端周期体系 |
