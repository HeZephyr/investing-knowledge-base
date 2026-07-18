---
title: 海外ETF
aliases: [Global ETF, 美国ETF]
category: products
markets: [全球, 美股, 港股]
level: beginner
status: validated
sources: [raw-official-sec-etf-bulletin, raw-official-sec-edgar, raw-official-irs-overseas-etf-taxes, raw-official-sec-index-funds]
updated: 2026-07-18
---

# 海外 ETF

海外 ETF 可以覆盖地区、行业、债券、商品和策略，但“ETF”只描述交易与基金结构的一部分，不代表低风险或适合长期持有。

## 核对清单

- 注册地、监管框架、发行人、托管、指数和法律结构。
- 总费率、买卖价差、规模、成交量、折溢价和跟踪误差。
- 实物/合成复制、证券借贷、衍生品、杠杆或反向目标。
- 分红政策、预扣税、遗产税、交易税费与投资者身份限制。
- 基金计价币种不等于资产真实货币暴露，需另看 [[汇率风险]]。

美国注册 ETF 可从 SEC EDGAR 查询招股书和定期持仓申报。参见 [[ETF]]、[[全球市场]]、[[黄金]]、[[流动性风险]]。

## 跨币种收益

投资者本币收益不是“基金显示币种”单独决定：`(1 + 资产本地收益) × (1 + 本币计价汇率变化) − 1`。基金可能另有货币套保，套保成本、展期和基差又会改变结果。

```python
from investkb.assets import cross_currency_return

home_return = cross_currency_return(local_return=0.10, fx_return=-0.05)
```

## 税务只做风险清单

IRS 2026 Publication 515 展示美国来源收入对外国收款人的一般预扣框架，协定、受益所有人资格和收入分类可能改变税率。IRS 2026-06-27 页面还提示：美国法下公司股票可能构成非居民非公民的美国所在地遗产资产，并存在 Form 706-NA 门槛与协定问题。

这些事实不能自动映射到某位读者。注册地相同的 ETF 也可能因分派性质、持有人身份、账户和协定不同而结果不同；同时还需核对居住地税制。仓库不提供个税结论，交易前应按当年规则咨询合资格专业人士。

## 常见失败

- 只看 ticker，不核对基金注册地、份额类别和实际资产暴露。
- 把报价币种等同已套保币种。
- 把一般 30% 预扣或 60,000 美元申报门槛写成对所有人的最终税率/免税额。
- 忽略交易时区、底层市场休市导致的折溢价和陈旧 NAV。

参见 [[ETF]]、[[指数]]、[[汇率风险]]、[[全球市场]]、[[流动性风险]]。
