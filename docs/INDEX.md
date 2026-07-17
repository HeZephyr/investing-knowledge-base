# 项目总索引

这是仓库级入口；网页用户从 `site/index.md` 进入，Obsidian 用户从 `wiki/dashboard.md` 进入。

## 按知识层

1. **来源层**：`raw/source-catalog.md` → 官方资料、论文、参考仓库卡片。
2. **知识层**：`wiki/index.md` → 市场、资产、产品、行业、概念、风险、量化。
3. **产出层**：`output/README.md` → 公司、基金、回测、交易检查与复盘模板。
4. **私人层**：`private/` → 本地持仓与个人研究，永不进入 Git 或 Pages。

## 按研究维度

- **地区**：全球框架 → A 股 / 港股 / 美股 / 韩国市场 → 后续日本、欧洲与新兴市场。
- **资产**：股票、基金/ETF、黄金与商品；后续债券、REIT、可转债、现金与外汇。
- **行业**：存储半导体作为第一份行业模板；后续可复制到能源、金融、消费、医药等。
- **方法**：市场规则 → 财务与估值 → 数据质量 → 回测 → 风险与组合。

## 工程入口

- `src/investkb/data/`：免费数据适配器与缓存模型。
- `src/investkb/backtest/`：避免未来函数的日线回测。
- `src/investkb/site.py`：Obsidian 内容转静态站与知识图谱。
- `src/investkb/publication.py`：公开/私人边界检查。
- `.github/workflows/`：CI、安全、定时数据健康检查与 Pages 发布。
- `skills/maintain-investing-knowledge-base/`：可移植的知识库维护 Skill、来源评估参考与脚手架。
- `config/knowledge-coverage.yaml`：版本化完成要求与证据；生成 `output/reports/knowledge-coverage.md`，不以页面数量冒充完成。

## 维护入口

- 开发协作：`CONTRIBUTING.md`
- 项目治理：`GOVERNANCE.md`
- 代理规范：`AGENTS.md`
- 安全报告：`SECURITY.md`
- 内容分层：`docs/architecture/content-layers.md`
- 经验与事故：`wiki/methods/经验与失败教训.md`
