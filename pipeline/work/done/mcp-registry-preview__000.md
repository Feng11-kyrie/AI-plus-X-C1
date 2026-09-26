今天，我们正式发布模型上下文协议（MCP）注册表——一个面向公开 MCP 服务器的开放目录与 API，用于改善可发现性与落地实现。通过标准化服务器的分发与发现方式，我们既扩大了它们的覆盖面，也让客户端更容易接入。

MCP 注册表现已开放预览。开始使用：

- 按照《向 MCP 注册表添加服务器》指南添加你的服务器（面向服务器维护者）
- 按照《访问 MCP 注册表数据》指南获取服务器数据（面向客户端维护者）

# MCP 服务器的事实单一来源

2025 年 3 月，我们曾表示希望为 MCP 生态构建一个中心化注册表。今天我们宣布，已正式上线 [https://registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) 作为官方 MCP 注册表。作为 MCP 项目的一部分，MCP 注册表以及其上游的 [OpenAPI 规格说明](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/official-registry-api.md) 均已开源——任何人都可以据此构建兼容的子注册表。

我们的目标是标准化服务器的分发与发现方式，提供一个子注册表可以据以构建的权威来源。这反过来会扩大服务器的覆盖面，帮助客户端更轻松地在整个 MCP 生态中找到所需服务器。
