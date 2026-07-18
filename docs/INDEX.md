# 项目总索引

这是仓库级入口；网页用户从 `site/index.md` 进入，Obsidian 用户从 `wiki/dashboard.md` 进入。

## 按知识层

1. **来源层**：`raw/source-catalog.md` → 官方资料、论文、参考仓库卡片。
2. **知识层**：`wiki/index.md` → 市场、资产、产品、行业、概念、风险、量化。
3. **产出层**：`output/README.md` → 公司、基金、回测、交易检查与复盘模板。
4. **私人层**：`private/` → 本地持仓与个人研究，永不进入 Git 或 Pages。

## 八轴能力地图

- **基础学科**：数学、概率统计、经济、会计与公司金融。
- **市场**：A 股、港股、美股、韩国、日本、欧盟、新兴市场 → 英国及逐国访问与跨境机制。
- **资产**：股票、基金/ETF、黄金、外汇、债券、商品、REIT、可转债 → 期权、互换及结构化产品。
- **行业**：通用框架 → 存储、能源、金融、消费、医药、互联网 → 更多行业与跨行业案例。
- **公司**：跨市场法定披露与历史时点 → 三表勾稽、收入和现金转换 → 治理、资本配置、稀释 → 反向 DCF、情景与可比估值。
- **方法**：统计推断、因果、时间序列、因子、回测、数据质量与负结果。
- **组合**：投资政策、配置、再平衡、流动性、压力测试、归因与决策日志。
- **工程**：数据适配、谱系、测试、发布、安全、监控、Skill 与私人隔离。

每个主题再区分内容就绪、练习已测、冻结案例验证和持续维护四个阶段。权威来源、会算、做过案例和能够自动维护互不替代；机器权威清单见 `config/knowledge-coverage.yaml`。

## 工程入口

- `src/investkb/data/`：免费数据适配器与缓存模型。
- `src/investkb/backtest/`：避免未来函数的日线回测。
- `src/investkb/company.py`：历史时点、三表、现金转换、稀释、反向 DCF、情景和可比估值练习。
- `src/investkb/site.py`：Obsidian 内容转静态站与知识图谱。
- `src/investkb/publication.py`：公开/私人边界检查。
- `.github/workflows/`：CI、安全、定时数据健康检查与 Pages 发布。
- `skills/maintain-investing-knowledge-base/`：可移植的知识库维护 Skill、来源评估参考与脚手架。
- `plugins/investing-research/`：可安装的只读金融仓库与 Skill bundle 审计插件；采用规则见“金融研究代码库审计”和“金融量化平台与 Skill 审计”（`wiki/engineering/`）。
- `config/knowledge-coverage.yaml`：版本化完成要求与证据；生成 `output/reports/knowledge-coverage.md`，不以页面数量冒充完成。
- `raw/cases/` + `config/cases/` + `output/cases/`：冻结公开数据、预注册和可离线复现的行业、公司、因子、失败策略与多资产组合案例。

## 维护入口

- 开发协作：`CONTRIBUTING.md`
- 项目治理：`GOVERNANCE.md`
- 代理规范：`AGENTS.md`
- 安全报告：`SECURITY.md`
- 内容分层：`docs/architecture/content-layers.md`
- 经验与事故：`wiki/methods/经验与失败教训.md`
