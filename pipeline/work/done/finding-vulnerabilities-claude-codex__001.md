## 引言

在 Semgrep，我们以应用安全（AppSec）为生、也为之着迷。我们长期在自己的产品中把 AI 生产化（[Assistant 背后的技术](https://semgrep.dev/blog/2024/the-tech-behind-semgrep-assistant/)、[用 promptfoo 测试我们的 AI 工作流](https://semgrep.dev/blog/2024/does-your-llm-thing-work-how-we-use-promptfoo/)、[用安全研究员的研判来评估自动分级处置的表现](https://semgrep.dev/blog/2025/building-an-appsec-ai-that-security-researchers-agree-with-96-of-the-time/)），持续研究传统确定性分析与现代 AI 上下文能力的最佳组合，而不追逐潮流。

这项研究就是那项长期使命的一部分。我们正在展开一次深入的、公开的探索，回答一个萦绕在每个人心头的问题：**LLM 在源代码中找漏洞，到底有多有效？**
