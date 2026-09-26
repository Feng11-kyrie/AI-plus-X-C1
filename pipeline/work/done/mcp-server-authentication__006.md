#### 第 2.2 步 —— 为生产环境创建新的 OAuth 应用

你需要重复第 2.1 步，为生产环境创建一个新的 OAuth 应用。

1. 访问 github.com/settings/developers ↗，按以下设置创建新的 OAuth 应用：

- Application name: My MCP Server (production)
- Homepage URL: 填入已部署 MCP 服务器的 workers.dev URL（例如 worker-name.account-name.workers.dev）
- Authorization callback URL: 填入已部署 MCP 服务器 workers.dev URL 的 /callback 路径（例如 worker-name.account-name.workers.dev/callback）

1. 对于你刚创建的 OAuth 应用，用 Wrangler CLI 填入 client ID 与 client secret：

*终端窗口*

```
npx wrangler secret put GITHUB_CLIENT_ID
```

*终端窗口*

```
npx wrangler secret put GITHUB_CLIENT_SECRET
```

```
npx wrangler secret put COOKIE_ENCRYPTION_KEY # add any random string here e.g. openssl rand -hex 32
```

1. 设置一个 KV 命名空间 a. 创建 KV 命名空间：b. 用返回的 KV ID 更新 `wrangler.jsonc` 文件：

   *终端窗口*
   ```
   npx wrangler kv namespace create "OAUTH_KV"
   ```

   ```
   {  "kvNamespaces": [    {      "binding": "OAUTH_KV",      "id": "<YOUR_KV_NAMESPACE_ID>"    }  ]}
   ```

2. 把 MCP 服务器部署到你的 Cloudflare `workers.dev` 域名：

   *终端窗口*
   ```
   npm run deploy
   ```

3. 用 [AI Playground ↗](https://playground.ai.cloudflare.com/)、MCP Inspector 或[其它 MCP 客户端](/agents/guides/test-remote-mcp-server/)连接运行在 `worker-name.account-name.workers.dev/mcp` 的服务器，并用 GitHub 完成认证。
