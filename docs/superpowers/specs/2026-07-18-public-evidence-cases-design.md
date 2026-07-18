# 公司、因子、策略与组合公开案例设计

## 目标

Issue #31 完成 v2 剩余五项 `case-validated` 能力。每项必须有预注册命题、公开冻结事实、费用/基准或估值桥、支持/不支持结论、自动测试与放弃条件。案例用于验证研究流程，不构成证券推荐或未来收益承诺。

## 复用与去重

- 公司正结果新增 Meta 2022—2024 财务快照，验证经营杠杆、FCF 转化和每股桥。
- 公司负结果复用 Aduhelm 的 FDA→CMS→Biogen 快照，新增公司研究“放弃原商业化命题”报告，不复制同一事实。
- 因子复现与无效策略共用 Kenneth French 2000—2025 年度最小快照，但使用两份独立预注册配置和报告。
- 多资产组合使用三只 A 股上市 ETF 的公开年末收盘价，明确为 price-return proxy；不冒充含分红总回报或可交易建议。

## 方案边界

### 公司正结果

命题：Meta 在 2022 成本高点后，到 2024 能在收入不收缩的同时使 GAAP 营业利润率和公司定义 FCF 率各提高至少 10 个百分点，且稀释股数不增加。成功只证明这段历史财务桥成立；不证明当前估值便宜、AI Capex 回报或未来增长。

### 公司负结果

命题与 healthcare case 相同：accelerated approval 足以带来广泛覆盖和可持续需求。公司级报告必须明确 `abandon_original_thesis=true`，列出何时可以重新研究，不把放弃产品命题扩大为放弃整家公司或治疗类别。

### 因子复现

固定 Kenneth French 2026-05 CRSP vintage 的 2000—2025 年度 Mkt-RF、SMB、HML、RF。复现 HML 算术均值、几何累计和正收益年份，不使用事后子样本挑选。上游文件有版权声明，仓库只保存完成计算所需的年度数值、版本与哈希，不保存完整月度文件。

### 无效策略

预注册年度反转规则：若上一年 `Mkt-RF < 0`，下一年持有市场总回报代理 `Mkt-RF + RF`；否则持有 RF。每次仓位变更收 10bp，2001—2025 与始终持有市场比较。失败条件是费用后 CAGR 不高于基准；不调参数、不加入止损。

### 多资产组合

使用 510300（权益）、511010（国债 ETF）、518880（黄金 ETF）2019—2025 年最后交易日收盘价。2020 初等权，年度再平衡到 1/3；首建仓和之后双边最小换手按 10bp 收费；基准为 510300 price return。报告同时给累计、CAGR、年波动和最大回撤。

该数据来自 AKShare 的新浪公开接口，当前 Eastmoney 路径失败已记录。收盘价未证明复权/分红处理，三资产单位不同且 ETF 有折溢价，所以只作方法案例；任何实盘采用前必须换成基金官方 NAV/总回报和真实费率。

## 文件结构

```text
raw/cases/{company-positive,factor-strategy,portfolio-public}/
config/cases/{company-positive,company-negative,factor-replication,negative-strategy,portfolio-public}.yaml
output/cases/{company-positive,company-negative,factor-replication,negative-strategy,portfolio-public}.md
src/investkb/evidence_cases.py
tests/test_public_evidence_cases.py
```

`evidence_cases.py` 只读通过 `investkb.cases` 验证的快照。因子与策略、组合计算采用确定性纯函数，拒绝缺期间、非连续年份、非法费率和零价格。测试固定正例、负例、费用、基准与报告字段。

## 覆盖升级

只有对应 source + report + test 全部存在才升级：`company-case-positive`、`company-case-negative`、`method-factor-replication`、`method-negative-results`、`portfolio-public-case`。现有 content/exercise 能力不因案例顺带升级；需要独立证据。
