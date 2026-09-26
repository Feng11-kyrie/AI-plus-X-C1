<!-- page 1 -->
ANTHROP\C
Anthropic 各团队如何使用 Claude Code

Anthropic 的内部团队正在用 Claude Code 改造他们的工作流，让开发者与非技术岗的同事都能承担复杂项目、自动化任务，并弥合此前限制其生产力的技能鸿沟。
通过对我们内部 Claude Code 重度用户的访谈，我们整理了各不同部门如何使用 Claude Code、它对工作的影响，以及给正在考虑采纳的其它组织的建议。

<!-- page 2 -->
目录
面向数据基础设施的 Claude Code　3
面向产品开发的 Claude Code　5
面向安全工程的 Claude Code　7
面向推理的 Claude Code　9
面向数据科学与可视化的 Claude Code　11
面向 API 的 Claude Code　13
面向增长营销的 Claude Code　15
面向产品设计的 Claude Code　17
面向强化学习工程的 Claude Code　19
面向法务的 Claude Code　21
2　Anthropic 各团队如何使用 Claude Code

<!-- page 3 -->
## 面向数据基础设施的 Claude Code

数据基础设施团队负责为全公司各团队组织所有业务数据。他们用 Claude Code 自动化例行的数据工程任务、排查复杂的基础设施问题，并创建有文档记录的工作流，让技术与非技术团队成员都能独立访问和操作数据。

**Claude Code 的主要用例**

**用截图排查 Kubernetes 问题**
当 Kubernetes 集群宕机、无法调度新 Pod 时，该团队用 Claude Code 诊断问题。他们把仪表盘截图喂给 Claude Code，由它带着他们逐个菜单走完 Google Cloud 的界面，直到发现一条提示 Pod IP 地址耗尽的警告。随后 Claude Code 给出了创建新 IP 池并将其加入集群的确切命令，从而免去了请网络专家介入的需要。

**为财务团队做纯文本工作流**
该团队教会财务团队成员编写描述其数据工作流的纯文本文件，再把文件载入 Claude Code，得到全自动的执行。没有任何编码经验的员工可以描述这样的步骤：「查询这个仪表盘、获取信息、运行这些查询、产出 Excel 输出」，而 Claude Code 会执行整个工作流，包括主动询问日期这类必需输入。

**帮助新人导航代码库**
当新的数据科学家加入团队时，会被告知用 Claude Code 来导航他们庞大的代码库。Claude Code 会读取他们的 Claude.md 文件（文档），识别与特定任务相关的文件，解释数据管线的依赖关系，并帮助新人理解哪些上游数据源喂给了各个仪表盘。这取代了传统的数据目录与可发现性工具。

**会话结束时的文档更新**
该团队会在每个任务结束时，让 Claude Code 总结刚完成的工作会话并提出改进建议。这形成了一个持续改进的闭环：Claude Code 根据实际使用情况，帮助打磨 Claude.md 文档与工作流说明，使后续迭代更有效。

**跨多个实例的并行任务管理**
处理长时间运行的数据任务时，他们会在不同仓库、针对不同项目打开多个 Claude Code 实例。每个实例都保有完整上下文，因此当他们几小时或几天后切回来时，Claude Code 清楚记得当初在做什么、停在哪里，从而实现真正意义上的并行工作流管理，且不丢失上下文。
3　面向数据基础设施的 Claude Code
