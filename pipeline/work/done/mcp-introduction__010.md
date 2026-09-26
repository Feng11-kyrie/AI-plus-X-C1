```javascript
// 1. Send user prompt to LLM with available tools context
const response = await anthropicClient.complete({
  prompt: "User: Can you list my projects?\nAssistant: ",
  model: "claude-3.5",
  tools: tools // list of tools from MCP server
});
for (const msg of response.messages) {
  if (msg.type === 'tool_use') {
    // 2. LLM decided to use a tool
    const { name, args } = msg;
    // 3. Call the tool via MCP
    const toolRes = await mcpClient.request({ method: 'tools/call', params: { name, arguments: args } });
    // 4. Inject tool result and resume LLM
    await anthropicClient.send({ role: 'system', content: `Tool result: ${toolRes.result}` });
  } else {
    // 5. Handle normal LLM reply (tool result likely integrated)
    console.log("Assistant:", msg.content);
  }
}
```

现实中，框架会替你处理其中大量工作，但上面的伪代码勾勒出 MCP 如何嵌入这个循环。关键在于：**MCP 为工具执行提供了标准化的调用／响应层**，AI 智能体代码可以挂接进去。无论你用的是 OpenAI、Anthropic 还是别的 LLM，MCP 都保持不变——它是模型意图与外部动作之间的黏合剂。

使用 MCP，开发者得到一条清晰、结构化的管线来扩展 AI 能力。代码变得更好维护（因为各处调用的是通用的 `mcpClient.request`，而不是按服务分别写代码），AI 也变得更强（因为它能接入任何支持 MCP 的服务）。调试同样更容易——你可以监控 JSON-RPC 消息，准确看到请求了什么、返回了什么，而不必去解析模型生成的文本来猜线索。
