# 冻结公开数据行业案例设计

## 目标

Issue #19 用能源、银行和消费三个端到端案例验证现有行业框架。案例不是行情预测或选股推荐，而是检验“宏观/监管指标能否映射到公司事实”。每个案例先固定命题、成功标准、失败条件和替代解释，再计算；支持与不支持结果同时发布。

## 方案比较

### A：每次运行实时 API

数据最新，但需要 Key、易受 schema/修订/限频影响，CI 不能复现历史结果，不采用。

### B：只写三篇手工报告

阅读方便，但数值、单位、哈希和结果无法机器复验，不满足 case-validated。

### C：小型官方数据快照 + 通用验证器 + 离线报告（采用）

只保存案例所需的少量政府公开事实。每个案例有 `manifest.yaml`、规范化 CSV、预注册配置和 Markdown 报告；实现检查 SHA-256、schema、主键、单位、可得时间、缺失/重复，再计算预先定义的指标。原始下载文件与临时响应不提交，生成过程和上游 URL写入 manifest。

## 历史时点纪律

案例的决策日不得早于任何输入的 `available_at`。SEC 数据保留 filing date 与 accession；Census 优先历史发布文件；FDIC/EIA 当前 API 快照若无法证明历史初值，只能用于“抓取日当时可知”的横截面或明确标为 current-corrected，不能回填过去决策。

每个输入记录 provider、endpoint/文件、参数、抓取时刻、数据截止日、行数、单位、主键与内容哈希。分析代码禁止联网；只有显式 ingest 命令未来可更新快照，更新必须产生新 vintage，不能覆盖旧文件。

## 三个案例命题

### 能源

检验“油价/库存变化足以解释综合能源公司的现金流”。正向部分检查 WTI 与公司经营现金流的方向；负向部分检查美国商业原油库存是否能稳定解释公司结果。失败意味着宏观信号必须经过产量、实现价、炼化、套保、成本和资本开支桥。

### 银行

检验“监管资本率看起来合格即可排除流动性脆弱”。用同一法律实体和季度的 FDIC 事实计算证券未实现损失、存款变化与资本缓冲。负结果预期是单一资本率不能替代存款结构、可变现资产与融资压力。

### 消费

检验“美国宏观零售增长可直接代理单家公司收入增长”。宏观与 SEC 公司收入按首次可得日对齐；正向部分只承认方向一致的区间，负向部分保留行业增长但公司表现分化或映射权重不足。

## 数据与代码结构

```text
raw/cases/{energy,bank,consumer}/
  manifest.yaml
  observations.csv
config/cases/{energy,bank,consumer}.yaml
src/investkb/cases.py
output/cases/{energy,bank,consumer}.md
tests/test_frozen_sector_cases.py
```

CSV 不保存 Cookie、Token、私人路径或持仓。`manifest.yaml` 的 `snapshot_sha256` 必须与原始 CSV 字节一致。通用加载器拒绝错误哈希、重复主键、未知单位、无时区时间、决策日早于可得日、非有限数值和 silent missing。

## 验证与覆盖

测试必须包含真实快照的确定性结果和临时坏 fixture。只有 source + report + test 三类证据齐全，才把 `sector-energy-case`、`sector-bank-case` 与 `sector-consumer-case` 提升为 validated。`sector-framework` 只有在三个案例都揭示并固化边界后再评估；不能用页面数量升级。

## 发布

Issue #19 → `codex/frozen-sector-cases` → PR → CI/Policy → squash merge。数据更新另开 Issue 和新 vintage；旧结果永不原地改写。
