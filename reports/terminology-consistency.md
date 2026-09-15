# 术语一致率报告（TERMINOLOGY CONSISTENCY）

> 由 `pipeline/qc_terminology.py` 自动生成，**请勿手工编辑**。

## 检查范围

| 项 | 值 |
|---|---|
| 术语表条目 | 171 条（其中需翻译 148 条） |
| 审计译稿 | 13 条 |
| 硬性禁用变体 | 338 个 |
| 提示级变体 | 27 个（只统计不判违规） |

## 一致率

**口径**：一致率 = 正式译法出现次数 /（正式译法出现次数 + 硬性违规次数）

| 指标 | 数值 |
|---|---|
| 正式译法出现次数 | 1,118 |
| **硬性违规次数** | **0** |
| **术语一致率（硬性口径）** | **100.00%** |
| 提示级命中次数 | 135（**不计入一致率**，见第三节） |
| 实际用到的术语 | 84 条 |
| 其中零违规 | 84 条 |

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
| Reasoning | 推理能力 | `ai-code-review-best-practices` |
| Reasoning | 推理能力 | `how-long-contexts-fail` |
| Reasoning | 推理能力 | `multi-agent-systems-ai-native` |
| Agent | 智能体 | `ai-code-review-best-practices` |
| Agentic | 智能体化的 | `benefits-agentic-ai-oncall` |
| Agentic | 智能体化的 | `copilot-prompt-injection-rce` |
| Agentic | 智能体化的 | `how-long-contexts-fail` |
| Agentic | 智能体化的 | `kubernetes-troubleshooting-ai` |
| Agentic | 智能体化的 | `multi-agent-systems-ai-native` |
| Deployment | 部署 | `copilot-prompt-injection-rce` |
| Diff | 差异 | `claude-code-best-practices` |
| Diff | 差异 | `copilot-prompt-injection-rce` |
| Specification (Spec) | 规格说明 | `observability-basics` |
| Triage | 分级处置 | `multi-agent-systems-ai-native` |
| Log | 日志 | `mcp-registry-preview` |
| Log | 日志 | `mcp-server-authentication` |
| Dashboard | 仪表盘 | `mcp-server-authentication` |
| Incident | 故障事件 | `kubernetes-troubleshooting-ai` |

## 三、提示级变体（仅统计）

这些变体在中文里本身是常用词，或是**另一个英文词**的合法译法，因此只统计、不判违规。例如 `proxy` 的标准译法就是「代理」，而「代理」是 Agent 的提示级变体。

| 术语 | 变体 | 篇目 | 次数 |
|---|---|---|---|
| Scaffolding | 框架 | `ai-code-review-best-practices` | 1 |
| Scaffolding | 框架 | `multi-agent-systems-ai-native` | 2 |
| Scaffolding | 框架 | `observability-basics` | 5 |
| Hallucination | 框架 | `ai-code-review-best-practices` | 1 |
| Hallucination | 框架 | `multi-agent-systems-ai-native` | 2 |
| Hallucination | 框架 | `observability-basics` | 5 |
| Retrieval-Augmented Generation (RAG) | 落地 | `ai-code-review-best-practices` | 10 |
| Retrieval-Augmented Generation (RAG) | 落地 | `mcp-registry-preview` | 2 |
| Retrieval-Augmented Generation (RAG) | 落地 | `observability-basics` | 2 |
| Inference | 推断 | `multi-agent-systems-ai-native` | 1 |
| Training | 培训 | `ai-code-review-best-practices` | 1 |
| Agent | 代理 | `mcp-server-authentication` | 2 |
| Tool Use | 工具使用 | `how-long-contexts-fail` | 1 |
| Tool Use | 调用工具 | `mcp-food-for-thought` | 1 |
| Tool Use | 调用工具 | `mcp-server-authentication` | 3 |
| Model Context Protocol (MCP) | 组织 | `ai-code-review-best-practices` | 2 |
| Model Context Protocol (MCP) | 组织 | `benefits-agentic-ai-oncall` | 1 |
| Model Context Protocol (MCP) | 组织 | `code-reviews-just-do-it` | 1 |
| Model Context Protocol (MCP) | 协调 | `how-long-contexts-fail` | 1 |
| Model Context Protocol (MCP) | 协调 | `kubernetes-troubleshooting-ai` | 1 |
| Model Context Protocol (MCP) | 组织 | `mcp-registry-preview` | 2 |
| Orchestration | 组织 | `ai-code-review-best-practices` | 2 |
| Orchestration | 组织 | `benefits-agentic-ai-oncall` | 1 |
| Orchestration | 组织 | `code-reviews-just-do-it` | 1 |
| Orchestration | 协调 | `how-long-contexts-fail` | 1 |
| Orchestration | 协调 | `kubernetes-troubleshooting-ai` | 1 |
| Orchestration | 组织 | `mcp-registry-preview` | 2 |
| Workflow | 流程 | `ai-code-review-best-practices` | 2 |
| Workflow | 流程 | `mcp-server-authentication` | 1 |
| Workflow | 流程 | `multi-agent-systems-ai-native` | 1 |
| Workflow | 流程 | `observability-basics` | 1 |
| Terminal | 控制台 | `mcp-server-authentication` | 1 |
| Rate Limit | 限流 | `kubernetes-troubleshooting-ai` | 1 |
| Codebase Understanding | 代码理解 | `ai-code-review-best-practices` | 1 |
| Specification (Spec) | 规范 | `ai-code-review-best-practices` | 3 |
| Specification (Spec) | 规范 | `claude-code-best-practices` | 1 |
| Specification (Spec) | 规范 | `observability-basics` | 1 |
| Vulnerability | 缺陷 | `ai-code-review-best-practices` | 1 |
| Vulnerability | 缺陷 | `code-reviews-just-do-it` | 4 |
| Vulnerability | 缺陷 | `copilot-prompt-injection-rce` | 2 |
| Blast Radius | 影响范围 | `copilot-prompt-injection-rce` | 1 |
| Tracing | 跟踪 | `copilot-prompt-injection-rce` | 1 |
| Tracing | 跟踪 | `observability-basics` | 1 |
| Trace | 轨迹 | `observability-basics` | 1 |
| Metric | 度量 | `observability-basics` | 1 |
| Log | 记录 | `ai-code-review-best-practices` | 1 |
| Log | 记录 | `benefits-agentic-ai-oncall` | 1 |
| Log | 记录 | `how-long-contexts-fail` | 1 |
| Log | 记录 | `mcp-food-for-thought` | 6 |
| Log | 记录 | `multi-agent-systems-ai-native` | 1 |
| Log | 记录 | `observability-basics` | 31 |
| Grounding | 落地 | `ai-code-review-best-practices` | 10 |
| Grounding | 落地 | `mcp-registry-preview` | 2 |
| Grounding | 落地 | `observability-basics` | 2 |

