# AI 协作日志

> **本文件由 `pipeline/translate.py` 自动生成，请勿手工编辑。**
> 原始事件流：`logs/journal.jsonl`（append-only，每翻译一块即写入一条）。

## 为什么是自动生成的

事后回忆补写的日志有明显特征：颗粒度均匀、没有失败记录、没有返工。
这份日志反过来——它由管线在每次调用时立即落盘，**不通过人工整理**，
因此失败、重试、校验不通过都会如实留在里面。

## 总览

| 指标 | 数值 |
|---|---|
| 记录事件总数 | 635 |
| 翻译块次 | 479 |
| 其中通过校验 | 437 |
| **其中未通过 / 失败** | **42** |
| 完成条目 | 36 |
| 出现过校验问题的块 | 42 |

## 按天汇总

挑战要求的是「**每日** AI 协作日志」，所以先把事件按日期聚合一遍，再看下面的逐块明细。

| 日期 | 翻译块次 | 通过 | 失败 | 条目数 | 净中文字符 | 当日最后事件 |
|---|---|---|---|---|---|---|
| 2026-09-15 | 162 | 143 | 19 | 13 | 106,478 | 16:17:35 |
| 2026-09-16 | 317 | 294 | 23 | 28 | 227,308 | 15:37:35 |

## 逐块记录

