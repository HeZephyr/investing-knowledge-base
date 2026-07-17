# Raw 来源目录

来源卡按机构与用途组织；机器审计以每张卡的 `id` 为稳定标识。本文件在每次 ingest 后更新。

## 官方来源

- `official/mainland/`：中国证监会、证券交易所、中基协等。
- `official/hong-kong/`：港交所、香港证监会、投委会等。
- `official/united-states/`：美国 SEC 投资者教育、EDGAR 与基金披露。
- `official/korea/`：韩国交易所交易和公司披露。
- `official/global/`：黄金基准、技术标准、汇率等跨市场来源。

首批覆盖：中国证监会、上交所、深交所、北交所、中基协、巨潮资讯、港交所、香港证监会和投委会，共 21 张来源卡。

## 研究与社区来源

- `books-and-papers/`：论文、教材与方法论入口。
- `community/`：只作为线索或经验参考的公开材料。
- `repositories/`：外部开源或公开代码库档案。
- `experts/`：从专家或机构公开原始作品提炼的可检验框架，不做人物背书。

首批研究材料包含组合理论、市场有效性、基金绩效和回测过拟合；外部项目包含 ExploreFinance、AKShare、BaoStock、Qlib、RQAlpha、Backtesting.py、Pyfolio 与 Awesome Quant。

扩展批次覆盖美股、韩国股市、海外 ETF、黄金、汇率与存储半导体。行业协会和标准组织资料为 B 级，涉及价格与标准全文时必须单独核验许可。

Issue #9 批次加入 Yale/Shiller 金融市场课程、AQR Data Library 与 GMO Research Library，用于对照行为、因子、估值和资产配置研究流。可下载序列、报告、逐字稿和图表不进入仓库；这里只保存规范链接、许可或条款边界、方法元数据与独立摘要。
