# 冻结案例：反向择时策略负结果

> 同一 2026-05 CRSP vintage；策略规则在读取结果前固定，评价期为 2001—2025 年。

## 预注册命题

若上一年 Mkt-RF 为负，下一年持有市场总收益，否则持有无风险资产；扣除每次仓位变化 10bp 后胜过持续持有市场。

- **预设成功标准**：费用后策略 CAGR 高于持续市场 CAGR。
- **预设失效条件**：费用后 CAGR 不高于基准，或规则需要事后调参。

## 来源事实

市场超额收益与 RF 来自同一官方三因子快照；SHA-256：`9d281587d0e1fcbf3eb9dd1fc12311a95acc42bed777171f367ea6c2ff097bb8`。

## 计算结果

策略只持有市场 6 年、发生 8 次仓位变化；费用后累计收益 160.97%、CAGR 3.91%，持续市场累计收益 794.55%、CAGR 9.16%。因此 `hypothesis_supported=false`，保留负结果而不优化阈值。

## 局限

年度信号极粗，RF 与可交易现金工具并非完全等价；没有滑点、税、借贷、基金跟踪误差和月内路径。单一失败规则不能证明所有趋势或反转策略无效。

## 离线复现

```bash
.venv/bin/python -c "from investkb.cases import load_case_snapshot; from investkb.evidence_cases import evidence_metrics; print(evidence_metrics(load_case_snapshot('raw/cases/factor-strategy/manifest.yaml', decision_date='2026-07-17'), analysis='negative_strategy', fee_bps=10))"
```

计算完全离线，并校验 SHA-256、连续年份与费用边界。
