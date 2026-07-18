# 医疗、互联网与存储研究系统设计

## 目标

Issue #20 把三个行业从主题页升级为可验证的研究系统：每个系统必须同时回答业务机制、监管/会计口径、跨市场差异、公司映射和“什么结果会推翻命题”。页面数量和篇幅不构成完成证据；只有一手来源、预注册配置、冻结快照、负结果报告和自动测试齐全才升级覆盖状态。

## 方案选择

### A：复制研报或维护实时抓取器

覆盖看似快，但付费材料不可再发布，实时接口会修订、限频或需要凭据，CI 也无法复现，不采用。

### B：只扩写三篇百科页面

适合阅读，但无法阻止终点替换、用户口径漂移或周期数据事后挑选，不满足 case-validated。

### C：行业框架 + 官方来源卡 + 小型冻结案例（采用）

每个行业建立独立 Wiki 与至少两张一手来源卡；沿用 `raw/cases/<case>/manifest.yaml`、规范化 CSV、预注册 YAML、离线计算器和报告的契约。案例只提交重算所需的小型公开事实，不复制受限全文、Cookie、Token 或个人投资数据。

## 三个行业的证据链

### 医药医疗

证据顺序为疾病自然史与未满足需求 → 预注册终点/效应量/多重性 → 临床结果与安全性 → FDA/NMPA/MFDS 等监管路径 → CMS/医保/商业支付与患者可及性 → 专利和独占期限 → 风险调整收入、现金消耗与融资稀释。研发概率只能作为同类项目的基准率，不能替代具体终点、入组、对照组和机制证据。

冻结案例检验“FDA 加速批准会自动转化为广泛支付与可持续需求”。Aduhelm 的 FDA surrogate-endpoint 批准、CMS coverage-with-evidence-development 和 Biogen 库存/采购承诺减值形成一条可审计的反例链。它不评价患者个体治疗选择，也不把事后失败率外推到所有药物。

### 互联网平台

证据顺序为用户定义与去重范围 → 获客/留存/参与度 cohort → 供需两侧网络效应 → 广告/佣金/订阅价格 × 数量 → 内容、支付和云基础设施成本 → 隐私、竞争和平台治理约束 → 自由现金流与增量资本回报。MAU、DAU、DAP、买家、商户和设备不是可互换单位。

冻结案例检验“活跃用户增长足以解释广告平台收入增长”。Meta 2023—2024 的 DAP、广告展示、每广告价格和收入拆解同时保留：用户增长提供部分支持，但价格与展示共同使单变量命题失败。

### 存储半导体

证据顺序为终端出货 × 单机 bit 含量 → DRAM/NAND/HBM 产品与认证 → wafer start、良率、die size、封装与 bit supply → 现货/合约/公司 ASP → 渠道和公司库存 → 收入、毛利、减值、资本开支与自由现金流。HBM 的晶圆和先进封装占用会改变传统 DRAM 的有效供给，不能只看名义 wafer capacity。

冻结案例检验“期末库存绝对下降是周期盈利修复的必要条件”。Micron FY2023—FY2024 收入、毛利率、库存、库存减值、资本开支和公司披露的 ASP/bit shipment 方向显示：库存仍上升时收入与毛利已经修复，因此绝对库存单指标失败；价格、产品组合、减值基数和供给纪律必须共同解释。

## 跨市场边界

- A 股/中国药企使用 NMPA/CDE 注册阶段与医保谈判口径；港股 18A 允许未盈利生物科技上市，现金跑道和核心产品资格更关键；美国区分 FDA approval、CMS coverage 与商业保险；韩国使用 MFDS 与本地披露。
- 中国平台重点核对 SAMR 竞争规则、数据和内容约束；美国结合 FTC/SEC 与州级隐私；欧盟 DMA/DSA/GDPR 对 gatekeeper 义务更具结构性；韩国使用 KFTC 与本地平台披露。不能把“用户数”跨产品、跨法规机械比较。
- 存储的生产、客户和上市地跨美国、韩国、中国/香港与全球供应链；Micron、Samsung、SK hynix 财年、币种、分部和 ASP 披露粒度不同。比较前必须统一产品、期间、币种、库存口径和晶圆/bit 单位。

## 文件与验证

```text
wiki/sectors/{医药医疗,互联网平台,存储半导体}.md
raw/official/{united-states,china,korea,europe,global}/...
raw/cases/{healthcare,internet,memory}/manifest.yaml
raw/cases/{healthcare,internet,memory}/observations.csv
config/cases/{healthcare,internet,memory}.yaml
output/cases/{healthcare,internet,memory}.md
tests/test_health_internet_memory.py
```

通用 `investkb.cases` 继续验证 SHA-256、相对路径、schema、有限数值、UTC 可得时间、决策日、单位和主键；新增三个确定性计算分支。测试必须检查预注册只运行一次、报告包含正/负结果、跨市场矩阵和失败复盘。只有 source + synthesis + report + test 证据完整时，才升级三个 content 和三个 case capability。

## 发布纪律

Issue #20 → `codex/health-internet-memory` → PR → CI/PR Policy → squash merge。未来更新另存 vintage，禁止用最终修订数据重写旧案例；任何需要登录、付费或访问控制绕过的来源保持 link-only 或替换为合法官方来源。
