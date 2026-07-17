---
id: raw-repo-myhhub-stock
title: myhhub/stock (InStock)
publisher: myhhub and contributors
url: https://github.com/myhhub/stock
retrieved: 2026-07-17
source_grade: B
markets: [A股, 基金]
usage: link-and-analyze-only
license: Apache-2.0
pinned_commit: b6e0ca2268cfbadd02f5ed052159c187b6670231
---
# myhhub/stock

## 代码事实

根 LICENSE 为 Apache-2.0。`instock/core` 分出 crawling、indicator、kline、pattern、strategy 和 backtest；另有 `instock/trade`、定时任务、Web UI 与 Docker。requirements 固定 numpy、pandas、TA-Lib、SQLAlchemy、requests、easytrader 等版本。抓取文件名显示东方财富、新浪等网页/接口适配，交易目录包含 robot 与 strategies。

本地只读扫描读取 108 个非敏感文本文件：backtest 10 个路径、provider 4、调整 2、成本 1、auto-trading 1。仓库缺少覆盖全部指标、复权、公司行动、未来函数、费用和订单失败的独立测试体系；扫描命中 4 个测试信号不能证明 200+ 维度正确。

## 上游声明

README 声称综合选股覆盖 200 多列，计算多类技术指标、K 线形态、筹码分布、策略验证和自动交易，并称部分结果与专业软件一致。这些都是可证伪声明：需要固定行情、公式、参数、复权、舍入和版本逐项对照，不能因截图或 Star 数直接采信。

## 认证与数据边界

抓取层依赖第三方站点和非正式接口时，字段、限频、反爬、Cookie、许可和稳定性都可能变化。Apache-2.0 只覆盖代码，不授予东方财富、新浪或券商数据再分发权。`easytrader` 与自动交易扩大到账户、资金和订单风险，本知识库不安装或运行交易服务。

## 采用决策

采用其 A 股领域分类、指标/形态目录和“选股后必须验证”的思想；公式只在独立手算 fixture 与历史时点测试后重写进自己的只读层。不复用抓取 Cookie、不照搬交易 robot、不把筛选命中当买入建议。自动交易明确拒绝进入第一版插件。
