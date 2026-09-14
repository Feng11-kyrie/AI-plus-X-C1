# 清洗前后对比报告（HTML → Markdown）

> 由 `pipeline/clean.py` 自动生成，**请勿手工编辑**。

## 为什么要清洗

原始 HTML 里绝大部分是导航、脚本与样式样板，不是正文。若直接把 HTML 交给翻译模型：

1. **浪费 token**——付费处理脚本与导航；
2. **污染结构**——译文里混入导航文字，破坏可读性；
3. **让覆盖度失真**——以为翻译了 128KB，实际只翻了 2KB 正文。

## 总体效果

| 指标 | 数值 |
|---|---|
| 处理篇数 | 31（其中可入管线 26 篇，失效 5 篇） |
| 原始 HTML 总量 | 6.28 MB |
| 清洗后 Markdown | 0.43 MB（可入管线部分 0.43 MB） |
| **有效篇目压缩率** | **7.0%**（体积降至 1/14.3） |
| 可翻译正文词数 | 65,156 |
| 翻译分块数 | 398 |

## 逐篇明细

`密度` = 清洗后体积 / 原始 HTML 体积。**密度越低，说明原始 HTML 里样板越多、清洗收益越大**——低到 1% 上下意味着99% 的原始体积都是垃圾，不清洗就等于把 99% 的 token 预算烧在导航和脚本上。

| 周 | 篇目 | 原始 HTML | 清洗后 | 密度 | 词数 | 分块 | 判定 | 失效模式 |
|---|---|---|---|---|---|---|---|---|
| W7 | `lessons-from-ai-code-reviews` | 0 KB | 0.0 KB | **0.0%** | 0 | 0 | **失效** | 文件 0 字节，抓取完全失败 |
| W5 | `how-warp-uses-warp` | 15 KB | 0.0 KB | **0.0%** | 1 | 0 | **失效** | Notion JS 渲染页：正文需 JavaScript 才能生成，静态抓取只能拿到外壳 |
| W1 | `prompt-engineering-guide` | 125 KB | 0.5 KB | **0.4%** | 82 | 0 | **失效** | SPA 导航壳：__NEXT_DATA__ 载荷为空，真实正文在未被抓取的子页面中 |
| W4 | `good-context-good-code` | 9 KB | 0.1 KB | **0.8%** | 13 | 0 | **失效** | 访问码 / 付费墙拦截：抓到的只是登录门页 |
| W5 | `warp-vs-claude-code` | 442 KB | 5.0 KB | **1.1%** | 615 | 9 | OK | — |
| W4 | `claude-code-best-practices` | 813 KB | 9.3 KB | **1.1%** | 1,487 | 6 | OK | — |
| W1 | `prompt-engineering-overview` | 1958 KB | 24.3 KB | **1.2%** | 3,678 | 32 | OK | — |
| W9 | `benefits-agentic-ai-oncall` | 139 KB | 5.4 KB | **3.9%** | 760 | 3 | OK | — |
| W3 | `specs-are-the-new-source-code` | 212 KB | 12.4 KB | **5.8%** | 1,912 | 7 | OK | — |
| W9 | `kubernetes-troubleshooting-ai` | 144 KB | 9.0 KB | **6.2%** | 1,221 | 6 | OK | — |
| W9 | `multi-agent-systems-ai-native` | 166 KB | 10.6 KB | **6.4%** | 1,439 | 5 | OK | — |
| W2 | `mcp-server-authentication` | 186 KB | 12.4 KB | **6.7%** | 1,701 | 11 | OK | — |
| W7 | `ai-code-review-best-practices` | 178 KB | 13.3 KB | **7.5%** | 1,901 | 12 | OK | — |
| W2 | `mcp-introduction` | 369 KB | 30.7 KB | **8.3%** | 4,721 | 19 | OK | — |
| W9 | `observability-basics` | 130 KB | 11.7 KB | **9.0%** | 1,699 | 27 | OK | — |
| W2 | `mcp-food-for-thought` | 54 KB | 5.2 KB | **9.7%** | 728 | 6 | OK | — |
| W3 | `writing-effective-tools-for-agents` | 199 KB | 21.7 KB | **10.9%** | 3,123 | 15 | OK | — |
| W7 | `how-to-review-code-effectively` | 193 KB | 21.7 KB | **11.2%** | 3,278 | 20 | OK | — |
| W7 | `code-reviews-just-do-it` | 47 KB | 6.2 KB | **13.1%** | 953 | 11 | OK | — |
| W6 | `agentic-ai-threats` | 383 KB | 53.6 KB | **14.0%** | 7,798 | 28 | OK | — |
| W6 | `context-rot` | 265 KB | 41.9 KB | **15.8%** | 6,271 | 32 | OK | — |
| W6 | `finding-vulnerabilities-claude-codex` | 112 KB | 24.0 KB | **21.4%** | 3,650 | 14 | OK | — |
| W6 | `owasp-top-ten` | 69 KB | 16.8 KB | **24.3%** | 2,311 | 24 | OK | — |
| W2 | `mcp-registry-preview` | 27 KB | 6.5 KB | **24.5%** | 796 | 3 | OK | — |
| W6 | `copilot-prompt-injection-rce` | 21 KB | 8.2 KB | **38.8%** | 1,240 | 14 | OK | — |
| W6 | `sast-vs-dast` | 49 KB | 21.6 KB | **43.7%** | 2,943 | 25 | OK | — |
| W3 | `devin-coding-agents-101` | 42 KB | 21.7 KB | **51.9%** | 3,488 | 43 | OK | — |
| W9 | `sre-introduction` | 43 KB | 24.5 KB | **56.5%** | 3,824 | 12 | OK | — |
| W3 | `how-long-contexts-fail` | 19 KB | 10.8 KB | **57.9%** | 1,579 | 8 | OK | — |
| W4 | `peeking-under-the-hood-of-claude-code` | 1 KB | 0.4 KB | **77.8%** | 44 | 0 | **失效** | 体积过小，抓到的是占位页 |
| W7 | `code-review-essentials` | 15 KB | 11.7 KB | **80.1%** | 2,040 | 6 | OK | — |

