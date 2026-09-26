本指南将展示如何使用 [Streamable HTTP 传输](/agents/model-context-protocol/transport/)——当前的 MCP 规格说明标准——在 Cloudflare 上部署你自己的远程 MCP 服务器。你有两种选择：

- **不带身份认证**——任何人都能连接并使用该服务器（无需登录）。
- **带[身份认证与授权](/agents/guides/remote-mcp-server/#add-authentication)**——用户在访问工具前先登录，你可以根据用户权限控制智能体能调用哪些工具。

## 选择方案

Agents SDK 提供多种创建 MCP 服务器的方式。选择适合你用例的方案：

| 方案 | 有状态？ | 需要 Durable Objects？ | 最适用场景 |
|---|---|---|---|
| [`createMcpHandler()`](/agents/api-reference/mcp-handler-api/) | 否 | 否 | 无状态工具，最简配置 |
| [`McpAgent`](/agents/api-reference/mcp-agent-api/) | 是 | 是 | 有状态工具、按会话保存状态、elicitation |
| 原生 `WebStandardStreamableHTTPServerTransport` | 否 | 否 | 完全掌控，不依赖 SDK |

- `createMcpHandler()` 是跑起一个无状态 MCP 服务器最快的方式。当你的工具不需要按会话保存状态时用它。
- `McpAgent` 为每个会话提供一个 Durable Object，内置状态管理、elicitation 支持，以及 SSE 与 Streamable HTTP 两种传输。
- 原生传输让你在不想用 Agents SDK 的辅助封装、而想直接使用 @modelcontextprotocol/sdk 时获得完全掌控。