## 四、逐术语统计

| 术语 | 正式译法 | policy | 出现次数 | 源文篇数 | 违规 |
|---|---|---|---|---|---|
| Agent | 智能体 | `translate` | 152 | 10 | ✅ |
| Model Context Protocol (MCP) | 模型上下文协议（MCP） | `acronym` | 135 | 3 | ✅ |
| Context | 上下文 | `translate` | 119 | 11 | ✅ |
| MCP Server | MCP 服务器 | `keep_en_first` | 59 | 4 | ✅ |
| Code Review | 代码评审 | `translate` | 56 | 5 | ✅ |
| Terminal | 终端 | `translate` | 35 | 4 | ✅ |
| Workflow | 工作流 | `translate` | 32 | 4 | ✅ |
| Application Programming Interface (API) | 应用程序接口（API） | `acronym` | 31 | 0 | ✅ |
| Trace | 追踪记录 | `translate` | 30 | 1 | ✅ |
| Deployment | 部署 | `translate` | 27 | 5 | ✅ |
| Log | 日志 | `translate` | 25 | 6 | ✅ |
| Metric | 指标 | `translate` | 24 | 1 | ✅ |
| Prompt | 提示词 | `translate` | 22 | 4 | ✅ |
| Tracing | 链路追踪 | `translate` | 22 | 1 | ✅ |
| Observability | 可观测性 | `translate` | 18 | 5 | ✅ |
| Pull Request (PR) | 拉取请求（PR） | `acronym` | 16 | 2 | ✅ |
| Dependency | 依赖 | `translate` | 16 | 4 | ✅ |
| Alert | 告警 | `translate` | 15 | 2 | ✅ |
| Large Language Model (LLM) | 大语言模型（LLM） | `acronym` | 13 | 0 | ✅ |
| Orchestration | 编排 | `translate` | 12 | 4 | ✅ |
| Context Window | 上下文窗口 | `translate` | 11 | 2 | ✅ |
| Repository | 仓库 | `translate` | 11 | 3 | ✅ |
| Vulnerability | 漏洞 | `translate` | 11 | 2 | ✅ |
| Multi-agent | 多智能体 | `translate` | 10 | 2 | ✅ |
| Codebase | 代码库 | `translate` | 10 | 3 | ✅ |
| Command-Line Interface (CLI) | 命令行界面（CLI） | `acronym` | 10 | 0 | ✅ |
| Evaluation | 评估 | `translate` | 9 | 1 | ✅ |
| Tool Use | 工具调用 | `translate` | 9 | 0 | ✅ |
| Site Reliability Engineering (SRE) | 站点可靠性工程（SRE） | `acronym` | 9 | 0 | ✅ |
| Continuous Integration (CI) | 持续集成（CI） | `acronym` | 8 | 0 | ✅ |
| Software Development Kit (SDK) | 软件开发工具包（SDK） | `acronym` | 8 | 0 | ✅ |
| Prompt Injection | 提示词注入 | `translate` | 8 | 1 | ✅ |
| Incident | 故障事件 | `translate` | 8 | 3 | ✅ |
| Inference | 推理 | `translate` | 7 | 0 | ✅ |
| Training | 训练 | `translate` | 7 | 3 | ✅ |
| Commit | 提交 | `translate` | 7 | 3 | ✅ |
| False Positive | 误报 | `translate` | 7 | 1 | ✅ |
| On-call | 值班 | `translate` | 7 | 3 | ✅ |
| Merge | 合并 | `translate` | 6 | 2 | ✅ |
| Telemetry | 遥测 | `translate` | 5 | 2 | ✅ |
| Alert Fatigue | 告警疲劳 | `translate` | 5 | 2 | ✅ |
| Hallucination | 幻觉 | `translate` | 4 | 1 | ✅ |
| Continuous Delivery (CD) | 持续交付（CD） | `acronym` | 4 | 0 | ✅ |
| Integrated Development Environment (IDE) | 集成开发环境（IDE） | `acronym` | 4 | 0 | ✅ |
| Diff | 差异 | `translate` | 4 | 2 | ✅ |
| Dashboard | 仪表盘 | `translate` | 4 | 1 | ✅ |
| Retrieval-Augmented Generation (RAG) | 检索增强生成（RAG） | `acronym` | 3 | 0 | ✅ |
| Embedding | 嵌入 | `translate` | 3 | 0 | ✅ |
| Benchmark | 基准测试 | `translate` | 3 | 1 | ✅ |
| Function Calling | 函数调用 | `translate` | 3 | 0 | ✅ |
| Branch | 分支 | `translate` | 3 | 1 | ✅ |
| Specification (Spec) | 规格说明 | `translate` | 3 | 3 | ✅ |
| Exploit | 漏洞利用 | `translate` | 3 | 1 | ✅ |
| Triage | 分级处置 | `translate` | 3 | 3 | ✅ |
| Runbook | 运维手册 | `translate` | 3 | 0 | ✅ |
| Mean Time To Recovery (MTTR) | 平均恢复时间（MTTR） | `acronym` | 3 | 1 | ✅ |
| Agentic | 智能体化的 | `translate` | 2 | 6 | ✅ |
| Coding Agent | 编码智能体 | `translate` | 2 | 1 | ✅ |
| Refactor | 重构 | `translate` | 2 | 1 | ✅ |
| Latency | 延迟 | `translate` | 2 | 1 | ✅ |
| Deliverable | 交付物 | `translate` | 2 | 1 | ✅ |
| Common Vulnerabilities and Exposures (CVE) | 通用漏洞披露（CVE） | `acronym` | 2 | 0 | ✅ |
| Remote Code Execution (RCE) | 远程代码执行（RCE） | `acronym` | 2 | 1 | ✅ |
| Root Cause Analysis (RCA) | 根因分析（RCA） | `acronym` | 2 | 2 | ✅ |
| Prompt Engineering | 提示词工程 | `translate` | 1 | 1 | ✅ |
| System Prompt | 系统提示词 | `translate` | 1 | 1 | ✅ |
| Fine-tuning | 微调 | `translate` | 1 | 0 | ✅ |
| Human-in-the-loop | 人在回路 | `translate` | 1 | 1 | ✅ |
| Technical Debt | 技术债 | `translate` | 1 | 1 | ✅ |
| Unit Test | 单元测试 | `translate` | 1 | 0 | ✅ |
| Integration Test | 集成测试 | `translate` | 1 | 0 | ✅ |
| Runtime | 运行时 | `translate` | 1 | 1 | ✅ |
| Sandbox | 沙箱 | `translate` | 1 | 0 | ✅ |
| Design Doc | 设计文档 | `translate` | 1 | 0 | ✅ |
| Stakeholder | 干系人 | `translate` | 1 | 0 | ✅ |
| Acceptance Criteria | 验收标准 | `translate` | 1 | 1 | ✅ |
| False Negative | 漏报 | `translate` | 1 | 0 | ✅ |
| Red Team | 红队 | `translate` | 1 | 0 | ✅ |
| Postmortem | 事后复盘 | `translate` | 1 | 0 | ✅ |
| Service Level Objective (SLO) | 服务等级目标（SLO） | `acronym` | 1 | 0 | ✅ |
| Service Level Agreement (SLA) | 服务等级协议（SLA） | `acronym` | 1 | 0 | ✅ |
| Toil | 琐务 | `translate` | 1 | 1 | ✅ |
| Autoremediation | 自动修复 | `translate` | 1 | 0 | ✅ |
| Threat Modeling | 威胁建模 | `translate` | 1 | 1 | ✅ |
| Reasoning | 推理能力 | `translate` | 0 | 3 | ✅ |

