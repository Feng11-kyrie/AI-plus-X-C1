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
