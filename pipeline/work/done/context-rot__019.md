我们的结果对未来的长上下文评估工作也有启示。一项常见局限——此前的长上下文基准研究也指出过——是倾向于把**输入长度**与**任务难度**混为一谈，因为更长的输入往往引入更复杂的推理。我们的实验把输入长度孤立为一个因素，并让任务难度保持恒定。未来工作的一个重要方向是厘清：模型表现退化中，有多少源于任务本身的内在难度，又有多少源于它有效处理长上下文的能力。

我们也没有解释这种表现退化背后的机制。我们的观察表明，上下文的结构属性——例如相关信息的位置或重复——会影响模型行为，但对于为什么会这样，我们还没有确切答案。研究这些效应需要更深入地探究机制可解释性，这超出了本报告的范围。

更广泛地说，我们的发现指向了**上下文工程**的重要性：审慎地构造与管理模型的上下文窗口。信息在模型上下文中的位置与呈现方式，强烈影响任务表现——这使它成为优化模型表现的一个有意义的未来工作方向。

# 结论

通过实验，我们证明 LLM 在不同输入长度下并不能保持一致的表现。即便在非字面检索或文本复现这样简单的任务上，我们也看到随输入长度增长而出现越来越明显的**非均匀性**。

我们的结果凸显了两件事：需要超越现有基准的更严格的长上下文评估，以及上下文工程的重要性。相关信息是否存在于模型上下文中并不是全部；**更重要的是这些信息是如何被呈现的**。我们证明连能力最强的模型对此也敏感，这使得有效的上下文工程成为可靠表现的必要条件。

# 脚注

[1]（2025 年 7 月 16 日）由 Kiran Vodrahalli（Google DeepMind）补充了 Latent List 的洞见并作了澄清

[2] 示例的原始来源：https://arxiv.org/pdf/2410.10813

# 参考文献

[1] Kamradt, G. (2023). Needle In A Haystack - Pressure Testing LLMs [GitHub Repository]. [Link](https://github.com/gkamradt/LLMTest_NeedleInAHaystack)

[2] Wu, D., Wang, H., Yu, W., Zhang, Y., Chang, K.-W., and Yu, D. (2025). LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory. arXiv preprint arXiv:2410.10813. [Link](https://arxiv.org/abs/2410.10813)

[3] Gemini Team, Georgiev, P., Lei, V. I., Burnell, R., Bai, L., Gulati, A., Tanzer, G., Vincent, D., Pan, Z., Wang, S., et al. (2024). Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context. arXiv preprint arXiv:2403.05530. [Link](https://arxiv.org/abs/2403.05530)

[4] OpenAI, Kumar, A., Yu, J., Hallman, J., Pokrass, M., Goucher, A., Ganesh, A., Cheng, B., McKinzie, B., Zhang, B., Koch, C., et al. (2025). Introducing GPT-4.1 in the API. [Link](https://openai.com/index/gpt-4-1/)

[5] Meta AI, (2025). The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation. [Link](https://ai.meta.com/blog/llama-4-multimodal-intelligence/)

[6] Modarressi, A., Deilamsalehy, H., Dernoncourt, F., Bui, T., Rossi, R. A., Yoon, S., and Schütze, H. (2025). NoLiMa: Long-Context Evaluation Beyond Literal Matching. arXiv preprint arXiv:2502.05167. [Link](https://arxiv.org/abs/2502.05167)

[7] Fu, H. Y., Shrivastava, A., Moore, J., West, P., Tan, C., and Holtzman, A. (2025). AbsenceBench: Language Models Can't Tell What's Missing. arXiv preprint arXiv:2506.11440. [Link](https://arxiv.org/abs/2506.11440)
