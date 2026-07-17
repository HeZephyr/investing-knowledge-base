# 金融与统计课程主干实施计划

**Goal:** 建立从零开始、可手算、可运行、可审计的金融与统计课程主干。

**Architecture:** Raw 卡记录开放教材、官方课程和固定代码库；Wiki 模块用统一教学合同合成；`investkb.education` 提供无网络纯函数练习；覆盖 v2 分别审计内容与练习阶段。

---

## Task 1：先定义失败测试

- 新建 `tests/test_education.py`，覆盖复利/贴现、有效年利率、离散矩、置信区间、Bonferroni、OLS、滚动切分、债券价格与久期的手算结果和非法输入。
- 新建 `tests/test_foundations_curriculum.py`，要求九个教学模块、固定章节、Raw 引用、索引可达和覆盖证据。
- 运行定向测试，确认失败来自模块/页面不存在。

## Task 2：实现教育纯函数

- 新建 `src/investkb/education.py`。
- 使用显式输入验证和不可变结果；拒绝 NaN/inf、概率不和为 1、样本过小、非法频率和不递增滚动窗口。
- 运行 `tests/test_education.py` 至 GREEN。

## Task 3：摄取课程与代码来源

- 新增 OpenIntro、OpenStax Finance、FPP3、MIT OCW、ISLP/NIST 等课程/教材来源卡。
- 新增 SciPy、statsmodels、ISLP labs、QuantEcon 仓库卡，固定 2026-07-17 审计 commit 和许可证状态。
- 更新 `raw/source-catalog.md`、`raw/repositories/catalog.md` 与 manifest。

## Task 4：编写九个教学模块

- 新建 `wiki/foundations/` 课程入口及九个模块页。
- 每页包含学习目标、核心概念、手算例、Python 实验、投资场景、常见误用、检查清单、进阶与来源。
- 不复制教材正文、图表、数据集或受限答案。

## Task 5：索引与覆盖

- 更新学习路线、Wiki 索引、dashboard、MkDocs、维护日志与经验账本。
- 将实际完成的 foundations/asset 能力提升到匹配阶段；其余保留明确 gap。
- 重新生成覆盖报告并验证确定性。

## Task 6：验证与发布

- 运行定向测试、Ruff 和 `scripts/verify.sh`。
- 自审许可证、私人信息、路径、重复内容和投资承诺。
- 分阶段提交，推送 `codex/finance-statistics-curriculum`，打开关闭 #17 的 PR；全部 required checks 通过后 squash merge。
