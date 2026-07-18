# 公司、因子、策略与组合公开案例实施计划

**Goal:** 完成剩余五项公开冻结案例能力，并保留正结果、负结果、费用和数据边界。

**Architecture:** 三个不可变快照支撑五份独立预注册报告；通用快照验证器守住谱系，新 evidence calculator 负责公司、因子、策略和组合纯计算。

---

## Task 1：RED 验收合同

- 新建 `tests/test_public_evidence_cases.py`。
- 固定公司正例阈值、公司负例放弃结论、因子复现结果、策略费用后失败和组合费用后结果。
- 要求五项 coverage 仅在 source/report/test 齐全时 validated。

## Task 2：冻结最小公开事实

- Meta：收入、营业利润、FCF、稀释股数和发布日期。
- Kenneth French：2000—2025 年度四因子列、2026-05 CRSP vintage、版权边界。
- A 股 ETF：三资产 2019—2025 年末收盘、provider/interface/参数、抓取日和失败 fallback。
- 计算并写入 manifest SHA-256，不提交完整上游文件。

## Task 3：实现纯计算器

- 公司：增长、利润率、FCF 率、每股 FCF、稀释。
- 因子：算术、几何累计、正负年份。
- 策略：滞后一年的仓位、换手、10bp 成本、CAGR 与基准差。
- 组合：资产收益、年度等权、漂移后换手、费用、累计/CAGR/波动/回撤。

## Task 4：五份报告与经验复盘

- 分别写预注册、来源、结果、反例/局限、放弃或保留条件和离线命令。
- 将版权最小化、接口 fallback、price vs total return、算术 vs 几何因子收益写入经验账本。

## Task 5：覆盖、索引与 PR

- 更新 Obsidian、MkDocs、Raw/Output 目录和覆盖报告。
- 跑定向测试、全量 verify、站点与秘密扫描。
- PR 关闭 #31；CI/Policy/review 通过后 squash merge。
