# Output 派生结果

此目录保存可以从 Wiki、配置和数据重新生成的研究结果。

- `reports/`：Markdown 研究、回测与知识覆盖审计报告；`knowledge-coverage.md` 明确列出仍未完成的要求。
- `cases/`：由冻结公开快照、预注册配置和测试支持的正/负行业案例；首批为[能源](cases/energy.md)、[银行](cases/bank.md) 与[消费](cases/consumer.md)，扩展批次为[医药](cases/healthcare.md)、[互联网](cases/internet.md) 与[存储](cases/memory.md)。
- `charts/`：PNG/SVG 图表。
- `screens/`：筛选结果和候选清单，不等同于买入建议。
- `templates/`：投资政策、公司/基金分析、交易前检查、复盘、通用实证证据卡与行业证据卡模板。

研究观点进入回测或案例前，先复制 `templates/实证证据卡.md`，预注册命题、数据时点、成本、失败标准与复现命令；发生工程或研究事故时复制 `templates/研究事故与教训.md`。负结果和数据事故都要保留。

行业研究使用更具体的预注册合同：

- `templates/能源周期证据卡.md`：物理供需、价格曲线、公司实现价、成本和资本开支。
- `templates/银行资产负债表证据卡.md`：法律实体、监管资本、资产质量、净息差和压力情景。
- `templates/消费单位经济证据卡.md`：量价结构、同店/cohort、渠道库存、现金转换和门店经济。

每份正式报告必须说明数据截止日、来源、假设、基准、费用、限制和复现命令。
