# Investing Research Auditor

一个 repo-local Codex 插件，用只读、离线、证据优先的流程审计金融数据、量化回测和 AI 交易代码库。插件不打包第三方源码，不连接数据商或券商，不读取 Cookie/Token，不下单。

## 安装

先克隆本知识库，再把仓库根目录注册为本地 marketplace。`marketplace.json` 位于仓库的 `.agents/plugins/`，但 `marketplace add` 参数是仓库根目录：

```bash
codex plugin marketplace add /absolute/path/to/investing-knowledge-base
codex plugin add investing-research@personal
codex plugin list
```

本 marketplace 名称由官方脚手架生成为 `personal`。若本机已有同名 marketplace，先用 `codex plugin marketplace list` 检查并选择独立环境，不能覆盖未知配置。

## 离线示例

先对已在本地、且不会提交的 clone 运行扫描器：

```bash
python plugins/investing-research/scripts/audit_repository.py data/reference-repos/openbb
```

输出只含相对文件路径、类别计数、HEAD 和许可证候选，不含匹配源码行。关键词是人工复核线索，不是功能证明。可以用 `--output /tmp/audit.json` 保存派生报告；不要把包含私人路径的临时文件提交。

## 认证隔离

扫描器跳过 `.env` 以及文件名含 Cookie、Token、credential、secret 的文件；不导入被审计项目，不发网络请求，不启动容器或服务。OpenBB provider 的 API Key、数据条款和缓存由用户自行合法配置，插件不会帮助绕过登录、风控或供应商限制。

任何 broker、copy trade、trade sync、自动交易、远端 agent 注册或 money-moving 权限都不属于第一版。需要这些能力时必须另开安全评审，明确账户、许可、最小权限、模拟环境和人工确认。

## 更新

仓库更新后先拉取并升级 marketplace 快照，再重新安装。开发者修改插件 manifest 时使用 plugin-creator 的 cachebuster 脚本，不手改本机 marketplace 配置：

```bash
git pull --ff-only
codex plugin marketplace upgrade personal
codex plugin add investing-research@personal
```

更新后开一个新 Codex task，让新 Skill 被重新加载。

## 卸载

```bash
codex plugin remove investing-research@personal
codex plugin marketplace remove personal
```

卸载只移除 Codex 配置和缓存，不删除知识库或用户本地审计 clone。执行前可用对应 `--help` 核对当前 CLI 语法。

## 许可与限制

插件自身随本仓库的 MIT 许可发布；被审计仓库和数据源各自适用独立许可。AI-Trader 没有根许可证时只允许 link-only 分析。结果不构成投资建议，也不保证第三方代码安全、数据准确或策略盈利。
