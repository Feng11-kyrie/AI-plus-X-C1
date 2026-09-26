### 第三方 OAuth

你可以把 MCP 服务器连接到任何支持 OAuth 2.0 规格说明的 [OAuth 提供方](/agents/model-context-protocol/authorization/#2-third-party-oauth-provider)，包括 GitHub、Google、Slack、[Stytch](/agents/model-context-protocol/authorization/#stytch)、[Auth0](/agents/model-context-protocol/authorization/#auth0)、[WorkOS](/agents/model-context-protocol/authorization/#workos) 等等。

下面的示例演示如何用 GitHub 作为 OAuth 提供方。

#### 第 1 步 —— 创建新的 MCP 服务器

运行以下命令，创建一个带 GitHub OAuth 的 MCP 服务器：

```
npm create cloudflare@latest -- my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```
yarn create cloudflare my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

```
pnpm create cloudflare@latest my-mcp-server-github-auth --template=cloudflare/ai/demos/remote-mcp-github-oauth
```

现在，你的 MCP 服务器已经搭好，依赖也已安装。进入该项目文件夹：

*终端窗口*

```
cd my-mcp-server-github-auth
```

你会注意到，在这个示例 MCP 服务器中，如果打开 `src/index.ts`，最主要的差别是 `defaultHandler` 被设成了 `GitHubHandler`：

*TypeScript*

```
import GitHubHandler from "./github-handler";
export default new OAuthProvider({  apiRoute: "/mcp",  apiHandler: MyMCP.serve("/mcp"),  defaultHandler: GitHubHandler,  authorizeEndpoint: "/authorize",  tokenEndpoint: "/token",  clientRegistrationEndpoint: "/register",});
```

这确保你的用户会被重定向到 GitHub 完成认证。不过要让它跑起来，你还需要按下面的步骤创建 OAuth 客户端应用。

#### 第 2 步 —— 创建 OAuth 应用

要用 GitHub 作为 MCP 服务器的身份认证提供方，你需要创建两个 [GitHub OAuth 应用 ↗](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)——一个用于本地开发，一个用于生产环境。

#### 第 2.1 步 —— 为本地开发创建新的 OAuth 应用

1. 访问 [github.com/settings/developers ↗](https://github.com/settings/developers)，按以下设置创建新的 OAuth 应用：
  - Application name: My MCP Server (local)
  - Homepage URL: http://localhost:8788
  - Authorization callback URL: http://localhost:8788/callback
2. 对于你刚创建的 OAuth 应用，把其 client ID 作为 `GITHUB_CLIENT_ID` 填入，并生成一个 client secret 作为 `GITHUB_CLIENT_SECRET` 填入项目根目录的 `.env` 文件——它[会被用于在本地开发中设置密钥](/workers/configuration/secrets/)。

   *终端窗口*
   ```
   touch .envecho 'GITHUB_CLIENT_ID="your-client-id"' >> .envecho 'GITHUB_CLIENT_SECRET="your-client-secret"' >> .envcat .env
   ```

3. 运行以下命令启动开发服务器：你的 MCP 服务器现在运行在 `http://localhost:8788/mcp`。

   *终端窗口*
   ```
   npm start
   ```

4. 在新终端中运行 [MCP inspector ↗](https://github.com/modelcontextprotocol/inspector)。MCP inspector 是一个交互式 MCP 客户端，让你能从浏览器连接 MCP 服务器并调用工具。

   *终端窗口*
   ```
   npx @modelcontextprotocol/inspector@latest
   ```

5. 在浏览器中打开 MCP inspector：

   *终端窗口*
   ```
   open http://localhost:5173
   ```

6. 在 inspector 中输入你的 MCP 服务器 URL：`http://localhost:8788/mcp`
7. 在右侧主面板点击 **OAuth Settings** 按钮，然后点击 **Quick OAuth Flow**。你应当会被重定向到 GitHub 的登录或授权页面。在授权 MCP 客户端（即 inspector）访问你的 GitHub 账号之后，你会被重定向回 inspector。
8. 在侧边栏点击 **Connect**，你应该会看到 “List Tools” 按钮，点击它会列出你的 MCP 服务器对外暴露的工具。
