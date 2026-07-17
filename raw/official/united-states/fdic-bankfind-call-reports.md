---
id: raw-us-fdic-bankfind-call-reports
title: FDIC BankFind Suite and Call Report Data
publisher: Federal Deposit Insurance Corporation
url: https://banks.data.fdic.gov/bankfind-suite/
retrieved: 2026-07-17
source_grade: A
markets: [美股]
usage: link-and-summarize
---
# FDIC BankFind 与 Call Report 数据

## 权威性与用途

FDIC BankFind Suite 提供美国受保存款机构的机构历史、分支、失败、存款和财务监管数据。Financials API 与批量下载可用于从 1992 年起按季度比较资产、负债、资本、收入和费用；FDIC 说明公开 API 提供 1,100 多个 Call Report 变量。

## 更新频率与字段

财务数据通常按季度更新，机构结构可按周更新，Summary of Deposits 按年更新。字段必须配合官方 definitions 文件使用，并保留 FDIC certificate 等稳定机构标识、报告期、单位（界面常以千美元显示）和合并范围。单季批量下载限制与 API 参数应记录在复现说明中。

## 许可与使用边界

这是 FDIC 面向公众的数据工具。本仓库只保存入口、元数据说明和独立摘要，不缓存全量机构数据；具体研究在派生结果中记录 endpoint、参数、抓取时间、行数和哈希。不得把工具的可访问性误解为对 FDIC 商标或第三方材料的授权。

## 利益冲突

FDIC 的职责包括存款保险与银行监管，数据服务监管和公共透明目标，不是股票研究产品。监管报表强调受保存款机构，上市控股公司、非银行子公司和管理层调整口径可能不完全一致。

## 历史修订

Call Report 可能更正，机构会合并、失败、改名或变更证书关系，字段定义也会演化。时间序列必须使用机构历史表处理生命周期，并保留首次可得值、后续修订和字段字典版本；不能用当前存续银行名单重建历史样本。

## 局限与失效条件

数据主要覆盖美国受保存款机构，不覆盖保险、券商或所有控股公司业务。监管会计与上市公司 GAAP 披露不总是同口径。若机构映射、合并范围、字段定义、单位或公告可得日不清楚，停止横向比较并回到原始 Call Report/SEC 披露。

关联：[[金融]]、[[美股市场]]、[[幸存者偏差]]。
