---
id: raw-repo-ai-trader
title: HKUDS/AI-Trader
publisher: HKUDS and contributors
url: https://github.com/HKUDS/AI-Trader
retrieved: 2026-07-17
source_grade: D
markets: [全球, 加密资产]
usage: link-and-analyze-only
license: NOASSERTION
pinned_commit: d03ff6c056b32ced735adf7c19ed8175adb1c8df
---
# HKUDS AI-Trader

## 代码事实

2026-07-17 固定 commit 没有根 LICENSE 文件，因此公开可见不等于允许复制。仓库含 FastAPI service、前端、研究导出、OpenAPI 文档，以及 `ai4trade`、`copytrade`、`tradesync`、`market-intel`、`polymarket` 等远端 Skill。server tests 覆盖权限、登录 token、注册实验、价格、排行榜和实时交易价格防护等服务逻辑。

本地只读扫描读取 137 个非敏感文本文件：认证信号 37、缓存 34、测试 23、auto/copy trading 19、provider 16。测试存在不等于交易策略有样本外优势，也不改变根许可证缺失。

## 上游声明

README 把项目描述为 fully-automated agent-native trading，鼓励远端注册、保留 broker、同步交易、复制优秀参与者并分享信号。排行榜、agent 收益和平台稳定性声明不能证明因果优势、费用后可复制性或未来收益。

## 认证与数据边界

远端 Skill、agent registration、broker sync、copy trade 和登录 token 都涉及外部账户、服务条款、身份与资金权限。任何 Cookie/Token 都不得进入公共仓库、扫描输出或 Codex prompt。没有根许可证时，本项目不复制其 Skill、API schema、服务代码或研究导出。

## 采用决策

只采用“把 agent 行为、事件和实验元数据单独记录”的研究线索；项目保持 link-only，不安装远端 Skill、不注册、不连接 broker、不同步或复制交易、不调用交易 API。若未来研究 AI agent，先做无资金沙盒、固定规则基准、费用后样本外评价和权限威胁模型。
