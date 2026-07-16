# AGENTS.md

本文件适用于整个仓库。目标是让任何 Codex 会话都按同一套可追溯、可验证的方式维护知识与代码。

## 不可违反的边界

1. `raw/` 是来源层：已有条目不得无记录覆盖；来源发生变化时新增版本，并在旧卡中写 superseded 关系。
2. `wiki/` 由代理维护、用户阅读。任何事实性结论都要在 frontmatter 的 `sources` 中引用 Raw ID。
3. `output/` 是派生结果，必须记录复现命令、数据截止日和限制。
4. 不承诺收益、不输出“必涨”结论、不把回测描述为实盘业绩。
5. 第一版禁止连接券商、自动交易、分钟/Tick 高频、杠杆和做空。
6. 不提交 API 密钥、账户、持仓、个人资产、行情缓存或第三方完整仓库。

## 来源等级

- A：监管机构、交易所、法定披露、基金正式文件、统计机构。
- B：同行评审论文、权威教材、维护良好且许可证明确的开源项目。
- C：专业媒体、机构研究和成熟投资者公开材料。
- D：论坛、社交媒体和未经验证的个人观点，只用于发现线索。

规则或事实冲突时优先更新的一手来源；不能消解的冲突在 Wiki 并列展示并标记 `status: disputed`。

## Raw 摄取流程

1. 读取并确认来源主体、发布日期、适用市场和版本。
2. 建立来源卡，填写 `id/title/publisher/url/retrieved/source_grade/markets/usage`。
3. 对文件快照记录 SHA-256；未知许可证使用 `NOASSERTION` 和 `link-and-analyze-only`。
4. 写简短摘要、可采纳内容、限制和关联 Wiki 页，不大段复制受版权保护内容。
5. 更新 `raw/source-catalog.md`、相关 Wiki 页、`wiki/index.md`。
6. 向 `wiki/log.md` 追加 ingest 记录，不改写旧日志。

## Query 流程

1. 先读 `wiki/index.md` 和相关 Wiki 页。
2. 对交易规则、费用、数据口径和高风险结论回查 Raw。
3. 区分来源事实、计算结果和推断；推断必须显式标记。
4. 用户要求沉淀时把结果写入 Wiki 或 `output/reports/`，更新索引与日志。

## Wiki 约定

所有知识页使用 YAML frontmatter：`title/aliases/category/markets/level/status/sources/updated`。正文优先包含定义、重要性、机制或公式、A/HK 差异、示例、误区、检查清单、相关页面和来源。

双链使用 `[[页面名]]`。关键页面必须从 `wiki/dashboard.md`、`wiki/index.md` 或其他主题页可达。重命名页面时同步修改所有双链。

## 量化与代码规则

- 新功能与 bugfix 必须先写会因目标行为缺失而失败的测试，再写最小实现。
- 数据、指标、费用、撮合和回测核心函数必须有手算小样本测试。
- 收盘信号只能在下一可交易时点成交；禁止同一 K 线偷看未来。
- 数据必须记录 provider、接口、参数、抓取时间、版本、行数和内容哈希。
- 空响应、字段变化、重复主键、OHLC 错误和非正价格必须显式失败。
- 策略研究必须包含基准、费用、滑点、不可成交、样本外和参数敏感性。

提交前运行：

```bash
.venv/bin/ruff check src tests
.venv/bin/pytest -q
```

## Lint 与日志

定期检查断链、关键孤儿页、缺来源、陈旧规则、冲突状态、未固定的第三方 commit 和未知许可证。日志只追加以下格式：

```markdown
## [YYYY-MM-DD] ingest|query|lint|research | 标题
- changed: [[页面]]
- sources: raw-id
- result: 一句话结果
```
