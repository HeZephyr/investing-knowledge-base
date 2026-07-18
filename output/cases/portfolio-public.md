# 冻结案例：A 股、国债与黄金等权组合

> 公开教学案例：510300、511010、518880 的 2019—2025 年末价格代理；不是个人持仓或配置建议。

## 预注册命题

三资产每年恢复 1/3 等权、按换手扣 10bp 后，在 2020—2025 年同时取得高于 510300 的 CAGR 与低于它的年度波动率。

- **预设成功标准**：费用后组合 CAGR 更高且样本年度波动率更低。
- **预设失效条件**：任一条件不满足，或价格序列缺年、非正或无法冻结。

## 来源事实

AKShare 的无认证 `fund_etf_hist_sina` 接口取得三个代码的年末收盘价；21 行 CSV 的 SHA-256：`20952f43012b5cd47bd1e8fa04c40056264c9ccf38bd537f548d82057a7b3d4a`。Eastmoney 路径在当前网络失败后使用合法公开备选，不使用 Cookie。

## 计算结果

首次建仓换手为 1，后续按前一年资产收益漂移后的权重计算单边换手并恢复等权。组合累计收益 61.66%、CAGR 8.33%、年度波动率 11.33%、最大回撤 -5.36%；510300 价格基准累计收益 16.04%、CAGR 2.51%、年度波动率 19.54%，故 `hypothesis_supported=true`。

## 局限

这是未复权年末价格代理，分红、利息分配及总收益调整未被证明；样本只有六个收益年，年末采样掩盖日内与年内回撤。黄金与股票端点对结果贡献很大，正回测不等于可投资预期或未来赚钱保证。

## 离线复现

```bash
.venv/bin/python -c "from investkb.cases import load_case_snapshot; from investkb.evidence_cases import evidence_metrics; print(evidence_metrics(load_case_snapshot('raw/cases/portfolio-public/manifest.yaml', decision_date='2026-07-17'), analysis='portfolio', fee_bps=10))"
```

离线复现会校验 SHA-256、单位、主键、连续年份、正价格与费用范围。
