## 如何编写工具

本节介绍如何与智能体协作，既写出工具、也持续改进你交给它们的工具。先快速搭出一个工具原型并在本地测试。接着跑一套全面的评估，用以度量后续改动。与智能体并肩工作，你可以不断重复「评估—改进」这个过程，直到智能体在真实任务上取得良好表现。

### 构建原型

不亲自动手，很难预料哪些工具智能体用起来顺手、哪些不顺手。先快速搭一个原型。如果你用 [Claude Code](https://www.anthropic.com/claude-code) 来写工具（可能一次就成），那么把你工具所依赖的软件库、API 或 SDK（包括可能的 [MCP SDK](https://modelcontextprotocol.io/docs/sdk)）的文档提供给 Claude 会很有帮助。对 LLM 友好的文档通常可以在官方文档站点的扁平 `llms.txt` 文件里找到（这是我们 [API 的](https://docs.anthropic.com/llms.txt)）。

把你的工具包进一个[本地 MCP 服务器](https://modelcontextprotocol.io/docs/develop/connect-local-servers)或[桌面扩展](https://www.anthropic.com/engineering/desktop-extensions)（DXT），就能在 Claude Code 或 Claude Desktop 应用中连接并测试它们。

要把本地 MCP 服务器连接到 Claude Code，运行 `claude mcp add <name> <command> [args...]`。

要把本地 MCP 服务器或 DXT 连接到 Claude Desktop 应用，分别进入 `Settings > Developer` 或 `Settings > Extensions`。

工具也可以直接传入 [Anthropic API](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview) 调用，用于程序化测试。

亲自试用这些工具，找出粗糙之处。从你的用户那里收集反馈，从而建立起对其预期用例与提示词的直觉。
