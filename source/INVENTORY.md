# 资料清点与缺口报告（INVENTORY）

> 本文件由 `pipeline/inventory.py` 自动生成，**请勿手工编辑**（改脚本后重跑）。
> 数据源：`source/syllabus.json` + `source/page_map.json`。

课程：**CS146S: The Modern Software Developer**（Stanford University，Fall 2025）
讲师：Mihail Eric ｜ 原始站点：https://themodernsoftware.dev/ ｜ 缓存于 2026-04-02

---

## 一、覆盖度分母（自证）

覆盖度不能只报一个百分比，必须先说清**分母是什么**。本报告采用的定义：

- **分母 = 大纲中指向本地文件的 readings = 34 条**（即 `pages/` 与 `pdfs/` 中有实体文件的条目）
- **其中可用 = 29 条**（HTML 26 + PDF 3），**确认无效 = 5 条**
- **分子 = 已产出中文译稿的可用条目数**（随管线推进更新）
- 目标：分子 / 分母 ≥ **80%**，即 ≥ 27 条

> **为什么不把外链算进分母**：大纲另有 10 条指向外部站点（YouTube / GitHub / X / 第三方博客），它们不受本地缓存控制，其可获得性取决于对方站点与账号权限，属于**扩展范围**，计入分母会让覆盖率失去可比性。详见第四节。

### 换算成硬指标

| 口径 | 数量 | 说明 |
|---|---|---|
| 分母（本地 readings） | 34 | HTML 31 + PDF 3 |
| **可用条目** | **29** | HTML 26 + PDF 3，内容完整可翻译 |
| **确认无效条目** | **5** | 全部为 HTML，详见第二节 |
| 达到 80% 所需最少条目 | 27 | ceil(34 × 0.8) |
| 可用英文正文字数（估） | ≈ 67,127 | 仅 HTML 可用条目（按清洗后正文计），PDF 未计 |

> ✅ **可行性**：可用条目 29 条 ≥ 目标 27 条。全部译完可达 85.3%。

> ⚠️ **注意**：PDF 条目 **必须纳入翻译范围** 才能达标记。若只翻译 HTML 部分，覆盖率为 26/34 = 76.5%，**低于目标**。

---

## 二、缺口清单（必须处理）

以下条目**已在 `pages/` 中登记，但内容不可用**，是当前管线的第一批待办：

| # | 周 | 标题 | 文件 | 原始字节 | 清洗后正文 | 失效模式 | 处置建议 |
|---|---|---|---|---|---|---|---|
| 1 | W1 | Prompt Engineering Guide | `prompt-engineering-guide.html` | 128476 | 530 字符 | SPA 导航壳：__NEXT_DATA__ 载荷为空，真实正文在未被抓取的子页面中 | 需补抓其指向的子页面，或将本页降级为索引 |
| 2 | W4 | Good Context Good Code | `good-context-good-code.html` | 9278 | 25 字符 | 访问码 / 付费墙拦截：抓到的只是登录门页 | 需人工获取 / 登录访问，或声明缺口 |
| 3 | W4 | Peeking Under the Hood of Claude Code | `peeking-under-the-hood-of-claude-code.html` | 550 | 428 字符 | 体积过小，抓到的是占位页 | 需人工导出，或声明缺口 |
| 4 | W5 | How Warp Uses Warp to Build Warp | `how-warp-uses-warp.html` | 15515 | 7 字符 | Notion JS 渲染页：正文需 JavaScript 才能生成，静态抓取只能拿到外壳 | 需人工获取 / 登录访问，或声明缺口 |
| 5 | W7 | Lessons from Millions of AI Code Reviews | `lessons-from-ai-code-reviews.html` | 0 | 1 字符 | 文件 0 字节，抓取完全失败 | 重新抓取源站 |

> 判定口径：剔除 script/style/nav/footer 等样板后，**正文不足 1500 字符**即视为无效——因为这类页面即使占着文件名，也无法进入翻译管线。

### 2.1 讲义（Slides）——**完全缺失**

`slides_info/` 为空目录：**课程 10 周的讲义元数据一条都未抓取到**。
大纲中登记的讲义链接如下（全部为 Google Slides/Drive，**需 Google 账号**，自动化抓取不可行）：

