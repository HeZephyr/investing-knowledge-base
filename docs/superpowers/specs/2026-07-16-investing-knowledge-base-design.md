# A 股与港股理财知识库设计

- 日期：2026-07-16
- 状态：已于 2026-07-16 获用户批准
- 项目路径：`/Users/zephyr/mycode/investing-knowledge-base`
- 远程仓库：同名 GitHub 私有仓库

## 1. 目标与原则

为完全没有持仓和交易经验的个人投资者建立一套中文、Obsidian 友好、可持续维护的 A 股与港股知识库。它不仅保存和整理资料，还包含免费的日线/周线数据管道、可复现的量化研究、回测、选股研究与报告输出能力。

项目以提高长期决策质量、控制风险和形成可验证研究流程为目标，不承诺盈利，不提供“必涨股票”，第一版不接券商账户、不自动下单、不处理分钟级或实时交易。

设计原则：

1. 原始资料可追溯，LLM 生成结论必须能回到来源。
2. 官方规则和一手披露优先于媒体、社区和二手总结。
3. 免费数据必须经过质量检查，不静默吞掉错误或空数据。
4. 所有策略必须计入可成交性、费用、滑点和样本外验证。
5. 知识、数据、代码和输出分层，Obsidian 默认只索引高信噪比内容。
6. 第三方材料只按许可证允许的方式使用，未知许可证默认不可复制。

## 2. 已选方案

采用“分阶段一体化”方案，同时建设知识、数据和量化骨架：

- 第一阶段：市场规则、风险、基金/ETF、新手路线和 Raw 来源体系。
- 第二阶段：免费数据适配器、缓存、标准化和数据质量检查。
- 第三阶段：透明的基础指标与回测引擎、研究模板、报告生成。
- 第四阶段：基本面、因子、滚动验证、组合与更复杂的研究。

不采用纯文档方案，因为无法验证投资想法；不采用量化优先方案，因为新手容易忽略交易规则、数据口径和统计陷阱。

## 3. 仓库结构

```text
investing-knowledge-base/
├── .obsidian/                 # 最小化、可移植的 Obsidian 配置
├── raw/                       # 不可原地修改的来源层
│   ├── official/
│   │   ├── mainland/
│   │   └── hong-kong/
│   ├── books-and-papers/
│   ├── community/
│   ├── repositories/
│   │   ├── catalog.md
│   │   └── cards/
│   ├── source-catalog.md
│   └── assets/
├── wiki/                      # LLM 维护、用户阅读的知识层
│   ├── index.md
│   ├── learning-path.md
│   ├── dashboard.md
│   ├── concepts/
│   ├── markets/
│   ├── products/
│   ├── company-analysis/
│   ├── funds/
│   ├── quant/
│   ├── risk/
│   ├── playbooks/
│   ├── glossary/
│   └── log.md
├── output/                    # 可重新生成的结果
│   ├── reports/
│   ├── charts/
│   ├── screens/
│   └── templates/
├── src/investkb/              # Python 包
│   ├── data/
│   ├── validation/
│   ├── indicators/
│   ├── backtest/
│   ├── strategies/
│   ├── portfolio/
│   ├── reporting/
│   └── cli.py
├── notebooks/                 # 编号的新手教程与研究实验
├── tests/
├── configs/
├── scripts/
├── data/                      # 下载缓存，Git 默认忽略
├── docs/
├── README.md
├── AGENTS.md
├── pyproject.toml
└── .gitignore
```

`raw`、`wiki`、`output` 是用户要求的三个主层。代码和数据缓存独立放置，避免 Raw 的“不可变来源”语义与不断刷新的行情数据冲突。

## 4. Raw 来源体系

### 4.1 来源级别

- A 级：监管机构、交易所、法定披露、基金公司正式文件、统计机构。
- B 级：同行评审论文、权威教材、维护良好且许可证明确的开源项目。
- C 级：专业媒体、机构研究、成熟投资者公开材料。
- D 级：论坛、社交媒体和未经验证的个人观点，只用于发现线索。

结论出现冲突时，优先采用更新的一手规则或披露；无法消解时在 Wiki 中并列记录，不强行合并。

### 4.2 首批内容范围

首批 Raw 至少建立以下专题的来源卡或合法快照：

