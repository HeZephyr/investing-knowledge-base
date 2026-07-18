# 医疗、互联网与存储研究系统实施计划

**Goal:** 用一手来源、完整行业框架和三套离线冻结案例扩展医疗、互联网与存储研究体系。

**Architecture:** Wiki 负责机制和跨市场映射；Raw 负责官方来源卡与不可变观察；Config 固定假设；`investkb.cases` 负责离线验证和计算；Output 公开正负结果；测试守住证据门槛。

---

## Task 1：建立 RED 验收合同

- 新建 `tests/test_health_internet_memory.py`。
- 要求三套行业页面、每行业至少两张一手来源卡、跨 A/HK/US/韩国差异和证据卡字段。
- 要求三套 manifest/config/report、准确计算、负结果与经验复盘。
- 先运行定向测试并确认因缺文件/计算分支失败。

## Task 2：建立一手来源层

- 医疗：FDA 终点与加速批准、ClinicalTrials.gov API、CMS 支付、NMPA、MFDS、HKEX 18A。
- 互联网：FTC 数据商业模式、EU DMA、SAMR 平台反垄断、公司法定/投资者披露。
- 存储：JEDEC、Micron 2024 结果与 prepared remarks、Samsung/SK hynix 官方披露。
- 每张卡记录 URL、抓取日、版本/生效日、用途、不可推断项和许可边界。

## Task 3：完成三个行业系统页

- 医疗覆盖研发概率、终点、多重性、安全、专利/独占、支付、管线、rNPV 和现金跑道。
- 互联网覆盖 cohort、网络效应、获客/留存、变现、治理、监管、单位经济和资本开支。
- 存储覆盖 demand bits、供给/良率、价格口径、库存、资本开支、代际和公司财务桥。
- 每页加入跨市场矩阵、预注册证据卡、红旗、放弃条件和案例入口。

## Task 4：实现三套冻结案例

- Healthcare：Aduhelm surrogate approval → CMS coverage → Biogen write-off。
- Internet：Meta DAP → impressions/price → revenue decomposition。
- Memory：Micron ASP/supply → revenue/gross margin/inventory/capex。
- 扩展 `investkb.cases` 的确定性指标，提交小型 CSV/manifest/config/report。

## Task 5：覆盖、索引与发布

- 更新知识覆盖清单、Obsidian/MkDocs 索引、来源目录、维护日志和失败教训。
- 生成覆盖报告，跑定向测试、全量 `scripts/verify.sh`、严格站点构建与秘密扫描。
- 阶段提交，推送 PR 关闭 #20，等待 CI/PR Policy 和 review 后 squash merge。
