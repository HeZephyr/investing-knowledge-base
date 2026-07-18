# 冻结公开数据行业案例实施计划

**Goal:** 用可离线复现的官方数据快照验证能源、银行和消费行业框架，并保留负结果。

**Architecture:** Raw 保存小型不可变快照与 manifest；config 保存预注册；`investkb.cases` 验证谱系并计算；Output 保存报告；测试阻止历史时点、哈希、单位和重复错误。

---

## Task 1：定义 RED 合同

- 新建 `tests/test_frozen_sector_cases.py`。
- 要求三套 manifest/CSV/config/report、固定 SHA、明确正负结果与复现命令。
- 要求坏哈希、重复主键、未来可得日、未知单位和缺失值失败。
- 要求三项 case coverage 只有 source/report/test 后才能 validated。

## Task 2：实现通用快照验证器

- 新建 `src/investkb/cases.py` 的不可变 manifest/observation 模型。
- 只读本地文件，验证相对路径、SHA、schema、时间、单位、主键和值。
- 提供确定性变化率、相关/压力比率等小函数，不加入网络依赖。

## Task 3：采集与规范化官方数据

- 能源：EIA/FRED 序列 + SEC filing facts。
- 银行：FDIC Financials/机构事实，固定法律实体和季度。
- 消费：Census 历史 MRTS release + SEC filing facts。
- 原始下载留在临时目录；只提交最小规范化观察值和完整上游元数据。

## Task 4：生成并审阅三份报告

- 逐案写预注册、来源事实、计算、推断、负结果、替代解释与局限。
- 报告由固定快照确定性渲染或由测试核对关键数值。
- 将数据修订、实体映射和宏观—公司错配写入经验账本。

## Task 5：覆盖、索引与发布

- 更新 Output/Wiki/MkDocs 索引和维护日志。
- 将三个 case requirement 提升为 validated，生成覆盖报告。
- 跑定向测试、全量 verify、公开秘密审计；PR 关闭 #19。
