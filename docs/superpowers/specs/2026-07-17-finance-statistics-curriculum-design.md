# 金融与统计课程主干设计

## 目标与边界

Issue #17 要把基础学科从书单或零散概念升级为完全新手可顺序学习、可手算、可运行、可纠错的课程主干。首批覆盖货币时间价值、概率与收益分布、抽样与估计、检验与多重比较、回归、时间序列、债券利率、公司金融及论文复现。

本批不把教材正文、受限习题答案或第三方 Notebook 复制进仓库；只保存来源卡、独立中文合成和原创小样本练习。真实证券预测与冻结实证案例继续使用 `case-validated` 门槛，不因教学代码存在而升级。

## 方案比较

### 方案 A：只建书单和阅读路线

快，但无法证明学习者会算，也不能防止年化、p 值、回归和预测中的常见误用。

### 方案 B：一次复制完整大学课程

内容量大，但版权、维护、难度和测试成本不可控，也会把第三方课程结构当成自己的能力证据。

### 方案 C：来源卡 + 原创模块 + 纯函数练习（采用）

以开放教材、官方课程和许可证明确的代码库建立 Raw 谱系；每个 Wiki 模块固定包含学习目标、公式直觉、手算例、Python 实验、投资场景、常见误用和检查清单。关键计算进入 `investkb.education` 的小型纯函数并用手算样本测试。

## 来源策略

- OpenIntro Statistics：统计主线，记录 CC BY-SA 3.0 与商标/例外边界。
- OpenStax Principles of Finance：金融主线，仅链接和独立摘要；记录当前网页许可、PDF许可可能不同以及页面对 LLM 摄取的额外限制。
- Forecasting: Principles and Practice：时间序列与滚动评估，记录在线版持续更新和 R 生态边界。
- MIT OpenCourseWare Finance Theory I：公司金融与资产定价课程入口，按课程许可链接使用。
- ISLP/ISLP labs：回归、重采样和多重检验；书籍与 BSD-2 实验仓库分开记录。
- SciPy、statsmodels、QuantEcon：只作为实现、诊断和教学架构参考；固定 commit，检查许可证。QuantEcon 当前仓库没有根许可证时使用 `NOASSERTION` 和 link-only。

商业出版物即使可以免费下载，也不等于允许复制。仓库不保存 PDF，不复刻受保护插图、习题答案或长段文字。

## 课程结构

课程入口按依赖顺序连接九个模块：

1. 复利与贴现。
2. 概率、随机变量与收益分布。
3. 抽样、估计与置信区间。
4. 假设检验、效应量与多重比较。
5. 回归、残差与稳健诊断。
6. 时间序列、基线与滚动预测。
7. 债券定价、久期与利率风险。
8. 公司金融、资本成本与资本配置。
9. 论文阅读、预注册与复现。

每页至少包含一个无需外部数据的数值例子、一个调用仓库函数的 Python 片段、一个错误用法和一个投资应用。页面 frontmatter 引用对应 Raw ID，导航从学习路线、Wiki 索引和 MkDocs 可达。

## 可执行练习 API

新增 `src/investkb/education.py`，只使用标准库与 NumPy：

- `future_value`、`present_value`、`effective_annual_rate`；
- `discrete_moments`；
- `mean_confidence_interval`；
- `bonferroni_threshold`；
- `simple_ols`；
- `rolling_origin_splits`；
- `bond_price`、`macaulay_duration`。

所有函数拒绝非有限值、无效概率、非法频率、空样本和不可定义的统计量。测试使用可手算的小数组，不用网络、随机数据或第三方教材答案。

## 覆盖状态

内容页只有 `source + synthesis` 才能成为 `content-ready: validated`；纯函数只有 `implementation + test` 才能支持相应 `exercise-tested: validated`。时间序列、公司金融等仍缺完整练习或案例时保持 reviewed。任何教学示例都不升级 `case-validated`。

## 发布验收

先写教育函数与课程契约的失败测试，再实现最小函数和页面。更新 Raw/仓库目录、学习路线、Wiki/MkDocs 索引、覆盖清单、维护日志和经验账本。运行 `scripts/verify.sh`，经 Issue #17、主题分支、PR、required checks 和 squash merge发布。
