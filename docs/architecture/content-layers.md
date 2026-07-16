# 内容分层与复用边界

## 两个正交结构

知识库同时按“可信加工阶段”和“研究维度”组织。

```text
阶段：Raw 来源 ──> Wiki 知识 ──> Output 研究产出
                          └──> Site 搜索 / 图谱 / 工具

维度：地区 markets × 资产 assets/products × 行业 sectors × 方法 concepts/quant/risk
```

同一事实只在 Raw 有一个来源卡；Wiki 页面引用它并从不同维度互相双链。这样新增韩国存储企业、美国黄金 ETF 或日本基金时，只组合已有“地区 + 资产/行业 + 方法”，不复制整套知识。

## Public 与 Private

| 内容 | Public Git/Pages | 本地 `private/` |
|---|---:|---:|
| 官方规则与来源卡 | 是 | 可缓存原文件 |
| 通用 Wiki、代码、空白模板 | 是 | 可扩展 |
| 个人持仓、成本、券商流水 | 否 | 是 |
| Cookie、Token、账号、SSH 私钥 | 否 | 必须使用系统钥匙串或 `.env` |
| 行情缓存与第三方仓库快照 | 否 | 是 |
| 脱敏且可复现的示例数据 | 审查后 | 是 |

Pages 构建器只读取 `wiki/`、`raw/`、`output/` 和 `site/`，不会读取 `private/`。`.gitignore` 与 CI 的 publication audit 构成双重防线。
