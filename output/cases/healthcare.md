# 冻结案例：Aduhelm 的批准、支付与需求门槛

> 决策日：2026-07-17。本案例检验医药研究框架，不评价患者是否应接受任何治疗，也不推荐 Biogen 或其他证券。

## 预注册命题

FDA 加速批准足以带来广泛支付准入和可持续需求。

- **预设成功标准**：没有材料性 payer 限制，且观察窗内没有需求相关的库存/采购承诺减值。
- **预设失效条件**：CMS 将覆盖限制在证据开发/合资格试验，或公司发生材料性需求相关减值。
- **替代解释**：surrogate 不确定性、安全监测、价格、诊断/输注容量、医生和患者接受度、竞争。

## 来源事实与首次可得日

- FDA 2021-06-07 决策备忘录：Aduhelm 获 accelerated approval，依据为降低脑淀粉样蛋白斑块的 surrogate endpoint；审评团队存在公开分歧。
- CMS 2022-04-07 NCD：对 accelerated-approval 的该类产品，覆盖限于符合条件的 FDA/NIH 试验；FDA 的安全有效门槛与 CMS 的 reasonable-and-necessary 门槛分离。
- Biogen 2024 年报回溯披露：2022 年第一季度因最终 NCD 记录约 275 百万美元库存及采购承诺减值。该年报事实最迟在 2025-02-13 可得；不冒充 2022 决策日前已知的最终修订表述。
- 规范化快照 3 行；SHA-256：`29f1040401f2d1344f0dda07c3832df7782878eb1f21b1971cee5dadfdef481b`。

## 计算结果

离线计算同时得到 `accelerated_approval=true`、`coverage_restricted=true` 和 `inventory_writeoff_usd_millions=275`，所以 `hypothesis_supported=false`。

### 正向证据

批准本身是真实的监管里程碑，且 accelerated approval 为严重疾病和未满足需求提供了基于 surrogate 的可用路径。这支持“监管事件能改变产品状态”，但只支持到批准层。

### 负结果

支付覆盖没有自动跟随批准扩展，公司随后记录材料性需求相关减值。命题被两个预设失效条件共同否定：**批准、支付和实际需求是三道不同门槛**。

## 失败复盘

若研究者只在批准 headline 后给峰值销售估值，会遗漏 surrogate 是否验证、payer 对临床获益的证据要求、影像/输注/监测容量与净价。275 百万美元减值也不是“产品价值为负”的估计，它包含特定库存、采购承诺和合作安排。

该案例是事后选择的框架反例，不能估计 accelerated approval 的总体商业成功率；也没有比较疗效、伤害或替代治疗。后续正结果案例应在 readout 前冻结 protocol/SAP、临床效应、支付规则、患者启动和持续率，再用未见数据验证。

## 离线复现

```bash
python -m investkb.cases raw/cases/healthcare/manifest.yaml --decision-date 2026-07-17
```

命令只读本地 CSV，验证 SHA-256、单位、重复键和可得时间；不访问患者数据、账号、Cookie、保险系统或券商。
