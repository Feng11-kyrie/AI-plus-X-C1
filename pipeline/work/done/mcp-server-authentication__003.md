## 通过本地代理从 MCP 客户端连接

现在你的远程 MCP 服务器已经跑起来了，你可以用 [`mcp-remote` 本地代理 ↗](https://www.npmjs.com/package/mcp-remote) 把 Claude Desktop 或其它 MCP 客户端连上去——即便你的 MCP 客户端在客户端侧不支持远程传输或授权也没关系。这让你能用真实的 MCP 客户端测试与远程 MCP 服务器交互是什么样子。

例如，要从 Claude Desktop 连接：

1. 更新 Claude Desktop 的配置，指向你的 MCP 服务器 URL：

   ```
   {  "mcpServers": {    "math": {      "command": "npx",      "args": [        "mcp-remote",        "https://remote-mcp-server-authless.your-account.workers.dev/mcp"      ]    }  }}
   ```

2. 重启 Claude Desktop 以加载该 MCP 服务器。完成后，Claude 就能调用你的远程 MCP 服务器了。
3. 要测试，可以让 Claude 使用你的某个工具。例如：Claude 应当调用该工具，并显示远程 MCP 服务器生成的结果。

   ```
   Could you use the math tool to add 23 and 19?
   ```

要了解如何在其它 MCP 客户端中使用远程 MCP 服务器，请参考[测试远程 MCP 服务器](/agents/guides/test-remote-mcp-server)。
