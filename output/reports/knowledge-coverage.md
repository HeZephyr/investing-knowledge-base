# 知识库覆盖审计

- 清单日期：2026-07-17
- 仓库就绪度，不是预期收益：**60.4%**
- 需求总数：42

> validated 只表示当前清单所列证据通过仓库规则；不保证投资收益，也不免除后续更新。

## 分轴状态

| 维度 | missing | seed | reviewed | validated | 就绪度 |
|---|---:|---:|---:|---:|---:|
| 市场 | 3 | 0 | 2 | 2 | 47.1% |
| 资产与产品 | 2 | 3 | 3 | 1 | 41.1% |
| 行业 | 2 | 0 | 5 | 0 | 46.4% |
| 研究方法 | 0 | 1 | 4 | 4 | 76.1% |
| 工程与维护 | 1 | 1 | 0 | 8 | 82.5% |

## 逐项证据与缺口

| ID | 维度 | 要求 | 状态 | 最后核验 | 证据 | 缺口 |
|---|---|---|---|---|---|---|
| `asset-bonds` | 资产与产品 | 债券与利率 | missing | 2026-07-17 | — | 缺国债、信用债、久期、凸性、违约与市场制度体系 |
| `asset-cash` | 资产与产品 | 现金与货币基金 | seed | 2026-07-17 | `synthesis:wiki/products/货币基金.md` | 补收益来源、流动性、信用与利率风险的官方来源和案例 |
| `asset-commodities` | 资产与产品 | 大宗商品 | missing | 2026-07-17 | — | 缺期货曲线、展期、库存、基差和代表性品种案例 |
| `asset-convertible` | 资产与产品 | 可转债 | seed | 2026-07-17 | `synthesis:wiki/products/可转债.md` | 补条款、赎回、转股、信用与估值的官方来源和案例 |
| `asset-equity` | 资产与产品 | 股票所有权与公司研究 | reviewed | 2026-07-17 | `synthesis:wiki/products/股票.md` | 缺真实公司披露、财务和估值的端到端案例 |
| `asset-fund-etf` | 资产与产品 | 公募基金与 ETF | validated | 2026-07-17 | `synthesis:wiki/products/ETF.md`<br>`test:tests/data/test_providers.py` | — |
| `asset-fx` | 资产与产品 | 汇率风险 | reviewed | 2026-07-17 | `synthesis:wiki/concepts/汇率风险.md`<br>`source:raw/official/global/fred-exchange-rates.md` | 缺对冲与不对冲组合的成本和情景案例 |
| `asset-gold` | 资产与产品 | 黄金与基准 | reviewed | 2026-07-17 | `synthesis:wiki/assets/黄金.md`<br>`source:raw/official/global/lbma-gold-benchmark.md` | 缺币种、实际利率、持有成本和产品差异的可复现实证案例 |
| `asset-reit` | 资产与产品 | REIT | seed | 2026-07-17 | `synthesis:wiki/products/REIT.md` | 补 A/HK/US 制度差异、现金流和估值案例 |
| `engineering-ci` | 工程与维护 | 多版本 CI 与保护检查 | validated | 2026-07-17 | `workflow:.github/workflows/ci.yml`<br>`test:tests/test_github_workflows.py` | — |
| `engineering-coverage` | 工程与维护 | 机器可审计覆盖报告 | validated | 2026-07-17 | `configuration:config/knowledge-coverage.yaml`<br>`test:tests/test_coverage.py` | — |
| `engineering-data-adapters` | 工程与维护 | A/HK 与基金免费数据适配 | validated | 2026-07-17 | `implementation:src/investkb/data/providers.py`<br>`test:tests/data/test_providers.py` | — |
| `engineering-global-data` | 工程与维护 | 美股、韩国与全球免费数据适配 | seed | 2026-07-17 | `source:raw/repositories/cards/yfinance.md` | 缺标准化适配器、公司行动、限频处理和离线契约测试 |
| `engineering-maintenance-skill` | 工程与维护 | 可复用知识库维护 Skill | validated | 2026-07-17 | `implementation:skills/maintain-investing-knowledge-base/SKILL.md`<br>`test:tests/test_knowledge_skill.py` | — |
| `engineering-monitoring` | 工程与维护 | 定时数据与链接健康检查 | validated | 2026-07-17 | `workflow:.github/workflows/provider-smoke.yml`<br>`test:tests/test_github_workflows.py` | — |
| `engineering-pages` | 工程与维护 | 可搜索互动 GitHub Pages | validated | 2026-07-17 | `configuration:mkdocs.yml`<br>`test:tests/test_site.py` | — |
| `engineering-private-research` | 工程与维护 | 私人观察池、持仓与决策日志 | missing | 2026-07-17 | — | 用户暂无持仓；需在本地 private 层建立不公开的投资政策与观察池 |
| `engineering-public-boundary` | 工程与维护 | 公开与私人边界 | validated | 2026-07-17 | `implementation:src/investkb/publication.py`<br>`test:tests/test_public_boundary.py` | — |
| `engineering-source-lineage` | 工程与维护 | Raw 来源谱系审计 | validated | 2026-07-17 | `implementation:src/investkb/sources.py`<br>`test:tests/test_sources.py` | — |
| `market-cn-rules` | 市场 | A 股交易、披露与产品规则 | validated | 2026-07-17 | `synthesis:wiki/markets/A股市场.md`<br>`source:raw/official/mainland/sse-trading-rules.md` | — |
| `market-emerging-rules` | 市场 | 新兴市场框架 | missing | 2026-07-17 | — | 缺市场分类、资本管制、托管和代表性市场案例 |
| `market-europe-rules` | 市场 | 欧洲主要市场 | missing | 2026-07-17 | — | 缺 EU/英国监管、交易所、UCITS 和跨币种研究 |
| `market-hk-rules` | 市场 | 港股交易、披露与产品规则 | validated | 2026-07-17 | `synthesis:wiki/markets/港股市场.md`<br>`source:raw/official/hong-kong/hkex-trading-rules.md` | — |
| `market-japan-rules` | 市场 | 日本市场 | missing | 2026-07-17 | — | 缺 JPX/FSA 官方来源、Wiki、费用与披露案例 |
| `market-korea-rules` | 市场 | 韩国市场、交易与披露 | reviewed | 2026-07-17 | `synthesis:wiki/markets/韩国股市.md`<br>`source:raw/official/korea/krx-investment-guide.md` | 补齐税务、公司行动、KRX 数据复现实例和一家公司披露案例 |
| `market-us-rules` | 市场 | 美股市场、披露与投资者保护 | reviewed | 2026-07-17 | `synthesis:wiki/markets/美股市场.md`<br>`source:raw/official/united-states/sec-edgar.md` | 补齐订单执行、费用、税务和公司行动的当前官方来源与案例 |
| `method-accounting` | 研究方法 | 财务报表与盈利质量 | reviewed | 2026-07-17 | `synthesis:wiki/concepts/财务三表.md`<br>`synthesis:wiki/concepts/盈利质量.md` | 缺公告时点、重述、现金流勾稽和真实公司案例 |
| `method-backtest` | 研究方法 | 无未来函数日线回测 | validated | 2026-07-17 | `synthesis:wiki/quant/回测基础.md`<br>`test:tests/backtest/test_engine.py` | — |
| `method-behavior` | 研究方法 | 行为金融与决策纪律 | reviewed | 2026-07-17 | `synthesis:wiki/risk/行为偏差.md`<br>`source:raw/experts/cards/shiller-yale-financial-markets.md` | 缺预承诺、决策日志和偏差复盘案例 |
| `method-data-quality` | 研究方法 | 数据质量与历史时点 | validated | 2026-07-17 | `synthesis:wiki/quant/数据质量.md`<br>`test:tests/validation/test_market.py` | — |
| `method-empirical` | 研究方法 | 因子与跨流派实证 | reviewed | 2026-07-17 | `synthesis:wiki/methods/投资研究证据矩阵.md`<br>`template:output/templates/实证证据卡.md` | 缺使用公开冻结数据的完整正负结果研究 |
| `method-lessons` | 研究方法 | 经验、失败假设与事故复盘 | validated | 2026-07-17 | `synthesis:wiki/methods/经验与失败教训.md`<br>`template:output/templates/研究事故与教训.md` | — |
| `method-portfolio` | 研究方法 | 组合构建与再平衡 | seed | 2026-07-17 | `synthesis:wiki/concepts/分散化.md` | 缺投资政策、相关性失稳、约束优化与再平衡案例 |
| `method-risk` | 研究方法 | 风险、回撤与仓位 | validated | 2026-07-17 | `synthesis:wiki/risk/最大回撤.md`<br>`test:tests/test_metrics.py` | — |
| `method-valuation` | 研究方法 | 估值与反向估值 | reviewed | 2026-07-17 | `synthesis:wiki/concepts/估值.md`<br>`source:raw/experts/cards/damodaran-valuation.md` | 缺多情景、敏感性和真实公司反向估值案例 |
| `sector-consumer` | 行业 | 消费 | reviewed | 2026-07-17 | `synthesis:wiki/sectors/消费.md`<br>`source:raw/official/united-states/census-monthly-retail-trade.md`<br>`template:output/templates/消费单位经济证据卡.md` | 缺宏观、终端、渠道库存与公司三表对齐的冻结数据案例 |
| `sector-energy` | 行业 | 能源 | reviewed | 2026-07-17 | `synthesis:wiki/sectors/能源.md`<br>`source:raw/official/united-states/eia-open-data.md`<br>`template:output/templates/能源周期证据卡.md` | 缺冻结历史 vintage 的供需、价格与公司财务端到端正负结果案例 |
| `sector-financials` | 行业 | 银行、保险与券商 | reviewed | 2026-07-17 | `synthesis:wiki/sectors/金融.md`<br>`source:raw/official/global/bis-basel-framework.md`<br>`template:output/templates/银行资产负债表证据卡.md` | 缺当地监管口径、历史可得 Call Report/披露与压力情景案例 |
| `sector-framework` | 行业 | 可复用行业研究框架 | reviewed | 2026-07-17 | `synthesis:wiki/sectors/周期行业研究.md` | 缺能源、银行、消费三个使用冻结公开数据的完整正负结果案例 |
| `sector-healthcare` | 行业 | 医药与医疗 | missing | 2026-07-17 | — | 缺研发概率、专利、支付体系、监管和公司案例 |
| `sector-internet` | 行业 | 互联网与平台 | missing | 2026-07-17 | — | 缺网络效应、获客、变现、监管和公司案例 |
| `sector-memory` | 行业 | 存储半导体 | reviewed | 2026-07-17 | `synthesis:wiki/sectors/存储半导体.md`<br>`source:raw/official/global/jedec-memory-standards.md` | 缺供需、价格、库存和公司财务的时间序列验证 |
