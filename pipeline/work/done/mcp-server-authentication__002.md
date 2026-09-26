### 通过 CLI

你可以用 [Wrangler CLI](/workers/wrangler) 在本地创建新的 MCP 服务器并部署到 Cloudflare。

1. 打开终端并运行以下命令：在初始化过程中，选择这些选项：- 对于 *Do you want to add an AGENTS.md file to help AI coding tools understand Cloudflare APIs?*，选择 `No`。- 对于 *Do you want to use git for version control?*，选择 `No`。- 对于 *Do you want to deploy your application?*，选择 `No`（我们会在部署前先测试这个服务器）。现在，你的 MCP 服务器已经搭好，依赖也已安装。

   ```
   npm create cloudflare@latest -- remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
   ```
   ```
   yarn create cloudflare remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
   ```
   ```
   pnpm create cloudflare@latest remote-mcp-server-authless --template=cloudflare/ai/demos/remote-mcp-authless
   ```

2. 进入项目文件夹：

   *终端窗口*
   ```
   cd remote-mcp-server-authless
   ```

3. 在新项目所在目录运行以下命令以启动开发服务器：从命令输出中查看本地端口。在本例中，MCP 服务器运行在端口 `8788` 上，MCP 端点 URL 为 `http://localhost:8788/mcp`。

   *终端窗口*
   ```
   npm start
   ```

   ```
   ⎔ Starting local server...[wrangler:info] Ready on http://localhost:8788
   ```

4. 要在本地测试该服务器：
  1. 在新终端中运行 [MCP inspector ↗](https://github.com/modelcontextprotocol/inspector)。MCP inspector 是一个交互式 MCP 客户端，让你能从浏览器连接 MCP 服务器并调用工具。MCP Inspector 会在你的浏览器中启动。你也可以手动打开浏览器访问 `http://localhost:<PORT>` 来启动它。从命令输出中查看 MCP Inspector 运行的本地端口。在本例中，MCP Inspector 服务在端口 `5173` 上。

     *终端窗口*
     ```
     npx @modelcontextprotocol/inspector@latest
     ```

     ```
     ð MCP Inspector is up and running at:  http://localhost:5173/?MCP_PROXY_AUTH_TOKEN=46ab..cd3
     ð Opening browser...
     ```

  2. 在 MCP inspector 中输入你的 MCP 服务器 URL（`http://localhost:8788/mcp`），并选择 **Connect**。选择 **List Tools** 以显示你的 MCP 服务器对外暴露的工具。
5. 现在你可以把 MCP 服务器部署到 Cloudflare 了。在项目目录下运行：如果你已经把[一个 git 仓库](/workers/ci-cd/builds/)连接到承载 MCP 服务器的 Worker，也可以向仓库主分支推送改动或合并拉取请求来完成部署。MCP 服务器会被部署到你的 `*.workers.dev` 子域，地址为 `https://remote-mcp-server-authless.your-account.workers.dev/mcp`。

   *终端窗口*
   ```
   npx wrangler@latest deploy
   ```

6. 要测试远程 MCP 服务器，把已部署 MCP 服务器的 URL（`https://remote-mcp-server-authless.your-account.workers.dev/mcp`）填入运行在 `http://localhost:5173` 的 MCP inspector。

现在你就有了一个可供 MCP 客户端连接的远程 MCP 服务器。