## 异常提示

以下 **5 篇**清洗后正文不足 1500 字符，**无法进入翻译管线**。
这些条目在覆盖度分母中仍占位，但拿不到内容——是必须先解决的缺口：

| 篇目 | 周 | 原始 HTML | 清洗后正文 | 失效模式 |
|---|---|---|---|---|
| `prompt-engineering-guide` | W1 | 125 KB | 548 字节 | SPA 导航壳：__NEXT_DATA__ 载荷为空，真实正文在未被抓取的子页面中 |
| `good-context-good-code` | W4 | 9 KB | 77 字节 | 访问码 / 付费墙拦截：抓到的只是登录门页 |
| `peeking-under-the-hood-of-claude-code` | W4 | 1 KB | 428 字节 | 体积过小，抓到的是占位页 |
| `how-warp-uses-warp` | W5 | 15 KB | 7 字节 | Notion JS 渲染页：正文需 JavaScript 才能生成，静态抓取只能拿到外壳 |
| `lessons-from-ai-code-reviews` | W7 | 0 KB | 1 字节 | 文件 0 字节，抓取完全失败 |

> 这些篇目**不会**产出 `clean/*.md`，也不会进入 `chunks.json`——即它们对翻译覆盖度贡献为 0。详见 `source/INVENTORY.md` 第二节。

## 产物

| 产物 | 位置 | 是否入库 |
|---|---|---|
| 清洗后英文底稿 | `clean/<unit>.md`（26 篇） | ✅ 入库，可人工抽检 |
| 翻译分块 | `pipeline/work/chunks.json`（398 块） | ⬜ 中间产物，可复跑再生 |
