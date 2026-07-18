# 冻结案例：HML 公开因子复现

> 数据版本：Kenneth French Data Library 2026-05 CRSP vintage；使用 2000—2025 年年度 HML。

## 预注册命题

在固定窗口内，HML 的年度算术均值与全期复合收益都为正。

- **预设成功标准**：两种口径同时大于 0。
- **预设失效条件**：任一口径不大于 0，或年度序列不连续。

## 来源事实

官方 Fama/French 三因子 ZIP 中提取 26 年 × 4 个最小年度事实；冻结 CSV 的 SHA-256：`9d281587d0e1fcbf3eb9dd1fc12311a95acc42bed777171f367ea6c2ff097bb8`。完整原始档案不再分发，须从官方资料库取得并遵守版权边界。

## 计算结果

HML 年度算术均值 1.95%，26 年全期复合收益 7.97%，正收益年份 14 个，故 `hypothesis_supported=true`。算术均值是单期平均，7.97% 是全期几何累乘结果，不是 CAGR。

## 局限

当前 vintage 会因 CRSP 历史修订而变化；年度聚合隐藏月内路径，窗口端点敏感；因子组合不是可直接无摩擦交易的 ETF，正历史结果不是未来溢价承诺。

## 离线复现

```bash
.venv/bin/python -c "from investkb.cases import load_case_snapshot; from investkb.evidence_cases import evidence_metrics; print(evidence_metrics(load_case_snapshot('raw/cases/factor-strategy/manifest.yaml', decision_date='2026-07-17'), analysis='factor'))"
```

离线流程先验证 SHA-256、年度连续性、单位和首次可得日。
