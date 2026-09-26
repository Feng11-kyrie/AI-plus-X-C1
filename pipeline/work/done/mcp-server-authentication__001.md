## 部署你的第一个 MCP 服务器

你可以先部署一个不带身份认证的[公开 MCP 服务器 ↗](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)，之后再补上用户身份认证与带范围的授权。如果你已经确定自己的服务器需要身份认证，可以直接跳到[下一节](/agents/guides/remote-mcp-server/#add-authentication)。

### 通过控制台

下面的按钮会引导你完成把[示例 MCP 服务器 ↗](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)部署到 Cloudflare 账号所需的全部步骤：

[![Deploy to Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

部署完成后，该服务器会运行在你的 `workers.dev` 子域上（例如 `remote-mcp-server-authless.your-account.workers.dev/mcp`）。你可以立即用 [AI Playground ↗](https://playground.ai.cloudflare.com/)（一个远程 MCP 客户端）、[MCP inspector ↗](https://github.com/modelcontextprotocol/inspector) 或[其它 MCP 客户端](/agents/guides/remote-mcp-server/#connect-from-an-mcp-client-via-a-local-proxy)连接它。

系统会在你的 GitHub 或 GitLab 账号下为这个 MCP 服务器新建一个 git 仓库，并配置为：每次你向仓库主分支推送改动或合并拉取请求时，自动部署到 Cloudflare。你可以克隆这个仓库、[在本地开发](/agents/guides/remote-mcp-server/#via-the-cli)，并开始用你自己的[工具](/agents/model-context-protocol/tools/)定制这个 MCP 服务器。