| 周 | 讲义 | 类型 | 链接 |
|---|---|---|---|
| W1 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1zT2Ofy88cajLTLkd7TcuSM4BCELvF9qQdHmlz33i4t0/edit?usp=sha |
| W1 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1MIhw8p6TLGdbQ9TcxhXSs5BaPf5d_h77QY70RHNfeGs/edit?usp=dri |
| W2 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/11CP26VhsjnZOmi9YFgLlonzdib9BLyAlgc4cEvC5Fps/edit?usp=sha |
| W2 | Completed Exercise | 其它外部 | https://drive.google.com/file/d/1YtpKFVG13DHyQ2i3HOtwyVJOV90nWeL2/view?usp=drive_link |
| W2 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1zSC2ra77XOUrJeyS85houg1DU7z9hq5Y4ebagTch-5o/edit?usp=dri |
| W2 | Completed Exercise | 其它外部 | https://drive.google.com/file/d/1J6lgZWcxPzpCpjujJSnW1aAkCYF6Yxv3/view?usp=drive_link |
| W3 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/11pQNCde_mmRnImBat0Zymnp8TCS_cT_1up7zbcj6Sjg/edit?usp=sha |
| W3 | Cognition | 其它外部 | https://cognition.ai/ |
| W3 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1i0pRttHf72lgz8C-n7DSegcLBgncYZe_ppU7dB9zhUA/edit?usp=sha |
| W3 | Design Doc Template | 其它外部 | https://drive.google.com/file/d/1MZ0Qx68Vzw4x5x_XcV8XiPLp7fFDe1LJ/view?usp=drive_link |
| W4 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/19mgkwAnJDc7JuJy0zhhoY0ZC15DiNpxL8kchPDnRkRQ/edit?usp=sha |
| W4 | Claude Code | 其它外部 | https://www.anthropic.com/claude-code |
| W4 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1bv7Zozn6z45CAh-IyX99dMPMyXCHC7zj95UfwErBYQ8/edit?usp=sha |
| W5 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1Djd4eBLBbRkma8rFnJAWMT0ptct_UGB8hipmoqFVkxQ/edit?usp=sha |
| W5 | Warp | 其它外部 | https://www.warp.dev/ |
| W5 | Slides (Figma) | 其它外部 | https://www.figma.com/slides/kwbcmtqTFQMfUhiMH8BiEx/Warp---Stanford--Copy-?node-id=9-116&t=oBWBC |
| W6 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1C05bCLasMDigBbkwdWbiz4WrXibzi6ua4hQQbTod_8c/edit?usp=sha |
| W6 | Semgrep | 其它外部 | https://semgrep.dev/ |
| W7 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1Mfe-auWAsg9URCujneKnHr0AbO8O-_U4QXBVOlO4qp0/edit?usp=sha |
| W7 | Graphite | 其它外部 | https://graphite.dev/ |
| W7 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1NkPzpuSQt6Esbnr2-EnxM9007TL6ebSPFwITyVY-QxU/edit?usp=sha |
| W8 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1DWbxgR-uynKJxBR7E9E/edit?usp=sharing |
| W8 | Vercel | 其它外部 | https://vercel.com/ |
| W8 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1hwF-RIkOJ_OFy17BKhzFyCtxSS7Pcf7p/view?usp=drive_link |
| W9 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/1DWbxgR-uynKJxBR7E9E/edit?usp=sharing |
| W9 | Resolve | 其它外部 | https://resolve.ai/ |
| W9 | Slides | Google Slides/Drive | https://docs.google.com/presentation/d/11WnEbMGc9kny_WBpMN10I8oP8XsiQOnM/view?usp=sharing |
| W10 | a16z | 其它外部 | https://a16z.com/ |
| W10 | assignment calendar | Google Slides/Drive | https://docs.google.com/spreadsheets/d/1-485SLHw_zn7A-UXiz88Dgjy_qUGx87Am6HUwQrKsN8/edit?gid=0#g |
| W10 | themodernsoftware.dev | 其它外部 | https://themodernsoftware.dev/ |

