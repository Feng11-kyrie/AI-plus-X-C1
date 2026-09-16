# 术语一致率报告（TERMINOLOGY CONSISTENCY）

> 由 `pipeline/qc_terminology.py` 自动生成，**请勿手工编辑**。

## 检查范围

| 项 | 值 |
|---|---|
| 术语表条目 | 171 条（其中需翻译 148 条） |
| 审计译稿 | 26 条 |
| 硬性禁用变体 | 317 个 |
| 提示级变体 | 48 个（只统计不判违规） |

## 一致率

**口径**：一致率 = 正式译法出现次数 /（正式译法出现次数 + 硬性违规次数）

| 指标 | 数值 |
|---|---|
| 正式译法出现次数 | 3,162 |
| **硬性违规次数** | **0** |
| **术语一致率（硬性口径）** | **100.00%** |
| 提示级命中次数 | 399（**不计入一致率**，见第三节） |
| 实际用到的术语 | 121 条 |
| 其中零违规 | 121 条 |

> ⚠️ **这个百分比只统计硬性禁用变体。** 术语表另有一批提示级变体，它们是中文常用词或**其它英文词**的合法译法（如 proxy → 代理、dashboard → 控制台），一律判违规会逼出错误的译文。读数时请把两者一起看——**单看 100% 会高估实际的一致性**。

✅ **全部硬性禁用变体零出现。**

## 一、违规明细（硬性）

无。

## 二、覆盖率缺口（参考项，不作门禁）

源文中出现某术语，但译文中完全没有出现它的正式译法。

**为什么只作参考而不判违规**——这个检查的误报率偏高，已知至少三类：

1. **正式译法依上下文而变**：`Agentic` 的正式译法是「智能体化的」，但在 `Agentic AI` 里按术语表应译「智能体 AI」，于是「智能体化的」自然不出现——这不是漏译。
2. **英文术语被有意保留**：如 `prompt`、`diff` 在中文技术写作里常保留英文，这类确实值得人工看一眼，但不必然算错。
3. **词边界匹配的局限**：英文词可能出现在短语内部。

按本项目的原则——**天天误报的校验器最终会被忽略**——因此只列出、不拦截。

| 术语 | 应为 | 篇目 |
|---|---|---|
| Prompt | 提示词 | `claude-code-best-practices` |
| Context | 上下文 | `mcp-server-authentication` |
| Context | 上下文 | `specs-are-the-new-source-code` |
| Reasoning | 推理能力 | `ai-code-review-best-practices` |
| Reasoning | 推理能力 | `finding-vulnerabilities-claude-codex` |
| Reasoning | 推理能力 | `how-long-contexts-fail` |
| Reasoning | 推理能力 | `multi-agent-systems-ai-native` |
| Reasoning | 推理能力 | `prompt-engineering-overview` |
| Reasoning | 推理能力 | `writing-effective-tools-for-agents` |
| Agent | 智能体 | `ai-code-review-best-practices` |
| Agentic | 智能体化的 | `benefits-agentic-ai-oncall` |
| Agentic | 智能体化的 | `copilot-prompt-injection-rce` |
| Agentic | 智能体化的 | `finding-vulnerabilities-claude-codex` |
| Agentic | 智能体化的 | `how-anthropic-uses-claude-code` |
| Agentic | 智能体化的 | `how-long-contexts-fail` |
| Agentic | 智能体化的 | `kubernetes-troubleshooting-ai` |
| Agentic | 智能体化的 | `mcp-introduction` |
| Agentic | 智能体化的 | `multi-agent-systems-ai-native` |
| Agentic | 智能体化的 | `writing-effective-tools-for-agents` |
| Boilerplate | 样板代码 | `how-openai-uses-codex` |
| Test Coverage | 测试覆盖率 | `how-anthropic-uses-claude-code` |
| Deployment | 部署 | `copilot-prompt-injection-rce` |
| Artifact | 制品 | `specs-are-the-new-source-code` |
| Diff | 差异 | `claude-code-best-practices` |
| Diff | 差异 | `copilot-prompt-injection-rce` |
| Diff | 差异 | `how-to-review-code-effectively` |
| Specification (Spec) | 规格说明 | `code-review-essentials` |
| Specification (Spec) | 规格说明 | `observability-basics` |
| Backlog | 待办列表 | `how-anthropic-uses-claude-code` |
| Exploit | 漏洞利用 | `finding-vulnerabilities-claude-codex` |
| Exploit | 漏洞利用 | `sast-vs-dast` |
| OWASP Top 10 | OWASP Top 10（OWASP 十大安全风险） | `owasp-top-ten` |
| False Positive | 误报 | `finding-vulnerabilities-claude-codex` |
| False Negative | 漏报 | `finding-vulnerabilities-claude-codex` |
| Triage | 分级处置 | `multi-agent-systems-ai-native` |
| Tracing | 链路追踪 | `how-openai-uses-codex` |
| Tracing | 链路追踪 | `sast-vs-dast` |
| Tracing | 链路追踪 | `writing-effective-tools-for-agents` |
| Trace | 追踪记录 | `finding-vulnerabilities-claude-codex` |
| Trace | 追踪记录 | `how-anthropic-uses-claude-code` |
| Trace | 追踪记录 | `how-openai-uses-codex` |
| Log | 日志 | `mcp-registry-preview` |
| Log | 日志 | `mcp-server-authentication` |
| Dashboard | 仪表盘 | `mcp-server-authentication` |
| Incident | 故障事件 | `how-to-review-code-effectively` |
| Incident | 故障事件 | `kubernetes-troubleshooting-ai` |