| 时间 | 条目 | 块 | 后端 | prompt | 原/译字符 | 用时 | 结果 |
|---|---|---|---|---|---|---|---|
| 15:25:48 | `warp-vs-claude-code` | 0 | queue | `01d516df5f56` | 1545/973 | — | ✅ |
| 15:25:48 | `warp-vs-claude-code` | 1 | queue | `3c1156174b50` | 1325/642 | — | ❌ 出现禁用变体「协调」（应为「编排」） |
| 15:25:48 | `warp-vs-claude-code` | 2 | queue | `522bc6c276f6` | 909/519 | — | ✅ |
| 15:25:48 | `warp-vs-claude-code` | 3 | queue | `d95a38af44a6` | 721/471 | — | ✅ |
| 15:25:59 | `warp-vs-claude-code` | 1 | queue | `3c1156174b50` | 1325/642 | — | ✅ |
| 15:26:51 | `mcp-food-for-thought` | 0 | queue | `69589c06eeb3` | 1408/872 | — | ❌ 出现禁用变体「上下文协议」（应为「模型上下文协议（MCP）」） |
| 15:26:51 | `mcp-food-for-thought` | 1 | queue | `dabe62f1d2e8` | 1475/875 | — | ✅ |
| 15:26:51 | `mcp-food-for-thought` | 2 | queue | `777ddeac2db9` | 921/588 | — | ❌ 出现禁用变体「检索增强」（应为「检索增强生成（RAG）」） |
| 15:26:51 | `mcp-food-for-thought` | 3 | queue | `634866ac8007` | 735/336 | — | ✅ |
| 15:26:51 | `benefits-agentic-ai-oncall` | 0 | queue | `a862b2069d5e` | 3413/1182 | — | ❌ 出现禁用变体「情境」（应为「上下文」）；出现禁用变体「流程」（应为「工作流」）；出现禁用变体「记录」（应为「日志」）；出 |
| 15:26:51 | `benefits-agentic-ai-oncall` | 1 | queue | `5248b3ecaca3` | 1235/424 | — | ❌ 出现禁用变体「故障」（应为「故障事件」） |
| 15:26:51 | `benefits-agentic-ai-oncall` | 2 | queue | `b113cf9eff8f` | 99/65 | — | ✅ |
| 15:27:27 | `mcp-food-for-thought` | 0 | queue | `f451eab73f14` | 1408/872 | — | ✅ |
| 15:27:27 | `mcp-food-for-thought` | 2 | queue | `170f9700389e` | 921/588 | — | ✅ |
| 15:27:27 | `warp-vs-claude-code` | 0 | queue | `7322f8c82247` | 1545/973 | — | ✅ |
| 15:27:27 | `warp-vs-claude-code` | 1 | queue | `a8f76a910161` | 1325/642 | — | ✅ |
| 15:27:27 | `benefits-agentic-ai-oncall` | 0 | queue | `ac1505d0fb17` | 3413/1182 | — | ❌ 出现禁用变体「情境」（应为「上下文」） |
| 15:27:27 | `benefits-agentic-ai-oncall` | 1 | queue | `60662066e28a` | 1235/424 | — | ✅ |
| 15:27:41 | `benefits-agentic-ai-oncall` | 0 | queue | `ac1505d0fb17` | 3413/1184 | — | ✅ |
| 15:32:24 | `mcp-food-for-thought` | 0 | queue | `f451eab73f14` | 1408/870 | — | ✅ |
| 15:32:24 | `mcp-food-for-thought` | 1 | queue | `dabe62f1d2e8` | 1475/875 | — | ✅ |
| 15:32:24 | `mcp-food-for-thought` | 2 | queue | `170f9700389e` | 921/588 | — | ✅ |
| 15:32:24 | `mcp-food-for-thought` | 3 | queue | `634866ac8007` | 735/336 | — | ✅ |
| 15:32:24 | `warp-vs-claude-code` | 0 | queue | `7322f8c82247` | 1545/973 | — | ✅ |
| 15:32:24 | `warp-vs-claude-code` | 1 | queue | `a8f76a910161` | 1325/642 | — | ✅ |
| 15:32:24 | `warp-vs-claude-code` | 2 | queue | `522bc6c276f6` | 909/519 | — | ✅ |
| 15:32:24 | `warp-vs-claude-code` | 3 | queue | `d95a38af44a6` | 721/471 | — | ✅ |
| 15:32:24 | `benefits-agentic-ai-oncall` | 0 | queue | `ac1505d0fb17` | 3413/1184 | — | ✅ |
| 15:32:24 | `benefits-agentic-ai-oncall` | 1 | queue | `60662066e28a` | 1235/424 | — | ✅ |
| 15:32:24 | `benefits-agentic-ai-oncall` | 2 | queue | `b113cf9eff8f` | 99/65 | — | ✅ |
| 15:59:34 | `mcp-registry-preview` | 0 | queue | `e08ef5e79c3e` | 1194/591 | — | ✅ |
| 15:59:34 | `mcp-registry-preview` | 1 | queue | `54b5e6e978f4` | 1203/494 | — | ✅ |
| 15:59:34 | `mcp-registry-preview` | 2 | queue | `d5a25e005e7e` | 3459/2148 | — | ✅ |
| 15:59:34 | `code-reviews-just-do-it` | 0 | queue | `94627e072ac7` | 3139/1354 | — | ❌ 出现禁用变体「代码审查」（应为「代码评审」） |
| 15:59:42 | `code-reviews-just-do-it` | 0 | queue | `94627e072ac7` | 3139/1354 | — | ✅ |
| 16:00:31 | `kubernetes-troubleshooting` | 0 | queue | `244109653a2c` | 1666/937 | — | ✅ |
| 16:00:31 | `kubernetes-troubleshooting` | 1 | queue | `6cccae495d52` | 1471/731 | — | ❌ 出现禁用变体「遥测数据」（应为「遥测」） |
| 16:00:31 | `kubernetes-troubleshooting` | 2 | queue | `2d8a1f00389b` | 2570/1221 | — | ❌ 出现禁用变体「遥测数据」（应为「遥测」） |
| 16:00:31 | `kubernetes-troubleshooting` | 3 | queue | `3cc86f27ae83` | 1324/579 | — | ✅ |
| 16:00:31 | `kubernetes-troubleshooting` | 4 | queue | `a375f8f61914` | 826/366 | — | ✅ |
| 16:00:31 | `kubernetes-troubleshooting` | 5 | queue | `e0568b989965` | 99/65 | — | ✅ |
| 16:00:37 | `kubernetes-troubleshooting` | 1 | queue | `6cccae495d52` | 1471/729 | — | ✅ |
| 16:00:37 | `kubernetes-troubleshooting` | 2 | queue | `2d8a1f00389b` | 2570/1219 | — | ✅ |
| 16:01:27 | `copilot-prompt-injection-r` | 0 | queue | `8bec118ea877` | 1254/752 | — | ✅ |
| 16:01:27 | `copilot-prompt-injection-r` | 1 | queue | `a9659c22b157` | 1744/926 | — | ✅ |
| 16:01:27 | `copilot-prompt-injection-r` | 2 | queue | `ff363c3026c4` | 953/495 | — | ✅ |
| 16:01:27 | `copilot-prompt-injection-r` | 3 | queue | `1b82048988f2` | 1088/393 | — | ✅ |
| 16:01:27 | `copilot-prompt-injection-r` | 4 | queue | `479a946ac43c` | 1469/758 | — | ✅ |
| 16:01:27 | `copilot-prompt-injection-r` | 5 | queue | `9cbfe0431a4c` | 548/357 | — | ❌ 出现禁用变体「缺陷」（应为「漏洞」）；出现禁用变体「威胁建模」（应为「威胁模型」） |
| 16:01:35 | `copilot-prompt-injection-r` | 0 | queue | `d1a1baa329f0` | 1254/752 | — | ✅ |
| 16:01:35 | `copilot-prompt-injection-r` | 4 | queue | `f97bca176f05` | 1469/758 | — | ✅ |
| 16:01:35 | `copilot-prompt-injection-r` | 5 | queue | `89a210c83113` | 548/357 | — | ✅ |
| 16:04:03 | `multi-agent-systems-ai-nat` | 0 | queue | `27958289d9d6` | 1714/836 | — | ✅ |
| 16:04:03 | `multi-agent-systems-ai-nat` | 1 | queue | `a726af335fe7` | 1890/681 | — | ✅ |
| 16:04:03 | `multi-agent-systems-ai-nat` | 2 | queue | `c946a43bc904` | 2852/990 | — | ❌ 出现禁用变体「语境」（应为「上下文」）；出现禁用变体「协调」（应为「编排」） |
| 16:04:03 | `multi-agent-systems-ai-nat` | 3 | queue | `e8e42959808a` | 2414/955 | — | ❌ 出现禁用变体「协调」（应为「编排」） |
| 16:04:03 | `multi-agent-systems-ai-nat` | 4 | queue | `1f981bd8ff61` | 448/291 | — | ✅ |
| 16:04:11 | `multi-agent-systems-ai-nat` | 1 | queue | `a726af335fe7` | 1890/681 | — | ✅ |
| 16:04:11 | `multi-agent-systems-ai-nat` | 2 | queue | `c946a43bc904` | 2852/993 | — | ❌ 出现禁用变体「协调」（应为「编排」） |
| 16:04:11 | `multi-agent-systems-ai-nat` | 3 | queue | `e8e42959808a` | 2414/955 | — | ❌ 出现禁用变体「协调」（应为「编排」） |
| 16:04:22 | `multi-agent-systems-ai-nat` | 2 | queue | `c946a43bc904` | 2852/993 | — | ✅ |
| 16:04:22 | `multi-agent-systems-ai-nat` | 3 | queue | `e8e42959808a` | 2414/955 | — | ✅ |
| 16:04:53 | `claude-code-best-practices` | 0 | queue | `7bee3ade6a89` | 2903/1635 | — | ✅ |
| 16:04:53 | `claude-code-best-practices` | 1 | queue | `89c1e5954cae` | 3022/1557 | — | ✅ |
| 16:04:53 | `claude-code-best-practices` | 2 | queue | `645ebeac27f5` | 1578/1042 | — | ✅ |
| 16:04:53 | `claude-code-best-practices` | 3 | queue | `0191769d9488` | 447/198 | — | ✅ |
| 16:10:02 | `how-long-contexts-fail` | 0 | queue | `7a4952eeb8c0` | 976/406 | — | ✅ |
| 16:10:02 | `how-long-contexts-fail` | 1 | queue | `9f4d3b9a9fbb` | 1119/529 | — | ✅ |
| 16:10:02 | `how-long-contexts-fail` | 2 | queue | `676c0ab14170` | 1346/573 | — | ✅ |
| 16:10:02 | `how-long-contexts-fail` | 3 | queue | `04eead01bbc7` | 2146/1080 | — | ✅ |
| 16:10:02 | `how-long-contexts-fail` | 4 | queue | `96707ee14964` | 3012/1181 | — | ✅ |
| 16:10:02 | `how-long-contexts-fail` | 5 | queue | `f887aee3514a` | 755/424 | — | ✅ |
| 16:14:01 | `observability-basics` | 0 | queue | `3fb1524e2704` | 1356/640 | — | ✅ |
| 16:14:01 | `observability-basics` | 1 | queue | `434d7f3f6756` | 1107/465 | — | ✅ |
| 16:14:01 | `observability-basics` | 2 | queue | `e193e2c0af90` | 806/381 | — | ✅ |
| 16:14:01 | `observability-basics` | 3 | queue | `595453e49b48` | 1155/538 | — | ❌ 出现禁用变体「遥测数据」（应为「遥测」） |
| 16:14:01 | `observability-basics` | 4 | queue | `33c6928326c6` | 1379/1275 | — | ✅ |
| 16:14:42 | `observability-basics` | 3 | queue | `595453e49b48` | 1155/536 | — | ✅ |
| 16:14:42 | `observability-basics` | 5 | queue | `ed66b37728b0` | 1092/508 | — | ❌ 出现禁用变体「规范」（应为「规格说明」） |
| 16:14:42 | `observability-basics` | 6 | queue | `87b3ccd63016` | 973/408 | — | ✅ |
| 16:14:42 | `observability-basics` | 7 | queue | `23c544cc1b46` | 908/330 | — | ❌ 出现禁用变体「跟踪」（应为「链路追踪」）；出现禁用变体「度量」（应为「指标」） |
| 16:14:42 | `observability-basics` | 8 | queue | `488992ddccff` | 826/326 | — | ✅ |
| 16:14:42 | `observability-basics` | 9 | queue | `f7dc9eb02d5b` | 383/165 | — | ❌ 出现禁用变体「轨迹」（应为「追踪记录」） |
| 16:14:52 | `mcp-food-for-thought` | 2 | queue | `efaad093036a` | 921/588 | — | ✅ |
| 16:14:52 | `mcp-registry-preview` | 0 | queue | `341955498869` | 1194/591 | — | ✅ |
| 16:14:52 | `how-long-contexts-fail` | 0 | queue | `022ef81a4a31` | 976/406 | — | ✅ |
| 16:14:52 | `how-long-contexts-fail` | 1 | queue | `2682f26a2dfd` | 1119/529 | — | ✅ |
| 16:14:52 | `how-long-contexts-fail` | 3 | queue | `c935c9db53cc` | 2146/1080 | — | ✅ |
| 16:14:52 | `how-long-contexts-fail` | 5 | queue | `8b75e4d8c0b9` | 755/424 | — | ✅ |
| 16:14:52 | `claude-code-best-practices` | 1 | queue | `9639363b7ac3` | 3022/1557 | — | ✅ |
| 16:14:52 | `copilot-prompt-injection-r` | 1 | queue | `29b264164940` | 1744/926 | — | ✅ |
| 16:14:52 | `code-reviews-just-do-it` | 0 | queue | `b167bfad385e` | 3139/1354 | — | ✅ |
| 16:14:52 | `benefits-agentic-ai-oncall` | 0 | queue | `6963c2987d47` | 3413/1184 | — | ✅ |
| 16:14:52 | `kubernetes-troubleshooting` | 1 | queue | `68da9c335e5c` | 1471/729 | — | ✅ |
| 16:14:52 | `kubernetes-troubleshooting` | 2 | queue | `1183a00ce75e` | 2570/1219 | — | ✅ |
| 16:14:52 | `multi-agent-systems-ai-nat` | 0 | queue | `a76f745d4141` | 1714/836 | — | ✅ |
| 16:14:52 | `multi-agent-systems-ai-nat` | 1 | queue | `6a37a7423c1f` | 1890/681 | — | ✅ |
| 16:14:52 | `multi-agent-systems-ai-nat` | 2 | queue | `b51a04d7cccc` | 2852/993 | — | ✅ |
| 16:14:52 | `multi-agent-systems-ai-nat` | 3 | queue | `b3c374d5873f` | 2414/955 | — | ✅ |
| 16:14:52 | `observability-basics` | 0 | queue | `9a3b6d3d5242` | 1356/640 | — | ✅ |
| 16:14:52 | `observability-basics` | 1 | queue | `8df156edc871` | 1107/465 | — | ✅ |
| 16:14:52 | `observability-basics` | 2 | queue | `3293ad41a76d` | 806/381 | — | ✅ |
| 16:14:52 | `observability-basics` | 3 | queue | `9bc9f7d59cb2` | 1155/536 | — | ✅ |
| 16:14:52 | `observability-basics` | 4 | queue | `b017628a6e91` | 1379/1275 | — | ✅ |
| 16:14:52 | `observability-basics` | 5 | queue | `4210237af8b0` | 1092/508 | — | ✅ |
| 16:14:52 | `observability-basics` | 6 | queue | `3fe869fc5997` | 973/408 | — | ✅ |
| 16:14:52 | `observability-basics` | 7 | queue | `080ad5069416` | 908/330 | — | ✅ |
| 16:14:52 | `observability-basics` | 8 | queue | `4d2e53807c86` | 826/326 | — | ✅ |
| 16:14:52 | `observability-basics` | 9 | queue | `d2e877ecf5bf` | 383/165 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 0 | queue | `db1ab4b695a1` | 1186/431 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 1 | queue | `d280ea697f48` | 778/291 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 2 | queue | `224d24e0cb98` | 1483/664 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 3 | queue | `4178b016d47d` | 1755/667 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 4 | queue | `98b0abbae211` | 1292/592 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 5 | queue | `3cb309da71cd` | 1404/620 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 6 | queue | `5d996ee199fc` | 649/260 | — | ✅ |
| 16:16:08 | `ai-code-review-best-practi` | 7 | queue | `28de270646e8` | 3047/1092 | — | ✅ |
| 16:16:55 | `mcp-server-authentication` | 0 | queue | `8904f93eccdb` | 1265/780 | — | ✅ |
| 16:16:55 | `mcp-server-authentication` | 1 | queue | `4d14ef86781c` | 1499/1059 | — | ✅ |
| 16:16:55 | `mcp-server-authentication` | 2 | queue | `af52330bbf94` | 2654/1839 | — | ✅ |
| 16:16:55 | `mcp-server-authentication` | 3 | queue | `440f6ef61b89` | 988/617 | — | ❌ 出现禁用变体「代理」（应为「智能体」） |
| 16:17:11 | `mcp-food-for-thought` | 0 | queue | `b3c037500500` | 1408/870 | — | ✅ |
| 16:17:11 | `mcp-food-for-thought` | 1 | queue | `ab39eaa9c16a` | 1475/875 | — | ✅ |
| 16:17:11 | `mcp-food-for-thought` | 2 | queue | `1e8ac5c0fb40` | 921/588 | — | ✅ |
| 16:17:11 | `mcp-food-for-thought` | 3 | queue | `e5213a9eb537` | 735/336 | — | ✅ |
| 16:17:11 | `mcp-server-authentication` | 0 | queue | `3551eb4d525b` | 1265/780 | — | ✅ |
| 16:17:11 | `mcp-server-authentication` | 1 | queue | `a32bc8aeec15` | 1499/1059 | — | ✅ |
| 16:17:11 | `mcp-server-authentication` | 2 | queue | `483da7217d61` | 2654/1839 | — | ✅ |
| 16:17:11 | `mcp-server-authentication` | 3 | queue | `05ab1ad9e51f` | 988/617 | — | ✅ |
| 16:17:11 | `how-long-contexts-fail` | 0 | queue | `148cf6237a2b` | 976/406 | — | ✅ |
| 16:17:11 | `how-long-contexts-fail` | 1 | queue | `88e76d142d25` | 1119/529 | — | ✅ |
| 16:17:11 | `how-long-contexts-fail` | 2 | queue | `f223be0da89f` | 1346/573 | — | ✅ |
| 16:17:11 | `how-long-contexts-fail` | 3 | queue | `85c4c3e1698d` | 2146/1080 | — | ✅ |
| 16:17:11 | `how-long-contexts-fail` | 4 | queue | `42d6a3eabfff` | 3012/1181 | — | ✅ |
| 16:17:11 | `claude-code-best-practices` | 1 | queue | `9308cc3c25ce` | 3022/1557 | — | ✅ |
| 16:17:11 | `claude-code-best-practices` | 2 | queue | `ae636e09876e` | 1578/1042 | — | ✅ |
| 16:17:11 | `warp-vs-claude-code` | 0 | queue | `b10f019f393e` | 1545/973 | — | ✅ |
| 16:17:11 | `warp-vs-claude-code` | 1 | queue | `c7608ef58321` | 1325/642 | — | ✅ |
| 16:17:11 | `warp-vs-claude-code` | 2 | queue | `d90afcc57cd3` | 909/519 | — | ✅ |
| 16:17:11 | `warp-vs-claude-code` | 3 | queue | `da04a6bd39b5` | 721/471 | — | ✅ |
| 16:17:11 | `copilot-prompt-injection-r` | 0 | queue | `733c483757ef` | 1254/752 | — | ✅ |
| 16:17:11 | `copilot-prompt-injection-r` | 2 | queue | `8a7d3c698617` | 953/495 | — | ✅ |
| 16:17:11 | `copilot-prompt-injection-r` | 4 | queue | `835c99de52b7` | 1469/758 | — | ✅ |
| 16:17:11 | `copilot-prompt-injection-r` | 5 | queue | `72a4d87ca771` | 548/357 | — | ✅ |
| 16:17:11 | `ai-code-review-best-practi` | 0 | queue | `146522bfd76b` | 1186/431 | — | ✅ |
| 16:17:11 | `ai-code-review-best-practi` | 2 | queue | `4138ea8c2925` | 1483/664 | — | ✅ |
| 16:17:11 | `ai-code-review-best-practi` | 4 | queue | `5cbf054d0dfe` | 1292/592 | — | ✅ |
| 16:17:11 | `ai-code-review-best-practi` | 5 | queue | `2cda2ed579a7` | 1404/620 | — | ✅ |
| 16:17:11 | `ai-code-review-best-practi` | 6 | queue | `e3bd1b9d16c9` | 649/260 | — | ✅ |
| 16:17:11 | `benefits-agentic-ai-oncall` | 0 | queue | `d612f6529aa2` | 3413/1184 | — | ✅ |
| 16:17:11 | `benefits-agentic-ai-oncall` | 1 | queue | `c522b4b49c7c` | 1235/424 | — | ✅ |
| 16:17:11 | `kubernetes-troubleshooting` | 0 | queue | `d05ef4fcfcd3` | 1666/937 | — | ✅ |
| 16:17:11 | `kubernetes-troubleshooting` | 2 | queue | `b3e512f63842` | 2570/1219 | — | ✅ |
| 16:17:11 | `kubernetes-troubleshooting` | 3 | queue | `910202f4522f` | 1324/579 | — | ✅ |
| 16:17:11 | `multi-agent-systems-ai-nat` | 0 | queue | `4af7d1a7a136` | 1714/836 | — | ✅ |
| 16:17:11 | `multi-agent-systems-ai-nat` | 1 | queue | `e494f5465899` | 1890/681 | — | ✅ |
| 16:17:11 | `multi-agent-systems-ai-nat` | 2 | queue | `c53c7cc406f5` | 2852/993 | — | ✅ |
| 16:17:11 | `multi-agent-systems-ai-nat` | 3 | queue | `889a2a4d8da5` | 2414/955 | — | ✅ |
| 16:17:35 | `mcp-server-authentication` | 4 | queue | `5c0665716f99` | 1122/592 | — | ✅ |
| 16:17:35 | `mcp-server-authentication` | 5 | queue | `9301564f8b5a` | 3394/2479 | — | ✅ |
| 16:17:35 | `mcp-server-authentication` | 6 | queue | `8ebe3f481fc9` | 1312/1016 | — | ✅ |
| 16:17:35 | `mcp-server-authentication` | 7 | queue | `6e4809938b14` | 96/59 | — | ✅ |
| 13:33:42 | `mcp-food-for-thought` | 0 | queue | `8f128e47868a` | 1408/870 | — | ✅ |
| 13:33:42 | `mcp-food-for-thought` | 2 | queue | `df1a31b9d822` | 921/588 | — | ✅ |
| 13:33:42 | `mcp-food-for-thought` | 3 | queue | `4a93aeb031e6` | 735/336 | — | ✅ |
| 13:33:42 | `mcp-registry-preview` | 0 | queue | `ec7412eb772f` | 1194/591 | — | ✅ |
| 13:33:42 | `mcp-registry-preview` | 1 | queue | `b81e58387a9a` | 1203/494 | — | ✅ |
| 13:33:42 | `mcp-registry-preview` | 2 | queue | `b46be7a19fd8` | 3459/2148 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 0 | queue | `f8f92351b7e4` | 1265/780 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 1 | queue | `74bc369193b5` | 1499/1059 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 2 | queue | `12028126f2be` | 2654/1839 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 3 | queue | `bdb0c1c982ac` | 988/617 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 4 | queue | `3186f1afb43a` | 1122/592 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 5 | queue | `9891f0da9d31` | 3394/2479 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 6 | queue | `0f8ae8ae8d9e` | 1312/1016 | — | ✅ |
| 13:33:42 | `mcp-server-authentication` | 7 | queue | `43f5358f16ff` | 96/59 | — | ✅ |
| 13:33:42 | `how-long-contexts-fail` | 0 | queue | `b47b46a63b2e` | 976/406 | — | ✅ |
| 13:33:42 | `how-long-contexts-fail` | 1 | queue | `ec9c90110eef` | 1119/529 | — | ✅ |
| 13:33:42 | `how-long-contexts-fail` | 2 | queue | `801c1c1bc109` | 1346/573 | — | ✅ |
| 13:33:42 | `how-long-contexts-fail` | 3 | queue | `e645993fd103` | 2146/1080 | — | ✅ |
| 13:33:42 | `how-long-contexts-fail` | 4 | queue | `404a1ceaf94f` | 3012/1181 | — | ✅ |
| 13:33:42 | `how-long-contexts-fail` | 5 | queue | `cf3924f6f4e7` | 755/424 | — | ✅ |
| 13:33:42 | `specs-are-the-new-source-c` | 0 | queue | `5d2ffaa000ed` | 1211/547 | — | ✅ |
| 13:33:42 | `specs-are-the-new-source-c` | 1 | queue | `3f609b38e780` | 2939/1291 | — | ❌ 出现禁用变体「产物」（应为「制品」）×3 |
| 13:33:42 | `specs-are-the-new-source-c` | 2 | queue | `2d772cba3502` | 1220/514 | — | ✅ |
| 13:33:42 | `specs-are-the-new-source-c` | 3 | queue | `7e7bed4b4235` | 3055/1763 | — | ✅ |
| 13:33:42 | `specs-are-the-new-source-c` | 4 | queue | `c2d1a82245f4` | 1688/837 | — | ✅ |
| 13:33:42 | `specs-are-the-new-source-c` | 5 | queue | `f0ba7c32849f` | 932/375 | — | ❌ 出现禁用变体「产物」（应为「制品」）×1 |
| 13:33:42 | `claude-code-best-practices` | 0 | queue | `237e05d3abd4` | 2903/1635 | — | ✅ |
| 13:33:42 | `claude-code-best-practices` | 1 | queue | `bcb669851203` | 3022/1557 | — | ✅ |
| 13:33:42 | `claude-code-best-practices` | 2 | queue | `749ccc4e7ed3` | 1578/1042 | — | ✅ |
| 13:33:42 | `warp-vs-claude-code` | 0 | queue | `8d2b41d50519` | 1545/973 | — | ✅ |
| 13:33:42 | `warp-vs-claude-code` | 1 | queue | `bf09898c190b` | 1325/642 | — | ✅ |
| 13:33:42 | `warp-vs-claude-code` | 2 | queue | `37ac00d4b836` | 909/519 | — | ✅ |
| 13:33:42 | `warp-vs-claude-code` | 3 | queue | `1099e7d41db3` | 721/471 | — | ✅ |
| 13:33:42 | `copilot-prompt-injection-r` | 1 | queue | `66efe6fbead6` | 1744/926 | — | ✅ |
| 13:33:42 | `copilot-prompt-injection-r` | 3 | queue | `238da6d82a77` | 1088/393 | — | ✅ |
| 13:33:42 | `copilot-prompt-injection-r` | 4 | queue | `028f59649afc` | 1469/758 | — | ✅ |
| 13:33:42 | `ai-code-review-best-practi` | 0 | queue | `9b23504cff94` | 1186/431 | — | ✅ |
| 13:33:42 | `ai-code-review-best-practi` | 3 | queue | `881cbb1f5643` | 1755/667 | — | ✅ |
| 13:33:42 | `ai-code-review-best-practi` | 5 | queue | `39ed5bd2a66f` | 1404/620 | — | ✅ |
| 13:33:42 | `code-reviews-just-do-it` | 0 | queue | `02247ff7d753` | 3139/1354 | — | ✅ |
| 13:33:42 | `benefits-agentic-ai-oncall` | 0 | queue | `a3e7554e44cc` | 3413/1184 | — | ✅ |
| 13:33:42 | `benefits-agentic-ai-oncall` | 1 | queue | `86cecf3316d1` | 1235/424 | — | ✅ |
| 13:33:42 | `kubernetes-troubleshooting` | 0 | queue | `78d0e72c04d1` | 1666/937 | — | ✅ |
| 13:33:42 | `kubernetes-troubleshooting` | 4 | queue | `0c3e32a49ff7` | 826/366 | — | ✅ |
| 13:33:42 | `multi-agent-systems-ai-nat` | 0 | queue | `cca7da95ef5e` | 1714/836 | — | ✅ |
| 13:33:42 | `multi-agent-systems-ai-nat` | 2 | queue | `b4b22548cf36` | 2852/993 | — | ✅ |
| 13:33:42 | `multi-agent-systems-ai-nat` | 3 | queue | `9ce30925f533` | 2414/955 | — | ✅ |
| 13:33:52 | `specs-are-the-new-source-c` | 1 | queue | `2ea552e19675` | 2939/1291 | — | ✅ |
| 13:33:52 | `specs-are-the-new-source-c` | 5 | queue | `910d2556bb35` | 932/375 | — | ✅ |
| 13:34:36 | `warp-vs-claude-code` | 1 | queue | `3000222b0a36` | 1325/642 | — | ✅ |
| 13:34:36 | `ai-code-review-best-practi` | 3 | queue | `c04988e54e1f` | 1755/667 | — | ✅ |
| 13:34:36 | `code-reviews-just-do-it` | 0 | queue | `54ca55a541d2` | 3139/1354 | — | ✅ |
| 13:35:24 | `code-review-essentials` | 0 | queue | `302c5fb19a47` | 1404/537 | — | ✅ |
| 13:35:24 | `code-review-essentials` | 1 | queue | `e4519b76f9a5` | 1887/680 | — | ✅ |
| 13:35:24 | `code-review-essentials` | 2 | queue | `1fbe3eb5230b` | 3213/1612 | — | ✅ |
| 13:35:24 | `code-review-essentials` | 3 | queue | `9493ca05b60f` | 2442/905 | — | ✅ |
| 13:35:24 | `code-review-essentials` | 4 | queue | `3b101a97d4c3` | 806/297 | — | ✅ |
| 13:39:56 | `how-openai-uses-codex` | 0 | queue | `d4941288e992` | 3136/1312 | — | ✅ |
| 13:39:56 | `how-openai-uses-codex` | 1 | queue | `93a4bd57f2cc` | 3324/1416 | — | ✅ |
| 13:39:56 | `how-openai-uses-codex` | 2 | queue | `9d6119fcb9e9` | 3279/1451 | — | ✅ |
| 13:39:56 | `how-openai-uses-codex` | 3 | queue | `90f11d03be83` | 1010/438 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 0 | queue | `effcf4538994` | 1245/639 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 1 | queue | `db705849ed9b` | 1927/1759 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 2 | queue | `979a23644afe` | 312/228 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 3 | queue | `0b5d038e401a` | 4273/2548 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 4 | queue | `af2332fe82eb` | 1374/1248 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 5 | queue | `d1d6017ce21b` | 874/508 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 6 | queue | `ce29b7e0bfc9` | 885/300 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 7 | queue | `bcc9e6c3634d` | 826/403 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 8 | queue | `71965b010e94` | 858/416 | — | ✅ |
| 13:41:18 | `owasp-top-ten` | 9 | queue | `303e418b8a00` | 1397/531 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 0 | queue | `974ec195c8b6` | 917/564 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 1 | queue | `94436a5380cb` | 1448/782 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 2 | queue | `5f4d59694fe5` | 1094/452 | — | ❌ 出现禁用变体「运行环境」（应为「运行时」）×1 |
| 13:43:57 | `sast-vs-dast` | 3 | queue | `d26381b35cb2` | 2031/940 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 4 | queue | `8e4519d86da0` | 788/299 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 5 | queue | `7fdc7d5f0175` | 1564/677 | — | ❌ 出现禁用变体「弱点」（应为「漏洞」）×2 |
| 13:43:57 | `sast-vs-dast` | 6 | queue | `6c5c88fae16d` | 1048/358 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 7 | queue | `eecaf7f33481` | 1723/667 | — | ❌ 链接数不符：原文 0，译文 1 |
| 13:43:57 | `sast-vs-dast` | 8 | queue | `c7291417989b` | 787/248 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 9 | queue | `889f8240ebc4` | 995/348 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 10 | queue | `23c8b636632d` | 1091/417 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 11 | queue | `80d37f827513` | 892/315 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 12 | queue | `51087dcde484` | 1221/469 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 13 | queue | `34b055c513b3` | 1502/670 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 14 | queue | `b8eff018c2f3` | 868/342 | — | ✅ |
| 13:43:57 | `sast-vs-dast` | 15 | queue | `8fc15e005921` | 1072/455 | — | ✅ |
| 13:44:11 | `copilot-prompt-injection-r` | 0 | queue | `19e2420f34af` | 1254/752 | — | ✅ |
| 13:44:11 | `copilot-prompt-injection-r` | 4 | queue | `12871d1c12d6` | 1469/758 | — | ✅ |
| 13:44:11 | `copilot-prompt-injection-r` | 5 | queue | `794073603b56` | 548/357 | — | ✅ |
| 13:44:11 | `sast-vs-dast` | 2 | queue | `5f4d59694fe5` | 1094/452 | — | ❌ 出现禁用变体「运行环境」（应为「运行时」）×1 |
| 13:44:11 | `sast-vs-dast` | 5 | queue | `493075bda9fa` | 1564/677 | — | ✅ |
| 13:44:11 | `sast-vs-dast` | 7 | queue | `eecaf7f33481` | 1723/619 | — | ✅ |
| 13:44:11 | `sast-vs-dast` | 10 | queue | `eee55885f7b2` | 1091/417 | — | ✅ |
| 13:44:11 | `sast-vs-dast` | 11 | queue | `8ea9f9f499c1` | 892/315 | — | ✅ |
| 13:44:11 | `sast-vs-dast` | 12 | queue | `e2b9401d9ab0` | 1221/469 | — | ✅ |
| 13:44:11 | `sast-vs-dast` | 14 | queue | `3c5f0d5ffa73` | 868/342 | — | ✅ |
| 13:44:11 | `ai-code-review-best-practi` | 5 | queue | `d4d69dfe1b71` | 1404/620 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 2 | queue | `8c694ac9df71` | 1094/452 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 7 | queue | `db20bdcc64eb` | 1723/619 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 8 | queue | `86313e6332ea` | 787/248 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 9 | queue | `14e62dcca3c7` | 995/348 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 11 | queue | `39b668f4dd7a` | 892/315 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 12 | queue | `cf712dd78243` | 1221/469 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 13 | queue | `17ce8f73259f` | 1502/670 | — | ✅ |
| 13:44:32 | `sast-vs-dast` | 14 | queue | `5b24418767f3` | 868/342 | — | ✅ |
| 13:44:32 | `ai-code-review-best-practi` | 1 | queue | `67e55962da70` | 778/291 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 0 | queue | `88974e6dfdd6` | 982/381 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 1 | queue | `6d249a066e73` | 1216/480 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 2 | queue | `2c64f1809e7d` | 1717/915 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 3 | queue | `2bd4811b502f` | 3393/1405 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 4 | queue | `ca0208f50656` | 1276/556 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 5 | queue | `9853734583f6` | 931/325 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 6 | queue | `c2db93fe83dd` | 2512/1013 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 7 | queue | `848deff28a25` | 1140/455 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 8 | queue | `07e531ad5b52` | 2180/1019 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 9 | queue | `f7a50a17b266` | 1209/462 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 10 | queue | `955e8b3e9c35` | 1710/863 | — | ✅ |
| 13:47:11 | `writing-effective-tools-fo` | 11 | queue | `90bd23ce2f2a` | 1346/664 | — | ❌ 出现禁用变体「MCP 协议」（应为「模型上下文协议（MCP）」）×1 |
| 13:47:11 | `sast-vs-dast` | 1 | queue | `e71ad96ef101` | 1448/782 | — | ✅ |
| 13:47:11 | `sast-vs-dast` | 7 | queue | `87c77bb4fa49` | 1723/619 | — | ✅ |
| 13:47:11 | `sast-vs-dast` | 8 | queue | `a0d7aa7d2b41` | 787/248 | — | ✅ |
| 13:47:11 | `sast-vs-dast` | 9 | queue | `a1c7cce794c4` | 995/348 | — | ✅ |
| 13:47:11 | `sast-vs-dast` | 10 | queue | `be33207461e1` | 1091/417 | — | ✅ |
| 13:47:11 | `sast-vs-dast` | 12 | queue | `80a7a4607efd` | 1221/469 | — | ✅ |
| 13:47:11 | `observability-basics` | 7 | queue | `0bb4031de0cf` | 908/330 | — | ✅ |
| 13:47:20 | `writing-effective-tools-fo` | 11 | queue | `90bd23ce2f2a` | 1346/671 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 0 | queue | `2721003fc17a` | 1025/445 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 1 | queue | `3749fb70aa57` | 3031/2041 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 2 | queue | `47282e3eaf8c` | 1612/851 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 3 | queue | `e9e03490efa1` | 1434/718 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 4 | queue | `58ae8cb6e282` | 2669/1052 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 5 | queue | `a062e5a8ef12` | 1155/437 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 6 | queue | `c78d0018e3a2` | 1577/592 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 7 | queue | `e5d9bd4d9687` | 1551/672 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 8 | queue | `e11240fa1cf8` | 1277/589 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 9 | queue | `9c00170f569b` | 942/443 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 10 | queue | `4c87723b3e2e` | 1114/412 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 11 | queue | `6ff86bf0be12` | 1022/581 | — | ✅ |
| 13:52:54 | `how-to-review-code-effecti` | 12 | queue | `c9a208ba5e26` | 129/100 | — | ✅ |
| 13:55:39 | `mcp-food-for-thought` | 0 | queue | `645bb959d3b5` | 1408/870 | — | ✅ |
| 13:55:39 | `mcp-food-for-thought` | 1 | queue | `2d15df002305` | 1475/875 | — | ✅ |
| 13:55:39 | `mcp-server-authentication` | 1 | queue | `3f81b7cd9c61` | 1499/1059 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 0 | queue | `c0159b1c23bd` | 2072/826 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 1 | queue | `593eaafcd8f6` | 1089/417 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 2 | queue | `37f333225df6` | 973/417 | — | ❌ 出现禁用变体「检查器」（应为「代码检查工具」）×1 |
| 13:55:39 | `devin-coding-agents-101` | 3 | queue | `075f030c4281` | 1087/438 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 4 | queue | `9c921f9a5bae` | 1121/461 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 5 | queue | `a51b6208bbe1` | 835/368 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 6 | queue | `127c7ae3319c` | 1173/403 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 7 | queue | `2032d628a350` | 1620/617 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 8 | queue | `de6e90cfceb9` | 871/335 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 9 | queue | `3f64ef890e53` | 1240/535 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 10 | queue | `d0c2f71814e1` | 1128/412 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 11 | queue | `9b80e8c1e35e` | 771/310 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 12 | queue | `5cdc40f9dac2` | 1180/439 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 13 | queue | `7864f8a09893` | 981/376 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 14 | queue | `5ea011370ba5` | 764/256 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 15 | queue | `12c8d9833275` | 807/313 | — | ✅ |
| 13:55:39 | `devin-coding-agents-101` | 16 | queue | `fee4882ea032` | 815/301 | — | ✅ |
| 13:55:39 | `how-long-contexts-fail` | 0 | queue | `4dfe4b9fd9b5` | 976/406 | — | ✅ |
| 13:55:39 | `how-long-contexts-fail` | 2 | queue | `796430b7d838` | 1346/573 | — | ✅ |
| 13:55:39 | `how-long-contexts-fail` | 3 | queue | `8096c4d1e241` | 2146/1080 | — | ✅ |
| 13:55:39 | `how-long-contexts-fail` | 4 | queue | `7d57a6d7fd58` | 3012/1181 | — | ✅ |
| 13:55:39 | `how-long-contexts-fail` | 5 | queue | `71482b4cf21a` | 755/424 | — | ✅ |
| 13:55:39 | `sast-vs-dast` | 8 | queue | `e7259b57d71d` | 787/248 | — | ✅ |
| 13:55:39 | `benefits-agentic-ai-oncall` | 0 | queue | `eb874c0c0d83` | 3413/1184 | — | ✅ |
| 13:55:39 | `kubernetes-troubleshooting` | 1 | queue | `2309d42fcc7c` | 1471/729 | — | ✅ |
| 13:55:39 | `kubernetes-troubleshooting` | 2 | queue | `99cb4460a2f6` | 2570/1219 | — | ✅ |
| 13:55:39 | `multi-agent-systems-ai-nat` | 2 | queue | `6a35be79ff1e` | 2852/993 | — | ✅ |
| 13:55:39 | `observability-basics` | 3 | queue | `ecb59e12ea37` | 1155/536 | — | ✅ |
| 13:55:46 | `devin-coding-agents-101` | 2 | queue | `cacfce756af2` | 973/417 | — | ✅ |
| 14:08:59 | `claude-code-best-practices` | 1 | queue | `0c995d88dd96` | 3022/1557 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 0 | queue | `386270c7859f` | 1571/781 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 1 | queue | `e3df116dee11` | 1071/454 | — | ❌ 出现禁用变体「语境」（应为「上下文」）×1 |
| 14:12:52 | `prompt-engineering-overvie` | 2 | queue | `4911d6e243a5` | 1107/359 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 3 | queue | `c3a071e73dad` | 1580/610 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 4 | queue | `9c05cb4f8602` | 1191/409 | — | ❌ 出现禁用变体「情境」（应为「上下文」）×1 |
| 14:12:52 | `prompt-engineering-overvie` | 5 | queue | `d46a1946d34d` | 859/359 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 6 | queue | `8ccfb1dd1de3` | 1068/372 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 7 | queue | `e24a0b916d0e` | 1076/386 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 8 | queue | `f0c4ca26c208` | 786/342 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 9 | queue | `5d1455509a11` | 861/343 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 10 | queue | `eb43084a486b` | 897/469 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 11 | queue | `3cc4588de474` | 767/260 | — | ✅ |
| 14:12:52 | `prompt-engineering-overvie` | 12 | queue | `5ae47664f9f7` | 1467/904 | — | ✅ |
| 14:13:00 | `prompt-engineering-overvie` | 1 | queue | `e3df116dee11` | 1071/452 | — | ✅ |
| 14:13:00 | `prompt-engineering-overvie` | 4 | queue | `9c05cb4f8602` | 1191/410 | — | ✅ |
| 14:15:07 | `finding-vulnerabilities-cl` | 0 | queue | `c9cfb242bd7b` | 2265/1057 | — | ❌ 出现禁用变体「假阳性」（应为「误报」）×2 |
| 14:15:07 | `finding-vulnerabilities-cl` | 1 | queue | `81aa00c3c6bd` | 806/478 | — | ✅ |
| 14:15:07 | `finding-vulnerabilities-cl` | 2 | queue | `01d5b791d0f0` | 842/299 | — | ❌ 出现禁用变体「假阳性」（应为「误报」）×2；出现禁用变体「假阴性」（应为「漏报」）×2 |
| 14:15:07 | `finding-vulnerabilities-cl` | 3 | queue | `0c164e54ffd4` | 3430/1963 | — | ✅ |
| 14:15:07 | `finding-vulnerabilities-cl` | 4 | queue | `38d004b7fb03` | 2374/1364 | — | ✅ |
| 14:15:07 | `finding-vulnerabilities-cl` | 5 | queue | `44d353b058ca` | 1175/886 | — | ❌ 出现禁用变体「假阳性」（应为「误报」）×2 |
| 14:15:07 | `finding-vulnerabilities-cl` | 6 | queue | `e76700c056f8` | 2093/885 | — | ❌ 出现禁用变体「假阳性」（应为「误报」）×3 |
| 14:15:07 | `finding-vulnerabilities-cl` | 7 | queue | `cfe78517cb3f` | 3034/1189 | — | ❌ 出现禁用变体「语境」（应为「上下文」）×1 |
| 14:15:07 | `finding-vulnerabilities-cl` | 8 | queue | `bd953e916160` | 777/280 | — | ✅ |
| 14:15:07 | `finding-vulnerabilities-cl` | 9 | queue | `50652094349d` | 851/520 | — | ✅ |
| 14:15:07 | `finding-vulnerabilities-cl` | 10 | queue | `0e5b2da8bde1` | 2352/1127 | — | ❌ 出现禁用变体「假阳性」（应为「误报」）×2；出现禁用变体「假阴性」（应为「漏报」）×3 |
| 14:15:07 | `finding-vulnerabilities-cl` | 11 | queue | `fedbbb8eeec4` | 1518/932 | — | ✅ |
| 14:15:16 | `finding-vulnerabilities-cl` | 0 | queue | `4c175ba8a188` | 2265/1057 | — | ✅ |
| 14:15:16 | `finding-vulnerabilities-cl` | 2 | queue | `fa9b98cd490b` | 842/299 | — | ✅ |
| 14:15:16 | `finding-vulnerabilities-cl` | 5 | queue | `a66438c2ed97` | 1175/886 | — | ✅ |
| 14:15:16 | `finding-vulnerabilities-cl` | 6 | queue | `ca71a7fc8b45` | 2093/885 | — | ✅ |
| 14:15:16 | `finding-vulnerabilities-cl` | 7 | queue | `cfe78517cb3f` | 3034/1187 | — | ✅ |
| 14:15:16 | `finding-vulnerabilities-cl` | 10 | queue | `796426e1882f` | 2352/1127 | — | ✅ |
| 14:15:16 | `sast-vs-dast` | 5 | queue | `b0d67217878e` | 1564/677 | — | ✅ |
| 14:15:16 | `sast-vs-dast` | 7 | queue | `b8cc755a2437` | 1723/619 | — | ✅ |
| 14:15:16 | `sast-vs-dast` | 8 | queue | `682a7828f085` | 787/248 | — | ✅ |
| 14:15:16 | `sast-vs-dast` | 14 | queue | `fab7025ce7bd` | 868/342 | — | ✅ |
| 14:15:16 | `ai-code-review-best-practi` | 3 | queue | `8c758af05b38` | 1755/667 | — | ✅ |
| 14:15:16 | `ai-code-review-best-practi` | 5 | queue | `0834a0575a42` | 1404/620 | — | ✅ |
| 14:15:16 | `ai-code-review-best-practi` | 7 | queue | `087067d27204` | 3047/1092 | — | ✅ |
| 14:17:00 | `sre-introduction` | 0 | queue | `d2f5ac3af228` | 2826/1012 | — | ✅ |
| 14:17:00 | `sre-introduction` | 1 | queue | `97905ad50283` | 2740/1132 | — | ✅ |
| 14:17:00 | `sre-introduction` | 2 | queue | `cdc3f2c30728` | 3009/1130 | — | ✅ |
| 14:17:00 | `sre-introduction` | 3 | queue | `b317f7f22634` | 1654/696 | — | ✅ |
| 14:17:00 | `sre-introduction` | 4 | queue | `bc9f7f6f4bc4` | 1921/702 | — | ✅ |
| 14:17:00 | `sre-introduction` | 5 | queue | `8fa8a042abd5` | 2612/991 | — | ✅ |
| 14:17:00 | `sre-introduction` | 6 | queue | `7d8cd144b38d` | 1152/398 | — | ✅ |
| 14:17:00 | `sre-introduction` | 7 | queue | `ae951e83837a` | 1146/506 | — | ❌ 出现禁用变体「平均修复时间」（应为「平均恢复时间（MTTR）」）×1 |
| 14:17:00 | `sre-introduction` | 8 | queue | `3d0bca53dd39` | 1577/509 | — | ✅ |
| 14:17:00 | `sre-introduction` | 9 | queue | `5f64fa757200` | 2341/884 | — | ✅ |
| 14:17:09 | `kubernetes-troubleshooting` | 0 | queue | `f43586f80a21` | 1666/937 | — | ✅ |
| 14:17:09 | `observability-basics` | 1 | queue | `d763d377472a` | 1107/465 | — | ✅ |
| 14:17:09 | `sre-introduction` | 7 | queue | `843aad7c6e83` | 1146/506 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 0 | queue | `1dbd6acdc16e` | 771/314 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 1 | queue | `63bdcd000f77` | 1514/853 | — | ❌ 出现禁用变体「MCP 协议」（应为「模型上下文协议（MCP）」）×1 |
| 14:22:40 | `mcp-introduction` | 2 | queue | `311a5d7e6cc8` | 3031/1267 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 3 | queue | `e1c376e0f614` | 1779/870 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 4 | queue | `ea79121e6c9e` | 1457/501 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 5 | queue | `f5d36ed85d11` | 1241/444 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 6 | queue | `bead8ae9a916` | 594/250 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 7 | queue | `4b12c0cbceb3` | 3372/1432 | — | ❌ 出现禁用变体「MCP 协议」（应为「模型上下文协议（MCP）」）×1 |
| 14:22:40 | `mcp-introduction` | 8 | queue | `f76acc422219` | 472/196 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 9 | queue | `e2780a3c5230` | 2998/1574 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 10 | queue | `c83eccdb7d67` | 1371/952 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 11 | queue | `1252e28fe425` | 1909/801 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 12 | queue | `6b5e612e43d0` | 1400/511 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 13 | queue | `dde88a259bfd` | 1074/358 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 14 | queue | `475cdd50a97d` | 1591/547 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 15 | queue | `694b57bb170d` | 1667/684 | — | ✅ |
| 14:22:40 | `mcp-introduction` | 16 | queue | `7046f9217a24` | 88/54 | — | ✅ |
| 14:22:40 | `ai-code-review-best-practi` | 3 | queue | `9fd819d6682e` | 1755/667 | — | ✅ |
| 14:22:40 | `benefits-agentic-ai-oncall` | 0 | queue | `b0d250117ddd` | 3413/1184 | — | ✅ |
| 14:22:40 | `kubernetes-troubleshooting` | 3 | queue | `a7ff4ba6a387` | 1324/579 | — | ✅ |
| 14:22:49 | `mcp-introduction` | 1 | queue | `63bdcd000f77` | 1514/851 | — | ✅ |
| 14:22:49 | `mcp-introduction` | 7 | queue | `4b12c0cbceb3` | 3372/1433 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 0 | queue | `85a90afd8adb` | 3341/1365 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 1 | queue | `17230c7fe3ea` | 3337/1363 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 2 | queue | `8132fd12905e` | 3240/1229 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 3 | queue | `ba7ddb8d9c3c` | 2968/1156 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 4 | queue | `429c62ebc0a1` | 3171/1279 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 5 | queue | `ba4dbb71e225` | 2931/1187 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 6 | queue | `3292ae3c2781` | 3306/1266 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 7 | queue | `895d98bc44f3` | 3323/1318 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 8 | queue | `5aee31a0f10c` | 3079/1205 | — | ✅ |
| 14:24:41 | `how-anthropic-uses-claude-` | 9 | queue | `7dda9b591d99` | 2815/1140 | — | ❌ 出现禁用变体「回退」（应为「回滚」）×1 |
| 14:24:41 | `how-anthropic-uses-claude-` | 10 | queue | `9ebcf67cdd8f` | 1669/684 | — | ✅ |
| 14:24:49 | `how-anthropic-uses-claude-` | 8 | queue | `c2c93af9fe16` | 3079/1205 | — | ✅ |
| 14:24:49 | `how-anthropic-uses-claude-` | 9 | queue | `0260bfd54a4b` | 2815/1140 | — | ✅ |
| 14:39:08 | `how-openai-uses-codex` | 1 | queue | `08e680712724` | 3324/1416 | — | ✅ |
| 14:39:08 | `how-openai-uses-codex` | 2 | queue | `ed7a8cd2fac2` | 3279/1451 | — | ✅ |
| 14:39:08 | `context-rot` | 0 | queue | `142cb50c3eec` | 2951/1312 | — | ✅ |
| 14:39:08 | `context-rot` | 1 | queue | `b60c56169a11` | 3126/1205 | — | ✅ |
| 14:39:08 | `context-rot` | 2 | queue | `d9cc1f83629f` | 1717/564 | — | ✅ |
| 14:39:08 | `context-rot` | 3 | queue | `2c8b72d9ba25` | 1064/458 | — | ❌ 出现禁用变体「嵌入向量」（应为「嵌入」）×1 |
| 14:39:08 | `context-rot` | 4 | queue | `3401e14df91a` | 1099/364 | — | ✅ |
| 14:39:08 | `context-rot` | 5 | queue | `ff287b296b28` | 1342/542 | — | ❌ 出现禁用变体「嵌入向量」（应为「嵌入」）×1 |
| 14:39:08 | `context-rot` | 6 | queue | `eacffc0cf59d` | 2347/1016 | — | ❌ 出现禁用变体「嵌入向量」（应为「嵌入」）×1 |
| 14:39:08 | `context-rot` | 7 | queue | `1a2b409c0727` | 1416/519 | — | ✅ |
| 14:39:08 | `context-rot` | 8 | queue | `a14e214dc4b9` | 1371/545 | — | ✅ |
| 14:39:08 | `context-rot` | 9 | queue | `c5c8a7298f7b` | 1725/620 | — | ✅ |
| 14:39:08 | `context-rot` | 10 | queue | `d9a93fc5a6fe` | 942/359 | — | ✅ |
| 14:39:08 | `context-rot` | 11 | queue | `88d5a570d832` | 1571/570 | — | ✅ |
| 14:39:28 | `context-rot` | 3 | queue | `2c8b72d9ba25` | 1064/456 | — | ✅ |
| 14:39:28 | `context-rot` | 5 | queue | `ff287b296b28` | 1342/540 | — | ✅ |
| 14:39:28 | `context-rot` | 6 | queue | `eacffc0cf59d` | 2347/1014 | — | ✅ |
| 14:40:45 | `context-rot` | 12 | queue | `425948126fdc` | 2338/814 | — | ✅ |
| 14:40:45 | `context-rot` | 13 | queue | `efd5db416a1e` | 887/386 | — | ✅ |
| 14:40:45 | `context-rot` | 14 | queue | `66613ee97fe1` | 2283/928 | — | ✅ |
| 14:40:45 | `context-rot` | 15 | queue | `607e53b0d351` | 3128/1598 | — | ✅ |
| 14:40:45 | `context-rot` | 16 | queue | `a681330c689f` | 237/89 | — | ✅ |
| 14:40:45 | `context-rot` | 17 | queue | `33d8fe7f8aaa` | 3303/1399 | — | ✅ |
| 14:41:44 | `context-rot` | 18 | queue | `3ae7f587ba4d` | 2891/1526 | — | ✅ |
| 14:41:44 | `context-rot` | 19 | queue | `1714829736b5` | 3265/2049 | — | ✅ |
| 14:41:44 | `context-rot` | 20 | queue | `bf4d95d70766` | 1646/1605 | — | ✅ |
| 14:41:44 | `context-rot` | 21 | queue | `406e9870c85b` | 803/421 | — | ✅ |
| 14:41:44 | `context-rot` | 22 | queue | `dbdbc402fbf2` | 826/442 | — | ✅ |
| 14:41:44 | `context-rot` | 23 | queue | `2ec1fa3f95dc` | 1009/405 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 0 | queue | `cdb973987b7e` | 1200/503 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 1 | queue | `825e69c96562` | 3190/1412 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 2 | queue | `3f90cadb5055` | 1596/579 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 3 | queue | `e39a1482ddfb` | 2864/1053 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 4 | queue | `b541c0d47c3e` | 2777/1104 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 5 | queue | `15f063bab250` | 2288/802 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 6 | queue | `b43b50d85a6c` | 1745/672 | — | ✅ |
| 14:43:10 | `agentic-ai-threats` | 7 | queue | `5597c2223b2a` | 927/304 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 8 | queue | `3f49588a15d9` | 3134/2874 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 9 | queue | `42360da74cc2` | 822/402 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 10 | queue | `53568d23e200` | 2691/2470 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 11 | queue | `7f9194988393` | 1765/1023 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 12 | queue | `9d8235359eba` | 1275/426 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 13 | queue | `706c4dacad1e` | 2485/2210 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 14 | queue | `5de019013d7c` | 3155/2154 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 15 | queue | `efa8dc5b88d5` | 3191/1892 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 16 | queue | `bf3cbb809532` | 2058/902 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 17 | queue | `65d7db46850a` | 3681/3446 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 18 | queue | `555fc21061e0` | 1589/698 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 19 | queue | `4cddf33a74a1` | 900/381 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 20 | queue | `635f20c1a460` | 787/282 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 21 | queue | `29493277fe87` | 942/384 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 22 | queue | `5d06603c5c8a` | 1825/926 | — | ✅ |
| 14:48:09 | `agentic-ai-threats` | 23 | queue | `c7905b71bdda` | 489/451 | — | ✅ |
| 14:49:41 | `mcp-introduction` | 6 | queue | `bead8ae9a916` | 594/290 | — | ✅ |
| 14:49:41 | `agentic-ai-threats` | 6 | queue | `b43b50d85a6c` | 1745/982 | — | ✅ |
| 14:50:39 | `agentic-ai-threats` | 7 | queue | `5597c2223b2a` | 927/305 | — | ✅ |

