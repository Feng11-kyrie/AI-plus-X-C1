<!-- source: source/pages/mcp-food-for-thought.html -->
<!-- week: 2 | chunks: 4 -->

[模型上下文协议](https://modelcontextprotocol.io/overview)（MCP）如今是件大事。它已成为让 LLM 访问他人所写工具的事实标准，而这自然就把它们变成了[智能体](https://simonwillison.net/2025/May/22/tools-in-a-loop/)。但为新的 MCP 服务器编写工具并不容易，于是人们常常提议[把现有 API 自动转换成 MCP 工具](https://blog.christianposta.com/semantics-matter-exposing-openapi-as-mcp-tools/)，通常借助 OpenAPI 元数据（[1](https://jedisct1.github.io/openapi-mcp/)、[2](https://www.gravitee.io/blog/turn-any-rest-api-into-mcp-server-inside-gravitee)）。

以我的经验，这样做行得通，但**效果并不好**。原因有几点：

## 智能体不擅长面对大量工具

众所周知，[VS Code 有 128 个工具的硬性上限](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)——但[许多模型在远未达到这个数量之前就已经难以准确调用工具了](https://arxiv.org/abs/2411.15399)。此外，每个工具及其描述都会占用宝贵的上下文窗口空间。

大多数 Web API 在设计时并未考虑这些约束！当这些 API 由代码调用时，为单个产品领域提供大量 API 并无问题；但如果每个 API 都映射成一个 MCP 工具，结果可能就不理想了。

从零开始设计的 MCP 工具通常[比单个 Web API 灵活得多](https://engineering.block.xyz/blog/blocks-playbook-for-designing-mcp-servers)，每个工具往往能承担好几个独立 API 的工作。

## API 会迅速耗尽上下文窗口

设想一个 API 每次返回 100 条记录，而每条记录都很宽（比如 50 个字段）。把这些结果原样发给智能体将消耗大量 Token；即便某个查询只需少数几个字段就能满足，最终每个字段还是都会进入上下文窗口。

API 通常按记录条数分页，但记录大小可能**差异极大**。一条记录可能包含一个占 100,000 [Token](https://learn.microsoft.com/en-us/dotnet/ai/conceptual/understanding-tokens) 的大文本字段，另一条则可能只占 10 个。把这些 API 结果直接塞进智能体的上下文窗口是一场赌博；有时没事，有时会直接爆掉。

数据的格式也可能是问题。如今大多数 Web API 返回 JSON，但 JSON 是 Token 效率很低的格式。看这个：

```json
[
  {
    "firstName": "Alice",
    "lastName": "Johnson",
    "age": 28
  },
  {
    "firstName": "Bob",
    "lastName": "Smith",
    "age": 35
  }
]
```

对比同样数据用 CSV 格式表达：

```csv
firstName,lastName,age
Alice,Johnson,28
Bob,Smith,35
```

CSV 数据**简洁得多**——每条记录消耗的 Token 只有一半。[通常 CSV、TSV，或（用于嵌套数据的）YAML 都是比 JSON 更好的选择](https://david-gilbertson.medium.com/llm-output-formats-why-json-costs-more-than-tsv-ebaf590bd541)。

这些问题都不是无法克服的。你可以设想自动加入工具参数，让智能体能够对字段做[投影](https://en.wikipedia.org/wiki/Projection_(relational_algebra))运算，自动截断或摘要化过大的结果，以及自动把 JSON 结果转成 CSV（嵌套数据则转 YAML）。但我见过的大多数服务器一样都没做。

## API 没有充分利用智能体独有的能力

API 返回结构化数据以供程序消费。这往往正是智能体希望从工具调用中得到的东西……但智能体**也**能处理其他更自由形式的指令。

例如，一个 `ask_question` 工具可以对某些文档执行检索增强生成（RAG）查询，然后以纯文本返回信息，用于指导下一次工具调用——完全跳过结构化数据。

再比如，一次 `search_cities` 工具调用可以既返回结构化的城市列表，**又**给出下一步该调用什么的建议：

```csv
city_name,population,country,region
Tokyo,37194000,Japan,Asia
Delhi,32941000,India,Asia
Shanghai,28517000,China,Asia

Suggestion: To get more specific information (weather, attractions, demographics), try calling get_city_details with the city_name parameter.
```

这种分层与工具链式调用[可以非常有效](https://engineering.block.xyz/blog/build-mcp-tools-like-ogres-with-layers)，而这恰恰是把 API 自动转换成工具时你会完全错失的东西。

## 如果智能体需要调用 API，它直接调就好了

像 Claude Code 这样的智能体，如今在编写并执行代码方面能力惊人，包括调用 Web API 的脚本。有人甚至据此[主张根本不需要 MCP](https://lucumr.pocoo.org/2025/7/3/tools/)！

我不同意这个结论，但我认为我们应该朝着冰球将要到达的地方滑。[智能体的沙箱化正在快速进步](https://github.com/openai/codex)，如果智能体直接调用 API 既简单又安全，那我们不如就这么做，把中间商去掉。

## 结论

智能体与 API 的典型消费者有着本质区别。从现有 API 自动生成 MCP 工具是可行的，但这样做很难**做好**。当智能体拿到的是为其独有能力与局限量身设计的工具时，它表现最好。
