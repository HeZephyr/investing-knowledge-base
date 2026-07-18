# Raw 来源目录

来源卡按机构与用途组织；机器审计以每张卡的 `id` 为稳定标识。本文件在每次 ingest 后更新。

## 官方来源

- `official/mainland/`：中国证监会、证券交易所、中基协等。
- `official/hong-kong/`：港交所、香港证监会、投委会等。
- `official/united-states/`：美国 SEC 投资者教育、EDGAR 与基金披露。
- `official/korea/`：韩国交易所交易和公司披露。
- `official/japan/`：JPX 交易清算与 FSA/EDINET 法定披露。
- `official/europe/`：ESMA 交易框架与欧盟披露/结算规则。
- `official/global/`：黄金基准、技术标准、汇率、能源统计与全球银行监管框架。

截至 2026-07-17，官方层新增 NIST/SEMATECH 统计手册，课程层新增 MIT OCW Finance Theory I。来源数量只用于库存管理，不代表知识要求已经完成。

## 研究与社区来源

- `books-and-papers/`：论文、教材与方法论入口。
- `community/`：只作为线索或经验参考的公开材料。
- `repositories/`：外部开源或公开代码库档案。
- `experts/`：从专家或机构公开原始作品提炼的可检验框架，不做人物背书。

首批研究材料包含组合理论、市场有效性、基金绩效和回测过拟合；外部项目包含 ExploreFinance、AKShare、BaoStock、Qlib、RQAlpha、Backtesting.py、Pyfolio 与 Awesome Quant。

扩展批次覆盖美股、韩国股市、海外 ETF、黄金、汇率与存储半导体。行业协会和标准组织资料为 B 级，涉及价格与标准全文时必须单独核验许可。

Issue #15 批次加入 EIA Open Data、OPEC Annual Statistical Bulletin、BIS Basel Framework、FDIC BankFind/Call Reports、美国 Census Monthly Retail Trade 与中国国家统计局社会消费品零售方法。六个入口分别支撑能源、金融和消费；聚合统计不能直接替代公司披露，更新后的历史值也不能冒充当时可得数据。

Issue #9 批次加入 Yale/Shiller 金融市场课程、AQR Data Library 与 GMO Research Library，用于对照行为、因子、估值和资产配置研究流。可下载序列、报告、逐字稿和图表不进入仓库；这里只保存规范链接、许可或条款边界、方法元数据与独立摘要。

Issue #17 批次加入 `openintro-statistics.md`、`openstax-principles-finance.md`、`forecasting-principles-practice.md`、`islp.md`、`nist-statistical-handbook.md` 与 `mit-finance-theory.md`，并审计 SciPy、statsmodels、ISLP Labs 和 QuantEcon 教学仓库。免费 PDF、公开 GitHub 和网页可读性均不自动授予复制或 LLM 摄取权；许可冲突或缺失时只链接并写独立摘要。

Issue #22 批次固定并审计 OpenBB、myhhub/stock、AI-Trader 与 ai_quant_trade。代码事实、上游声明和我们的推断分栏记录；完整 clone 只留在 ignored 本地目录。OpenBB 的 provider 分层可借鉴，A 股筛选与 AI/自动交易声明必须另做可证伪测试；无根许可证、远端认证、复制交易和自动下单默认隔离。

Issue #26 批次固定 FinHack 与 finance-quant-skills。FinHack 的平台分层和 A 股规则清单作为可证伪设计输入，但当前重构状态、`setup.py` 写副作用和测试缺口阻止默认安装；finance-quant-skills 因缺根许可证记为 NOASSERTION，13 个 Skill 按复制内容、网络、Token/Cookie、提示注入、专有终端和实盘下单逐项分级，完整 bundle 不安装。

Issue #18 批次加入 `jpx-trading-clearing.md`、`fsa-edinet.md`、`esma-trading.md`、`eu-transparency-settlement.md`、`eu-investment-funds-ucits.md`、`imf-areaer.md`、`world-bank-gfdd.md`、`bis-debt-statistics.md`、`sec-bond-bulletins.md` 与 `cftc-futures-basics.md`。它们支撑日本、欧盟、新兴市场访问、债券与商品；动态规则按 2026-07-17 核验，未来生效文本、最终修订数据和当前分类不得回填历史。

Issue #19 批次在 `raw/cases/` 固定 EIA/FRED、FDIC、Census/FRED 与公司法定披露的最小规范化事实。三套 manifest 保存上游参数、索引/报告时间、行数、单位和 SHA-256；current-corrected 序列只用于 2026-07-17 决策日的回顾性框架验证，不能冒充历史首次发布值。负结果与访问失败同样保留。

Issue #20 批次加入 FDA 临床终点、ClinicalTrials.gov API、CMS 覆盖、NMPA、HKEX 18A、MFDS、FTC、EU DMA、SAMR 以及 Meta/Micron/Samsung/SK hynix 官方披露。三套新 manifest 把 Aduhelm 批准—支付—减值、Meta 用户—展示—价格—收入、Micron ASP—库存—毛利—Capex 固定为离线反例；监管批准不能替代支付，用户总量不能替代变现拆解，公司 ASP 方向也不能冒充独立现货/合约价格。

Issue #31 批次加入 Meta 官方年度财务、Kenneth French Data Library 2026-05 CRSP vintage，以及通过 AKShare 无认证 Sina 接口取得的 510300/511010/518880 年末价格代理。只保存支持计算的最小年度事实和 SHA-256，不重分发完整上游档案；ETF 未复权价格不能冒充总收益，正回测与单一失败策略都不能外推成投资建议。
