<!-- source: source/pages/mcp-server-authentication.html -->
<!-- week: 2 | chunks: 8 -->

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

## 部署你的第一个 MCP 服务器

你可以先部署一个不带身份认证的[公开 MCP 服务器 ↗](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)，之后再补上用户身份认证与带范围的授权。如果你已经确定自己的服务器需要身份认证，可以直接跳到[下一节](/agents/guides/remote-mcp-server/#add-authentication)。

### 通过控制台

下面的按钮会引导你完成把[示例 MCP 服务器 ↗](https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)部署到 Cloudflare 账号所需的全部步骤：

[![Deploy to Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

部署完成后，该服务器会运行在你的 `workers.dev` 子域上（例如 `remote-mcp-server-authless.your-account.workers.dev/mcp`）。你可以立即用 [AI Playground ↗](https://playground.ai.cloudflare.com/)（一个远程 MCP 客户端）、[MCP inspector ↗](https://github.com/modelcontextprotocol/inspector) 或[其它 MCP 客户端](/agents/guides/remote-mcp-server/#connect-from-an-mcp-client-via-a-local-proxy)连接它。

系统会在你的 GitHub 或 GitLab 账号下为这个 MCP 服务器新建一个 git 仓库，并配置为：每次你向仓库主分支推送改动或合并拉取请求时，自动部署到 Cloudflare。你可以克隆这个仓库、[在本地开发](/agents/guides/remote-mcp-server/#via-the-cli)，并开始用你自己的[工具](/agents/model-context-protocol/tools/)定制这个 MCP 服务器。

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

## 添加身份认证

你先前部署的公开 MCP 服务器示例允许任何客户端在不登录的情况下连接并调用工具。要为你的 MCP 服务器加上用户身份认证，可以接入 Cloudflare Access，或把第三方服务作为 OAuth 提供方。你的 MCP 服务器负责处理安全的登录流程，并签发访问令牌，供 MCP 客户端发起已认证的工具调用。用户通过 OAuth 提供方登录，并以带范围的权限，授权其 AI 智能体与你的 MCP 服务器所暴露的工具交互。

### Cloudflare Access OAuth

你可以把 MCP 服务器配置为要求通过 Cloudflare Access 完成用户身份认证。Cloudflare Access 充身份聚合层，校验用户邮箱、来自你现有[身份提供方](/cloudflare-one/integrations/identity-providers/)（如 GitHub 或 Google）的信号，以及 IP 地址或设备证书等其它属性。当用户连接 MCP 服务器时，会被提示登录所配置的身份提供方，只有通过你的 [Access 策略](/cloudflare-one/access-controls/policies/#selectors)才会获得访问权限。

分步部署指南请参考[用 Access for SaaS 保护 MCP 服务器](/cloudflare-one/access-controls/ai-controls/saas-mcp/)。

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

## 后续步骤

**MCP Tools**
为你的 MCP 服务器添加工具。

**Authorization**
定制身份认证与授权。