## 管线级事件（非逐块）

| 时间 | 事件 | 说明 |
|---|---|---|
| 2026-09-16T14:46:38 | `qc_criterion_fix` | 全量术语审计改为源文驱动：与 translate.py 逐块校验共用 termcheck.select_terms() |
| 2026-09-16T14:50:24 | `table_row_loss_found` | 逐块校验只看代码围栏数与链接数，不看表格行数，于是三处整行丢失一路通过校验；新增 pipeline/check_tables.py 作为门禁 |
| 2026-09-16T14:50:44 | `term_decision` | 「每个智能体的系统指令」改为「系统提示词」——这一处改的是译文，不是规则 |
| 2026-09-16T14:56:53 | `broken_unit_recheck` | 重抓 5 篇失效条目：2 篇能定位到原始 URL，其中 1 篇查明是视频而非文章；另 3 篇归档里没有留下 URL，拒绝猜测 |
| 2026-09-16T15:32:34 | `deliverable_name_mismatch` | 交付物改名 + 新增 pipeline/check_deliverables.py：AI 日志从 logs/ai-journal.md 改为仓库根目录 AI日志.md；四个「拿来说明」的文件名也含「拿来说明」 |
| 2026-09-16T15:37:35 | `ci_yaml_broken` | 我把 .github/workflows/checks.yml 的注释写成 `//`（JavaScript 风格），整个工作流解析失败；新增 pipeline/check_workflow.py 做本地自检 |

