---
title: A股市场
aliases: [中国内地股票市场]
category: markets
markets: [A股]
level: beginner
status: validated
sources: [raw-official-sse-investor-education, raw-official-szse-investor-education, raw-official-sse-trading-rules]
updated: 2026-07-18
---

# A 股市场

A 股是在中国内地证券交易所交易、以人民币计价的股票。不同交易所和板块在投资者适当性、涨跌幅、申报与交易单位上可能不同，不能用一套规则概括所有证券。

新手先分清证券代码所属市场与板块，再查看 [[交易时段]]、[[交易费用]] 和公告。公司研究从交易所或巨潮资讯的法定披露开始。

## 订单练习边界

上交所当前入口显示主板常见买入申报以 100 股整数倍、A股最小价格变动 0.01 元、一般股票日涨跌幅 10%；科创板、风险警示、上市初期、重新上市和新规则生效期存在差异。2026 年规则更新还改变盘后定价与风险警示参数，因此不能把三个数字写成全市场永久常量。

`MarketRule` 要求显式输入板块、生效日、tick、lot、参考价和涨跌幅；`validate_order` 拒绝停牌、规则生效前日期、越界价格和错误申报单位。`calculate_fees` 分项保存佣金、经手/过户与卖出侧税费，具体费率仍回到当日官方与券商合同。

市场订单不保证价格，涨跌停也不保证可成交。参见 [[市场微观结构]]、[[清算结算与托管]]、[[公司行动与退市]]。