## 三、提示级变体（仅统计）

这些变体只统计、不判违规。原因是本检查的一项**结构性局限**：

> **校验器只看中文输出，无法知道某个中文词对应的是哪个英文词。**

于是凡是「本术语的错误译法」同时又是「**邻近英文词的正确译法**」的词，都会被误判。实测中反复出现的例子：

| 提示级变体 | 它其实对应的英文 | 属于哪个术语的禁用变体 |
|---|---|---|
| 代理 | proxy | Agent（智能体） |
| 控制台 | dashboard / console | Terminal（终端） |
| 轨迹 | trail | Trace（追踪记录） |
| 弱点 | weakness | Vulnerability（漏洞） |
| 开发周期 | development cycle | SDLC（软件开发生命周期） |
| 相关方 | party / parties | Stakeholder（干系人） |
| 数据泄露 | data leak | Data Exfiltration（数据外泄） |
| 度量 | measure（动词） | Metric（指标） |

彻底解决需要把译文与源文按句对齐，再判断每个中文词对应哪个英文词——那会把校验器复杂化一个数量级，且对齐本身也会出错。

**当前选择：接受一定误报，维持「人判断规则对不对、机器判断符合不符合规则」的分工。**
代价是硬性一致率这个数字只覆盖「无歧义错译」，读数时必须与下面的提示级命中合看。