### `qc_criterion_fix`　2026-09-16T14:46:38

- **why**：context-rot 被判 9 处「退化」硬性违规，而该篇源文的英文是 degradation（20 处），全文无 regression；9 处全为假违规并使 CI 变红
- **how**：relevant_terms 的实现上移到 termcheck.py；qc_terminology.py 只为源文中出现过的术语检查禁用变体；被豁免的命中逐条写进报告「一·附」
- **result**：硬性违规 9 → 0；一致率 100.00%；被豁免命中 9 处全部可见
- **cost**：门禁在「源文用别的英文写法表达同一术语」时不再拦截，该局限已写进报告

### `table_row_loss_found`　2026-09-16T14:50:24

- **why**：agentic-ai-threats 第 6 块源表 12 行、译稿 10 行（两行重复载荷行与单元格内重复文本被当噪声删掉）；mcp-introduction 第 6 块源表 10 行、译稿 6 行（4 行 colSpan 分节行被并进数据行）；sast-vs-dast 源清洗稿 0 行表、译稿 12 行
- **how**：1) 前两处按源文逐格重建，重复行与重复载荷文本逐字保留；2) 第三处查源 HTML，确认那张表是 div 嵌套而非 <table>，属清洗管线盲区，差异登记进 pipeline/config/table-exceptions.json；3) 新增 check_tables.py 并接入 CI（检查 4）
- **result**：表行数差异 3 篇 → 1 篇（唯一一篇已登记例外、含证据与处置决定）；检查器自检：对修复前的 mcp-introduction 能报出 源 10 → 译 6
- **cost**：check_tables.py 只比行数、不比单元格内容，单元格里的删改仍抓不到；比 contentAccuracy 要求的更粗

