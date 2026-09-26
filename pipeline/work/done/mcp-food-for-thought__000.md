[模型上下文协议](https://modelcontextprotocol.io/overview)（MCP）如今是件大事。它已成为让 LLM 访问他人所写工具的事实标准，而这自然就把它们变成了[智能体](https://simonwillison.net/2025/May/22/tools-in-a-loop/)。但为新的 MCP 服务器编写工具并不容易，于是人们常常提议[把现有 API 自动转换成 MCP 工具](https://blog.christianposta.com/semantics-matter-exposing-openapi-as-mcp-tools/)，通常借助 OpenAPI 元数据（[1](https://jedisct1.github.io/openapi-mcp/)、[2](https://www.gravitee.io/blog/turn-any-rest-api-into-mcp-server-inside-gravitee)）。

以我的经验，这样做行得通，但**效果并不好**。原因有几点：

## 智能体不擅长面对大量工具

众所周知，[VS Code 有 128 个工具的硬性上限](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)——但[许多模型在远未达到这个数量之前就已经难以准确调用工具了](https://arxiv.org/abs/2411.15399)。此外，每个工具及其描述都会占用宝贵的上下文窗口空间。

大多数 Web API 在设计时并未考虑这些约束！当这些 API 由代码调用时，为单个产品领域提供大量 API 并无问题；但如果每个 API 都映射成一个 MCP 工具，结果可能就不理想了。

从零开始设计的 MCP 工具通常[比单个 Web API 灵活得多](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)，每个工具往往能承担好几个独立 API 的工作。