- A 股与港股市场结构、开户与参与方式、交易时段、订单、结算。
- 主板、科创板、创业板、北交所、港股主板/GEM、沪深港通。
- 涨跌幅、停牌、除权除息、复权、股票代码、交易单位。
- 佣金、交易费、印花税、平台费、汇率与股息税的口径。
- 股票、指数、ETF、公募基金、REITs、可转债和货币基金。
- 招股书、公告、年报、财务三表、审计意见、公司治理。
- 估值、盈利质量、行业分析、竞争优势与风险清单。
- 资产配置、分散、仓位、最大回撤、行为偏差和投资骗局。
- 数据清洗、收益率、复权、幸存者偏差、未来函数、过拟合。
- 回测、因子检验、样本外测试、滚动验证与交易成本。

每个 Raw 条目必须包含来源机构、标题、原始 URL、获取日期、发布日期/版本、适用市场、来源等级、许可证或使用限制、内容哈希和关联 Wiki 页面。

### 4.3 外部代码库

第三方仓库不直接 vendor 到主仓库。每个参考项目建立一张来源卡，保存：

- 仓库 URL、用途、默认分支、固定 commit、最近活动日期。
- Star 仅作为社区关注度信号，不作为正确性证明。
- README 与 LICENSE 的合法快照或链接及内容哈希。
- 值得借鉴的模块、不能直接采用的部分、依赖和许可证风险。
- 与本项目对应的设计决策及验证记录。

首批目录包括：

- `hiboys/ExploreFinance`：参考中文知识分类、学习路径和 Obsidian 组织方式。页面未发现明确许可证，默认只做结构研究，不复制内容。
- `akfamily/akshare`：A 股、港股、基金与宏观数据接口；记录其学术研究定位和上游公开数据风险。
- `baostock/baostock` 或其官方发布：A 股免费数据备用与交叉校验。
- `microsoft/qlib`：数据、模型、策略、回测和实验管理架构参考；高级阶段再采用。
- `ricequant/rqalpha`：A 股交易规则、撮合、账户和费用建模参考；注意其非商业使用限制。
- `kernc/backtesting.py`：轻量回测 API 和策略表达参考。
- `quantopian/pyfolio`、`empyrical` 及维护中的继任项目：绩效与风险指标参考；弃用项目不直接作为核心依赖。
- `wilsonfreitas/awesome-quant`：仅作为发现索引，每个候选仍需独立核验。

脚本可以把固定 commit 浅克隆到 `data/reference-repos/`，该目录不提交 Git，也不进入 Obsidian 知识导航。

## 5. Wiki 与 Obsidian

Wiki 页面使用中文文件名或稳定英文 slug，统一 YAML frontmatter：

```yaml
---
title: 最大回撤
aliases: [Maximum Drawdown, MDD]
category: risk
markets: [A股, 港股]
level: beginner
status: reviewed
sources: [raw-official-sse-001]
updated: 2026-07-16
---
```

页面正文包含：一句话定义、为什么重要、核心机制/公式、A/HK 差异、示例、常见误区、检查清单、相关页面与来源。

Obsidian 配置只提交必要设置：附件目录、排除 `data/` 与开发缓存、模板目录、文件链接风格。核心功能不依赖第三方插件；Dataview 查询作为可选增强，缺少插件时仍能正常阅读。

`wiki/index.md` 是内容目录，`wiki/dashboard.md` 是学习入口，`wiki/log.md` 是追加式操作日志。所有关键页至少有一个入口链接，lint 检查孤儿页、断链、缺来源、陈旧规则和冲突状态。

## 6. 免费数据架构

### 6.1 数据提供商

- 主适配器：AKShare，覆盖 A 股、港股、ETF、基金、指数、财务和宏观。
- A 股备用：BaoStock，用于日线和基础信息交叉验证。
- 官方来源：交易所/监管机构的清单、规则和披露只在条款允许范围内获取。
- 港股备用：第一版先保留适配器接口，不依赖未经核验的非官方接口保证可用性。

免费接口没有服务等级保证。每次抓取记录 provider、接口名、参数、时间、库版本、行数、字段和内容哈希。

### 6.2 数据流

```text
provider -> immutable download cache -> schema normalization
         -> quality checks -> parquet datasets -> research/backtest
         -> reproducibility manifest -> report
```

统一行情字段至少包括：市场、代码、交易日、开高低收、成交量、成交额、复权类型、币种、来源和抓取时间。原始下载与标准化结果分开保存。

### 6.3 失败与校验

- 网络失败、接口改名、空数据、字段变化必须显式报错。
- 检查主键重复、交易日缺口、负价格、OHLC 逻辑、异常跳变和复权连续性。
- 策略运行前检查数据截止日，防止把未来信息带入历史时点。
- 交叉来源差异超过阈值时阻止发布报告，并生成差异清单。

## 7. 量化研究与回测

第一版采用透明、易测试的 pandas/NumPy 日线研究管道，避免一开始引入复杂机器学习平台。Qlib 和 RQAlpha 作为架构参考或后续可选后端。

