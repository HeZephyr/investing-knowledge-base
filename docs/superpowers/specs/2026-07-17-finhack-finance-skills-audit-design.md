# FinHack 与金融 Skill 包审计设计

## 目标与授权

Issue #26 审计 `FinHackCN/finhack` 与 `lzwme/finance-quant-skills`。完整第三方仓库只保存在 ignored `data/reference-repos/`；公共仓库只提交固定 commit 的来源卡、原创比较页、采用矩阵、测试和本项目自己的只读 Skill。

本次“看看”包含架构与供应链审计，不包含安装或执行第三方项目、连接数据商、读取 Cookie/Token、启动服务、连接券商或下单。Star 只用于发现，不作为可靠性、收益或安全证据。

## 两类对象必须分开

FinHack 是平台型框架，目标覆盖采集、因子、机器学习、回测、任务编排与交易接入。审计重点是当前固定 commit 是否可运行、安装是否修改工作树、数据与认证依赖、历史时点和复权语义、回测成交规则，以及模拟/实盘边界。

finance-quant-skills 是可被代理读取和执行的 Skill 集合。审计不仅看代码许可证，还看每个 Skill 的指令、脚本、复制文档、依赖、网络、凭证、Cookie、专有客户端、提示注入和资金操作面。不能把仓库级声明自动传递给复制进来的第三方文档。

## 许可证判定

- FinHack 根 `LICENSE.txt` 是 GPL v3 正文，README 声明 GPL-3.0 与商业许可双轨；公共卡记为 `GPL-3.0-only OR LicenseRef-Commercial`，商业条款仍需另行签约，不能把占位说明当已获授权。
- finance-quant-skills 的 README 声称 MIT，但固定 commit 没有根 LICENSE/COPYING，`pyproject.toml` 也未声明许可证；公共卡记为 `NOASSERTION`。在上游补齐许可证且逐项核对复制内容前，只做 link-only 分析。
- 代码许可、数据商条款、官方文档版权、模型/图片/模板许可分别判断。

## 安全采用分级

| 等级 | 条件 | 默认动作 |
|---|---|---|
| A 原创重写 | 思想可复用、许可与证据清晰、无凭证/订单面 | 在本仓库独立实现并测试 |
| B 可选只读适配 | 许可证清晰，网络与 Key 可隔离，有离线 fixture | 用户自行安装，CI 不访问实时源 |
| C link-only | 许可证未知、复制文档权利不清或质量未验证 | 只保存链接、commit 和审计结论 |
| D quarantine | Cookie、账号口令、专有客户端、实盘/资金操作或远端执行 | 默认不安装、不运行、不加载 |
| E reject | 绕过认证、隐蔽持久化、无人工确认下单或不可接受许可 | 明确拒绝 |

finance-quant-skills 必须逐 Skill 分级。`pywencai` 的 Cookie/F12 流程、`miniqmt`/`qmt-docs` 的订单与资金操作面进入 quarantine；Tushare/JQData 等需要 Token 或账号的模块只能在合法条款、最小权限和用户主动配置后成为可选只读适配。

## 本项目 Skill

在 `investing-research` 插件增加 `audit-finance-skills`。它审计已经合法存在于本地的 Skill bundle，复用现有离线扫描器，再人工检查根与嵌套许可证、安装脚本、指令注入、依赖与网络、凭证路径、Cookie、浏览器调试指令、券商/订单/转账能力和复制文档来源。

Skill 不安装第三方包、不执行脚本、不导入模块、不读取敏感文件、不输出秘密值、不连接浏览器会话或券商。输出是逐 Skill 的证据矩阵、隔离决策、未知项与下一项安全测试。

## 验证

- RED 测试先约束两张 Raw 卡、固定 commit、许可证结论、深度比较页、新 Skill 和插件版本。
- 用 skill-creator 官方 `init_skill.py` 与 `quick_validate.py` 生成和校验 Skill。
- 用 plugin-creator 官方 validator 校验插件；运行全量测试、站点构建、覆盖与公开边界检查。
- 只有验证通过后才更新本地 marketplace 快照、提交 PR 并等待 required checks。

## 发布边界

Issue #26 → `codex/finhack-finance-skills-audit` → PR → required checks → squash merge。任何接受新许可证、安装第三方 Skill、发送凭证、读取浏览器 Cookie、连接专有交易客户端或触发订单的动作都不属于本 Issue。