### 2.2 视频字幕——**完全缺失**

大纲中的视频均为 YouTube 外链，**无任何字幕文件被获取**。
若要把视频字幕纳入覆盖范围，需额外的一手获取步骤（yt-dlp 等），
且需评估网络可达性与版权边界。**当前决定：不纳入分母，列为扩展范围。**

---

## 三、逐周工作单元清单

图例：`OK` 可用 ｜ `EMPTY` 0 字节 ｜ `PLACEHOLDER` 占位页 ｜ `LOW` 有文件但正文不足 ｜ `EXTERNAL` 外链

### Week 1：Introduction to Coding LLMs and AI Development ／ 编码 LLM 与 AI 开发导论

Topics：Course logistics、What is an LLM actually、How to prompt effectively

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| EXTERNAL | external/link | Deep Dive into LLMs | `https://www.youtube.com/watch?v=7xTGNNLPyMI` | — |
| EXTERNAL | external/link | AI Prompt Engineering: A Deep Dive | `https://www.youtube.com/watch?v=T9aRN5JkmL8` | — |
| **LOW** | local/html | Prompt Engineering Guide | `source/pages/prompt-engineering-guide.html` | 79 |
| OK | local/html | Prompt Engineering Overview | `source/pages/prompt-engineering-overview.html` | 3,678 |
| OK | local/pdf | How OpenAI Uses Codex | `source/pdfs/how-openai-uses-codex.pdf` | — |

### Week 2：The Anatomy of Coding Agents ／ 编码智能体的解剖学

Topics：Tool use and function calling、MCP (Model Context Protocol)

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| EXTERNAL | external/link | Sample MCP Server Implementations | `https://github.com/modelcontextprotocol/servers` | — |
| EXTERNAL | external/link | MCP Server SDK | `https://github.com/modelcontextprotocol/typescript-sdk/tree/main?tab=readme-ov-file#server` | — |
| OK | local/html | MCP Food-for-Thought | `source/pages/mcp-food-for-thought.html` | 728 |
| OK | local/html | MCP Introduction | `source/pages/mcp-introduction.html` | 4,721 |
| OK | local/html | MCP Registry | `source/pages/mcp-registry-preview.html` | 796 |
| OK | local/html | MCP Server Authentication | `source/pages/mcp-server-authentication.html` | 1,909 |

### Week 3：The AI IDE ／ AI IDE

Topics：Context management and code understanding、PRDs for agents、IDE integrations and extensions

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| EXTERNAL | external/link | Getting AI to Work In Complex Codebases | `https://github.com/humanlayer/advanced-context-engineering-for-coding-agents/blob/main/ace-fca.md` | — |
| EXTERNAL | external/link | How FAANG Vibe Codes | `https://x.com/rohanpaul_ai/status/1959414096589422619` | — |
| OK | local/html | Devin: Coding Agents 101 | `source/pages/devin-coding-agents-101.html` | 3,488 |
| OK | local/html | How Long Contexts Fail | `source/pages/how-long-contexts-fail.html` | 1,579 |
| OK | local/html | Specs Are the New Source Code | `source/pages/specs-are-the-new-source-code.html` | 1,914 |
| OK | local/html | Writing Effective Tools for Agents | `source/pages/writing-effective-tools-for-agents.html` | 3,254 |

### Week 4：Claude Code and Agentic Coding ／ Claude Code 与智能体编程

Topics：Claude Code architecture and internals、Agentic coding workflows、Context engineering for agents

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| EXTERNAL | external/link | Super Claude | `https://github.com/SuperClaude-Org/SuperClaude_Framework` | — |
| EXTERNAL | external/link | Awesome Claude Agents | `https://github.com/vijaythecoder/awesome-claude-agents` | — |
| OK | local/html | Claude Best Practices | `source/pages/claude-code-best-practices.html` | 1,487 |
| **LOW** | local/html | Good Context Good Code | `source/pages/good-context-good-code.html` | 4 |
| **PLACEHOLDER** | local/html | Peeking Under the Hood of Claude Code | `source/pages/peeking-under-the-hood-of-claude-code.html` | 44 |
| OK | local/pdf | How Anthropic Uses Claude Code | `source/pdfs/how-anthropic-uses-claude-code.pdf` | — |

