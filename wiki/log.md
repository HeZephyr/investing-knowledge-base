---
title: 维护日志
aliases: [Log]
category: operations
markets: [A股, 港股]
level: beginner
status: active
sources: []
updated: 2026-07-18
---

# 维护日志

## [2026-07-16] research | 初始化知识库
- changed: [[dashboard]], [[index]], [[learning-path]]
- sources: 用户提供的 LLM Wiki 模式
- result: 建立 Raw、Wiki、Output 三层结构和新手入口。

## [2026-07-16] ingest | 首批 A 股与港股资料
- changed: [[A股市场]], [[港股市场]], [[ETF]], [[数据质量]], [[回测基础]]
- sources: 33 张官方、论文与开源项目来源卡
- result: 建立市场、产品、分析、风险与量化五类新手知识基线。

## [2026-07-16] research | 免费数据与日线回测骨架
- changed: [[数据质量]], [[未来函数]], [[回测基础]], [[换手与交易成本]]
- sources: raw-repo-akshare, raw-repo-baostock, raw-repo-rqalpha
- result: A/HK 日线适配、质量检查、次日开盘成交、费用和复现报告均可测试运行。

## [2026-07-17] ingest | 行为、因子与估值研究流
- changed: [[投资研究证据矩阵]], [[公开投资框架]]
- sources: raw-expert-shiller-yale-financial-markets, raw-research-aqr-data-library, raw-expert-gmo-research-library
- result: 建立跨流派可证伪矩阵与许可安全的实证证据模板，不再分发第三方原始数据。

## [2026-07-17] research | 覆盖审计与失败教训
- changed: [[经验与失败教训]], [[index]], [[dashboard]]
- sources: raw-research-aqr-data-library, raw-expert-gmo-research-library
- result: 用证据清单报告真实缺口，并把 CI、许可、数据修订、SSE 与负结果经验转成防复发规则。

## [2026-07-17] ingest | 能源、金融与消费行业研究包
- changed: [[能源]], [[金融]], [[消费]], [[周期行业研究]], [[经验与失败教训]]
- sources: raw-us-eia-open-data, raw-global-opec-asb, raw-global-bis-basel-framework, raw-us-fdic-bankfind-call-reports, raw-us-census-monthly-retail-trade, raw-cn-nbs-retail-sales-methodology
- result: 建立三种行业研究语言与预注册证据卡，明确宏观总量、历史修订、来源激励和本地监管口径不能直接替代公司结论。

## [2026-07-17] research | 八轴四阶段覆盖体系
- changed: [[经验与失败教训]], [[index]], [[dashboard]]
- sources: 仓库现有 Raw、Wiki、Output、测试与工作流证据
- result: 将 42 个粗主题重构为 135 项原子能力，基线从 60.4% 调整为 36.5%，并公开 11 项冻结案例全部尚未验证的真实缺口。

## [2026-07-17] ingest | 金融与统计课程主干
- changed: [[金融与统计基础]], [[复利与贴现]], [[概率与收益分布]], [[抽样与估计]], [[假设检验与多重比较]], [[回归与诊断]], [[时间序列与预测]], [[债券与利率基础]], [[公司金融基础]], [[论文阅读与复现]], [[经验与失败教训]]
- sources: raw-book-openintro-statistics, raw-book-openstax-principles-finance, raw-book-fpp3, raw-book-islp, raw-official-nist-stat-handbook, raw-course-mit-finance-theory, raw-repo-scipy, raw-repo-statsmodels, raw-repo-islp-labs, raw-repo-quantecon-python-intro
- result: 建立九模块课程、八组手算纯函数与非法输入测试；许可冲突使用 link-only，部分练习不冒充完整能力，覆盖就绪度从 36.5% 提升到 45.8%。

## [2026-07-17] audit | 四个金融代码库与只读插件
- changed: [[金融研究代码库审计]], [[经验与失败教训]], [[index]], [[dashboard]]
- sources: raw-repo-openbb, raw-repo-myhhub-stock, raw-repo-ai-trader, raw-repo-ai-quant-trade
- result: 固定 commit 审计 OpenBB、myhhub/stock、AI-Trader 与 ai_quant_trade；新增离线安全扫描器、Codex 插件清单与 fixture 测试，默认隔离凭据、远端 agent、复制交易和自动下单。

## [2026-07-17] ingest | 全球市场、债券与商品体系
- changed: [[全球市场]], [[日本市场]], [[欧盟市场]], [[新兴市场访问]], [[债券]], [[大宗商品]], [[经验与失败教训]]
- sources: raw-official-jpx-trading-clearing, raw-official-fsa-edinet, raw-official-esma-trading, raw-official-eu-transparency-settlement, raw-official-eu-investment-funds-ucits, raw-official-imf-areaer, raw-official-world-bank-gfdd, raw-official-bis-debt-statistics, raw-official-sec-bond-bulletins, raw-official-cftc-futures-basics
- result: 建立市场 × 资产矩阵与十张动态规则卡；新增久期/凸性、YTM、信用损失、基差和展期练习，仓库就绪度从 46.5% 提升到 51.0%，冻结案例仍保持 0/11。

## [2026-07-17] audit | FinHack 与金融 Skill 供应链
- changed: [[金融量化平台与Skill审计|金融量化平台与 Skill 审计]], [[金融研究代码库审计]], [[经验与失败教训]], [[index]]
- sources: raw-repo-finhack, raw-repo-finance-quant-skills
- result: 固定审计平台与 13 个 Skill；识别 setup 安装写副作用、缺根许可证、复制文档、Cookie/Token、提示注入与实盘下单面；插件 v0.2 增加只读 `$audit-finance-skills`，不安装第三方 bundle。

