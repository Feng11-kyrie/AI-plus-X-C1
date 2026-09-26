### 6. 性能优化

训练 AI 评审流程识别性能问题，例如：

- 查找 N+1 查询模式
- 检查不必要的重复计算
- 识别低效的数据结构
- 标记未经优化的资源使用

随后由人工评审者判断：

- 这里的列表推导式确实更高效吗？
- 它提升了可读性吗？
- 这个操作是不是本就该换一种数据结构？

[Graphite Agent](https://graphite.com/features/agent) 会自动识别你 PR 中的性能瓶颈，帮你在低效问题进入生产环境之前就抓住它。它的上下文分析理解你的整个代码库，从而给出可执行的性能建议。

### 流行的 AI 代码评审工具

#### Graphite Agent

[Graphite Agent](https://graphite.com/features/agent) 工具因其与开发工作流的深度集成以及对代码的上下文理解而脱颖而出。核心特性包括：

- 跨整个仓库的上下文代码理解
- 自动生成 PR 摘要与描述
- 尊重项目既有模式的智能代码建议
- 与 GitHub 的深度集成

![Graphite Agent 评论截图](/images/content/guides/ai-code-review-implementation-best-practices/Graphite Agent-comment.png)

Graphite Agent 擅长的不是理解孤立的代码片段，而是理解整个代码库，这让它的建议更相关、也更贴合项目标准。
