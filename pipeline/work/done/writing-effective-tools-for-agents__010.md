### 对工具描述做提示词工程

现在我们来到改进工具最有效的方法之一：**对工具描述与规格说明做提示词工程**。因为它们会被载入智能体的上下文，它们合起来能把智能体引导向有效的工具调用行为。

写工具描述与规格说明时，想一想你会如何向团队里的新同事介绍这个工具。考虑你可能默认带入的上下文——特殊的查询格式、小众术语的定义、底层资源之间的关系——并把它显式写出来。通过清晰描述（并用严格的数据模型强制）预期的输入与输出来避免歧义。特别是，输入参数应当命名得毫无歧义：与其用名为 `user` 的参数，不如试试 `user_id`。

有了评估，你就能更有把握地度量提示词工程带来的影响。即便对工具描述做细微打磨，也可能带来显著的改进。我们对工具描述做了精确优化之后，Claude Sonnet 3.5 在 [SWE-bench Verified](https://www.anthropic.com/engineering/swe-bench-sonnet) 评估上取得了当时的最优表现，错误率大幅下降、任务完成度提升。

工具定义的其它最佳实践见我们的[开发者指南](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#best-practices-for-tool-definitions)。如果你在为 Claude 构建工具，我们还建议读一读工具是如何被动态载入 Claude [系统提示词](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use#tool-use-system-prompt)的。最后，如果你在为 MCP 服务器编写工具，[工具注解](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)有助于披露哪些工具需要开放世界访问权限，或会做破坏性改动。
