---
id: raw-repo-finhack
title: FinHackCN/finhack
publisher: FinHackCN contributors
url: https://github.com/FinHackCN/finhack
retrieved: 2026-07-17
source_grade: B
markets: [A股, 港股, 美股, 全球]
usage: link-and-analyze-only
license: GPL-3.0-only OR LicenseRef-Commercial
pinned_commit: dedbbd0b7accfed035ba05f07d76726d8754bbf7
---
# FinHack

## 代码事实

固定 commit 日期为 2026-07-14。根 `LICENSE.txt` 保存 GPL v3 正文，README 声明 GPL-3.0 与商业许可双轨；`COMMERCIAL_LICENSE.txt` 只是商业许可取得方式与待协商条款的概要，含联系信息占位，不能视为本项目已经得到商业授权。

目录覆盖 collector、factor、trainer、backtest/trader、project template 与任务运行组件。Tushare collector 从配置读取 token 与数据库名，并调度 A股、基金、期货、美股、港股、可转债、外汇等采集任务。`setup.py` 在 packaging 阶段遍历 `finhack/`，为缺失目录创建 `__init__.py`，并重写 `finhack/__init__.py`；因此连构建/安装元数据也不是只读动作。

回测规则实现包含退市、停牌、涨跌停、ST、主板、交易数量、T+1/T+0、成交量约束、税费、最低佣金和滑点。源码同时保留“不严谨”“怕后面有坑”等注释，并在部分方法引用未以 `self.context` 限定的 `context`；这要求独立测试，不能仅凭目录或 README 判定正确。

本地只读扫描发现 311 个可扫描文本文件；backtest、成本、公司行动和缓存均有关键词线索，而 conventional test-suite 证据很弱。“testmodule”和 `testStrategy.py` 多为框架示例名称，不等于 pytest 单元测试覆盖率。

## 上游声明

README 把项目定位为可扩展量化金融研究框架，列出数据采集、因子计算/挖掘/分析、机器学习、策略、回测与交易接入，并声称支持 A 股涨跌停、T+1 与动态复权。README 开头也明确警告当前正在大改重构、当天更新代码“运行不了了”。后一句是当前采用决策中的高权重反证。

## 认证与执行边界

Tushare token、数据库、QMT/MiniQMT 或其他交易适配都不进入公共知识库。克隆只用于离线 grep，不运行 `setup.py`、安装依赖、启动 MySQL/Redis、执行 collector、加载策略或连接交易终端。

GPL 与商业许可约束代码使用；Tushare、行情、财报和交易终端的数据与账户条款需要独立判断。动态复权、历史财务披露时间、退市样本、涨跌停可成交性、费用和滑点必须用冻结数据 fixture 复验。

## 采用决策

采用“采集—因子—训练—回测—任务编排”的模块边界作为研究架构参考；把 A 股交易规则实现转成可证伪测试清单。当前固定 commit 不安装、不 vendor、不作为生产数据或交易引擎。只有上游恢复可运行状态、补齐独立测试、隔离安装副作用并通过本项目冻结 fixture 后，才考虑 GPL 兼容的可选只读适配。
