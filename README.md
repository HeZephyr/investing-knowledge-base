# 全球投资知识库

面向完全新手的中文全球投资学习与量化研究仓库。它把原始来源、持续维护的 Wiki、免费行情代码和可复现研究放在一起，并可直接作为 Obsidian 仓库打开。首批可交易实现聚焦 A/HK，知识范围已扩展到美股、韩国、日本、欧盟与新兴市场，以及全球 ETF/基金、债券、商品、黄金、存储半导体、能源、金融、消费、医药和互联网平台，并通过机器覆盖审计继续增加统计训练、地区、资产、行业与冻结数据案例。

> [!WARNING]
> 本项目用于学习和研究，不构成投资建议，也不承诺盈利。历史回测不代表未来表现。第一版不连接券商、不自动下单，只研究 A 股和港股的日线/周线数据。

## 从哪里开始

1. 在 Obsidian 选择“打开本地仓库”，选中本目录。
2. 打开 [学习仪表盘](wiki/dashboard.md)，从风险与市场规则开始。
3. 阅读 [学习路线](wiki/learning-path.md)，不要跳过交易成本、复权和未来函数。
4. 需要追溯结论时，从 Wiki 页的 `sources` 返回 `raw/` 来源卡。

仓库的分层、地区/资产/行业索引和公开/私人边界见 [项目总索引](docs/INDEX.md)。贡献必须从 Issue 开始并通过 PR；详见 [贡献指南](CONTRIBUTING.md)。

维护者和 AI 代理可复用仓库内的 [`maintain-investing-knowledge-base` Skill](skills/maintain-investing-knowledge-base/SKILL.md)，统一执行来源摄取、知识合成、索引、数据验证、公开边界和 PR 发布。

对外部金融代码库的采用先经过[金融研究代码库审计](wiki/engineering/金融研究代码库审计.md)。仓库内的 `investing-research` 插件只扫描已经合法下载的本地代码，不联网、不读取 Cookie/Token、不连接券商或自动下单；安装和更新命令见 [`plugins/investing-research/README.md`](plugins/investing-research/README.md)。

[金融量化平台与 Skill 审计](wiki/engineering/金融量化平台与Skill审计.md)进一步比较 FinHack 与 finance-quant-skills，并把每个 Agent Skill 当作可执行供应链材料检查。插件 v0.2 增加 `$audit-finance-skills`，默认不安装第三方 Skill、不执行上游脚本，并隔离 Cookie、账号和实盘订单能力。

网页版本会由 GitHub Pages 自动发布，提供中文全文搜索、知识图谱、学习进度与复利/费用/回撤计算器。学习进度仅保存在浏览器本地。

## 完成度怎么计算

[覆盖审计](output/reports/knowledge-coverage.md)把体系拆成基础学科、市场、资产、行业、公司、方法、组合和工程 8 个轴，共 135 项原子能力。v2 初始基线为 36.5%；完成金融统计、代码库审计、全球市场资产、十一项冻结证据能力，以及基础学科、全球市场、公司、研究方法与组合实验室后为 **90.9%**。基础学科 20/20、市场制度 16/16、公司研究 16/16、研究方法 18/18、组合与风控 14/14 已验证，其余轴仍按真实缺口推进。

- `content-ready`：权威来源与中文合成均就绪。
- `exercise-tested`：计算、代码或练习有自动测试。
- `case-validated`：使用冻结公开数据完成可复现的正/负结果案例。
- `maintenance-live`：CI 或定时工作流持续守护。

覆盖率表示仓库就绪度，不表示投资胜率或预期收益。当前 11 项案例能力已全部通过冻结公开数据、报告和自动测试验证；其余内容、练习与维护能力仍按审计缺口推进，不会用空模板或叙事页伪装成完成。

## 三层结构

- `raw/`：不可原地改写的来源卡、官方资料和合法快照。
- `wiki/`：由 LLM 维护、适合阅读和双链浏览的中文知识网络。
- `output/`：研究报告、图表、筛选结果和空白模板。

行情缓存放在 `data/cache/`，第三方仓库临时快照放在 `data/reference-repos/`；两者均不会提交 Git，也不会污染 Obsidian 导航。

## 5 分钟开发环境

```bash
/Users/zephyr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m venv .venv
.venv/bin/pip install -e '.[dev,data,site]'
.venv/bin/pytest -q
```

常用命令：

```bash
investkb sources audit raw
investkb wiki lint
investkb data fetch CN 510300 --start 2024-01-01 --end 2024-12-31 --adjustment none
investkb fund nav 000001 --start 2024-01-01 --end 2024-12-31
investkb demo backtest --offline
python -m investkb.site
mkdocs serve
```

## 研究纪律

- 官方规则、法定披露和基金文件优先；社区材料只作为线索或方法参考。
- 免费接口没有服务等级保证，空数据和字段变化必须报错。
- 收盘生成的信号最早在下一可交易时点成交。
- 回测必须披露样本池、基准、费用、滑点、参数、数据截止日和限制。
- 不把 Star 数、名人观点、单次回测或短期涨幅当作正确性证据。

## 项目状态

第一版已具备 Raw/Wiki 审计、免费 A/HK 日线与基金净值适配、数据质量检查、次日成交回测、指标和报告生成。设计和实施计划位于 `docs/superpowers/`，实际验收结果见 [第一版验收记录](docs/verification/first-release.md)。

运行完整健康检查：

```bash
scripts/verify.sh
```
