# 术语表（Glossary）

> 本文件由 `pipeline/glossary_tool.py` 从 `glossary.csv` 自动渲染，**请勿手工编辑**。
> **唯一真源是 `glossary.csv`**（机器可读，管线直接消费）。

## 使用政策

| policy | 含义 |
|---|---|
| `translate` | 译成中文，全文统一使用该译法 |
| `acronym` | 保留缩写，首次出现时给出中文全称 |
| `keep_en_first` | 首次出现写「中文（English）」，之后用中文 |
| `keep_en` | 专有名词/产品名，保留英文不译 |

## 禁用变体的两个等级

| 列 | 等级 | 校验行为 |
|---|---|---|
| `forbidden_zh` | **硬性** | 译文中出现即判该块不通过，必须返工 |
| `forbidden_soft` | 提示级 | 只记录不拦截——用于「记录」「流程」这类在中文里本身就常用、单用也说得通的词 |

另有两条中文特有的判定规则（见 `pipeline/translate.py` 的 `variant_hits`）：

1. **被正式译法包含的变体一律跳过**——「上下文协议」是「模型上下文协议（MCP）」的子串，子串匹配会把正确译文判成违规。
2. 宁可漏报也不误报：一个天天误报的校验器最终会被忽略。

**术语总数：171 条**（硬性禁用变体 338 条 + 提示级 27 条，由 `pipeline/translate.py` 逐块强制校验）

## 核心 LLM 与提示词（28 条）

| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |
|---|---|---|---|---|---|
| Large Language Model (LLM) | 大语言模型（LLM） | `acronym` | 大型语言模型、大模型语言 | — | 59 |
| Context | 上下文 | `translate` | 语境、情境、脉络 | — | 58 |
| Prompt | 提示词 | `translate` | 提示语、提示词条、promt | — | — |
| Prompt Engineering | 提示词工程 | `translate` | 提示工程、提示词工程学、指令工程 | — | — |
| System Prompt | 系统提示词 | `translate` | 系统指令、系统 prompt | — | — |
| Context Window | 上下文窗口 | `translate` | 上下文长度、语境窗口、上下文视窗 | — | — |
| Context Engineering | 上下文工程 | `translate` | 情境工程、语境工程、上下文工程学 | — | — |
| Context Rot | 上下文腐化 | `translate` | 上下文腐烂、上下文衰减、上下文退化 | — | — |
| Vibe Coding | 氛围编程 | `keep_en_first` | 感觉编程、氛围编码、Vibe 编码、直觉编程 | — | — |
| Scaffolding | 脚手架 | `translate` | 支架、骨架代码 | 框架 | — |
| Hallucination | 幻觉 | `translate` | 臆造、胡编、虚构输出 | 框架 | — |
| Fine-tuning | 微调 | `translate` | 精调、微调训练 | — | — |
| Few-shot | 少样本 | `translate` | 少量样本、少次示例、few shot | — | — |
| Zero-shot | 零样本 | `translate` | 无样本、零次示例 | — | — |
| Chain of Thought | 思维链 | `translate` | 思考链、推理链、思维链条 | — | — |
| Retrieval-Augmented Generation (RAG) | 检索增强生成（RAG） | `acronym` | 增强检索生成 | 落地 | — |
| Token | Token | `keep_en` | 词元、令牌 | 标记 | — |
| Temperature | 温度 | `translate` | 温度值、随机度 | — | — |
| Embedding | 嵌入 | `translate` | 向量化、嵌入向量 | — | — |
| Vector Database | 向量数据库 | `translate` | 矢量数据库、向量库 | — | — |
| Inference | 推理 | `translate` | 推演、模型推导 | 推断 | — |
| Reasoning | 推理能力 | `translate` | 思考链、推论、思维过程 | — | — |
| Training | 训练 | `translate` | 训练过程 | 培训 | — |
| Benchmark | 基准测试 | `translate` | 测评、跑分 | — | — |
| Model Card | 模型卡 | `translate` | 模型卡片、模型说明卡 | — | — |
| Evaluation | 评估 | `translate` | 评测、评价、测试评估 | — | — |
| Grounding | 溯源锚定 | `translate` | 接地、基础事实 | 落地 | — |
| Distractor | 干扰项 | `translate` | 干扰词、混淆项、分散项 | — | — |

