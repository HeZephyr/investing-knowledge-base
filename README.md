# A 股与港股理财知识库

面向完全新手的中文投资学习与量化研究仓库。它把原始来源、持续维护的 Wiki、免费行情代码和可复现研究放在一起，并可直接作为 Obsidian 仓库打开。

> [!WARNING]
> 本项目用于学习和研究，不构成投资建议，也不承诺盈利。历史回测不代表未来表现。第一版不连接券商、不自动下单，只研究 A 股和港股的日线/周线数据。

## 从哪里开始

1. 在 Obsidian 选择“打开本地仓库”，选中本目录。
2. 打开 [学习仪表盘](wiki/dashboard.md)，从风险与市场规则开始。
3. 阅读 [学习路线](wiki/learning-path.md)，不要跳过交易成本、复权和未来函数。
4. 需要追溯结论时，从 Wiki 页的 `sources` 返回 `raw/` 来源卡。

## 三层结构

- `raw/`：不可原地改写的来源卡、官方资料和合法快照。
- `wiki/`：由 LLM 维护、适合阅读和双链浏览的中文知识网络。
- `output/`：研究报告、图表、筛选结果和空白模板。

行情缓存放在 `data/cache/`，第三方仓库临时快照放在 `data/reference-repos/`；两者均不会提交 Git，也不会污染 Obsidian 导航。

## 5 分钟开发环境

```bash
/Users/zephyr/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m venv .venv
.venv/bin/pip install -e '.[dev,data]'
.venv/bin/pytest -q
```

常用命令：

```bash
investkb sources audit raw
investkb wiki lint
investkb data fetch CN 510300 --start 2024-01-01 --end 2024-12-31 --adjustment none
investkb fund nav 000001 --start 2024-01-01 --end 2024-12-31
investkb demo backtest --offline
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
