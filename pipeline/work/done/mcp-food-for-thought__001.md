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