## 智能体与工具调用（15 条）

| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |
|---|---|---|---|---|---|
| Model Context Protocol (MCP) | 模型上下文协议（MCP） | `acronym` | 模型情境协议、MCP 协议 | 组织、协调 | 325 |
| Agent | 智能体 | `translate` | 智能代理、AI 代理、代理人、Agent 体 | 代理 | 45 |
| Agentic | 智能体化的 | `translate` | 代理式、自治式、Agent 化 | — | 31 |
| Guardrails | 护栏 | `translate` | 防护栏、护栏机制、安全围栏 | — | — |
| Sub-agent | 子智能体 | `translate` | 子代理、次级智能体 | — | — |
| Multi-agent | 多智能体 | `translate` | 多代理、多 Agent、多智能系统 | — | — |
| Coding Agent | 编码智能体 | `translate` | 编程代理、代码智能体、编码代理 | — | — |
| Tool Use | 工具调用 | `translate` | 工具运用 | 工具使用、调用工具 | — |
| Function Calling | 函数调用 | `translate` | 功能调用、函数呼叫 | — | — |
| MCP Server | MCP 服务器 | `keep_en_first` | 模型上下文协议服务器、MCP 服务端 | — | — |
| Orchestration | 编排 | `translate` | 编排调度 | 组织、协调 | — |
| Workflow | 工作流 | `translate` | 工作流程、作业流 | 流程 | — |
| Human-in-the-loop | 人在回路 | `translate` | 人在环中、人工介入、人类在环 | — | — |
| Autonomy | 自主性 | `translate` | 自治性、自动化程度 | — | — |
| Agent Loop | 智能体循环 | `translate` | 代理循环、智能体回路 | — | — |

## 软件工程（36 条）

| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |
|---|---|---|---|---|---|
| Pull Request (PR) | 拉取请求（PR） | `acronym` | 合并请求、拉取申请、PR 请求 | — | 12 |
| Codebase | 代码库 | `translate` | 代码基底、代码基础、代码仓 | — | — |
| Repository | 仓库 | `translate` | 版本库、存储库、代码仓库 | — | — |
| Commit | 提交 | `translate` | 递交、确认提交 | — | — |
| Branch | 分支 | `translate` | 枝干、代码分支 | — | — |
| Merge | 合并 | `translate` | 归并、融合 | — | — |
| Code Review | 代码评审 | `translate` | 代码审查、代码复查、代码审核 | — | — |
| Refactor | 重构 | `translate` | 重写、重新构建、翻新 | — | — |
| Technical Debt | 技术债 | `translate` | 技术债务、技术欠账 | — | — |
| Legacy Code | 遗留代码 | `translate` | 历史代码、旧代码、遗产代码 | — | — |
| Boilerplate | 样板代码 | `translate` | 模板代码、重复代码、锅炉板 | — | — |
| Linter | 代码检查工具 | `translate` | 检查器、语法检查器、Lint 器 | — | — |
| Continuous Integration (CI) | 持续集成（CI） | `acronym` | 连续集成、持续整合 | — | — |
| Continuous Delivery (CD) | 持续交付（CD） | `acronym` | 持续部署、连续交付 | — | — |
| Unit Test | 单元测试 | `translate` | 单位测试、模块测试 | — | — |
| Integration Test | 集成测试 | `translate` | 整合测试、联合测试 | — | — |
| Test Coverage | 测试覆盖率 | `translate` | 覆盖度 | — | — |
| Regression | 回归 | `translate` | 退化、回退 | — | — |
| Deployment | 部署 | `translate` | 发布上线、布署、部署上线 | — | — |
| Rollback | 回滚 | `translate` | 回退、撤回、回滚操作 | — | — |
| Artifact | 制品 | `translate` | 工件、产物、构建物 | — | — |
| Integrated Development Environment (IDE) | 集成开发环境（IDE） | `acronym` | 整合开发环境、开发集成环境 | — | — |
| Terminal | 终端 | `translate` | 命令行窗口 | 控制台 | — |
| Command-Line Interface (CLI) | 命令行界面（CLI） | `acronym` | 命令行接口、命令界面 | — | — |
| Software Development Kit (SDK) | 软件开发工具包（SDK） | `acronym` | 软件开发套件、开发包 | — | — |
| Application Programming Interface (API) | 应用程序接口（API） | `acronym` | 应用编程界面、接口 API | — | — |
| Runtime | 运行时 | `translate` | 运行环境、运行时期 | — | — |
| Dependency | 依赖 | `translate` | 依赖性、依存项 | — | — |
| Sandbox | 沙箱 | `translate` | 沙盒、隔离环境 | — | — |
| Rate Limit | 速率限制 | `translate` | 频率限制、速率上限 | 限流 | — |
| Latency | 延迟 | `translate` | 时延、延时、迟滞 | — | — |
| Throughput | 吞吐量 | `translate` | 吞吐率、处理量 | — | — |
| Diff | 差异 | `translate` | 差分、变更差异、补丁 | — | — |
| Codebase Understanding | 代码库理解 | `translate` | 仓库理解 | 代码理解 | — |
| Spec-Driven Development | 规格驱动开发 | `translate` | 规范驱动开发、文档驱动开发 | — | — |
| Specification (Spec) | 规格说明 | `translate` | 规格书、需求规格 | 规范 | — |

## 安全（32 条）

| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |
|---|---|---|---|---|---|
| Prompt Injection | 提示词注入 | `translate` | 提示注入、prompt 注入、指令注入 | — | — |
| Static Application Security Testing (SAST) | 静态应用安全测试（SAST） | `acronym` | 静态安全测试、静态代码安全检测 | — | — |
| Dynamic Application Security Testing (DAST) | 动态应用安全测试（DAST） | `acronym` | 动态安全测试、动态安全检测 | — | — |
| Runtime Application Self-Protection (RASP) | 运行时应用自保护（RASP） | `acronym` | 运行时自保护、运行期自防护 | — | — |
| Software Composition Analysis (SCA) | 软件成分分析（SCA） | `acronym` | 软件组成分析、依赖成分分析 | — | — |
| Vulnerability | 漏洞 | `translate` | 脆弱性、弱点 | 缺陷 | — |
| Exploit | 漏洞利用 | `translate` | 利用程序、攻击利用、漏洞开发 | — | — |
| Common Vulnerabilities and Exposures (CVE) | 通用漏洞披露（CVE） | `acronym` | 公共漏洞库、漏洞编号 CVE | — | — |
| Common Weakness Enumeration (CWE) | 通用缺陷枚举（CWE） | `acronym` | 通用弱点枚举、缺陷列表 CWE | — | — |
| OWASP Top 10 | OWASP Top 10（OWASP 十大安全风险） | `keep_en_first` | OWASP 前十、OWASP 十大漏洞、OWASP 排行榜 | — | — |
| Cross-Site Scripting (XSS) | 跨站脚本攻击（XSS） | `acronym` | 跨站点脚本、XSS 脚本攻击 | — | — |
| Server-Side Request Forgery (SSRF) | 服务端请求伪造（SSRF） | `acronym` | 服务器端请求伪造、SSRF 攻击 | — | — |
| Insecure Direct Object Reference (IDOR) | 不安全的直接对象引用（IDOR） | `acronym` | 越权访问、直接对象引用漏洞 | — | — |
| Broken Object Level Authorization (BOLA) | 对象级授权失效（BOLA） | `acronym` | 对象级权限绕过、BOLA 漏洞 | — | — |
| Remote Code Execution (RCE) | 远程代码执行（RCE） | `acronym` | 远程命令执行、远端代码执行 | — | — |
| SQL Injection | SQL 注入 | `translate` | SQL 注入攻击、SQL 植入 | — | — |
| Attack Surface | 攻击面 | `translate` | 攻击表面、受攻击面 | — | — |
| Threat Model | 威胁模型 | `translate` | 风险模型 | — | — |
| False Positive | 误报 | `translate` | 假阳性、错误告警 | — | — |
| False Negative | 漏报 | `translate` | 假阴性、漏检 | — | — |
| False Positive Rate (FPR) | 假阳性率（FPR） | `acronym` | 假报率 | 误报率 FPR | — |
| True Positive Rate (TPR) | 真阳性率（TPR） | `acronym` | 正确检出率 | 真报率 | — |
| Triage | 分级处置 | `translate` | 分诊、分类处理、优先级排序 | — | — |
| Least Privilege | 最小权限 | `translate` | 最小特权、最低权限 | — | — |
| Supply Chain Attack | 供应链攻击 | `translate` | 供应链入侵、链条攻击 | — | — |
| Credential | 凭据 | `translate` | 凭证、证书凭据、登录信息 | — | — |
| Data Exfiltration | 数据外泄 | `translate` | 数据渗出、数据窃取、数据泄露 | — | — |
| Blast Radius | 影响半径 | `translate` | 爆炸半径、波及范围 | 影响范围 | — |
| Sandbox Escape | 沙箱逃逸 | `translate` | 沙盒逃逸、突破沙箱 | — | — |
| Red Team | 红队 | `translate` | 红色团队、攻击方 | — | — |
| Needle in a Haystack (NIAH) | 大海捞针测试（NIAH） | `acronym` | 针尖测试 | — | — |
| Threat Modeling | 威胁建模 | `translate` | — | — | — |

