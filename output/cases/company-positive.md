# 冻结案例：Meta 经营改善正结果

> 决策日：2026-07-17。这里只检验公开财务命题，不作估值，也不构成证券推荐。

## 预注册命题

Meta 2022—2024 年收入增长，同时 GAAP 营业利润率与自由现金流率各改善至少 10 个百分点，且稀释股数不增长。

- **预设成功标准**：收入上升；两项利润率各改善至少 10 个百分点；稀释股数不增加。
- **预设失效条件**：收入下降、任一利润率改善不足 10 个百分点，或稀释股数增加。

## 来源事实

Meta 官方 2023、2024 全年业绩提供收入、GAAP 营业利润、自由现金流及稀释股数。12 条规范化观察的 SHA-256：`70e81cdfabffdeb5e05572184542babd23d2c68e7a7f13f3bd59ef12af00d508`。

## 计算结果

2022—2024 年收入增长 41.07%；营业利润率改善 17.35 个百分点；自由现金流率改善 15.86 个百分点；稀释股数变化 -3.26%；每稀释股自由现金流增长 192.08%。全部通过预设门槛，`hypothesis_supported=true`。

## 局限

这是会计期端点比较，未把重组、广告周期、汇率、法律应计、资本开支时点与营运资本分别归因；正结果不代表当前价格便宜，也不保证未来延续。

## 离线复现

```bash
.venv/bin/python -c "from investkb.cases import load_case_snapshot; from investkb.evidence_cases import evidence_metrics; print(evidence_metrics(load_case_snapshot('raw/cases/company-positive/manifest.yaml', decision_date='2026-07-17'), analysis='company'))"
```

复现只读取公开冻结 CSV，先校验 SHA-256、单位、主键与可得时点。
