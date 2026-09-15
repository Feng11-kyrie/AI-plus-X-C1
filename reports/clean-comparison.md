# 清洗前后对比报告（HTML/PDF → Markdown）

> 由 `pipeline/clean.py` 自动生成，**请勿手工编辑**。

## 为什么要清洗

原始 HTML 里绝大部分是导航、脚本与样式样板，不是正文。若直接把 HTML 交给翻译模型：

1. **浪费 token**——付费处理脚本与导航；
2. **污染结构**——译文里混入导航文字，破坏可读性；
3. **让覆盖度失真**——以为翻译了 128KB，实际只翻了 2KB 正文。

## 总体效果

| 指标 | 数值 |
|---|---|
| 处理条目数 | 34（HTML 31 + PDF 3） |
| 可入管线 | **29**（HTML 26 + PDF 3） |
| 失效 | 5 |
| 原始体积 | 20.82 MB |
| 清洗后 Markdown | 0.54 MB |
| **有效条目压缩率** | **2.6%**（降至 1/38.2） |
| 可翻译正文词数 | 82,879 |
| 翻译分块数 | 272（合并小块前为 398 块——合并见「合并过小相邻块」的设计说明） |
| 平均块大小 | 2,073 字符（合并前中位数仅 795） |

## 逐篇明细

三列质量指标的含义：

- **密度** = 清洗后体积 / 原始体积。越低说明样板越多、清洗收益越大。低到 1% 上下意味着 99% 的原始体积是垃圾。
- **留存** = 正文容器文字量 → Markdown 纯文字量的留存率。这是**防静默丢内容的主判据**，低于 90% 报警。
- **修复** = 该篇修掉的乱码行数 / 剔除的样板行数。

| 周 | 篇目 | 格式 | 原始 | 清洗后 | 密度 | 留存 | 修复 | 词数 | 分块 | 判定 | 失效模式 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| W1 | `how-openai-uses-codex` | pdf | 7852 KB | 12.7 KB | **0.2%** | n/a | — | 2,117 | 4 | OK | PDF 未逐页校验，按可用计 |
| W4 | `how-anthropic-uses-claude-code` | pdf | 6073 KB | 38.4 KB | **0.6%** | n/a | — | 6,032 | 11 | OK | PDF 未逐页校验，按可用计 |
| W4 | `claude-code-best-practices` | html | 813 KB | 9.4 KB | **1.2%** | **100.0%** | — | 1,487 | 4 | OK | — |
| W5 | `warp-vs-claude-code` | html | 442 KB | 5.1 KB | **1.2%** | **100.0%** | — | 615 | 4 | OK | — |
| W1 | `prompt-engineering-overview` | html | 1958 KB | 24.3 KB | **1.2%** | **100.0%** | — | 3,678 | 14 | OK | — |
| W9 | `benefits-agentic-ai-oncall` | html | 139 KB | 5.4 KB | **3.9%** | **100.0%** | — | 760 | 3 | OK | — |
| W7 | `ai-assisted-code-review-assessment` | pdf | 963 KB | 52.5 KB | **5.4%** | n/a | — | 8,051 | 9 | OK | PDF 未逐页校验，按可用计 |
| W3 | `specs-are-the-new-source-code` | html | 212 KB | 12.9 KB | **6.1%** | **100.0%** | — | 1,914 | 6 | OK | — |
| W9 | `kubernetes-troubleshooting-ai` | html | 144 KB | 9.0 KB | **6.2%** | **100.0%** | — | 1,221 | 6 | OK | — |
| W9 | `multi-agent-systems-ai-native` | html | 166 KB | 10.6 KB | **6.4%** | **100.0%** | — | 1,439 | 5 | OK | — |
| W7 | `ai-code-review-best-practices` | html | 178 KB | 13.3 KB | **7.5%** | **98.8%** | — | 1,901 | 8 | OK | — |
| W2 | `mcp-server-authentication` | html | 186 KB | 14.3 KB | **7.7%** | **100.0%** | 22乱/0样 | 1,909 | 8 | OK | — |
| W7 | `code-reviews-just-do-it` | html | 47 KB | 3.7 KB | **7.7%** | **99.8%** | — | 562 | 1 | OK | — |
| W2 | `mcp-introduction` | html | 369 KB | 30.7 KB | **8.3%** | **100.0%** | — | 4,721 | 17 | OK | — |
| W9 | `observability-basics` | html | 130 KB | 11.7 KB | **9.0%** | **100.0%** | — | 1,699 | 10 | OK | — |
| W2 | `mcp-food-for-thought` | html | 54 KB | 5.2 KB | **9.7%** | **100.0%** | — | 728 | 4 | OK | — |
| W7 | `how-to-review-code-effectively` | html | 193 KB | 21.7 KB | **11.2%** | **100.0%** | — | 3,278 | 13 | OK | — |
| W3 | `writing-effective-tools-for-agents` | html | 199 KB | 22.6 KB | **11.4%** | **100.0%** | — | 3,254 | 12 | OK | — |
| W6 | `agentic-ai-threats` | html | 383 KB | 54.4 KB | **14.2%** | **100.0%** | — | 7,901 | 24 | OK | — |
| W6 | `context-rot` | html | 265 KB | 50.2 KB | **18.9%** | **99.9%** | — | 7,602 | 24 | OK | — |
| W6 | `finding-vulnerabilities-claude-codex` | html | 112 KB | 24.9 KB | **22.2%** | **100.0%** | — | 3,789 | 12 | OK | — |
| W6 | `owasp-top-ten` | html | 70 KB | 16.8 KB | **24.1%** | **100.0%** | — | 2,311 | 10 | OK | — |
| W2 | `mcp-registry-preview` | html | 27 KB | 6.5 KB | **24.5%** | **100.0%** | — | 796 | 3 | OK | — |
| W6 | `copilot-prompt-injection-rce` | html | 21 KB | 8.2 KB | **38.8%** | **100.0%** | — | 1,240 | 6 | OK | — |
| W6 | `sast-vs-dast` | html | 49 KB | 21.6 KB | **43.7%** | **100.0%** | — | 2,943 | 16 | OK | — |
| W3 | `devin-coding-agents-101` | html | 42 KB | 21.7 KB | **51.9%** | **100.0%** | — | 3,488 | 17 | OK | — |
| W9 | `sre-introduction` | html | 43 KB | 24.4 KB | **56.1%** | **100.0%** | 34乱/0样 | 3,824 | 10 | OK | — |
| W3 | `how-long-contexts-fail` | html | 19 KB | 10.8 KB | **57.9%** | **100.0%** | — | 1,579 | 6 | OK | — |
| W7 | `code-review-essentials` | html | 15 KB | 11.7 KB | **80.1%** | **100.0%** | — | 2,040 | 5 | OK | — |
| W7 | `lessons-from-ai-code-reviews` | html | 0 KB | 0.0 KB | **0.0%** | **0.0%** | — | 0 | 0 | **失效** | 文件 0 字节，抓取完全失败 |
| W5 | `how-warp-uses-warp` | html | 15 KB | 0.0 KB | **0.0%** | **100.0%** | — | 1 | 0 | **失效** | Notion JS 渲染页：正文需 JavaScript 才能生成，静态抓取只能拿到外壳 |
| W4 | `good-context-good-code` | html | 9 KB | 0.0 KB | **0.3%** | **90.5%** | 0乱/3样 | 4 | 0 | **失效** | 访问码 / 付费墙拦截：抓到的只是登录门页 |
| W1 | `prompt-engineering-guide` | html | 125 KB | 0.5 KB | **0.4%** | **99.8%** | 0乱/1样 | 79 | 0 | **失效** | SPA 导航壳：__NEXT_DATA__ 载荷为空，真实正文在未被抓取的子页面中 |
| W4 | `peeking-under-the-hood-of-claude-code` | html | 1 KB | 0.4 KB | **77.8%** | **100.0%** | — | 44 | 0 | **失效** | 体积过小，抓到的是占位页 |

