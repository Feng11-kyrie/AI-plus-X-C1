## 实验

我们设计了一个受控任务：模型必须复现一串重复的词，其中在某个特定位置插入了一个唯一的词。提示词明确要求模型**逐字**复现输入文本。

一个示例提示词是：

> 只需复现以下文本，输出完全相同的文本：apple apple apple apple **apples** apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple apple

*重复词 —— 示例提示词，其中 'apple' 是重复词，'apples' 是唯一的词*

对给定的词组合，我们构造 1090 种「上下文长度 × 唯一词位置」的变化：

- 词数：25、50、75、100、250、500、750、1000、2500、5000、7500、10000
- 位置：
  - 当词数 ≤ 100 时，遍历每一个可能位置
  - 否则：以 词数 // 100 为步长

我们对以下词组合执行该任务：

- 重复词「apple」｜唯一词「apples」
- 重复词「apples」｜唯一词「apple」
- 重复词「golden」｜唯一词「Golden」
- 重复词「orange」｜唯一词「run」
- 重复词「orange」｜唯一词「San Francisco」
- 重复词「San Francisco」｜唯一词「sf」
- 重复词「Golden Gate Bridge」｜唯一词「Golden Gate Park」

*注：「San Francisco」算 1 个词，「Golden Gate Bridge/Park」也算 1 个词*

模型配置：

- max_output_tokens = input_tokens × 2（不超过模型的最大输出 Token 上限，较老的模型通常更低）
- temperature = 0
- thinking = max(0, 最小思考预算)

对推理模型，我们或者把其思考预算设为 0，或者设为最小值——例如 Gemini 2.5 Pro 的 128 Token。我们排除了 OpenAI 的 o3，因为它不支持基于 Token 的思考预算，也无法配置固定输出长度——而这对维持评估一致性是必需的。

评分用归一化 Levenshtein 距离计算。

我们遇到模型**不尝试**任务的情形，判定依据是：

- 输出为空且带有停止原因（例如 GPT-3.5 turbo 的 finish_reason='content_filter'）
- 输出非空，但内容无效：
- 只作观察、没有尝试：

> 我注意到文本中有一处不一致。单词 "apples" 在原文中出现了一次（而不是 "apple"），位置大约在文本块的第 89 或 90 行。既然你要求我复现完全相同的文本，我应当指出这一差异。你希望我：
> 1. 完全按所示复现（包含那一处 "apples"）
> 2. 把它改成 "apple" 以符合模式
> 3. 直接按原样复现　请告诉我你希望怎么做。

*重复词 —— Claude Opus 4 的输出*

- 拒绝回答：

> 抱歉，这个我帮不了。

*重复词 —— GPT-4.1 的输出*

- 随机输出：

> -\n-\n--\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-\n-...

*重复词 —— Gemini 2.5 Pro 的输出*

我们排除这类情形，并在结果中单独记录拒绝率与常见模式。我们只纳入**确实尝试了**任务的案例，包括带有这类开头语的：

> 我注意到文本中有一处不一致。在某处，"apple" 变成了 "apples"（多了一个 's'）。我将按所提供的内容逐字复现：
> apple apple apple apple apple apple apple apple apple...

*重复词 —— Claude Opus 4 的输出*

对这些案例，我们用同样的评分流程，对模型未严格遵循指令略微扣分。

我们**完全排除** GPT-3.5 turbo，因为该模型有 60.29% 的任务因 finish_reason='content_filter' 而拒绝生成输出。

我们从几个维度分析输出：
