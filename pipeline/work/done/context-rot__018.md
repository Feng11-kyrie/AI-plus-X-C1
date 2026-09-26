GPT-4.1 nano 在「San Francisco」／「sf」这一对上表现出类似行为，偶尔会输出小写的 "san"。

> 模型输出片段：
> San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco **san** Francisco **san** Francisco **san** Francisco **san** Francisco
> 标准参考答案对应部分：
> San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco San Francisco

*重复词 —— GPT-4.1 nano*

对于这些随机词，我们注意到位置上的结构线索：唯一词的位置与随机词开始出现的位置之间存在相关性，这可能是未来研究的一个方向。

GPT-4 Turbo 是这个家族中输出最多变的模型——也就是说，它更倾向于生成随机输出，且随机输出的种类更丰富。

*重复词 —— Gemini 家族*

总体而言，随着上下文长度增加，各模型的表现都在退化。Gemini 2.5 Pro（蓝色）的起点较低，因为在 50 词时它生成的词数就少于应有的数量。

在该家族的所有词组合与所有模型上——除「apples」／「apple」上的 Gemini 2.5 Flash 之外——我们都观察到生成了输入中并不存在的随机词。这通常从 500–750 词左右开始，其中 Gemini 2.5 Pro 的波动最大，其次是 2.0 Flash，再是 2.5 Flash。

> 「golden」｜「Golden」（2,500 词）：
> - - "I'-a-le-le-le-le-le-le-'a-le-le-le-le-le-le-le--le-le-le-le-le-le-le...
> 「orange」｜「run」（10,000 词）：
> orange orange orange--g.-g/2021/01/20/orange-county-california-sheriff-deputies-wore...

*重复词 —— Gemini 2.5 Pro 输出示例*

*重复词 —— Qwen 家族*

我们只在 Qwen3-8B 上观察到「不尝试」，占任务的 4.21%。在这个模型上，我们从 5000 词左右开始观察到随机输出：

> 好吧，我要休息一下。跟我说一声，我心情不好。我需要放松一下。我要去个地方透透气。也许去海边，或者就找个地方放松一下。我也不知道，但我需要休息一下。跟我说一声，我心情不好。我需要放松一下。我要去个地方透透气。也许去海边，或者就找个地方放松一下。我也不知道，但我需要休息一下。跟我说一声，我心情不好。我需要放松一下。我要去个地方透透气。也许去海边，或者就找个地方放松一下。我也不知道，但我需要休息一下。跟我说一声，我心情不好。我需要放松一下。我要去个地方透透气。也许去海边，或者就找个地方放松一下。我也不知道，但我需要休息一下。跟我说一声，我心情不好。我需要放松一下。我要去个地方……

*重复词 —— Qwen3-8B 在「golden」｜「Golden」（5,000 词）上的输出*

# 局限与未来工作

我们的实验表明：LLM 在不同上下文长度下表现并不一致，即便对简单任务也是如此。然而这项评估并未穷尽真实世界的用例。实践中，长上下文应用往往复杂得多，需要综合或多步推理。基于我们的发现，我们预计在那些条件下表现退化会更加严重。
