---
id: raw-repo-openbb
title: OpenBB-finance/OpenBB
publisher: OpenBB and contributors
url: https://github.com/OpenBB-finance/OpenBB
retrieved: 2026-07-17
source_grade: B
markets: [全球]
usage: link-and-analyze-only
license: AGPL-3.0-only
pinned_commit: ebee248ed0bccca65bdfc78e7faae676488f4e5b
---
# OpenBB

## 代码事实

固定 commit 的根 LICENSE 声明全部文件为 AGPL-3.0。仓库把 `openbb_platform/core`、主题 extensions、provider packages、CLI、desktop 和 examples 分开；core 的 `standard_models` 使用 `QueryParams` 与 `Data` 类型统一请求/结果，具体供应商在 provider 包实现。README 提供 Python API、FastAPI REST API 和 Workspace 后端连接。

本地只读扫描读取 1,925 个非敏感文本文件：provider 信号 1,498 个路径、认证信号 409、公司行动 388、缓存 261、测试 211。字符串计数不是覆盖率或质量证明；关键价值是“标准模型—provider 实现—router/extension—输出对象”的可替换分层。

## 上游声明

上游把 ODP 定位为一次接入、多端消费的数据基础设施，并展示 `obb.equity.price.historical("AAPL")`。provider 表把数据源标为 None、Free 或 Paid。这里的“Free”只表示上游列出的最低订阅层，不保证无需注册、无需 API Key、没有限频、允许再分发或数据准确。

## 认证与数据边界

README 明确部分 provider 需要 API Key，可放在用户设置文件或运行时配置。插件和知识库不读取该文件，不保存 Key，也不把 Cookie 当公共适配方案。每个 provider 的数据许可、字段、调整、时区、公司行动、历史修订和服务等级独立于 OpenBB 的代码许可证。

OpenBB 的 AGPL 适用于代码；provider 数据可能是公共、免费层或付费授权。部署修改后的网络服务、组合插件或再分发结果前，需要分别评估 AGPL 与供应商条款。

## 采用决策

采用标准模型、provider registry、extension 和统一输出的架构思想；把 OpenBB 作为可选、用户自行安装的只读数据层，不 vendor 源码，不作为 A股/港股唯一数据源，不在默认 CI 发实时请求。第一版插件只审计本地仓库，不启动 OpenBB API/MCP，也不处理认证。
