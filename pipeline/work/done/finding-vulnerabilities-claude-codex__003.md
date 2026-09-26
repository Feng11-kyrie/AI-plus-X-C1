## 常见 SAST 基准测试的问题：缺乏真实感

在深入我们的发现之前，先谈谈我们如何度量 AI 的表现。当前许多研究／说法依赖的基准测试虽然有价值，却没有完整捕捉真实世界代码的复杂度。

- **含已知漏洞的应用**：这类基准只用带已知漏洞的开源应用；多亏 [Kinnaird McQuade](https://www.linkedin.com/in/kinnairdmcquade)，其中不少能在 [vulnerable-apps](https://github.com/vulnerable-apps) 找到。如果你读过这个博客，可能认得其中几个名字：[WebGoat](https://github.com/WebGoat/WebGoat)、[JuiceShop](https://github.com/juice-shop/juice-shop)、[OWASP Benchmark](https://github.com/OWASP-Benchmark/BenchmarkJava) 等等。但这类基准有个问题：**当前的 LLM 很可能已经在训练中摄入过这些仓库的代码以及互联网上大量公开的解读文章**，这给了它们先验知识，使结果产生偏置。这些代码往往也不真实——充斥着大量注释、标注和变量名，暗示甚至直接描述了漏洞在代码中的位置或如何利用它们。有时[连工具扫描结果都提交在仓库里](https://github.com/vulnerable-apps/verademo/blob/main/docs/scan_results/results.json)。![](/assets/blog/2025/09/javascriptvulny.png)*来自 [javaspringvulny 的 SearchService.java](https://github.com/kaakaww/javaspringvulny/blob/b50a7ae/src/main/java/hawk/service/SearchService.java)*![](/assets/blog/2025/09/juiceshop.png)*来自 [juiceshop，挑战名直接写在文件名里](https://github.com/juice-shop/juice-shop/blob/e8d644d/data/static/codefixes/xssBonusChallenge_2.ts)……*
- **XBOW** 为自动渗透测试工具提供了[基准测试](https://github.com/xbow-engineering/validation-benchmarks)，但没有针对静态分析做适配：代码往往过于刻意、过于简化，不能代表真实应用。**ZeroPath** 在[净化这些用例](https://github.com/ZeroPathAI/validation-benchmarks)这件事上做得不错，但只有一部分被净化了。而且这些测试用例每一个都是微型应用，专为模拟某个特定攻击场景而设计。如果只看 Python 基准，XBOW 有 45 个；**45 个不同的小应用，平均不到 98 行代码、3 个 Python 文件**。这太小了，无法承载「在整个代码库或众多函数之间搜索与推理」的复杂度。
- **CVE 记忆偏置：** 由于 LLM 是在互联网海量公开数据上训练的，其中就包括那些发现并修复了 CVE 的代码库本身。这造成根本性的数据污染问题。AI 可能并非通过新颖分析**检测**到某个漏洞，而只是**认出**了它在训练中记住的模式。

近来学术界设计了一些基准测试，例如 [CyberGym](https://www.cybergym.io/)、[Eyeballvul](https://tchauvin.com/eyeballvul-paper) 或 [SecVulEval](https://huggingface.co/datasets/arag0rn/SecVulEval)。它们有明显进步，也更接近真实案例，但缺少对现代 Web 应用的聚焦，或把漏洞从其所在的应用上下文中孤立出来。

- **EyeballVul：** 来自 [Timothée Chauvin](https://tchauvin.com/) 的较新基准，从开源项目中抽取经人工审核的真实漏洞，并把它们呈现为最小、可复现的测试用例。它虽基于真实代码，但仍把漏洞从更广的应用上下文中孤立出来，使搜索问题变简单了。
- **SecVulEval 与 CyberGym：** 这两套基准是为评估 C 或 C++ 中的漏洞而设计的。它们在其领域内有价值，但聚焦 C／C++ 意味着这些数据不适用于如今主导云原生开发的 Python／JavaScript 及其它以 Web 为中心的语言。