## [2026-07-17] research | 能源、银行与消费冻结案例
- changed: [[能源]], [[金融]], [[消费]], [[经验与失败教训]], [[index]]
- sources: raw-us-eia-open-data, raw-us-fdic-bankfind-call-reports, raw-us-census-monthly-retail-trade, ExxonMobil/Target/Walmart 法定披露
- result: 建立三套带 SHA-256、首次可得日、单位与离线验证的公开快照；保留能源幅度失败、SVB 简单资本率反例和 Target 宏观背离，三项 case capability 首次达到 validated。

## [2026-07-17] research | 医药、互联网与存储研究系统
- changed: [[医药医疗]], [[互联网平台]], [[存储半导体]], [[经验与失败教训]], [[index]], [[dashboard]]
- sources: raw-us-fda-clinical-endpoints, raw-us-clinicaltrials-gov-api, raw-us-cms-amyloid-coverage, raw-cn-nmpa-drug-registration, raw-hk-hkex-biotech-18a, raw-kr-mfds-drug-approval, raw-us-ftc-platform-data-practices, raw-eu-digital-markets-act, raw-cn-samr-platform-antitrust, raw-company-meta-platform-metrics, raw-company-micron-memory-results, raw-kr-memory-company-disclosures
- result: 建立研发—支付—现金流、用户—变现—治理、bit—价格—库存—Capex 三条证据链；冻结 Aduhelm、Meta 与 Micron 反例，六项行业内容/案例能力完成，仓库就绪度升至 56.9%。

## [2026-07-18] research | 公司、因子、失败策略与公开组合案例
- changed: [[经验与失败教训]], [[index]], output/cases/company-positive.md, output/cases/company-negative.md, output/cases/factor-replication.md, output/cases/negative-strategy.md, output/cases/portfolio-public.md
- sources: Meta 官方年度业绩、Kenneth French Data Library 2026-05 CRSP vintage、Sina via AKShare 公开 ETF 历史价格
- result: 完成公司正结果与明确放弃原命题、HML 因子复现、费用后失败策略及三资产组合；11/11 案例能力全部具备来源、报告和测试，仓库就绪度升至 60.6%。

## [2026-07-17] research | 公司研究可计算实验室
- changed: [[法定披露与历史时点]], [[三表勾稽与现金转换]], [[收入确认与合同经济]], [[资本配置治理与稀释]], [[估值实验室]], [[财务三表]], [[盈利质量]], [[经验与失败教训]], [[dashboard]]
- sources: raw-global-ifrs-ias-1, raw-global-ifrs-ias-7, raw-global-ifrs-15, raw-global-ifrs-ias-33, raw-us-investor-edgar-research, raw-expert-damodaran-valuation
- result: 建立历史时点与重述、双重三表勾稽、现金周期、完全稀释股数、反向 DCF、概率情景和亏损倍数边界；公司研究轴 16/16 validated，仓库就绪度升至 68.8%。

## [2026-07-17] research | 组合治理、风险与归因实验室
- changed: [[投资政策与目标]], [[资产配置与再平衡]], [[组合风险预算与压力测试]], [[基准与绩效归因]], [[决策日志与过程评分]], [[分散化]], [[仓位管理]], [[流动性风险]], [[基准]], [[经验与失败教训]], [[dashboard]]
- sources: raw-us-investor-asset-allocation, raw-us-sec-fund-liquidity-risk, raw-paper-markowitz-1952, raw-paper-sharpe-1966
- result: 建立无个人持仓的 IPS 校验、配置集中度、费用后再平衡、退出天数、风险贡献、正反压力、Brinson 归因和过程评分；组合轴 14/14 validated，仓库就绪度升至 75.4%。

## [2026-07-18] research | 预注册、走步、因果与事件研究实验室
- changed: [[研究预注册与证据等级]], [[因果推断与识别]], [[事件研究]], [[样本外测试]], [[时间序列与预测]], [[因子研究]], [[幸存者偏差]], [[未来函数]], [[经验与失败教训]], [[dashboard]]
- sources: raw-book-causal-inference-what-if, raw-paper-mackinlay-event-studies, raw-paper-shumway-delisting-bias, raw-research-kenneth-french-data-library
- result: 建立带 embargo 的 expanding/rolling walk-forward、规范预注册哈希、自相关/随机游走/EWMA 基线和市场模型 CAR；研究方法轴 18/18 validated，仓库就绪度升至 79.5%。

## [2026-07-18] research | 数学、统计、经济、会计与危机史基础实验室
- changed: [[投资数学与优化]], [[微观经济与产业组织]], [[宏观账户周期与货币传导]], [[金融危机与机制复盘]], [[假设检验与多重比较]], [[回归与诊断]], [[财务三表]], [[盈利质量]], [[论文阅读与复现]], [[经验与失败教训]]
- sources: raw-course-mit-linear-algebra, raw-course-mit-calculus, raw-book-openstax-principles-economics, raw-official-us-bea-national-accounts, raw-official-us-federal-reserve-monetary-policy, raw-official-us-federal-reserve-history-crises, IFRS 官方卡与冻结 HML 数据
- result: 建立效应量/功效、HC1/杠杆/Cook 距离、显式种子 bootstrap，补齐数学优化、微观产业、宏观账户、货币传导、会计应计与危机机制；基础学科轴 20/20 validated，仓库就绪度升至 85.5%。