### Week 5：Warp and the AI Terminal ／ Warp 与 AI 终端

Topics：AI-native terminal development、Agentic development workflows

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| EXTERNAL | external/link | Warp University | `https://www.warp.dev/university?slug=university` | — |
| **LOW** | local/html | How Warp Uses Warp to Build Warp | `source/pages/how-warp-uses-warp.html` | 1 |
| OK | local/html | Warp vs Claude Code | `source/pages/warp-vs-claude-code.html` | 615 |

### Week 6：AI Security and Vulnerability Detection ／ AI 安全与漏洞检测

Topics：Security testing (SAST vs DAST)、Prompt injection attacks、AI-assisted vulnerability detection、OWASP Top 10

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| EXTERNAL | external/link | Vulnerability Prompt Analysis with O3 | `https://github.com/SeanHeelan/o3_finds_cve-2025-37899/blob/master/system_prompt_uafs.prompt` | — |
| OK | local/html | Agentic AI Threats: Identity Spoofing and Im | `source/pages/agentic-ai-threats.html` | 7,901 |
| OK | local/html | Context Rot: Understanding Degradation in AI | `source/pages/context-rot.html` | 7,602 |
| OK | local/html | Copilot Remote Code Execution via Prompt Inj | `source/pages/copilot-prompt-injection-rce.html` | 1,240 |
| OK | local/html | Finding Vulnerabilities in Modern Web Apps U | `source/pages/finding-vulnerabilities-claude-codex.html` | 3,789 |
| OK | local/html | OWASP Top Ten: The Leading Web Application S | `source/pages/owasp-top-ten.html` | 2,311 |
| OK | local/html | SAST vs DAST | `source/pages/sast-vs-dast.html` | 2,943 |

### Week 7：AI-Powered Code Review ／ AI 驱动的代码评审

Topics：Code review best practices、AI-assisted code review、Automated review tooling

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| OK | local/html | AI Code Review Implementation Best Practices | `source/pages/ai-code-review-best-practices.html` | 1,901 |
| OK | local/html | Code Review Essentials for Software Teams | `source/pages/code-review-essentials.html` | 2,040 |
| OK | local/html | Code Reviews: Just Do It | `source/pages/code-reviews-just-do-it.html` | 1,010 |
| OK | local/html | How to Review Code Effectively | `source/pages/how-to-review-code-effectively.html` | 3,278 |
| **EMPTY** | local/html | Lessons from Millions of AI Code Reviews | `source/pages/lessons-from-ai-code-reviews.html` | — |
| OK | local/pdf | AI-Assisted Assessment of Coding Practices i | `source/pdfs/ai-assisted-code-review-assessment.pdf` | — |

### Week 8：Full-Stack AI Development and Deployment ／ 全栈 AI 开发与部署

Topics：Multi-stack web application development、AI-assisted deployment pipelines

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|

_（本周无 readings）_

### Week 9：SRE, Observability, and Agentic On-Call ／ SRE、可观测性与智能体值班

Topics：Site Reliability Engineering fundamentals、Observability and monitoring、AI agents in on-call engineering、Multi-agent systems

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| OK | local/html | Your New Autonomous Teammate / Benefits of A | `source/pages/benefits-agentic-ai-oncall.html` | 760 |
| OK | local/html | Kubernetes Troubleshooting with AI | `source/pages/kubernetes-troubleshooting-ai.html` | 1,221 |
| OK | local/html | Role of Multi Agent Systems in Making Softwa | `source/pages/multi-agent-systems-ai-native.html` | 1,439 |
| OK | local/html | Observability Basics You Should Know | `source/pages/observability-basics.html` | 1,699 |
| OK | local/html | Introduction to Site Reliability Engineering | `source/pages/sre-introduction.html` | 3,824 |

### Week 10：The Future of AI in Software Engineering ／ AI 在软件工程中的未来

Topics：Future trends in AI-assisted development、Industry perspectives and career implications、Final project presentations

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|

_（本周无 readings）_

