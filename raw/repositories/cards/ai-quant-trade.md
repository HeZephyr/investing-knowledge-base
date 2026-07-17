---
id: raw-repo-ai-quant-trade
title: charliedream1/ai_quant_trade
publisher: charliedream1 and contributors
url: https://github.com/charliedream1/ai_quant_trade
retrieved: 2026-07-17
source_grade: C
markets: [A股, 美股, 全球]
usage: link-and-analyze-only
license: Apache-2.0
pinned_commit: 275b62509340ce2a730886886ed2618e1bb0ca97
---
# ai_quant_trade

## 代码事实

根 LICENSE 为 Apache-2.0。仓库更像大型知识/示例集合：`ai_notes`、数据、因子、NLP、传统策略、机器学习、深度/强化学习、图网络、模拟/实盘、在线平台与资源索引并存。requirements 跨越多个研究栈；不同示例可能有各自环境、外部数据和许可。

本地只读扫描读取 754 个非敏感文本文件：backtest 98 个路径、tests 56、provider 50、adjustment 42、costs 41、authentication 36。专门 `unit_test` 目录在固定 commit 只发现一套动量轮动 fixture/测试；目录广度不等于所有示例经过统一回归验证。

## 上游声明

README 宣传从学习、模拟到实盘，列出高频、AI/RL、自动因子挖掘和具体高年化案例；仓库同时含付费社群/知识产品图片与文档。收益数字必须追问样本、基准、费用、滑点、容量、复权、退市、尝试次数和样本外，不能作为采用理由。

## 认证与数据边界

示例涉及 Wind 等商业数据、在线平台、实盘模拟和多种第三方项目。Apache-2.0 不覆盖外部数据、论文、图片、嵌套资源或被链接仓库。插件不安装其总 requirements、不运行实盘目录、不读取本地商业数据或凭据。

## 采用决策

采用“按数据—因子—策略—回测—报告组织学习实验”和独立 momentum fixture 的测试思路；逐示例审计后才可重写最小算法。拒绝整仓依赖安装、收益宣传外推、高频/实盘默认启用和付费内容复制。所有研究先离线、无资金、带基准与负结果。
