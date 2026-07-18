---
id: raw-official-us-treasury-yield-curve
title: Daily Treasury Par Yield Curve Rates and Methodology
publisher: U.S. Department of the Treasury
url: https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve
retrieved: 2026-07-18
source_grade: A
markets: [美股, 债券]
usage: link-and-summarize
---
# 美国财政部国债收益率曲线

## 权威性与用途

美国财政部发布每日票面收益率曲线、CSV/XML 入口和编制说明，可用于无付费 Key 的期限结构教学与时间戳明确的基准输入。

## 当前核验事实

票面曲线依据最近发行国债的场外市场指示性买方报价估计，并在固定期限读取收益率；2021-12-06 起采用 monotone convex spline。它不是逐笔成交价，也不同于零息曲线和单只国债 YTM。

## 许可与使用边界

链接并概括美国政府数据；程序抓取应尊重开发者通知、字段修订和频率，不在仓库复制大规模实时历史库。

## 历史时点与修订

检索日 2026-07-18。曲线存在期限新增、中断、恢复和方法变更，回测必须保留观察日、发布时间、曲线类型、期限字段与修订状态。

## 局限与失效条件

票面曲线不能直接折现任意现金流；跨币种、信用债和含权债还需零息/远期曲线、信用、流动性、税务与期权模型。