| 术语 | 变体 | 篇目 | 次数 |
|---|---|---|---|
| Context Window | 上下文长度 | `writing-effective-tools-for-agents` | 1 |
| Scaffolding | 框架 | `ai-code-review-best-practices` | 1 |
| Scaffolding | 框架 | `devin-coding-agents-101` | 1 |
| Scaffolding | 框架 | `finding-vulnerabilities-claude-codex` | 5 |
| Scaffolding | 框架 | `how-anthropic-uses-claude-code` | 2 |
| Scaffolding | 框架 | `how-to-review-code-effectively` | 1 |
| Scaffolding | 框架 | `mcp-introduction` | 11 |
| Scaffolding | 框架 | `multi-agent-systems-ai-native` | 2 |
| Scaffolding | 框架 | `observability-basics` | 5 |
| Scaffolding | 框架 | `sast-vs-dast` | 3 |
| Scaffolding | 框架 | `sre-introduction` | 1 |
| Hallucination | 框架 | `ai-code-review-best-practices` | 1 |
| Hallucination | 框架 | `devin-coding-agents-101` | 1 |
| Hallucination | 框架 | `finding-vulnerabilities-claude-codex` | 5 |
| Hallucination | 框架 | `how-anthropic-uses-claude-code` | 2 |
| Hallucination | 框架 | `how-to-review-code-effectively` | 1 |
| Hallucination | 框架 | `mcp-introduction` | 11 |
| Hallucination | 框架 | `multi-agent-systems-ai-native` | 2 |
| Hallucination | 框架 | `observability-basics` | 5 |
| Hallucination | 框架 | `sast-vs-dast` | 3 |
| Hallucination | 框架 | `sre-introduction` | 1 |
| Retrieval-Augmented Generation (RAG) | 落地 | `ai-code-review-best-practices` | 10 |
| Retrieval-Augmented Generation (RAG) | 落地 | `mcp-introduction` | 1 |
| Retrieval-Augmented Generation (RAG) | 落地 | `mcp-registry-preview` | 2 |
| Retrieval-Augmented Generation (RAG) | 落地 | `observability-basics` | 2 |
| Retrieval-Augmented Generation (RAG) | 落地 | `sast-vs-dast` | 1 |
| Retrieval-Augmented Generation (RAG) | 落地 | `specs-are-the-new-source-code` | 2 |
| Retrieval-Augmented Generation (RAG) | 落地 | `sre-introduction` | 1 |
| Inference | 推演 | `code-review-essentials` | 1 |
| Inference | 推演 | `how-anthropic-uses-claude-code` | 1 |
| Inference | 推断 | `how-openai-uses-codex` | 1 |
| Inference | 推断 | `multi-agent-systems-ai-native` | 1 |
| Training | 培训 | `ai-code-review-best-practices` | 1 |
| Training | 培训 | `prompt-engineering-overview` | 1 |
| Agent | 代理 | `mcp-server-authentication` | 2 |
| Tool Use | 工具使用 | `how-long-contexts-fail` | 1 |
| Tool Use | 调用工具 | `mcp-food-for-thought` | 1 |
| Tool Use | 调用工具 | `mcp-introduction` | 2 |
| Tool Use | 调用工具 | `mcp-server-authentication` | 3 |
| Tool Use | 工具使用 | `writing-effective-tools-for-agents` | 2 |
| Tool Use | 调用工具 | `writing-effective-tools-for-agents` | 1 |
| Model Context Protocol (MCP) | 组织 | `ai-code-review-best-practices` | 2 |
| Model Context Protocol (MCP) | 组织 | `benefits-agentic-ai-oncall` | 1 |
| Model Context Protocol (MCP) | 组织 | `code-review-essentials` | 1 |
| Model Context Protocol (MCP) | 组织 | `code-reviews-just-do-it` | 1 |
| Model Context Protocol (MCP) | 组织 | `devin-coding-agents-101` | 1 |
| Model Context Protocol (MCP) | 组织 | `how-anthropic-uses-claude-code` | 4 |
| Model Context Protocol (MCP) | 协调 | `how-anthropic-uses-claude-code` | 3 |
| Model Context Protocol (MCP) | 协调 | `how-long-contexts-fail` | 1 |
| Model Context Protocol (MCP) | 组织 | `how-openai-uses-codex` | 2 |
| Model Context Protocol (MCP) | 组织 | `how-to-review-code-effectively` | 2 |
| Model Context Protocol (MCP) | 协调 | `kubernetes-troubleshooting-ai` | 1 |
| Model Context Protocol (MCP) | 组织 | `mcp-introduction` | 2 |
| Model Context Protocol (MCP) | 组织 | `mcp-registry-preview` | 2 |
| Model Context Protocol (MCP) | 组织 | `owasp-top-ten` | 3 |
| Model Context Protocol (MCP) | 协调 | `owasp-top-ten` | 1 |
| Model Context Protocol (MCP) | 组织 | `sast-vs-dast` | 3 |
| Model Context Protocol (MCP) | 组织 | `sre-introduction` | 3 |
| Orchestration | 组织 | `ai-code-review-best-practices` | 2 |
| Orchestration | 组织 | `benefits-agentic-ai-oncall` | 1 |
| Orchestration | 组织 | `code-review-essentials` | 1 |
| Orchestration | 组织 | `code-reviews-just-do-it` | 1 |
| Orchestration | 组织 | `devin-coding-agents-101` | 1 |
| Orchestration | 组织 | `how-anthropic-uses-claude-code` | 4 |
| Orchestration | 协调 | `how-anthropic-uses-claude-code` | 3 |
| Orchestration | 协调 | `how-long-contexts-fail` | 1 |
| Orchestration | 组织 | `how-openai-uses-codex` | 2 |
| Orchestration | 组织 | `how-to-review-code-effectively` | 2 |
| Orchestration | 协调 | `kubernetes-troubleshooting-ai` | 1 |
| Orchestration | 组织 | `mcp-introduction` | 2 |
| Orchestration | 组织 | `mcp-registry-preview` | 2 |
| Orchestration | 组织 | `owasp-top-ten` | 3 |
| Orchestration | 协调 | `owasp-top-ten` | 1 |
| Orchestration | 组织 | `sast-vs-dast` | 3 |
| Orchestration | 组织 | `sre-introduction` | 3 |
| Workflow | 流程 | `ai-code-review-best-practices` | 2 |
| Workflow | 流程 | `code-review-essentials` | 3 |
| Workflow | 流程 | `devin-coding-agents-101` | 4 |
| Workflow | 流程 | `finding-vulnerabilities-claude-codex` | 4 |
| Workflow | 流程 | `how-anthropic-uses-claude-code` | 5 |
| Workflow | 流程 | `how-openai-uses-codex` | 3 |
| Workflow | 流程 | `how-to-review-code-effectively` | 4 |
| Workflow | 流程 | `mcp-introduction` | 8 |
| Workflow | 流程 | `mcp-server-authentication` | 1 |
| Workflow | 流程 | `multi-agent-systems-ai-native` | 1 |
| Workflow | 流程 | `observability-basics` | 1 |
| Workflow | 流程 | `owasp-top-ten` | 2 |
| Workflow | 流程 | `sast-vs-dast` | 3 |
| Workflow | 流程 | `specs-are-the-new-source-code` | 5 |
| Workflow | 流程 | `sre-introduction` | 1 |
| Workflow | 流程 | `writing-effective-tools-for-agents` | 1 |
| Human-in-the-loop | 人工介入 | `how-anthropic-uses-claude-code` | 1 |
| Human-in-the-loop | 人工介入 | `sre-introduction` | 1 |
| Refactor | 重写 | `code-review-essentials` | 2 |
| Refactor | 重写 | `how-openai-uses-codex` | 1 |
| Refactor | 重写 | `prompt-engineering-overview` | 1 |
| Linter | 检查器 | `devin-coding-agents-101` | 1 |
| Rollback | 回退 | `how-anthropic-uses-claude-code` | 2 |
| Artifact | 产物 | `specs-are-the-new-source-code` | 4 |
| Artifact | 产物 | `sre-introduction` | 1 |
| Terminal | 控制台 | `mcp-server-authentication` | 1 |
| Runtime | 运行环境 | `sast-vs-dast` | 1 |
| Rate Limit | 限流 | `kubernetes-troubleshooting-ai` | 1 |
| Codebase Understanding | 代码理解 | `ai-code-review-best-practices` | 1 |
| Codebase Understanding | 代码理解 | `how-openai-uses-codex` | 3 |
| Specification (Spec) | 规范 | `ai-code-review-best-practices` | 3 |
| Specification (Spec) | 规范 | `claude-code-best-practices` | 1 |
| Specification (Spec) | 规范 | `observability-basics` | 1 |
| Specification (Spec) | 规范 | `owasp-top-ten` | 4 |
| Software Development Life Cycle (SDLC) | 开发周期 | `how-anthropic-uses-claude-code` | 1 |
| Software Development Life Cycle (SDLC) | 开发周期 | `how-openai-uses-codex` | 1 |
| Design Doc | 设计稿 | `devin-coding-agents-101` | 1 |
| Design Doc | 设计稿 | `how-anthropic-uses-claude-code` | 4 |
| Stakeholder | 相关方 | `code-review-essentials` | 1 |
| Deliverable | 产出物 | `specs-are-the-new-source-code` | 1 |
| Vulnerability | 缺陷 | `ai-code-review-best-practices` | 1 |
| Vulnerability | 缺陷 | `code-review-essentials` | 2 |
| Vulnerability | 缺陷 | `code-reviews-just-do-it` | 4 |
| Vulnerability | 缺陷 | `copilot-prompt-injection-rce` | 2 |
| Vulnerability | 缺陷 | `finding-vulnerabilities-claude-codex` | 2 |
| Vulnerability | 弱点 | `finding-vulnerabilities-claude-codex` | 1 |
| Vulnerability | 缺陷 | `sast-vs-dast` | 9 |
| Vulnerability | 弱点 | `sast-vs-dast` | 3 |
| Vulnerability | 缺陷 | `sre-introduction` | 1 |
| False Positive | 假阳性 | `finding-vulnerabilities-claude-codex` | 11 |
| False Negative | 假阴性 | `finding-vulnerabilities-claude-codex` | 5 |
| Data Exfiltration | 数据泄露 | `sast-vs-dast` | 1 |
| Blast Radius | 影响范围 | `copilot-prompt-injection-rce` | 1 |
| Observability | 运行环境 | `sast-vs-dast` | 1 |
| Tracing | 跟踪 | `copilot-prompt-injection-rce` | 1 |
| Tracing | 跟踪 | `how-anthropic-uses-claude-code` | 1 |
| Tracing | 跟踪 | `how-to-review-code-effectively` | 1 |
| Tracing | 跟踪 | `observability-basics` | 1 |
| Tracing | 跟踪 | `sast-vs-dast` | 1 |
| Tracing | 跟踪 | `sre-introduction` | 2 |
| Tracing | 跟踪 | `writing-effective-tools-for-agents` | 1 |
| Trace | 轨迹 | `observability-basics` | 1 |
| Metric | 度量 | `finding-vulnerabilities-claude-codex` | 4 |
| Metric | 度量 | `observability-basics` | 1 |
| Metric | 度量 | `sre-introduction` | 2 |
| Metric | 度量 | `writing-effective-tools-for-agents` | 3 |
| Log | 记录 | `ai-code-review-best-practices` | 1 |
| Log | 记录 | `benefits-agentic-ai-oncall` | 1 |
| Log | 记录 | `how-anthropic-uses-claude-code` | 3 |
| Log | 记录 | `how-long-contexts-fail` | 1 |
| Log | 记录 | `how-openai-uses-codex` | 2 |
| Log | 记录 | `how-to-review-code-effectively` | 1 |
| Log | 记录 | `mcp-food-for-thought` | 6 |
| Log | 记录 | `multi-agent-systems-ai-native` | 1 |
| Log | 记录 | `observability-basics` | 31 |
| Log | 记录 | `owasp-top-ten` | 3 |
| Log | 记录 | `sre-introduction` | 2 |
| Log | 记录 | `writing-effective-tools-for-agents` | 4 |
| Dashboard | 看板 | `how-to-review-code-effectively` | 1 |
| Runbook | 操作手册 | `sre-introduction` | 4 |
| Mean Time To Recovery (MTTR) | 平均修复时间 | `sre-introduction` | 1 |
| Grounding | 落地 | `ai-code-review-best-practices` | 10 |
| Grounding | 落地 | `mcp-introduction` | 1 |
| Grounding | 落地 | `mcp-registry-preview` | 2 |
| Grounding | 落地 | `observability-basics` | 2 |
| Grounding | 落地 | `sast-vs-dast` | 1 |
| Grounding | 落地 | `specs-are-the-new-source-code` | 2 |
| Grounding | 落地 | `sre-introduction` | 1 |

