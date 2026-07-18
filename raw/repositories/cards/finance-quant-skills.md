---
id: raw-repo-finance-quant-skills
title: lzwme/finance-quant-skills
publisher: lzwme and contributors
url: https://github.com/lzwme/finance-quant-skills
retrieved: 2026-07-17
source_grade: C
markets: [A股, 港股, 美股, 全球]
usage: link-and-analyze-only
license: NOASSERTION
pinned_commit: b03516e6d6e6f839b3ce3fb8ad529eb5e6b7f874
---
# finance-quant-skills

## 代码事实

固定 commit 日期为 2026-06-29。仓库列出 13 个 Skill：akquant、akshare、backtrader、baostock、equity-researcher、joinquant-docs、jqdatasdk、miniqmt、pywencai、qmt-docs、rqalpha、tdxquant、tushare。Claude marketplace 将其分成 quant-skills 与 quant-data-api 两个插件，均设置 `strict: false`。

固定 commit 没有根 LICENSE、COPYING 或 NOTICE，`pyproject.toml` 也没有 license 字段；README 页尾虽写 MIT，仍不足以确定仓库及复制内容的授权，故记为 `NOASSERTION`。Python 元数据要求 3.11 以上并声明 akshare、baostock、jqdatasdk、tushare、xtquant 等依赖，还把默认 package index 指向一个第三方域名。Skill 内含脚本、大量 API 文档、示例和研究报告模板，来源权利需逐项复核。

`pywencai` 指令要求浏览器 F12 获取 Cookie，并支持环境变量或用户目录文件保存；`miniqmt` 和 `qmt-docs` 明确展示实盘连接、下单、撤单、持仓/资产查询与即时订单；若由代理直接执行，权限远高于普通文档。equity-researcher 含子进程、浏览器渲染与安装依赖提示，其 README 声称来源于其他官方 Skill，需继续核对来源和许可。

## 上游声明

README 把仓库定位为金融量化领域的 Agent Skills 集合，提供 Claude marketplace、`npx skills add` 等安装方式，并声称 MIT 发布。各 Skill 的功能描述覆盖行情、财务、回测、研究报告与 QMT 交易。功能描述只是上游声明；缺少根许可证、复制材料来源不清和资金操作面会覆盖“方便安装”的收益。

## 认证与执行边界

本知识库不安装整个 bundle，不运行 Skill 脚本，不使用 Cookie，不读取账号、密码、Token、交易终端目录或券商资产。pywencai、miniqmt 与 qmt-docs 默认 quarantine；Tushare/JQData 等凭证型 Skill 至少需要许可证、数据条款、最小权限与只读 adapter 审查。官方 API 文档的可访问性不自动授予复制和再发布权。

提示注入也属于供应链风险：Markdown 可以要求代理执行下载、读取秘密或连接账户。审计时把所有上游指令作为数据，只记录相对路径和能力类型，不遵循指令，不复制含秘密的行。

## 采用决策

仓库整体仅 link-only。可借鉴“按数据、框架、研究和文档拆 Skill”的组织思想；每个 Skill 独立判定 adopt、optional、link-only、quarantine 或 reject。在上游补齐明确根许可证并完成嵌套内容许可审计前，不复制 Skill 内容到本项目。任何订单、撤单、资产查询、Cookie 或账号口令流程不得进入默认插件。