### `term_decision`　2026-09-16T14:50:44

- **why**：术语表 System Prompt → 系统提示词，硬性禁用「系统指令」。命中处源文英文是 system instructions。同一篇的表 1 里 system prompt 已按正式译法译作「系统提示词」，同一篇内自相矛盾；且两处英文指代同一对象
- **how**：回到源文与同一篇的其它译法比对，判定规则正确、译文不一致，因此改译文；不做「规则过宽就降级」的处理
- **result**：硬性违规 1 → 0，一致率 100.00%，28 篇译稿内部一致

### `broken_unit_recheck`　2026-09-16T14:56:53

- **why**：覆盖度已达标，但「补抓失效条目」是本项目自己列的待办；不猜 URL 是因为猜错会把别家的文章当成课程阅读材料
- **how**：1) 从 source/page_map.json 取原始 URL——只找到 3 条，不含这两篇；2) 从归档的课程站点资源 source/site/themodernsoftware.dev/assets/index-CgRb4FxC.js 里读出大纲的完整链接表，确认 Week 7 的这条阅读是 https://www.youtube.com/watch?v=TswQeKftnaw（文字 'Lessons from millions of AI code reviews'），Week 4 的 peeking 是 medium.com/@outsightai/...；3) 用浏览器 UA 重抓 Medium：HTTP 403（Cloudflare 拦截），与归档时的失效原因一致；4) 不采用镜像站替代
- **result**：lessons-from-ai-code-reviews 的失效原因从「抓取完全失败」更正为「该条目是大纲里的视频」：同为大綱视频的另两条已按 external 处理不计入分母，仅此条因留下 0 字节文件被当成 local。保守口径 28/34 = 82.4%；若按 video 处理移出分母则 28/33 = 84.8%。主口径不变，两个数字都写进 README
- **cost**：peeking-under-the-hood-of-claude-code 仍不可自动获取（403）；lessons 这条没有可翻译的正文（视频无字幕），因此 28 条就是当前可达的上限

