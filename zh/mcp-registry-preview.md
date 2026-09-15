<!-- source: source/pages/mcp-registry-preview.html -->
<!-- week: 2 | chunks: 3 -->

今天，我们正式发布模型上下文协议（MCP）注册表——一个面向公开 MCP 服务器的开放目录与 API，用于改善可发现性与落地实现。通过标准化服务器的分发与发现方式，我们既扩大了它们的覆盖面，也让客户端更容易接入。

MCP 注册表现已开放预览。开始使用：

- 按照《向 MCP 注册表添加服务器》指南添加你的服务器（面向服务器维护者）
- 按照《访问 MCP 注册表数据》指南获取服务器数据（面向客户端维护者）

# MCP 服务器的事实单一来源

2025 年 3 月，我们曾表示希望为 MCP 生态构建一个中心化注册表。今天我们宣布，已正式上线 [https://registry.modelcontextprotocol.io](https://registry.modelcontextprotocol.io) 作为官方 MCP 注册表。作为 MCP 项目的一部分，MCP 注册表以及其上游的 [OpenAPI 规格说明](https://github.com/modelcontextprotocol/registry/blob/main/docs/reference/api/official-registry-api.md) 均已开源——任何人都可以据此构建兼容的子注册表。

我们的目标是标准化服务器的分发与发现方式，提供一个子注册表可以据以构建的权威来源。这反过来会扩大服务器的覆盖面，帮助客户端更轻松地在整个 MCP 生态中找到所需服务器。

## 公开与私有子注册表

在构建中心化注册表时，我们很重视不去削弱社区与企业已建成的现有注册表。MCP 注册表充当公开 MCP 服务器的权威来源，各组织可以按自定义标准[创建子注册表](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/registry-aggregators.mdx)。例如：

**公开子注册表**，比如与各个 MCP 客户端绑定的、带有明确取向的「MCP 应用市场」，可以自由地增补与增强其从上游 MCP 注册表摄取的数据。每一种 MCP 终端用户画像都有不同需求，理应由 MCP 客户端应用市场以其鲜明的取向去服务各自的终端用户。

**私有子注册表**将存在于对隐私与安全有严格要求的企业内部，而 MCP 注册表为这些企业提供了可供构建的单一上游数据源。我们至少会与这些私有实现共享 API schema，以便相关的 SDK 与工具链能在整个生态中复用。

无论哪种情况，MCP 注册表都是起点——它是 MCP 服务器维护者发布并维护自述信息的中心位置，供下游消费者加工并交付给各自的终端用户。

## 社区驱动的审核机制

MCP 注册表是由注册表工作组维护、以宽松许可证授权的官方 MCP 项目。社区成员可以提交 issue，举报违反 MCP [审核准则](https://github.com/modelcontextprotocol/registry/blob/main/docs/modelcontextprotocol-io/moderation-policy.mdx)的服务器——例如含垃圾信息、恶意代码，或冒充正规服务。随后注册表维护者可将这些条目列入拒绝名单，并追溯性地从公开访问中移除。

# 开始使用

开始使用：

- 按照《向 MCP 注册表添加服务器》指南添加你的服务器（面向服务器维护者）
- 按照《访问 MCP 注册表数据》指南获取服务器数据（面向客户端维护者）

MCP 注册表的这一预览版旨在帮助我们在正式可用之前改善用户体验，不提供数据持久性保证或其他担保。我们建议 MCP 采用者密切关注开发进展，因为在注册表正式可用之前可能出现破坏性变更。

随着注册表的持续开发，我们欢迎在 [modelcontextprotocol/registry GitHub 仓库](https://github.com/modelcontextprotocol/registry)上提出反馈与贡献：Discussion、Issue 与 Pull Request 都欢迎。

# 感谢 MCP 社区

MCP 注册表从一开始就是协作的成果，我们无比感激广大开发者社区的热情与支持。

2025 年 2 月，它作为一个草根项目起步——MCP 的创建者 [David Soria Parra](https://github.com/dsp-ant) 与 [Justin Spahr-Summers](https://github.com/jspahrsummers) 邀请 [PulseMCP](https://www.pulsemcp.com/) 与 [Goose](https://block.github.io/goose/) 团队协助构建一个中心化的社区注册表。来自 [PulseMCP](https://www.pulsemcp.com/) 的注册表维护者 [Tadas Antanavicius](https://github.com/tadasant) 牵头了最初的工作，与来自 [Block](https://block.xyz/) 的 [Alex Hancock](https://github.com/alexhancock) 协作。很快，[GitHub](https://github.com/) 的 MCP 负责人、注册表维护者 [Toby Padilla](https://github.com/toby) 也加入进来；最近，来自 [Anthropic](https://www.anthropic.com/) 的 [Adam Jones](https://github.com/domdomegg) 作为注册表维护者加入，推动项目走到今天的发布。MCP 注册表开发的[最初公告](https://github.com/modelcontextprotocol/registry/discussions/11)列出了来自至少 9 家公司的 16 位贡献者。

还有许多人为这个项目落地做出了关键贡献：来自 [Stacklok](https://stacklok.com/) 的 [Radoslav Dimitrov](https://github.com/rdimitrov)、来自 [GitHub](https://github.com/) 的 [Avinash Sridhar](https://github.com/sridharavinash)、来自 [VS Code](https://code.visualstudio.com/) 的 [Connor Peet](https://github.com/connor4312)、来自 [NuGet](https://www.nuget.org/) 的 [Joel Verhagen](https://github.com/joelverhagen)、来自 [Last9](https://last9.io/) 的 [Preeti Dewani](https://github.com/pree-dew)、来自 [Microsoft](https://www.microsoft.com/) 的 [Avish Porwal](https://github.com/Avish34)、[Jonathan Hefner](https://github.com/jonathanhefner)，以及许多提供代码评审与开发支持的 Anthropic 与 GitHub 员工。我们也感谢[注册表贡献者名单](https://github.com/modelcontextprotocol/registry/graphs/contributors)上的每一位，以及所有参与[讨论与 issue](https://github.com/modelcontextprotocol/registry)的人。

我们深深感谢每一位为这项基础性开源基础设施投入的人。我们正在一起帮助全球的开发者和组织构建更可靠、更懂上下文的 AI 应用。谨代表 MCP 社区，谢谢大家。
