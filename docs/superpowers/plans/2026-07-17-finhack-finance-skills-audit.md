# FinHack 与金融 Skill 包审计实施计划

**Goal:** 交付两个固定 commit 的平台/Skill 供应链审计，并为现有插件增加安全、只读的 Skill bundle 审计能力。

**Architecture:** ignored clone 提供取证；Raw 固定事实；Wiki 综合架构与逐 Skill 采用矩阵；repo-local plugin 只包含原创审计指令，不 vendor 或安装第三方内容。

---

## Task 1：建立 RED 合同

- 新建 `tests/test_finance_skill_audit.py`。
- 断言两张来源卡的 pinned commit、许可证和事实/声明/边界/决策结构。
- 断言比较页包含安装副作用、缺失根许可证、Cookie、Token、实盘下单、复制文档与逐 Skill 分级。
- 断言新 Skill 明确只读、不安装、不执行、不读取凭证、不下单。

## Task 2：固定证据

- 记录 HEAD、日期、根与嵌套许可证、包元数据和顶层架构。
- FinHack 复核 README 可运行状态、`setup.py` 写操作、采集器认证、复权、因子、回测、成本、规则与交易适配器。
- finance-quant-skills 枚举全部 Skill、脚本、依赖、外部来源、凭证类型、网络和资金操作面。
- 扫描器命中只作为线索，所有强结论回到相对文件路径。

## Task 3：用官方脚手架增加 Skill

- 运行 skill-creator `init_skill.py` 创建 `plugins/investing-research/skills/audit-finance-skills`，只创建需要的 references。
- 用 `apply_patch` 写 SKILL 与审计分级参考；生成 `agents/openai.yaml`。
- 升级插件版本和 README，说明两个 Skill 的职责与安全边界。

## Task 4：Raw、Wiki 与索引

- 新建 `raw/repositories/cards/finhack.md` 和 `finance-quant-skills.md`。
- 新建 `wiki/engineering/金融量化平台与Skill审计.md`，写平台层和逐 Skill 采用矩阵。
- 更新来源 manifest、Raw/Wiki/站点索引、更新日志、经验与失败教训。
- 只补充现有 `engineering-audit-plugin` 的证据，不伪造新的覆盖项或提高固定 taxonomy 分母。

## Task 5：验证与发布

- 运行定向测试、`quick_validate.py`、plugin validator、`scripts/verify.sh` 和公开敏感信息检查。
- 使用官方 cachebuster/marketplace upgrade 流程更新本机已安装插件。
- 提交、推送、打开关联 #26 的 PR；required checks 全绿后 squash merge。