## SRE 与可观测性（25 条）

| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |
|---|---|---|---|---|---|
| Site Reliability Engineering (SRE) | 站点可靠性工程（SRE） | `acronym` | 网站可靠性工程、可靠性工程 SRE | — | — |
| Observability | 可观测性 | `translate` | 可观察性、监控能力 | — | — |
| Telemetry | 遥测 | `translate` | 远程测量、遥测数据 | — | — |
| Tracing | 链路追踪 | `translate` | 链路跟踪、追踪体系 | 跟踪 | — |
| Trace | 追踪记录 | `translate` | 调用链快照 | 轨迹 | — |
| Span | Span | `keep_en` | 跨度、片段、区段 | — | — |
| Metric | 指标 | `translate` | 度量值、监控指标 | 度量 | — |
| Log | 日志 | `translate` | 日志文件、Log 记录 | 记录 | — |
| Dashboard | 仪表盘 | `translate` | 仪表板、看板、监控面板 | — | — |
| Alert | 告警 | `translate` | 警报、报警、提醒 | — | — |
| Alert Fatigue | 告警疲劳 | `translate` | 警报疲劳、告警过载 | — | — |
| Incident | 故障事件 | `translate` | 事故 | — | — |
| On-call | 值班 | `translate` | 随时待命、值守、在线值班 | — | — |
| Postmortem | 事后复盘 | `translate` | 尸检报告、事后分析、事故报告 | — | — |
| Runbook | 运维手册 | `translate` | 操作手册、运行手册、预案 | — | — |
| Service Level Objective (SLO) | 服务等级目标（SLO） | `acronym` | 服务水平目标、服务级别目标 | — | — |
| Service Level Indicator (SLI) | 服务等级指标（SLI） | `acronym` | 服务水平指标、服务级别指标 | — | — |
| Service Level Agreement (SLA) | 服务等级协议（SLA） | `acronym` | 服务水平协议、服务级别协议 | — | — |
| Mean Time To Recovery (MTTR) | 平均恢复时间（MTTR） | `acronym` | 平均修复时间、平均恢复时长 | — | — |
| Root Cause Analysis (RCA) | 根因分析（RCA） | `acronym` | 根本原因分析、根因定位 | — | — |
| Toil | 琐务 | `translate` | 苦工、重复性劳动、杂务 | — | — |
| Blameless | 无指责的 | `translate` | 免责的、非责难的、无责备 | — | — |
| Chaos Engineering | 混沌工程 | `translate` | 混乱工程、混沌测试 | — | — |
| Capacity Planning | 容量规划 | `translate` | 产能规划、容量计划 | — | — |
| Autoremediation | 自动修复 | `translate` | 自动补救、自动处置 | — | — |

