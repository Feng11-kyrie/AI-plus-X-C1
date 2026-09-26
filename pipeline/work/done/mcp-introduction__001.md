## 什么是模型上下文协议（MCP）？

MCP 本质上是 AI 应用与外部工具或数据源之间的**通用适配器**。它[定义了一套通用协议](https://www.anthropic.com/news/model-context-protocol#:~:text=MCP%20addresses%20this%20challenge,to%20the%20data%20they%20need)（构建在 JSON-RPC 2.0 之上），让 AI 助手能以结构化方式调用外部服务的函数、获取数据或使用预定义提示词。不必再让每个 LLM 应用为每个 API 或数据库编写定制代码，[MCP 为所有交互提供了一种标准化的「语言」](https://medium.com/data-and-beyond/the-model-context-protocol-mcp-the-ultimate-guide-c40539e2a8e7#:~:text=https%3A%2F%2Fmodelcontextprotocol)。

MCP 这一层让 AI 应用能够安全地访问外部数据源与工具并与之交互。它充任大语言模型（LLM）与各类数据库、应用或 API 之间的桥梁，促成无缝集成与功能实现，而无需大量定制编码。

为实现这一点，MCP 采用**客户端—服务器架构**。由 AI 驱动的应用（例如聊天机器人、IDE 助手或智能体）作为*宿主（host）*，运行一个 MCP *客户端（client）*组件；而每一套外部集成则作为一个 MCP *服务器（server）*运行。服务器通过 MCP 暴露能力（例如函数、数据资源或提示词模板），客户端连接上来以使用这些能力。这种分离意味着 AI 模型**不直接与 API 对话**；而是经由 MCP 的客户端／服务器握手，由这一层来组织数据交换。

[来源](https://generativeai.pub/mcp-servers-explained-python-and-agentic-ai-tool-integration-aa2ddca6cbe5)
