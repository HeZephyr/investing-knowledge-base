---
id: raw-official-fsa-edinet
title: EDINET Disclosure and API v2
publisher: Financial Services Agency Japan
url: https://disclosure2.edinet-fsa.go.jp/week0020.aspx
retrieved: 2026-07-17
source_grade: A
markets: [日本股市]
usage: link-and-summarize
---
# 日本 FSA EDINET

## 权威性与用途

EDINET 是日本金融厅的法定披露检索系统，可按提交人、发行人、证券代码和文档类型检索年度/半年度证券报告、大量持有报告与临时报告，并提供 taxonomy/code list。它是研究日本公司披露时点和 XBRL 口径的首要入口之一。

## 当前核验事实

2026-07-17 首页说明 EDINET API v2 需要注册并签发 API key，规范从 Operation Guides 获取且主要为日文。网页可公开检索不代表 API 匿名，也不代表英文翻译完整。免费 Key 属于个人凭据，只从环境变量读取，不进入仓库、日志或报告。

## 许可与使用边界

本仓库不保存 API key、批量文档、XBRL 全文、附件或浏览器会话，只链接和概括字段。提交文件的版权、第三方审计报告、图片及翻译可能有独立权利；机器摄取和再分发前逐项核验。

## 历史时点

研究必须保存 document ID、提交时间、报告期、修订/更正关系、taxonomy 版本、抓取时间和内容哈希。后来更正的报告不能静默覆盖当时可得版本；API schema 和维护窗口也会变化。

## 局限与失效条件

EDINET 文件以日文为主，证券代码与法律实体映射可能变化；API 可因维护、限频或认证失败不可用。若找不到原始提交时间、修订链或适用会计口径，不做历史时点公司比较，也不使用翻译工具生成的文本替代原文判断。

