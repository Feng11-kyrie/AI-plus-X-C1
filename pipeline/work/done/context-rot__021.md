## LLM 评判器对齐

我们在 NIAH 与 LongMemEval 实验中都使用 LLM 评判器来评估输出。这些评判器通过以下流程校准到人类判断：

1. 人工标注一部分模型输出为错误／正确（NIAH 约 500 条，LongMemEval 约 600 条）
2. 用 GPT-4.1 对同一部分模型输出标注错误／正确。
3. 计算人类与模型判断一致的比例，得到对齐分数。
4. 根据对不一致之处的人工检视，迭代提示词。
5. 重复第 2–4 步，直到对齐分数 > 0.99。

## 测试的模型

由于上下文窗口或 thinking_budget 的限制，并非全部 18 个模型都出现在每个实验中。

### Anthropic

- Claude Opus 4
- Claude Sonnet 4
- Claude Sonnet 3.7
- Claude Sonnet 3.5
- Claude Haiku 3.5

### OpenAI

- o3
- GPT-4.1
- GPT-4.1 mini
- GPT-4.1 nano
- GPT-4o
- GPT-4 Turbo
- GPT-3.5 Turbo
