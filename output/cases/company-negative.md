# 冻结案例：Aduhelm 原商业化命题被否定

> 决策日：2026-07-17。本案例复用医药冻结快照，不评价治疗选择，也不推荐或否定整家公司。

## 预注册命题

FDA 加速批准足以带来广泛支付准入和可持续需求。

- **预设成功标准**：无材料性 payer 限制，也无需求相关库存或采购承诺减值。
- **预设失效条件**：CMS 把覆盖限制在合资格试验，或公司发生材料性需求相关减值。

## 来源事实

FDA 批准事实、CMS 受限覆盖决定、Biogen 披露约 2.75 亿美元相关减值共同构成 3 行快照；SHA-256：`29f1040401f2d1344f0dda07c3832df7782878eb1f21b1971cee5dadfdef481b`。

## 计算结果

`accelerated_approval=true`、`coverage_restricted=true`、`inventory_writeoff_usd_millions=275`，因此 `hypothesis_supported=false`，并明确 `abandon_original_thesis=true`：**放弃原命题**“批准会自动转化为广泛支付和持续需求”。

这不等于放弃整家公司，也不等于否定全部阿尔茨海默病药物；失败的只是这一个带时间、产品和商业化路径约束的命题。

## 重新研究条件

只有出现可独立验证的新证据，例如标签/确认性试验改变、支付范围和净价改善、患者启动与持续率、真实世界安全监测容量及公司资本配置更新，才建立新命题；不得把旧命题静默改写。

## 局限

这是事后框架反例，不能估计加速批准产品的总体成功率，也不比较临床净获益。后见信息必须按首次可得日使用。

## 离线复现

```bash
.venv/bin/python -m investkb.cases raw/cases/healthcare/manifest.yaml --decision-date 2026-07-17
```

命令校验 SHA-256、单位、主键与可得时点，不访问患者、Cookie、保险或券商数据。