## 产品与流程（14 条）

| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |
|---|---|---|---|---|---|
| Software Development Life Cycle (SDLC) | 软件开发生命周期（SDLC） | `acronym` | 软件开发生命圈、开发周期 | — | — |
| Product Requirements Document (PRD) | 产品需求文档（PRD） | `acronym` | 产品需求书、需求文档 PRD | — | — |
| Design Doc | 设计文档 | `translate` | 设计稿、设计方案文档 | — | — |
| Stakeholder | 干系人 | `translate` | 利益相关者、相关方、干系方 | — | — |
| Scope Creep | 范围蔓延 | `translate` | 范围蠕变、需求蔓延 | — | — |
| Acceptance Criteria | 验收标准 | `translate` | 接受标准、验收条件 | — | — |
| User Story | 用户故事 | `translate` | 用户需求故事、使用者故事 | — | — |
| Deliverable | 交付物 | `translate` | 交付成果、可交付物、产出物 | — | — |
| Backlog | 待办列表 | `translate` | 积压工作、待办事项、需求池 | — | — |
| Milestone | 里程碑 | `translate` | 里程点、阶段节点 | — | — |
| Retrospective | 回顾会议 | `translate` | 复盘会、反思会 | — | — |
| After Action Review (AAR) | 行动后复盘（AAR） | `acronym` | 事后审查、行动回顾、AAR 复盘会 | — | — |
| Dogfooding | 自产自用 | `translate` | 吃狗粮、内部试用、自用测试 | — | — |
| Minimum Viable Product (MVP) | 最小可行产品（MVP） | `acronym` | 最简可行产品、最小可用产品 | — | — |

## 工具与专有名词（不译）（21 条）

| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |
|---|---|---|---|---|---|
| Claude | Claude | `keep_en` | — | — | 143 |
| Claude Code | Claude Code | `keep_en` | — | — | 62 |
| Gemini | Gemini | `keep_en` | — | — | 30 |
| OpenAI | OpenAI | `keep_en` | — | — | 22 |
| GitHub Copilot | GitHub Copilot | `keep_en` | — | — | 22 |
| Semgrep | Semgrep | `keep_en` | — | — | 21 |
| Anthropic | Anthropic | `keep_en` | — | — | 19 |
| Kubernetes | Kubernetes | `keep_en` | — | — | 19 |
| SARIF | SARIF | `keep_en` | — | — | 5 |
| Codex | Codex | `keep_en` | — | — | — |
| Cursor | Cursor | `keep_en` | — | — | — |
| Warp | Warp | `keep_en` | — | — | — |
| Devin | Devin | `keep_en` | — | — | — |
| Cognition | Cognition | `keep_en` | — | — | — |
| Docker | Docker | `keep_en` | — | — | — |
| GitHub | GitHub | `keep_en` | — | — | — |
| Git | Git | `keep_en` | — | — | — |
| VS Code | VS Code | `keep_en` | — | — | — |
| Vercel | Vercel | `keep_en` | — | — | — |
| Figma | Figma | `keep_en` | — | — | — |
| Notion | Notion | `keep_en` | — | — | — |

