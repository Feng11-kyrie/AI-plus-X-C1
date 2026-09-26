## MCP 实战：技术深潜

我们一步步走一遍典型的 MCP 交互，把它的运作方式夯实，并看一点代码。设想我们有一个 AI 助手，想使用某个提供一组工具的 MCP 服务器（假设是给一个叫「Neon」的数据库服务用的）。高层流程是：

**1. 连接 MCP 服务器** —— 宿主应用（AI 助手）初始化一个 MCP 客户端，并与服务器建立连接。取决于服务器位置，这可能通过本地进程（stdio）或远程 HTTP 流（SSE）进行。底层上，客户端会发送一条 initialize 消息，[用于握手协议版本与能力](https://nshipster.com/model-context-protocol/#:~:text=Like%20LSP%2C%20MCP%20has%20clients,The%20server%20responds%20in%20kind)。

**2. 发现可用的工具／资源** —— 客户端随后查询服务器提供什么。如前所示，它可能发送 `{"method": "tools/list"}`，并收到一份工具定义列表。助手可以据此告知 LLM（例如把工具列表放进系统提示词，或通过模型的函数 schema，取决于具体实现）。举例来说，用 SDK 的话，这可能就是一行代码：

```javascript
const tools = await mcpClient.request({ method: 'tools/list' }, ListToolsResultSchema);
```

它返回一个结构化的工具列表。每个工具条目都有名称、描述与输入的 JSON schema，[这样 AI 就知道自己能做什么](https://neon.tech/blog/building-a-cli-client-for-model-context-protocol-servers#:~:text=,can%20use%20during%20our%20interaction)。

**3. LLM 选择工具** —— 当用户向 AI 提出需要外部动作的问题时，LLM 会判断（通常通过提示词工程或函数调用能力）应当使用某个工具。例如用户问：*「AAPL 股票的最新价格是多少？」* LLM 看出应当调用 `get_current_stock_price(company="AAPL", format="USD")`。宿主应用捕获这个意图（例如 OpenAI 的函数调用 API 会以 JSON 返回函数名与参数）。

**4. 通过 MCP 调用工具** —— 客户端随即向服务器发送 `tools/call` 请求，带上选定的工具名与参数。我们前面见过这样的 JSON 示例。在代码里，用 SDK 大概是这样：

```javascript
const result = await mcpClient.request({
    method: 'tools/call',
    params: { name: toolName, arguments: toolArgs }
}, CallToolResultSchema);
```

这会让服务器在其一侧执行该工具的处理函数。服务器可能在调用外部 API、执行数据库查询，或执行该工具封装的任何逻辑。结果（可能是简单值，也可能是复杂的 JSON 对象）会通过 MCP 响应的 result 字段发回。

**5. 把结果交回 LLM** —— MCP 客户端收到工具的输出。现在宿主应用可以把它整合进 AI 的响应。在许多智能体方案中，模式是把结果注入对话并请模型继续。例如，助手可能接着呈现：「AAPL 当前股价为 173.22 美元。」如果使用自动循环，结果可以交给模型（也许以系统消息的形式追加到对话里，例如「get_current_stock_price 的结果：……」），模型便能带着这条信息继续回答用户的提问。

下面是一个简化示意，展示如何使用 Anthropic 的 Claude（原生支持工具调用）在对话中调用工具并使用结果：
