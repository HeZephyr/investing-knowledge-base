---
title: ETF
aliases: [交易型开放式指数基金]
category: products
markets: [A股, 港股, 基金]
level: beginner
status: validated
sources: [raw-official-sse-etf, raw-official-sec-index-funds, raw-official-sec-etf-bulletin, raw-official-sp-index-mathematics]
updated: 2026-07-18
---

# ETF

ETF 在交易所交易，同时具有基金净值和二级市场价格。评价时关注跟踪标的、费用、跟踪差异、流动性、折溢价、复制方法和交易单位。

跟踪差异是基金收益减基准收益的平均偏离，跟踪误差是该主动收益的波动；一个描述方向/成本，一个描述不稳定性。比较前统一价格/总收益、税前/税后、币种、分红再投资、净值时点和频率。

```python
from investkb.assets import tracking_statistics

stats = tracking_statistics(fund_returns, benchmark_returns, periods_per_year=252)
```

折溢价是市场价格相对同一时点 NAV/IOPV 的偏离，不等于跟踪误差。成交量也不等于真实流动性；还要看底层证券、做市、买卖价差、申赎篮子和极端时的估值时差。

同一主题 ETF 不一定等价；先读招募说明书和定期报告。新手不把杠杆、反向或复杂商品 ETF 当作普通指数基金。
