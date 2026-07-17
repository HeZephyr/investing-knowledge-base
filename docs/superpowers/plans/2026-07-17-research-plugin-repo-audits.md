# 金融研究插件与仓库审计实施计划

**Goal:** 交付四仓库证据审计、只读 Codex 插件、安装文档与离线安全测试。

**Architecture:** ignored clone 用于人工/脚本审计；公共 Raw 卡与 Wiki 矩阵保存结论；repo marketplace 插件只包含 Skill、脚本和 fixture，不包含第三方源码或认证。

---

## Task 1：定义失败测试

- 新建 `tests/test_investing_research_plugin.py`，要求 manifest、marketplace、Skill、README 与脚本存在。
- 创建临时仓库 fixture，包含许可证、普通代码和敏感 `.env`；断言扫描只读、离线、不泄漏值、只输出相对路径和固定分类。
- 断言四张 Raw 卡、矩阵、固定 commit 和许可证边界。

## Task 2：用官方脚手架创建插件

- 从 plugin-creator skill root 运行 `create_basic_plugin.py investing-research --path <repo>/plugins --marketplace-path <repo>/.agents/plugins/marketplace.json --with-skills --with-scripts --with-assets --with-marketplace`。
- 用 `apply_patch` 完善 manifest、README、Skill、脚本和 fixture；不手写 marketplace 初始结构。
- 运行 `validate_plugin.py` 与 `quick_validate.py`。

## Task 3：实现只读扫描器

- 只遍历允许的文本扩展名；敏感/构建/数据路径先于读取过滤。
- 可选读取本地 `.git` 元数据但不联网；输出稳定 JSON，不含源码行和绝对路径。
- 为十二类信号设置有界关键词，声明 false positive/false negative。

## Task 4：审计四个本地 clone

- 固定 HEAD、根许可证、最新提交日、顶层架构、测试与文档。
- count-only grep provider、认证、复权、时区、公司行动、缓存、回测、成本、未来函数和自动交易；再人工检查关键 README/配置/测试。
- OpenBB 说明 provider/extension/standard model；其余项目区分代码事实、README 声明和未验证营销。

## Task 5：Raw、Wiki、安装与覆盖

- 更新 OpenBB 卡，新建 stock、AI-Trader、ai_quant_trade 三卡和 manifest/catalog。
- 新建 `wiki/engineering/金融研究代码库审计.md` 对比矩阵与采用/拒绝决策。
- 插件 README 写安装、更新、卸载、无 CLI fallback、认证隔离和示例。
- 更新索引、日志、经验账本和 `engineering-audit-plugin` 覆盖证据；仅在插件验证和离线测试通过后 validated。

## Task 6：验证与发布

- 运行定向测试、两个官方 validator、`scripts/verify.sh` 和公开 diff 强密钥审计。
- 推送主题分支，打开关闭 #22 的 PR；required checks 全绿后 squash merge。
