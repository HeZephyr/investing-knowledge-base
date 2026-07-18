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

截至 2026-07-18，基础学科批次新增 MIT OCW 线性代数/微积分、OpenStax 经济学入口、BEA 国民账户、美联储政策工具与危机史。来源数量只用于库存管理，不代表知识要求已经完成。

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

Issue #33 批次加入 IFRS Foundation 的 IAS 1、IAS 7、IFRS 15、IAS 33 概览/实施材料及 SEC Investor.gov 的 EDGAR 研究入口。来源卡只链接和独立摘要，不复制标准全文；公式练习覆盖历史时点、重述、勾稽、现金周期、稀释和估值边界，不能替代适用司法辖区准则或专业意见。

Issue #35 批次加入 Investor.gov 资产配置/分散/再平衡入口与 SEC 开放式基金流动性规则指南，并复用 Markowitz 与 Sharpe 原始论文卡。监管基金规则不直接套到个人账户；公开模块只提炼目标、市场深度和定期复核原则，所有示例保持无个人持仓。

Issue #37 批次加入 Hernán/Robins《Causal Inference: What If》原作者入口、MacKinlay 事件研究综述和 Shumway 退市偏差论文，并更新 Kenneth French 因子构造/version 边界。教材和论文均采用 link-and-summarize；事件 CAR 只表示相对正常收益模型的关联，不自动升级为因果或交易信号。

Issue #39 批次加入 `mit-linear-algebra.md`、`mit-calculus.md`、`openstax-principles-economics.md`、`bea-national-accounts.md`、`federal-reserve-monetary-policy.md` 与 `federal-reserve-history-crises.md`。OpenStax 页面同时出现开放许可和生成式 AI 摄取限制，因此继续采用 link-and-summarize-only/NOASSERTION；宏观历史修订不回填实时决策，危机史按触发、资产负债表放大、market plumbing、政策与结果分层。

Issue #41 批次加入 FCA/LSE/HMRC/CREST、SEC/FINRA/DTCC 与 HKEX Stock Connect 八张运行来源卡。动态规则保存检索日与生效边界；英国 2027 Securities Transfer Tax 草案不提前替代现行 SDRT，T+1、配额、假日、币种和公司行动不跨市场硬编码。

Issue #43 批次加入股票权利、货币基金、中美国债曲线、上交所可转债、内地/香港/美国 REIT、CFTC 衍生品、SEC 期权/指数基金/结构化票据、S&P 指数数学及 IRS 2026 跨境税务入口。税务只形成按年度复验的问题清单，不推断个人身份；期货换月案例使用明确标注的合成价格与 SHA-256，避免重分发行情或把连续合约跳空伪装成收益。

Issue #45 批次加入 UNSD ISIC Rev.5、IFRS 17、IAIS ICS、NIST CHIPS、TSMC 2025 20-F、美国 Census M3/SOC、USGS MCS 2026 与 SEC S-K 1300。官方分类只作索引，宏观订单/住房/矿产统计不直接映射公司；法定公司披露只示范字段，不升级为全行业事实。
