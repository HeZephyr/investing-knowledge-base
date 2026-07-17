---
id: raw-us-eia-open-data
title: EIA Open Data API v2 Technical Documentation
publisher: U.S. Energy Information Administration
url: https://www.eia.gov/opendata/documentation.php
retrieved: 2026-07-17
source_grade: A
markets: [全球, 美股]
usage: link-and-summarize
---
# EIA Open Data

## 权威性与用途

EIA 是美国能源统计机构。Open Data API v2 提供石油、天然气、电力、煤炭和能源价格等层级化数据及元数据，适合定义能源研究中的数量、频率、单位和地区口径。它是行业事实入口，不是证券收益预测模型。

## 更新频率与字段

不同路线包含日度、周度、月度、季度和年度数据。典型字段包括 `period`、`series-description`、`value`、`unit`，并通过 facets 区分产品、地区、过程或用途。具体发布滞后必须读取对应数据集元数据与发布日历；API 文档和版本说明持续更新。

## 许可与使用边界

EIA 的 Copyrights and Reuse 页面说明，美国政府出版物通常属于公有领域，站内数据、文件、数据库和报告可在注明来源及发布日期后使用；第三方图片、投稿材料和 EIA 商标不在该一般许可内。本仓库只保存独立摘要和规范链接。API 注册密钥免费但属于使用者凭据，不进入 Git、日志、示例 URL 或 Pages。

## 利益冲突

EIA 不销售投资产品，但其统计服务服务于美国公共政策，分类、采样和发布时间以官方统计目的设计。官方身份不消除测量误差，也不能替代公司法定披露。

## 历史修订

API v2 有版本和补丁记录；数据集可能修订历史值、频率逻辑、分类或元数据。可复现研究必须保存抓取时间、完整参数、API 版本、行数和内容 SHA-256；历史回测不得把后来修订值当成当时已知值。

## 局限与失效条件

免费接口没有投资研究 SLA，可能限频、超时或改 schema。总库存不等于可交割库存，产量不等于上市公司销量，基准价格也不等于公司实现价。若单位、频率、时区、修订状态或公司暴露无法对齐，停止推断并把证据标记为不足。

关联：[[能源]]、[[周期行业研究]]、[[数据质量]]。