## 四、逐术语统计

| 术语 | 正式译法 | policy | 出现次数 | 源文篇数 | 违规 |
|---|---|---|---|---|---|
| Agent | 智能体 | `translate` | 356 | 16 | ✅ |
| Model Context Protocol (MCP) | 模型上下文协议（MCP） | `acronym` | 323 | 5 | ✅ |
| Context | 上下文 | `translate` | 206 | 20 | ✅ |
| Prompt | 提示词 | `translate` | 156 | 12 | ✅ |
| Pull Request (PR) | 拉取请求（PR） | `acronym` | 122 | 7 | ✅ |
| Vulnerability | 漏洞 | `translate` | 114 | 4 | ✅ |
| MCP Server | MCP 服务器 | `keep_en_first` | 106 | 8 | ✅ |
| Application Programming Interface (API) | 应用程序接口（API） | `acronym` | 106 | 0 | ✅ |
| Code Review | 代码评审 | `translate` | 100 | 9 | ✅ |
| Workflow | 工作流 | `translate` | 90 | 7 | ✅ |
| Site Reliability Engineering (SRE) | 站点可靠性工程（SRE） | `acronym` | 71 | 1 | ✅ |
| Codebase | 代码库 | `translate` | 67 | 11 | ✅ |
| Static Application Security Testing (SAST) | 静态应用安全测试（SAST） | `acronym` | 67 | 1 | ✅ |
| Large Language Model (LLM) | 大语言模型（LLM） | `acronym` | 64 | 0 | ✅ |
| Evaluation | 评估 | `translate` | 58 | 3 | ✅ |
| Deployment | 部署 | `translate` | 58 | 10 | ✅ |
| Dynamic Application Security Testing (DAST) | 动态应用安全测试（DAST） | `acronym` | 54 | 1 | ✅ |
| Dependency | 依赖 | `translate` | 43 | 8 | ✅ |
| Inference | 推理 | `translate` | 36 | 1 | ✅ |
| Terminal | 终端 | `translate` | 36 | 4 | ✅ |
| Log | 日志 | `translate` | 34 | 8 | ✅ |
| Commit | 提交 | `translate` | 33 | 5 | ✅ |
| Trace | 追踪记录 | `translate` | 30 | 4 | ✅ |
| Tool Use | 工具调用 | `translate` | 28 | 1 | ✅ |
| Metric | 指标 | `translate` | 28 | 2 | ✅ |
| Prompt Engineering | 提示词工程 | `translate` | 27 | 5 | ✅ |
| Repository | 仓库 | `translate` | 27 | 7 | ✅ |
| Merge | 合并 | `translate` | 27 | 5 | ✅ |
| Alert | 告警 | `translate` | 25 | 4 | ✅ |
| Continuous Integration (CI) | 持续集成（CI） | `acronym` | 24 | 2 | ✅ |
| Training | 训练 | `translate` | 22 | 7 | ✅ |
| Runtime Application Self-Protection (RASP) | 运行时应用自保护（RASP） | `acronym` | 22 | 1 | ✅ |
| Tracing | 链路追踪 | `translate` | 22 | 4 | ✅ |
| Runtime | 运行时 | `translate` | 21 | 4 | ✅ |
| On-call | 值班 | `translate` | 21 | 4 | ✅ |
| Refactor | 重构 | `translate` | 19 | 5 | ✅ |
| Observability | 可观测性 | `translate` | 19 | 6 | ✅ |
| Command-Line Interface (CLI) | 命令行界面（CLI） | `acronym` | 17 | 0 | ✅ |
| Specification (Spec) | 规格说明 | `translate` | 17 | 6 | ✅ |
| Coding Agent | 编码智能体 | `translate` | 16 | 2 | ✅ |
| Common Weakness Enumeration (CWE) | 通用缺陷枚举（CWE） | `acronym` | 15 | 0 | ✅ |
| Incident | 故障事件 | `translate` | 15 | 6 | ✅ |
| Continuous Delivery (CD) | 持续交付（CD） | `acronym` | 14 | 0 | ✅ |
| Software Development Kit (SDK) | 软件开发工具包（SDK） | `acronym` | 14 | 0 | ✅ |
| True Positive Rate (TPR) | 真阳性率（TPR） | `acronym` | 14 | 1 | ✅ |
| Branch | 分支 | `translate` | 13 | 4 | ✅ |
| Unit Test | 单元测试 | `translate` | 13 | 1 | ✅ |
| Diff | 差异 | `translate` | 13 | 3 | ✅ |
| Software Development Life Cycle (SDLC) | 软件开发生命周期（SDLC） | `acronym` | 13 | 1 | ✅ |
| Insecure Direct Object Reference (IDOR) | 不安全的直接对象引用（IDOR） | `acronym` | 13 | 1 | ✅ |
| SQL Injection | SQL 注入 | `translate` | 13 | 2 | ✅ |
| False Positive | 误报 | `translate` | 13 | 2 | ✅ |
| Dashboard | 仪表盘 | `translate` | 13 | 2 | ✅ |
| Context Window | 上下文窗口 | `translate` | 12 | 3 | ✅ |
| Multi-agent | 多智能体 | `translate` | 12 | 2 | ✅ |
| Function Calling | 函数调用 | `translate` | 12 | 1 | ✅ |
| Orchestration | 编排 | `translate` | 12 | 4 | ✅ |
| Cross-Site Scripting (XSS) | 跨站脚本攻击（XSS） | `acronym` | 11 | 1 | ✅ |
| False Positive Rate (FPR) | 假阳性率（FPR） | `acronym` | 10 | 1 | ✅ |
| Benchmark | 基准测试 | `translate` | 9 | 2 | ✅ |
| Integrated Development Environment (IDE) | 集成开发环境（IDE） | `acronym` | 9 | 0 | ✅ |
| Prompt Injection | 提示词注入 | `translate` | 8 | 1 | ✅ |
| Triage | 分级处置 | `translate` | 8 | 5 | ✅ |
| Telemetry | 遥测 | `translate` | 8 | 3 | ✅ |
| Capacity Planning | 容量规划 | `translate` | 7 | 1 | ✅ |
| Hallucination | 幻觉 | `translate` | 6 | 1 | ✅ |
| Fine-tuning | 微调 | `translate` | 6 | 1 | ✅ |
| Chain of Thought | 思维链 | `translate` | 6 | 1 | ✅ |
| Embedding | 嵌入 | `translate` | 6 | 0 | ✅ |
| Credential | 凭据 | `translate` | 6 | 0 | ✅ |
| Alert Fatigue | 告警疲劳 | `translate` | 6 | 2 | ✅ |
| Runbook | 运维手册 | `translate` | 6 | 0 | ✅ |
| Mean Time To Recovery (MTTR) | 平均恢复时间（MTTR） | `acronym` | 6 | 1 | ✅ |
| Test Coverage | 测试覆盖率 | `translate` | 5 | 3 | ✅ |
| System Prompt | 系统提示词 | `translate` | 4 | 3 | ✅ |
| Zero-shot | 零样本 | `translate` | 4 | 1 | ✅ |
| Rollback | 回滚 | `translate` | 4 | 1 | ✅ |
| Latency | 延迟 | `translate` | 4 | 2 | ✅ |
| Common Vulnerabilities and Exposures (CVE) | 通用漏洞披露（CVE） | `acronym` | 4 | 0 | ✅ |
| Server-Side Request Forgery (SSRF) | 服务端请求伪造（SSRF） | `acronym` | 4 | 0 | ✅ |
| Postmortem | 事后复盘 | `translate` | 4 | 1 | ✅ |
| Context Rot | 上下文腐化 | `translate` | 3 | 1 | ✅ |
| Retrieval-Augmented Generation (RAG) | 检索增强生成（RAG） | `acronym` | 3 | 0 | ✅ |
| Design Doc | 设计文档 | `translate` | 3 | 1 | ✅ |
| Minimum Viable Product (MVP) | 最小可行产品（MVP） | `acronym` | 3 | 0 | ✅ |
| Exploit | 漏洞利用 | `translate` | 3 | 3 | ✅ |
| False Negative | 漏报 | `translate` | 3 | 1 | ✅ |
| Context Engineering | 上下文工程 | `translate` | 2 | 1 | ✅ |
| Vibe Coding | 氛围编程 | `keep_en_first` | 2 | 0 | ✅ |
| Scaffolding | 脚手架 | `translate` | 2 | 1 | ✅ |
| Few-shot | 少样本 | `translate` | 2 | 1 | ✅ |
| Reasoning | 推理能力 | `translate` | 2 | 7 | ✅ |
| Guardrails | 护栏 | `translate` | 2 | 1 | ✅ |
| Agentic | 智能体化的 | `translate` | 2 | 10 | ✅ |
| Sub-agent | 子智能体 | `translate` | 2 | 0 | ✅ |
| Autonomy | 自主性 | `translate` | 2 | 1 | ✅ |
| Agent Loop | 智能体循环 | `translate` | 2 | 0 | ✅ |
| Technical Debt | 技术债 | `translate` | 2 | 1 | ✅ |
| Linter | 代码检查工具 | `translate` | 2 | 0 | ✅ |
| Integration Test | 集成测试 | `translate` | 2 | 0 | ✅ |
| Regression | 回归 | `translate` | 2 | 0 | ✅ |
| Sandbox | 沙箱 | `translate` | 2 | 1 | ✅ |
| Spec-Driven Development | 规格驱动开发 | `translate` | 2 | 1 | ✅ |
| Product Requirements Document (PRD) | 产品需求文档（PRD） | `acronym` | 2 | 0 | ✅ |
| Deliverable | 交付物 | `translate` | 2 | 1 | ✅ |
| Backlog | 待办列表 | `translate` | 2 | 2 | ✅ |
| Remote Code Execution (RCE) | 远程代码执行（RCE） | `acronym` | 2 | 1 | ✅ |
| Attack Surface | 攻击面 | `translate` | 2 | 0 | ✅ |
| Service Level Objective (SLO) | 服务等级目标（SLO） | `acronym` | 2 | 0 | ✅ |
| Root Cause Analysis (RCA) | 根因分析（RCA） | `acronym` | 2 | 2 | ✅ |
| Human-in-the-loop | 人在回路 | `translate` | 1 | 1 | ✅ |
| Boilerplate | 样板代码 | `translate` | 1 | 2 | ✅ |
| Stakeholder | 干系人 | `translate` | 1 | 0 | ✅ |
| Acceptance Criteria | 验收标准 | `translate` | 1 | 1 | ✅ |
| Dogfooding | 自产自用 | `translate` | 1 | 1 | ✅ |
| Red Team | 红队 | `translate` | 1 | 0 | ✅ |
| Service Level Agreement (SLA) | 服务等级协议（SLA） | `acronym` | 1 | 0 | ✅ |
| Toil | 琐务 | `translate` | 1 | 1 | ✅ |
| Blameless | 无指责的 | `translate` | 1 | 0 | ✅ |
| Autoremediation | 自动修复 | `translate` | 1 | 0 | ✅ |
| Threat Modeling | 威胁建模 | `translate` | 1 | 1 | ✅ |
| Artifact | 制品 | `translate` | 0 | 1 | ✅ |
| OWASP Top 10 | OWASP Top 10（OWASP 十大安全风险） | `keep_en_first` | 0 | 1 | ✅ |

