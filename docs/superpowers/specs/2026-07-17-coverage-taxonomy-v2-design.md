# 知识覆盖分类 v2 设计

## 背景与授权

Issue #16 来自用户对当前内容规模和章节深度的直接质疑：42 个粗粒度要求会让“有一页 Wiki”过早变成 reviewed/validated，60.4% 因而不能代表一个庞大、可训练、可实证、可维护的投资知识体系。

用户已授权持续自主建设并要求多用 Issue/PR、书籍、论文、GitHub 仓库与网上资料。Issue #16 固定本批边界：只升级完成度定义、清单颗粒度、证据门槛与报告，不在同一 PR 大量新增课程正文；金融统计内容由 Issue #17 紧随实施。

## 方案比较

### 方案 A：只把 42 行拆成 100 行

改动最小，但仍沿用“页面存在即可接近完成”的逻辑；拆分可能只是数字膨胀，不能区分看过、会算、做过案例与能持续维护。

### 方案 B：taxonomy 与 evidence 拆成两个配置文件

定义和状态职责清晰，但需要跨文件 ID 对齐、迁移与双重审计，容易出现 taxonomy 有要求而 coverage 漏状态，现阶段复杂度超过收益。

### 方案 C：单文件原子能力 + 阶段证据（采用）

每条要求仍在 `config/knowledge-coverage.yaml`，但 schema v2 新增 `stage`。一个主题可有多条原子能力，例如“概率基础内容”“概率手算/Python 练习”“抽样偏差投资案例”。报告同时按知识轴、证据状态和能力阶段汇总。

## 知识轴

v2 使用八个互不替代的轴：

1. `foundations`：数学、概率统计、经济金融与会计基础。
2. `markets`：司法辖区、交易、披露、结算、税费与投资者保护。
3. `assets`：股票、债券、基金、现金、外汇、商品、REIT、衍生品等法律与现金流结构。
4. `sectors`：产业链、商业模式、指标、财务与估值应用。
5. `company`：法定披露、三表勾稽、盈利质量、估值、治理与公司案例。
6. `methods`：实证、因果、时间序列、因子、回测、数据质量与行为纪律。
7. `portfolio`：投资政策、组合构建、再平衡、风险、绩效归因与决策记录。
8. `engineering`：数据适配、测试、谱系、发布、安全、监控、Skill 与私人隔离。

## 能力阶段

每条要求必须指定一个阶段；阶段不是状态的同义词：

| stage | 问题 | validated 的最小证据组合 |
|---|---|---|
| `content-ready` | 是否有权威来源和完整中文合成？ | `source + synthesis` |
| `exercise-tested` | 是否能通过手算、代码或测试执行？ | `synthesis + test` 或 `implementation + test` |
| `case-validated` | 是否用冻结公开数据完成正/负结果案例？ | `source + report + test` |
| `maintenance-live` | 是否由持续工作流守护？ | `workflow + test` |

阶段门槛只在 `status: validated` 时强制满足。`missing` 没有证据；`seed` 有单点材料；`reviewed` 有经检查的部分证据但仍有明确 gap；`validated` 只表示这条原子能力的指定阶段证据齐全，不表示整个主题、投资系统或收益已经完成。

模板、配置或页面数量不能替代上述组合。多个同类证据不算多个能力阶段。

## 清单规模与分布

首版 v2 目标约 120 条，至少 100 条，覆盖：

- 金融/统计基础：货币时间价值、概率、分布、抽样、估计、检验、回归、时间序列、因果、会计和公司金融。
- 市场：A/HK/US/韩国、日本、欧洲、新兴市场与跨境访问。
- 资产：股票、债券、基金、现金、外汇、黄金、商品、REIT、可转债、衍生品。
- 行业：通用框架、存储、能源、金融、消费、医药、互联网及冻结案例。
- 公司与方法：披露时点、三表、质量、估值、治理、实证、回测、偏差和负结果。
- 组合与工程：IPS、配置、再平衡、风险、绩效、免费数据、CI、Pages、安全、监控和 Skill。

新增能力没有证据时必须标记 missing；因此分母和缺口会增加，v2 readiness 预计显著低于 v1 的 60.4%。报告要明确显示“基线变更”，防止把下降误解为删除成果。

## 数据模型与验证

`CoverageRequirement` 新增 `stage: str`；schema 版本必须是 2。允许轴和阶段采用固定枚举。验证继续检查唯一 ID、日期、路径、证据 kind 和 gap，并新增：

- 未知 stage/axis 失败。
- validated 必须满足该 stage 的一个完整证据组合。
- reviewed/seed 不得伪装成阶段完成，必须保留 gap。
- 仓库清单至少 100 条、八轴和四阶段均有要求；临时测试 fixture 不受规模限制。
- 报告按轴与阶段各生成一张状态/就绪度表，并在逐项表加入阶段列。

## 迁移原则

现有 42 条不机械保留 validated：

- 有 source+synthesis 的市场/内容能力可作为 `content-ready: validated`。
- 有 implementation/synthesis + test 的代码与方法能力可作为 `exercise-tested: validated`。
- 没有冻结公开数据报告的，不得变成 `case-validated: validated`。
- 工程能力只有 workflow+test 同时存在才可 `maintenance-live: validated`。
- 一条旧要求同时混合多个能力时拆分，新条目按实际证据分别 missing/reviewed/validated。

## 输出与兼容

- CLI 名称保持 `coverage validate|report`，避免工作流和维护 Skill 断裂。
- 报告标题继续强调“仓库就绪度，不是预期收益”。
- README、AGENTS、Skill 与 Pages 覆盖入口解释 v2 阶段。
- schema v1 不再接受，避免旧清单被静默解释；迁移在同一 PR 原子完成。

## 测试与发布

先写 schema v2、未知阶段、阶段证据组合、100+ 清单和报告阶段表的失败测试，再修改实现和迁移清单。运行完整 `scripts/verify.sh`，确认 v2 报告连续生成字节一致、公开边界与 MkDocs strict 通过。

只通过 Issue #16、`codex/coverage-taxonomy-v2`、PR、required checks 和 squash merge 发布。经验账本记录“粗粒度清单制造虚高完成度”及迁移前后分母/分数变化。
