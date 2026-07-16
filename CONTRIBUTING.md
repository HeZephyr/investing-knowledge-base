# 贡献指南

本项目采用 Issue → 分支 → Pull Request → CI → Review → 合并的公开协作流程。禁止直接在 `main` 上开发或推送。

## 第一次贡献

1. Fork 仓库或成为协作者，安装 Python 3.11+。
2. 从 Issue 创建短分支：`codex/<topic>`、`feat/<topic>`、`fix/<topic>` 或 `docs/<topic>`。
3. 安装：`python -m pip install -e '.[dev,data,site]'`。
4. 代码和 Bug 修复先写失败测试；事实和规则先建立 Raw 来源卡。
5. 同步 Wiki、[总索引](docs/INDEX.md)与必要日志，运行 `scripts/verify.sh`。
6. 用 Conventional Commits 提交，创建 PR，并请求 CODEOWNER 或领域维护者审查。

## PR 规则

- 标题格式：`feat(site): add global market index`、`data(korea): update KRX rules`。
- 正文必须关联 Issue，说明来源/数据截止日、风险、验证和公开边界。
- 作者不能审批自己的 PR；维护者以 squash merge 为默认合并方式。
- 涉及交易规则、费用、数据口径、公开边界、Actions 或依赖权限的改动至少需要一名维护者批准。
- 大变更拆成可独立审查的 PR；避免把内容采集、核心代码重构和 UI 改版混在一起。

## 内容贡献

- Raw 优先一手和稳定 URL，只写摘要与可采纳事实，不复制付费或受版权保护全文。
- Wiki 明确区分事实、计算与推断；来源写入 frontmatter `sources`。
- 市场内容按 `markets/`，资产按 `assets/`，产品按 `products/`，行业按 `sectors/`；交叉主题通过双链连接，不重复复制。
- 所有“最新”“现行”信息注明检索日期，过时内容通过新版本替代并保留历史关系。

## 本地公开层

个人持仓、券商记录、资产配置、Cookie、Token 和私人研究放在被 Git 忽略的 `private/`。运行 `python -m investkb.publication` 会检查误放路径和强特征密钥，但它不能替代人工复核。