### `deliverable_name_mismatch`　2026-09-16T15:32:34

- **why**：挑战的 required_deliverables 写着 `README.md,*AI日志*,*AAR*,*拿来说明*`——这四个是**通配符**。glob('*AI日志*') 在本仓库原先返回 0 项：路径 logs/ai-journal.md 里没有「AI日志」四个字。内容一字不少，但在检查器眼里这份交付物不存在，而 rubric 红线 missing_artifacts（产物完整性 ≤5）与 no_ai_log（复盘质量 ≤5）会直接扣死。同理 `*拿来说明*` 要求「至少 3 个」，若只有外层目录叫拿来说明，按文件计数只有 1 项
- **how**：1) 渲染产物改到仓库根目录 AI日志.md（同时满足顶层与递归通配）；2) 拿来说明目录移到仓库根、四个文件名加「拿说明」前缀；3) 新增 check_deliverables.py，直接读挑战包的 required_deliverables 原文，按通配符真匹配并按文件计数，空文件也算失败，接入 CI（检查 5）；4) 全仓库路径引用同步更新
- **result**：四个通配符全部匹配：README.md×1、*AI日志*×1、*AAR*×1、*拿来说明*×4（要求 ≥3）；自检依据是修复前 glob('*AI日志*') = 0 项
- **cost**：顺带发现「按天汇总」缺失——挑战要的是『每日』AI 协作日志，原先只有逐块记录，现补上按天聚合表（09-15：162 块；09-16：317 块）

