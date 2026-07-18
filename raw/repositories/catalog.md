# 外部代码库目录

每个项目一张来源卡，记录固定 commit、许可证、用途和限制。Star 只代表关注度，不能替代代码审计、测试或投资证据。

完整仓库仅按需浅克隆到 `data/reference-repos/`，不会提交到本项目。

## 知识组织与 A/HK 基础

- [ExploreFinance](cards/explorefinance.md)：中文知识组织参考，许可证未知，只分析链接。
- [AKShare](cards/akshare.md)：A/HK 与基金免费数据主适配器。
- [BaoStock](cards/baostock.md)：A 股免费数据备用。
- [Qlib](cards/qlib.md)：高级量化架构参考。
- [RQAlpha](cards/rqalpha.md)：A 股撮合、费用与账户参考。
- [Backtesting.py](cards/backtesting-py.md)：轻量策略 API 参考。
- [Pyfolio](cards/pyfolio.md)：风险与绩效报告参考。
- [Awesome Quant](cards/awesome-quant.md)：项目发现索引。

## 全球与韩国数据

- [FinanceDataReader](cards/finance-data-reader.md)：KRX、全球代码、价格、指数与汇率读取参考。
- [OpenDartReader](cards/open-dart-reader.md)：韩国 Open DART 法定披露客户端参考。
- [yfinance](cards/yfinance.md)：全球便利行情回退层，非官方且无 SLA。
- [OpenBB](cards/openbb.md)：多供应商数据集成架构，注意 AGPL 与插件条款。

## A 股筛选与 AI 交易审计

- [myhhub/stock](cards/myhhub-stock.md)：A 股抓取、指标、筛选与回测参考；自动交易排除。
- [HKUDS/AI-Trader](cards/ai-trader.md)：根许可证缺失且涉及远端注册、broker sync 与 copy trade，仅链接分析。
- [ai_quant_trade](cards/ai-quant-trade.md)：Apache-2.0 的大型教学/示例集合，逐示例审计，不采信收益宣传。
- [FinHack](cards/finhack.md)：GPL/商业双许可的平台架构参考；当前重构版明示可能不可运行，安装有工作树写副作用。
- [finance-quant-skills](cards/finance-quant-skills.md)：13 个 Skill 的发现入口；根许可未确认，Cookie、专有客户端与实盘能力逐项隔离。

## 组合、回测与高级研究

- [QuantStats](cards/quantstats.md)：绩效指标和 tear sheet。
- [vectorbt](cards/vectorbt.md)：大规模向量化实验，注意 Commons Clause 与过拟合。
- [PyPortfolioOpt](cards/pyportfolioopt.md)：组合优化与风险模型。
- [FinRL](cards/finrl.md)：强化学习研究环境，只作高级实验参考。

## 金融、统计与计算课程

- [SciPy](cards/scipy.md)：概率分布、检验、优化和数值算法参考。
- [statsmodels](cards/statsmodels.md)：回归、诊断、稳健协方差和时间序列参考。
- [ISLP Labs](cards/islp-labs.md)：BSD-2 的 Python 章节实验环境参考，不复制 Notebook。
- [QuantEcon Python Intro](cards/quantecon-python-intro.md)：计算经济学课程结构；根许可证未确认，仅分析链接。

候选项目先进入 Issue；只有许可证、固定 commit、适用范围、失败模式和可验证用途齐全后才进入目录。
