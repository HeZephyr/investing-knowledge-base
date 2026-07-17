# 金融研究插件与第三方仓库审计设计

## 目标与授权

Issue #22 根据用户明确要求，把 OpenBB、myhhub/stock、HKUDS/AI-Trader 和 charliedream1/ai_quant_trade 本地下载、grep、比较，并沉淀为可安装 Codex 插件。完整第三方源码只存在 ignored `data/reference-repos/`；公共仓库提交固定 commit 来源卡、审计矩阵、原创只读脚本、Skill 和安装文档。

## 方案比较

### 方案 A：把四个仓库作为 submodule 或 vendor 目录

便于浏览，但引入许可证、体积、供应链、更新和 Obsidian 噪声，AI-Trader 还没有根许可证，不能采用。

### 方案 B：插件直接连接 OpenBB 与交易平台

功能看似完整，但安装时需要网络、供应商 Key、数据条款，甚至券商/复制交易权限；第一版无法保证 fork 安全和默认只读。

### 方案 C：本地只读审计插件（采用）

插件包含一个审计 Skill 和一个只读扫描脚本。脚本只接受本地目录或离线 fixture，不发网络请求、不读取 `.env`/Cookie/Token 文件、不调用第三方模块、不写被审计仓库、不下单；输出许可证、固定 Git commit、架构信号与风险类别的路径/数量，不输出匹配行或凭据值。

## 第三方定位

- OpenBB：数据接入与标准化架构参考。AGPL-3.0-only；provider 数据条款和认证独立，安装包不等于数据免费、准确或可再分发。
- myhhub/stock：A 股抓取、指标、形态、筛选、回测和自动交易一体化项目。Apache-2.0；README 的 200+ 条件、指标一致性与策略胜率是待验证声明，自动交易默认排除。
- AI-Trader：agent-native live/copy trade、broker sync 与远端 Skill 平台。根许可证缺失，且授权面接近资金操作；只保留链接分析，不能安装其 Skill、复制代码或注册交易。
- ai_quant_trade：Apache-2.0 的教学/示例集合，覆盖数据、因子、ML/RL 和模拟/实盘目录；README 含高收益、高频和付费社群宣传，示例与平台级可靠性必须分开。

Star 数只做发现信号，不进入正确性评分。四个仓库的 README 声明要回到代码、测试、许可证和可复现输出核验。

## 插件结构

使用 plugin-creator 官方脚手架生成 repo/team marketplace：

```text
.agents/plugins/marketplace.json
plugins/investing-research/
  .codex-plugin/plugin.json
  README.md
  skills/audit-finance-repositories/SKILL.md
  scripts/audit_repository.py
  assets/fixtures/sample-repository/...
```

插件不声明 MCP、App、hook 或外部认证。Skill 指导用户在当前仓库建立来源卡、审计矩阵和适配决策；默认先运行离线 fixture，再由用户明确提供本地 clone 路径。它不得读取浏览器会话、Cookie、Token、`.env`、持仓或券商配置。

## 审计模型

扫描器返回稳定 JSON：仓库名、HEAD commit、许可证候选、可扫描文件数，以及 provider/auth/cache/corporate-actions/timezone/adjustment/backtest/costs/lookahead/auto-trading/tests/docs 十二类信号的计数和相对路径。限制：字符串命中只是线索，不证明功能正确或风险存在；结果必须由人工阅读关键文件复核。

扫描器忽略 `.git`、虚拟环境、构建产物、二进制、图片、数据文件和所有 `.env`/credential/cookie/token/secret 文件。输出不包含源码片段、环境值或绝对私人路径。

## 测试与证据

- 先测试插件 manifest、marketplace、Skill 章节和默认只读边界。
- fixture 放入普通代码、假 `.env`、交易函数名称和许可证；测试证明敏感文件未读、无网络导入、被审计树哈希不变、输出只含相对路径。
- 用脚本本地扫描四个 ignored clone，结果用于写卡和矩阵，但不把生成的绝对路径或第三方内容提交。
- plugin-creator `validate_plugin.py` 和 skill-creator `quick_validate.py` 必须通过。

## 安装文档

repo marketplace 不是默认个人 marketplace，文档必须先执行 `codex plugin marketplace add <repo-root>/.agents/plugins`，再按 marketplace name 安装；更新使用 cachebuster/reinstall 流程，卸载使用 Codex CLI 当前帮助核验后的命令。若本机没有 `codex` CLI，只提供可复制命令并明确尚未实机安装，不伪造成功。

## 发布边界

Issue #22 → `codex/research-plugin-repo-audits` → PR → required checks → squash merge。任何需要接受新许可、使用账户会话、发送 Key、注册远端交易代理、连接券商或下单的步骤停止并请求用户单独授权；知识库建设不以绕过认证为手段。