### `ci_yaml_broken`　2026-09-16T15:37:35

- **why**：YAML 的注释是 `#`。三行 `//` 让 GitHub 直接判该次运行失败，而且 jobs 列表为空——点进去看不到任何失败步骤，只有 failure 两个字。徽章变红但**没有任何信息量**：不是某个检查没过，是检查根本没跑
- **how**：改回 `#`；新增 check_workflow.py：检查 // 注释、tab 缩进、每个步骤有没有 run/uses、五个门禁步骤是否都还在；脚本对带 // 与带 tab 的样本能报警（自检过）
- **result**：run 35069352079 的失败原因定位并修复；工作流自检 0 问题
- **cost**：这个检查在 CI 里跑有点自己救自己的意味（解析失败时 CI 不会启动），真实价值在本地提交前；已如实写在报告的脚注里

## 失败与返工记录

这一节是日志里最有价值的部分——它记录的是**真实踩过的坑**。

### `warp-vs-claude-code` 第 1 块

- 时间：2026-09-15T15:25:48+0800　后端：queue　prompt 哈希：`3c1156174b50`
- 问题：出现禁用变体「协调」（应为「编排」）

### `mcp-food-for-thought` 第 0 块

- 时间：2026-09-15T15:26:51+0800　后端：queue　prompt 哈希：`69589c06eeb3`
- 问题：出现禁用变体「上下文协议」（应为「模型上下文协议（MCP）」）

### `mcp-food-for-thought` 第 2 块

- 时间：2026-09-15T15:26:51+0800　后端：queue　prompt 哈希：`777ddeac2db9`
- 问题：出现禁用变体「检索增强」（应为「检索增强生成（RAG）」）

### `benefits-agentic-ai-oncall` 第 0 块

- 时间：2026-09-15T15:26:51+0800　后端：queue　prompt 哈希：`a862b2069d5e`
- 问题：出现禁用变体「情境」（应为「上下文」）
- 问题：出现禁用变体「流程」（应为「工作流」）
- 问题：出现禁用变体「记录」（应为「日志」）
- 问题：出现禁用变体「事件」（应为「故障事件」）
- 问题：出现禁用变体「故障」（应为「故障事件」）

### `benefits-agentic-ai-oncall` 第 1 块

- 时间：2026-09-15T15:26:51+0800　后端：queue　prompt 哈希：`5248b3ecaca3`
- 问题：出现禁用变体「故障」（应为「故障事件」）

### `benefits-agentic-ai-oncall` 第 0 块

- 时间：2026-09-15T15:27:27+0800　后端：queue　prompt 哈希：`ac1505d0fb17`
- 问题：出现禁用变体「情境」（应为「上下文」）

### `code-reviews-just-do-it` 第 0 块

- 时间：2026-09-15T15:59:34+0800　后端：queue　prompt 哈希：`94627e072ac7`
- 问题：出现禁用变体「代码审查」（应为「代码评审」）

### `kubernetes-troubleshooting-ai` 第 1 块

- 时间：2026-09-15T16:00:31+0800　后端：queue　prompt 哈希：`6cccae495d52`
- 问题：出现禁用变体「遥测数据」（应为「遥测」）

### `kubernetes-troubleshooting-ai` 第 2 块

- 时间：2026-09-15T16:00:31+0800　后端：queue　prompt 哈希：`2d8a1f00389b`
- 问题：出现禁用变体「遥测数据」（应为「遥测」）

### `copilot-prompt-injection-rce` 第 5 块

- 时间：2026-09-15T16:01:27+0800　后端：queue　prompt 哈希：`9cbfe0431a4c`
- 问题：出现禁用变体「缺陷」（应为「漏洞」）
- 问题：出现禁用变体「威胁建模」（应为「威胁模型」）

### `multi-agent-systems-ai-native` 第 2 块

- 时间：2026-09-15T16:04:03+0800　后端：queue　prompt 哈希：`c946a43bc904`
- 问题：出现禁用变体「语境」（应为「上下文」）
- 问题：出现禁用变体「协调」（应为「编排」）

### `multi-agent-systems-ai-native` 第 3 块

- 时间：2026-09-15T16:04:03+0800　后端：queue　prompt 哈希：`e8e42959808a`
- 问题：出现禁用变体「协调」（应为「编排」）

### `multi-agent-systems-ai-native` 第 2 块

- 时间：2026-09-15T16:04:11+0800　后端：queue　prompt 哈希：`c946a43bc904`
- 问题：出现禁用变体「协调」（应为「编排」）

### `multi-agent-systems-ai-native` 第 3 块

- 时间：2026-09-15T16:04:11+0800　后端：queue　prompt 哈希：`e8e42959808a`
- 问题：出现禁用变体「协调」（应为「编排」）

### `observability-basics` 第 3 块

- 时间：2026-09-15T16:14:01+0800　后端：queue　prompt 哈希：`595453e49b48`
- 问题：出现禁用变体「遥测数据」（应为「遥测」）

### `observability-basics` 第 5 块

- 时间：2026-09-15T16:14:42+0800　后端：queue　prompt 哈希：`ed66b37728b0`
- 问题：出现禁用变体「规范」（应为「规格说明」）

### `observability-basics` 第 7 块

- 时间：2026-09-15T16:14:42+0800　后端：queue　prompt 哈希：`23c544cc1b46`
- 问题：出现禁用变体「跟踪」（应为「链路追踪」）
- 问题：出现禁用变体「度量」（应为「指标」）

### `observability-basics` 第 9 块

