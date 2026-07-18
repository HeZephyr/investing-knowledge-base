---
id: raw-us-clinicaltrials-gov-api
title: ClinicalTrials.gov Data API v2
publisher: U.S. National Library of Medicine
url: https://clinicaltrials.gov/data-api/about-api/api-migration
retrieved: 2026-07-17
source_grade: A
markets: [美股, 全球]
usage: link-and-summarize
---
# ClinicalTrials.gov API v2

`/api/v2/studies` 可按 NCT ID 或查询式返回 protocol、outcome、results、版本日期等结构化字段，分页上限和字段模型以官方文档为准。注册记录是申办方/责任方提交的信息：状态、终点和完成日期会更新，不能把当前记录回填为历史当时所知，也不可把“有结果”自动解释成阳性、获批或商业成功。

研究快照应固定 NCT ID、下载参数、记录版本、首次提交/最近更新、结果发布日期和 SHA-256；对 primary outcome 的 measure、time frame、analysis population 与预注册版本分别保存。
