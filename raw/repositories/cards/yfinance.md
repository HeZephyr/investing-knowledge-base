---
id: raw-repo-yfinance
title: ranaroussi/yfinance
publisher: Ran Aroussi and contributors
url: https://github.com/ranaroussi/yfinance
retrieved: 2026-07-18
source_grade: B
markets: [美股, 全球]
usage: link-and-analyze-only
license: Apache-2.0
pinned_commit: 38c73ce33fb1ee77d37a0998c95c06e60356298e
---
# yfinance

## 固定版本与代码事实

2026-07-18 通过 GitHub API 复核，默认分支 HEAD 仍为 `38c73ce…`，根许可证由 GitHub 识别为 Apache-2.0。项目是 Yahoo Finance 公开页面/接口的社区客户端，覆盖价格、公司行动和部分基本面；代码许可证不授予 Yahoo 数据再分发权。

## 采用与拒绝

采用 `download` 与 `Ticker.actions` 作为无 Key 的全球研究便利入口，放在注入 client 的 provider 边界后，用离线 fixture 固定列、日期、复权、公司行动和失败行为。美股、韩国及全球证券必须显式登记 provider symbol、币种和交易所时区；不从裸 ticker 猜市场。

不把 yfinance 当法定披露、交易所事实或生产 SLA；不存完整上游响应，不用 Cookie，不绕过限频，不把缺失成交额估算成事实，不在确定性 PR 测试请求网络。价格调整与现金分红/拆股分别保存，避免重复计入。

## 失效条件

项目不隶属 Yahoo，数据使用权受 Yahoo 条款约束，页面、字段、复权和限频可变化。空响应、多层列、必需字段漂移、重复日期、非法 OHLC 或负成交量必须失败；定时 smoke 与离线契约测试承担不同职责。