- 时间：2026-09-15T16:14:42+0800　后端：queue　prompt 哈希：`f7dc9eb02d5b`
- 问题：出现禁用变体「轨迹」（应为「追踪记录」）

### `mcp-server-authentication` 第 3 块

- 时间：2026-09-15T16:16:55+0800　后端：queue　prompt 哈希：`440f6ef61b89`
- 问题：出现禁用变体「代理」（应为「智能体」）

### `specs-are-the-new-source-code` 第 1 块

- 时间：2026-09-16T13:33:42+0800　后端：queue　prompt 哈希：`3f609b38e780`
- 问题：出现禁用变体「产物」（应为「制品」）×3

### `specs-are-the-new-source-code` 第 5 块

- 时间：2026-09-16T13:33:42+0800　后端：queue　prompt 哈希：`f0ba7c32849f`
- 问题：出现禁用变体「产物」（应为「制品」）×1

### `sast-vs-dast` 第 2 块

- 时间：2026-09-16T13:43:57+0800　后端：queue　prompt 哈希：`5f4d59694fe5`
- 问题：出现禁用变体「运行环境」（应为「运行时」）×1

### `sast-vs-dast` 第 5 块

- 时间：2026-09-16T13:43:57+0800　后端：queue　prompt 哈希：`7fdc7d5f0175`
- 问题：出现禁用变体「弱点」（应为「漏洞」）×2

### `sast-vs-dast` 第 7 块

- 时间：2026-09-16T13:43:57+0800　后端：queue　prompt 哈希：`eecaf7f33481`
- 问题：链接数不符：原文 0，译文 1

### `sast-vs-dast` 第 2 块

- 时间：2026-09-16T13:44:11+0800　后端：queue　prompt 哈希：`5f4d59694fe5`
- 问题：出现禁用变体「运行环境」（应为「运行时」）×1

### `writing-effective-tools-for-agents` 第 11 块

- 时间：2026-09-16T13:47:11+0800　后端：queue　prompt 哈希：`90bd23ce2f2a`
- 问题：出现禁用变体「MCP 协议」（应为「模型上下文协议（MCP）」）×1

### `devin-coding-agents-101` 第 2 块

- 时间：2026-09-16T13:55:39+0800　后端：queue　prompt 哈希：`37f333225df6`
- 问题：出现禁用变体「检查器」（应为「代码检查工具」）×1

### `prompt-engineering-overview` 第 1 块

- 时间：2026-09-16T14:12:52+0800　后端：queue　prompt 哈希：`e3df116dee11`
- 问题：出现禁用变体「语境」（应为「上下文」）×1

### `prompt-engineering-overview` 第 4 块

- 时间：2026-09-16T14:12:52+0800　后端：queue　prompt 哈希：`9c05cb4f8602`
- 问题：出现禁用变体「情境」（应为「上下文」）×1

### `finding-vulnerabilities-claude-codex` 第 0 块

- 时间：2026-09-16T14:15:07+0800　后端：queue　prompt 哈希：`c9cfb242bd7b`
- 问题：出现禁用变体「假阳性」（应为「误报」）×2

### `finding-vulnerabilities-claude-codex` 第 2 块

- 时间：2026-09-16T14:15:07+0800　后端：queue　prompt 哈希：`01d5b791d0f0`
- 问题：出现禁用变体「假阳性」（应为「误报」）×2
- 问题：出现禁用变体「假阴性」（应为「漏报」）×2

### `finding-vulnerabilities-claude-codex` 第 5 块

- 时间：2026-09-16T14:15:07+0800　后端：queue　prompt 哈希：`44d353b058ca`
- 问题：出现禁用变体「假阳性」（应为「误报」）×2

### `finding-vulnerabilities-claude-codex` 第 6 块

- 时间：2026-09-16T14:15:07+0800　后端：queue　prompt 哈希：`e76700c056f8`
- 问题：出现禁用变体「假阳性」（应为「误报」）×3

### `finding-vulnerabilities-claude-codex` 第 7 块

- 时间：2026-09-16T14:15:07+0800　后端：queue　prompt 哈希：`cfe78517cb3f`
- 问题：出现禁用变体「语境」（应为「上下文」）×1

### `finding-vulnerabilities-claude-codex` 第 10 块

- 时间：2026-09-16T14:15:07+0800　后端：queue　prompt 哈希：`0e5b2da8bde1`
- 问题：出现禁用变体「假阳性」（应为「误报」）×2
- 问题：出现禁用变体「假阴性」（应为「漏报」）×3

### `sre-introduction` 第 7 块

- 时间：2026-09-16T14:17:00+0800　后端：queue　prompt 哈希：`ae951e83837a`
- 问题：出现禁用变体「平均修复时间」（应为「平均恢复时间（MTTR）」）×1

### `mcp-introduction` 第 1 块

- 时间：2026-09-16T14:22:40+0800　后端：queue　prompt 哈希：`63bdcd000f77`
- 问题：出现禁用变体「MCP 协议」（应为「模型上下文协议（MCP）」）×1

### `mcp-introduction` 第 7 块

- 时间：2026-09-16T14:22:40+0800　后端：queue　prompt 哈希：`4b12c0cbceb3`
- 问题：出现禁用变体「MCP 协议」（应为「模型上下文协议（MCP）」）×1

### `how-anthropic-uses-claude-code` 第 9 块

- 时间：2026-09-16T14:24:41+0800　后端：queue　prompt 哈希：`7dda9b591d99`
- 问题：出现禁用变体「回退」（应为「回滚」）×1

### `context-rot` 第 3 块

- 时间：2026-09-16T14:39:08+0800　后端：queue　prompt 哈希：`2c8b72d9ba25`
- 问题：出现禁用变体「嵌入向量」（应为「嵌入」）×1

### `context-rot` 第 5 块

- 时间：2026-09-16T14:39:08+0800　后端：queue　prompt 哈希：`ff287b296b28`
- 问题：出现禁用变体「嵌入向量」（应为「嵌入」）×1

### `context-rot` 第 6 块

- 时间：2026-09-16T14:39:08+0800　后端：queue　prompt 哈希：`eacffc0cf59d`
- 问题：出现禁用变体「嵌入向量」（应为「嵌入」）×1

## 条目汇总

| 条目 | 周 | 块数 | 中文字符 | 完成时间 |
|---|---|---|---|---|
| `warp-vs-claude-code` | W5 | 4 | 2,714 | 2026-09-15T15:25:59 |
| `warp-vs-claude-code` | W5 | 4 | 2,714 | 2026-09-15T15:26:51 |
| `mcp-food-for-thought` | W2 | 4 | 2,781 | 2026-09-15T15:27:27 |
| `warp-vs-claude-code` | W5 | 4 | 2,714 | 2026-09-15T15:27:27 |
| `mcp-food-for-thought` | W2 | 4 | 2,781 | 2026-09-15T15:27:41 |
| `warp-vs-claude-code` | W5 | 4 | 2,714 | 2026-09-15T15:27:41 |
| `benefits-agentic-ai-oncall` | W9 | 3 | 1,789 | 2026-09-15T15:27:41 |
| `mcp-food-for-thought` | W2 | 4 | 2,743 | 2026-09-15T15:32:24 |
| `mcp-registry-preview` | W2 | 3 | 3,307 | 2026-09-15T15:59:34 |
| `code-reviews-just-do-it` | W7 | 1 | 1,431 | 2026-09-15T15:59:42 |
| `kubernetes-troubleshooting-ai` | W9 | 6 | 3,978 | 2026-09-15T16:00:37 |
| `copilot-prompt-injection-rce` | W6 | 6 | 3,763 | 2026-09-15T16:01:35 |
| `multi-agent-systems-ai-native` | W9 | 5 | 3,839 | 2026-09-15T16:04:22 |
| `claude-code-best-practices` | W4 | 4 | 4,512 | 2026-09-15T16:04:53 |
| `how-long-contexts-fail` | W3 | 6 | 4,269 | 2026-09-15T16:10:02 |
| `observability-basics` | W9 | 10 | 5,109 | 2026-09-15T16:14:52 |
| `ai-code-review-best-practices` | W7 | 8 | 4,700 | 2026-09-15T16:16:08 |
| `mcp-server-authentication` | W2 | 8 | 8,520 | 2026-09-15T16:17:35 |
| `specs-are-the-new-source-code` | W3 | 6 | 5,410 | 2026-09-16T13:33:52 |
| `code-review-essentials` | W7 | 5 | 4,107 | 2026-09-16T13:35:24 |
| `how-openai-uses-codex` | W1 | 4 | 4,690 | 2026-09-16T13:39:56 |
| `owasp-top-ten` | W6 | 10 | 8,648 | 2026-09-16T13:41:18 |
| `sast-vs-dast` | W6 | 16 | 8,022 | 2026-09-16T13:44:32 |
| `writing-effective-tools-for-agents` | W3 | 12 | 8,634 | 2026-09-16T13:47:20 |
| `how-to-review-code-effectively` | W7 | 13 | 9,018 | 2026-09-16T13:52:54 |
| `devin-coding-agents-101` | W3 | 17 | 7,302 | 2026-09-16T13:55:46 |
| `prompt-engineering-overview` | W1 | 13 | 6,129 | 2026-09-16T14:13:00 |
| `finding-vulnerabilities-claude-codex` | W6 | 12 | 11,069 | 2026-09-16T14:15:16 |
| `sre-introduction` | W9 | 10 | 8,031 | 2026-09-16T14:17:09 |
| `mcp-introduction` | W2 | 17 | 11,678 | 2026-09-16T14:22:49 |
| `how-anthropic-uses-claude-code` | W4 | 11 | 13,275 | 2026-09-16T14:24:49 |
| `context-rot` | W6 | 24 | 19,796 | 2026-09-16T14:41:44 |
| `agentic-ai-threats` | W6 | 24 | 27,423 | 2026-09-16T14:48:09 |
| `mcp-introduction` | W2 | 17 | 11,718 | 2026-09-16T14:49:41 |
| `agentic-ai-threats` | W6 | 24 | 27,733 | 2026-09-16T14:49:41 |
| `agentic-ai-threats` | W6 | 24 | 27,734 | 2026-09-16T14:50:39 |

