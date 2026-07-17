---
title: 维护日志
aliases: [Log]
category: operations
markets: [A股, 港股]
level: beginner
status: active
sources: []
updated: 2026-07-17
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
