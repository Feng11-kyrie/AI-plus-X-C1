生成式 AI 已经如此彻底地改变了[软件开发](https://resolve.ai/glossary/what-is-the-future-of-software-engineering)，你可以在几小时内搭出完整的服务；但要搞清楚这些服务究竟哪里出了问题，仍然得在碎片化的工具之间做极其费力的排查。从代码生成到代码评审，编码智能体承担了构建侧的工作。但[生产环境调试](https://resolve.ai/glossary/what-is-debugging)呢？仍然靠人工。看下面这个例子：

| 编码 | 生产 |
|---|---|
| 要写一个服务：你打开 AI 原生开发环境，让 AI「创建一个处理重试与超时的支付服务」。AI 结合你代码库的上下文，生成带错误处理的实现 | 同一个服务出现高延迟时：你先提出一个假设 → 去 Datadog 查指标 → 切到 Loki 查日志 → 交叉比对部署历史 → 对齐时间戳 →……如此往复 |

问题不在于 AI 的能力，而在于我们如何设计 AI 系统。大多数工程团队仍然只是用 AI 工具把原有工作流跑得更快，而没有重新设想软件开发与生产运维本该如何端到端地运作。

在 Resolve AI，我们一直在为工程师构建用于[生产系统](https://resolve.ai/glossary/what-are-production-systems-in-software-engineering)的多智能体系统。我们一直主张工程应当走向 AI 原生（即工程师主要与[自主智能体](https://resolve.ai/glossary/what-is-agentic-ai)交互来完成生产系统上的工作），而软件工程领域的大多数生成式 AI 讨论，却都集中在用 Copilot 与编码助手写出 AI 生成的代码。

我们最近向[斯坦福大学的研究生 AI 课程](https://www.youtube.com/watch?v=z7RBPQL0rZ4)介绍了我们的方法，深入讲解了支撑 AI 原生工程工作流的 AI 智能体及其架构模式。