功能范围：

- 收益率、波动率、最大回撤、夏普、索提诺、卡玛、胜率、盈亏比和换手率。
- 买入持有、定投、均线趋势、横截面动量、低波动、质量/估值筛选示例。
- 单资产和简单多资产组合、再平衡、现金、基准对比。
- A/HK 分市场配置交易单位、费用、税费、滑点、停牌和涨跌停约束。
- 信号在已知信息之后成交，禁止同一根 K 线读取收盘价又按该收盘价无摩擦成交。
- 时间切分、样本外验证、滚动窗口、参数敏感性和多重尝试警告。

研究输出必须包含策略假设、数据区间、样本池构造、基准、费用、参数、指标、回撤、交易记录、限制和复现命令。

## 8. 学习路线与输出

新手路线按顺序组织：

1. 风险、骗局、现金管理和“不懂不买”。
2. A/HK 市场规则与交易成本。
3. 指数、ETF、基金和分散化。
4. 公司、财报、估值和行业。
5. Python、数据口径和统计基础。
6. 基准、回测、策略验证和复盘。

`output/templates/` 提供空白投资政策书、研究问题、公司分析、基金分析、交易前检查、回测报告和复盘模板；第一版不保存真实资产、账户和持仓。

## 9. 自动化与代理规则

`AGENTS.md` 将规定：

- Raw 只新增版本，不覆盖或无来源改写。
- 摄取流程先登记、再摘要、再更新关联页、索引和日志。
- Query 优先读 Wiki，关键结论回查 Raw，并在输出中引用。
- 代码变更以测试驱动，数据与回测核心逻辑必须有单元测试。
- 定期执行断链、孤儿页、缺引用、陈旧规则、数据与回测检查。
- 禁止承诺收益、隐去风险、把回测当实盘、使用未来数据。

CLI 计划提供 `sources audit`、`data fetch`、`data validate`、`backtest run`、`report build`、`wiki lint` 等命令。

## 10. 测试与验收

### 文档验收

- README 能让新手在 15 分钟内找到学习入口并运行健康检查。
- Obsidian 直接打开仓库，主要目录、双链、附件和模板正常。
- Raw 来源目录覆盖上述所有主题且每项可追溯。
- Wiki 无断链、无孤儿关键页、关键事实均有来源。

### 代码验收

- 在干净 Python 环境中安装并通过测试。
- 至少一组 A 股、一组港股、一组 ETF/基金数据样例可抓取或由固定测试夹具验证。
- 数据接口变化时给出可诊断错误。
- 手算小样本与引擎的收益、持仓、费用和回撤一致。
- 测试能捕获信号错位、未来函数、费用遗漏和不可成交场景。
- 示例策略可一条命令复现并生成 Markdown、CSV 和 PNG 报告。

### Git 与隐私验收

- GitHub 仓库为私有，默认分支为 `main`，远程关联和首次推送成功。
- 不提交行情缓存、虚拟环境、密钥、账户、个人资产和第三方完整仓库。
- README、AGENTS、许可证/来源策略和 Git 忽略规则齐全。

## 11. 非目标与后续扩展

第一版明确不做：实盘下单、分钟/Tick 高频、融资融券、期权期货、荐股通知、收益承诺、复杂深度学习和 LLM 自主交易。

后续只有在数据质量、基准回测和研究纪律稳定后，才评估 Qlib 因子研究、组合优化、公告/财报结构化、定时数据更新、模拟盘与券商只读接口。

## 12. 已核验参考入口

- [上交所投资者教育](https://edu.sse.com.cn/)
- [深交所投资者教育中心](https://investor.szse.cn/aboutus/eductionCentre/index.html)
- [港交所个人投资者入门](https://www.hkex.com.hk/Global/Exchange/FAQ/Getting-Started/Getting-Started-for-individual-investors?sc_lang=en)
- [港交所证券风险说明](https://www.hkex.com.hk/Products/Securities/Understanding-Risks-of-Securities-Traded-on-the-Exchange?sc_lang=en)
- [香港证监会投资者专区](https://www.sfc.hk/TC/Investor-corner)
- [AKShare](https://github.com/akfamily/akshare)
- [BaoStock](https://www.baostock.com/)
- [ExploreFinance](https://github.com/hiboys/ExploreFinance)
- [Qlib](https://github.com/microsoft/qlib)
- [RQAlpha](https://github.com/ricequant/rqalpha)
- [Backtesting.py](https://github.com/kernc/backtesting.py)
- [Awesome Quant](https://github.com/wilsonfreitas/awesome-quant)