## 一、有效性检查

以下 **5 条**清洗后正文不足 1500 字符，**无法进入翻译管线**。这些条目在覆盖度分母中仍占位，但拿不到内容——是必须先解决的缺口：

| 篇目 | 周 | 格式 | 原始 | 清洗后正文 | 失效模式 |
|---|---|---|---|---|---|
| `prompt-engineering-guide` | W1 | html | 125 KB | 533 字节 | SPA 导航壳：__NEXT_DATA__ 载荷为空，真实正文在未被抓取的子页面中 |
| `good-context-good-code` | W4 | html | 9 KB | 25 字节 | 访问码 / 付费墙拦截：抓到的只是登录门页 |
| `peeking-under-the-hood-of-claude-code` | W4 | html | 1 KB | 428 字节 | 体积过小，抓到的是占位页 |
| `how-warp-uses-warp` | W5 | html | 15 KB | 7 字节 | Notion JS 渲染页：正文需 JavaScript 才能生成，静态抓取只能拿到外壳 |
| `lessons-from-ai-code-reviews` | W7 | html | 0 KB | 1 字节 | 文件 0 字节，抓取完全失败 |

> 这些条目**不会**产出 `clean/*.md`，也不会进入 `chunks.json`——即它们对翻译覆盖度贡献为 0。详见 `source/INVENTORY.md` 第二节。

## 二、内容丢失检查

清洗最容易出的错是**静默丢内容**——文件还在、看着正常，但正文缺了一块。体积指标对此完全无感，所以必须有独立的元素级校验。

✓ 未发现内容丢失。全部有效条目的文字留存率均达标，且代码块数量在「原始 → 正文容器 → Markdown」三个层次保持一致。

校验方法：对每条比对三个层次的元素数量

| 层次 | 含义 |
|---|---|
| `raw` | 整个原始文件（含样板） |
| `main` | 剔除样板、选定正文容器之后 |
| `md` | 最终 Markdown |

`raw → main` 的差距暴露**样板剔除误伤正文**；`main → md` 的差距暴露**渲染器漏渲染**。代码块单独严判：它一旦丢了围栏，内容会被当散文翻译，而代码必须逐字保留。

## 三、产物

| 产物 | 位置 | 是否入库 |
|---|---|---|
| 清洗后英文底稿 | `clean/<unit>.md`（29 条） | ✅ 入库，可人工抽检 |
| 翻译分块 | `pipeline/work/chunks.json`（272 块） | ⬜ 中间产物，可复跑再生 |
