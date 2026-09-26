## 添加身份认证

你先前部署的公开 MCP 服务器示例允许任何客户端在不登录的情况下连接并调用工具。要为你的 MCP 服务器加上用户身份认证，可以接入 Cloudflare Access，或把第三方服务作为 OAuth 提供方。你的 MCP 服务器负责处理安全的登录流程，并签发访问令牌，供 MCP 客户端发起已认证的工具调用。用户通过 OAuth 提供方登录，并以带范围的权限，授权其 AI 智能体与你的 MCP 服务器所暴露的工具交互。

### Cloudflare Access OAuth

你可以把 MCP 服务器配置为要求通过 Cloudflare Access 完成用户身份认证。Cloudflare Access 充身份聚合层，校验用户邮箱、来自你现有[身份提供方](/cloudflare-one/integrations/identity-providers/)（如 GitHub 或 Google）的信号，以及 IP 地址或设备证书等其它属性。当用户连接 MCP 服务器时，会被提示登录所配置的身份提供方，只有通过你的 [Access 策略](/cloudflare-one/access-controls/policies/#selectors)才会获得访问权限。

分步部署指南请参考[用 Access for SaaS 保护 MCP 服务器](/cloudflare-one/access-controls/ai-controls/saas-mcp/)。
