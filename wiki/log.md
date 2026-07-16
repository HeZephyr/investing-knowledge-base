---
title: 维护日志
aliases: [Log]
category: operations
markets: [A股, 港股]
level: beginner
status: active
sources: []
updated: 2026-07-16
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
