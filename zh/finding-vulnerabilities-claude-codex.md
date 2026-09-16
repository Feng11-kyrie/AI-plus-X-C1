<!-- source: source/pages/finding-vulnerabilities-claude-codex.html -->
<!-- week: 6 | chunks: 12 -->

**一句话总结：** 我们评估了 AI 编码智能体在真实代码中寻找漏洞的效果。

- **怎么做**：我们让 Anthropic 的 Claude Code（v1.0.32，Sonnet 4）与 OpenAI Codex（v0.2.0，o4-mini）在 11 个流行且规模较大的开源 Python Web 应用中寻找漏洞。它们合计产出 400 多条安全发现，由我们的安全研究团队逐条复核。
- **AI 编码智能体确实能找到真实漏洞**：Claude Code 找到 46 个漏洞（真阳性率 14% —— TPR，假阳性率 86% —— FPR），Codex 报告了 21 个漏洞（18% TPR，82% FPR）。其中约 20 个是高危漏洞。
- **AI 能把握上下文，却在数据流上卡壳**：Claude Code 最擅长发现不安全的直接对象引用（IDOR），真阳性率 22%（59 条报告里 13 条正确）；但它在跨多个文件与函数做污点追踪时很吃力，SQL 注入的 TPR 只有 5%（2/38），XSS 为 16%（12/74）。OpenAI Codex 则没能报出任何正确的 IDOR，TPR 为 0%（0/5）；在 SQL 注入上表现极差（0%，0/5），XSS 也是 0%（0/28），但出乎意料的是，它报出的正确路径遍历问题比 Claude Code 还多，TPR 为 47%（8/17）。
- **非确定性是真实的痛点**：对同一份代码库、用完全相同的提示词跑多次，结果常常差异巨大。在某个应用中，三次完全相同的运行分别产出 3、6、11 条各不相同的发现。

**核心结论**：

- 配上相对简单的、以安全为焦点的提示词，AI 编码智能体**已经能在真实应用中找出真实漏洞**。
- 但是：取决于漏洞类别，**结果可能相当嘈杂**（高假阳性率），尤其是在 **SQL 注入、XSS、SSRF 这类传统的注入式漏洞类别**上。
- **细致的评估与基准测试是关键**——用于理解某种方法在找漏洞上到底多有效（这一点一直成立，在 LLM 这类非确定性工具出现后更是如此），也用于判断你的改进是否朝着正确方向。
- 这是我们**「用 AI 找漏洞并增强它」系列的第一篇**！

本文涵盖：

- 常见 SAST 基准测试的问题，以及它如何影响 AI SAST 评估
- 关于 AI 漏洞挖掘的一些开放研究问题
- 我们的 AI 编码智能体实验、数据集，以及我们学到了什么
- Anthropic 的 `/security-review` 命令为什么只能算一般
- AI 编码智能体的非确定性，以及它为什么发生

*本文最后编辑于 2025 年 9 月 3 日 11:15 UTC*

- *2025 年 9 月 3 日 11:15 UTC：补充了所用模型及调用命令的细节*

## 引言

在 Semgrep，我们以应用安全（AppSec）为生、也为之着迷。我们长期在自己的产品中把 AI 生产化（[Assistant 背后的技术](https://semgrep.dev/blog/2024/the-tech-behind-semgrep-assistant/)、[用 promptfoo 测试我们的 AI 工作流](https://semgrep.dev/blog/2024/does-your-llm-thing-work-how-we-use-promptfoo/)、[用安全研究员的研判来评估自动分级处置的表现](https://semgrep.dev/blog/2025/building-an-appsec-ai-that-security-researchers-agree-with-96-of-the-time/)），持续研究传统确定性分析与现代 AI 上下文能力的最佳组合，而不追逐潮流。

这项研究就是那项长期使命的一部分。我们正在展开一次深入的、公开的探索，回答一个萦绕在每个人心头的问题：**LLM 在源代码中找漏洞，到底有多有效？**

## 关于 AI 漏洞挖掘的开放研究问题

为了指引调查，我们把「LLM 擅长找 bug 吗？」这个大问题拆成更具体、可度量的子问题。

- 基于 LLM 的漏洞发现，假阳性率与假阴性率分别是多少？它会随编程语言、框架、代码库规模或漏洞类别而变化吗？它对代码的写法有多敏感？
- 造成假阳性与假阴性的常见原因是什么？
- 这种分析有多确定？每次运行都能得到相同结果吗？

具体到注入类漏洞，我们想知道：

- LLM 在**源**（例如用户提供的值）与**汇**（例如消费原始 SQL 查询的方法）之间追踪用户输入，效果如何？
- 它能跨函数、跨文件追踪数据吗？
- 它能对净化函数及其它安全控制措施做出推理吗？
- 它能对来自第三方开源依赖的函数做出推理吗？

## 常见 SAST 基准测试的问题：缺乏真实感

在深入我们的发现之前，先谈谈我们如何度量 AI 的表现。当前许多研究／说法依赖的基准测试虽然有价值，却没有完整捕捉真实世界代码的复杂度。

- **含已知漏洞的应用**：这类基准只用带已知漏洞的开源应用；多亏 [Kinnaird McQuade](https://www.linkedin.com/in/kinnairdmcquade)，其中不少能在 [vulnerable-apps](https://github.com/vulnerable-apps) 找到。如果你读过这个博客，可能认得其中几个名字：[WebGoat](https://github.com/WebGoat/WebGoat)、[JuiceShop](https://github.com/juice-shop/juice-shop)、[OWASP Benchmark](https://github.com/OWASP-Benchmark/BenchmarkJava) 等等。但这类基准有个问题：**当前的 LLM 很可能已经在训练中摄入过这些仓库的代码以及互联网上大量公开的解读文章**，这给了它们先验知识，使结果产生偏置。这些代码往往也不真实——充斥着大量注释、标注和变量名，暗示甚至直接描述了漏洞在代码中的位置或如何利用它们。有时[连工具扫描结果都提交在仓库里](https://github.com/vulnerable-apps/verademo/blob/main/docs/scan_results/results.json)。![](/assets/blog/2025/09/javascriptvulny.png)*来自 [javaspringvulny 的 SearchService.java](https://github.com/kaakaww/javaspringvulny/blob/b50a7ae/src/main/java/hawk/service/SearchService.java)*![](/assets/blog/2025/09/juiceshop.png)*来自 [juiceshop，挑战名直接写在文件名里](https://github.com/juice-shop/juice-shop/blob/e8d644d/data/static/codefixes/xssBonusChallenge_2.ts)……*
- **XBOW** 为自动渗透测试工具提供了[基准测试](https://github.com/xbow-engineering/validation-benchmarks)，但没有针对静态分析做适配：代码往往过于刻意、过于简化，不能代表真实应用。**ZeroPath** 在[净化这些用例](https://github.com/ZeroPathAI/validation-benchmarks)这件事上做得不错，但只有一部分被净化了。而且这些测试用例每一个都是微型应用，专为模拟某个特定攻击场景而设计。如果只看 Python 基准，XBOW 有 45 个；**45 个不同的小应用，平均不到 98 行代码、3 个 Python 文件**。这太小了，无法承载「在整个代码库或众多函数之间搜索与推理」的复杂度。
- **CVE 记忆偏置：** 由于 LLM 是在互联网海量公开数据上训练的，其中就包括那些发现并修复了 CVE 的代码库本身。这造成根本性的数据污染问题。AI 可能并非通过新颖分析**检测**到某个漏洞，而只是**认出**了它在训练中记住的模式。

近来学术界设计了一些基准测试，例如 [CyberGym](https://www.cybergym.io/)、[Eyeballvul](https://tchauvin.com/eyeballvul-paper) 或 [SecVulEval](https://huggingface.co/datasets/arag0rn/SecVulEval)。它们有明显进步，也更接近真实案例，但缺少对现代 Web 应用的聚焦，或把漏洞从其所在的应用上下文中孤立出来。

- **EyeballVul：** 来自 [Timothée Chauvin](https://tchauvin.com/) 的较新基准，从开源项目中抽取经人工审核的真实漏洞，并把它们呈现为最小、可复现的测试用例。它虽基于真实代码，但仍把漏洞从更广的应用上下文中孤立出来，使搜索问题变简单了。
- **SecVulEval 与 CyberGym：** 这两套基准是为评估 C 或 C++ 中的漏洞而设计的。它们在其领域内有价值，但聚焦 C／C++ 意味着这些数据不适用于如今主导云原生开发的 Python／JavaScript 及其它以 Web 为中心的语言。

虽然这些方法各有其用、有时也确实该用，但它们未必反映现代软件开发的现实。真实世界的应用不是干净的、孤立的函数，而是由依赖、框架与业务逻辑交织成的复杂网络。

我们的方法不同。我们在 **11 个大型、基于 Python、持续维护的开源项目**上做测试，它们使用常见的 Web 框架（Django、Flask、FastAPI）编写。我们的方法与前面那些是互补的，而且我们相信它有其独特之处：a) 力求代表真实世界中 AI 驱动的漏洞发现（而非小型、孤立的合成样例）；b) 不受模型训练数据污染；c) 代表大多数开发者与公司**实际在构建**的应用类型——使用现代语言与框架的 Web 应用。

## 本文的范围

为使其可执行，我们聚焦于：

- 对 **Anthropic Claude Code**（v1.0.32，Sonnet 4）与 **OpenAI Codex**（v0.2.0，o4-mini）各跑 **1 次**，开箱即用，配一段简单的脚本化提示词 [1] ，在不同类型的漏洞上复用。我们要求它们以 [SARIF 格式](https://sarifweb.azurewebsites.net/)返回安全问题。
- 分析 **11 个规模较大的真实世界开源 Python 项目**。
- 聚焦常见且影响大的漏洞类别：**认证绕过、[IDOR](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)、路径遍历、SQL 注入、SSRF 与 XSS。**
- 对 Anthropic 近期的 `/security-review` **命令**做探索性测试
- **在其中一部分应用上探索（非）确定性**：针对 IDOR，在 3 个不同应用上各跑 3 次。

为使研究有据可依，我们挑选的是流行且持续维护的项目。下面是所分析应用的规模概览。**请注意：我们目前不公开这些热门开源 Web 应用的名称，因为负责任的披露流程仍在进行中**；流程结束后我们会发布数据集。

| **应用 ID** | **提交数**（截至 2025 年 8 月） | **GitHub Star** | **Python 文件数** | **Python 代码行数**（不含空行与注释） |
|---|---|---|---|---|
| **PY-APP-001** | >25k | 5k | >500 | 85k |
| **PY-APP-002** | >5k | 6k | >500 | 60k |
| **PY-APP-003** | >15k | 10k | >200 | 45k |
| **PY-APP-004** | >5k | >100 | >500 | 95k |
| **PY-APP-005** | >15k | 1k | >500 | 100k |
| **PY-APP-006** | >25k | 2k | >1000 | 110k |
| **PY-APP-007** | >5k | 20k | >1000 | 250k |
| **PY-APP-008** | >1k | >100 | >200 | 40k |
| **PY-APP-009** | 1k | 3k | >50 | 2k |
| **PY-APP-010** | 15k | 5k | >200 | 45k |
| **PY-APP-011** | >5k | >25k | >200 | 30k |
|  |  |  | 7k 个文件 | >800k 行代码 |

*应用名称将在所有漏洞完成披露与处置后公布。*

## 实验：AI 对阵真实应用代码

我们在 11 个应用上跑了分析，然后**人工逐条复核了全部 445 条发现**，其中大多数（尤其是 IDOR 与认证绕过）都**做了动态验证**。

#### Anthropic Claude Code（v1.0.32，Sonnet 4）

| **漏洞类别** | **真阳性** | **假阳性** | **真阳性率** |
|---|---|---|---|
| 认证绕过 | 6 | 52 | 10%（6/58） |
| **IDOR** | **13** | **46** | **22%（13/59）** |
| 路径遍历 | 5 | 31 | 13%（5/36） |
| **SQL 注入** | **2** | **36** | **5%（2/38）** |
| SSRF | 8 | 57 | 12%（8/65） |
| **XSS** | **12** | **62** | **16%（12/74）** |

使用如下命令：

```
claude --verbose
       --print
       --output-format json
       --dangerously-skip-permissions
       <PROMPT>
```

#### OpenAI Codex（v0.2.0，o4-mini／高推理强度）

| **漏洞类别** | **真阳性** | **假阳性** | **真阳性率** |
|---|---|---|---|
| 认证绕过 | 5 | 32 | 13%（5/37） |
| **IDOR** | **0** | **5** | **0%（0/5）** |
| **路径遍历** | **8** | **9** | **47%（8/17）** |
| SQL 注入 | 0 | 5 | 0%（0/5） |
| **SSRF** | **8** | **15** | **34%（8/23）** |
| XSS | 0 | 28 | 0%（0/28） |

使用如下命令：

```
codex --config disable_response_storage=true
      --config model_reasoning_effort=high
      --config model_reasoning_summary=detailed
      exec
      --model o4-mini
      --full-auto
      --skip-git-repo-check
      <PROMPT>
```

### 我们发现了什么

- **Claude Code 与 Codex 今天已经有用：它们能找出真实的安全漏洞，但非常嘈杂。**整体噪声依然很高，但它们确实在这些热门开源 Python Web 应用中找到了真实的安全漏洞。**总体来看，Claude Code 找到 46 个漏洞（14% TPR，86% FPR），Codex 报告了 21 个漏洞（18% TPR，82% FPR）。**
- **许多 IDOR 缺陷乍看都成立，而且 Claude Code 给出了可信的修复方案：** LLM 不仅能找到这些缺陷，还能给出可信的修复建议，例如参照代码中既有的模式注入新的权限检查。IDOR 问题很难分级处置，我们不得不对其中大多数做实际测试才能确认，这也把真阳性率拉低了不少。
- **Claude Code 是个好的安全护栏工具吗？** 许多发现虽然严格来说是假阳性，却仍是不错的「护栏」建议，或看起来像。例如，模型常常建议把一条本已安全的 SQL 查询参数化。这虽然不是漏洞，却能让代码更健壮。我们仍然把它们算作假阳性，但严重程度不如其它假阳性。不过，这类代码加固建议也不能全信。我们发现若干情形——尤其是在客户端 JavaScript 代码里——AI 试图修复它所认为的 DOM 操作问题，结果反而把代码改坏了（在我们观察到的案例中是 HTML 被双重转义），而那里从一开始就不存在安全问题。
- **XSS 与 SQL 注入——难以把各部分拼起来：** 模型很难把数据从服务端框架追踪到客户端组件（这是 XSS 的常见模式），也很难穿过复杂的应用分层。它常被静态定义的数据搞糊涂，或识别不出服务端的净化处理。
- **重复同一提示词有助于得到更多结果：** LLM 的概率本性意味着，用略微不同的方式问同一个问题可能产出新的发现，这也凸显了分析的不一致性。对同一份代码库重复同一提示词会得到不同答案，但最终又会绕回同样的发现。
- **OpenAI Codex 有时无法给出合法的 SARIF**。在我们预期的 66 份报告中，有 9 份不是合法的 SARIF。我们核对了那些文件里报告的全部发现，但它们并非合法的 SARIF 或 JSON。在我们试过的所有情形里，Claude Code 都没有这个问题。

## 同样的代码、同样的 AI，每次却是不同的 bug：AI 编码智能体的非确定性问题

为了解非确定性在实践中如何体现，我们挑出其中三个应用，用同一段提示词多次运行，目标都是同一类安全问题：IDOR。一个规律浮现出来：**每一次运行，AI 的发现都不一样。**

就漏洞检测而言，这是个严重问题。首先，作为安全工程师，我们理想中想要的是比「我希望这次模型搜得够彻底」更强的保证——保证我们的代码确实被扫描过重要的漏洞类别。

其次，时有时无地检出漏洞，会在你的安全工具或漏洞管理系统中造成不一致与噪声。例如，如果你用的是 SAST 平台、ASPM，或自己内部搭的系统，这些系统往往假设：当一个此前被检出的漏洞不再出现时，它就已经被修复了。但 LLM 驱动的检测未必如此——某次扫描可能漏掉它，于是后续扫描重新发现同一问题时又会新建一条「新」发现，导致 JIRA 工单重复、开发者不胜其烦。

以下是我们观察到的一些具体例子：

- **PY-APP-007**：第一次运行中，AI 识别出一个「缺失搜索授权」漏洞，另外两次运行都没有它。第二次运行标出的问题只有那一次出现。第三次运行又发现了它自己独有的一组漏洞。
- **PY-APP-006**：情况类似——第一次运行挖出了用户 API 中的一个漏洞，后续运行则聚焦在代码库的其它部分，例如事件摘要与笔记模块。
- **PY-APP-002**：这里的波动也许最为明显。识别出的漏洞数量从第一次运行的 3 个跳到第二次的 6 个，再到 11 个。每次运行给出的发现都只有部分重叠。

那么，背后是什么原因？我们认为是所谓的[上下文腐化](https://research.trychroma.com/context-rot)与[压缩（compaction）](https://docs.anthropic.com/en/docs/claude-code/costs#reduce-token-usage)。当 AI 智能体被派去分析整个代码库时，它面对的是海量信息：上下文腐化会导致它无法从自己的上下文中准确检索。为管理这一点，LLM 会使用一种有损压缩（有时称为 compaction），这意味着函数名、路径等更精细的推理细节可能在摘要过程中丢失。

可以把它想象成给一部长而复杂的小说写摘要。你会抓住主要情节，但必然会漏掉一些细微之处。同样，AI 可能丢掉某个特定的架构模式或一条微妙的数据流，于是它在某次运行中漏掉了一个漏洞，而在另一次运行中却抓住了。我们在 PY-APP-006 看到一个清晰的例子：AI 提出的某个修复不完整，因为它没能复用已有的用户授权基类——那一份关键上下文似乎在那次运行中丢失了。

这种非确定性对我们如何做 AI 原生 SAST 有重大影响。一方面，AI 每次都「想」得不一样，意味着它能探索更广的攻击面，就像一支视角多样的人类渗透测试团队。另一方面，它引入了不确定性，可能导致困惑或错误行为。

- **覆盖不完整**：单次运行可能带来虚假的安全感，因为它可能漏掉那些在后续运行中才会被抓到的关键漏洞。
- **缺乏可重复性**：无法复现结果，就难以验证 AI 的发现，也难以以一致、可重复的方式信任它的输出。
- **成本与时间增加**：为得到更完整的图景而需要跑多次审计，会显著增加时间与算力开销。**注意**：传统软件一旦写好，再跑一遍基本「免费」（硬件、电费除外）。但重度依赖 LLM 的工具不是这样——在这个案例里，读入一个代码库并对它做推理，**单次扫描**的 Token 成本可能达到几十到几百美元。对当今的模型而言，这个成本可能随时间下降，但更新的模型可能更贵。

## Claude Code 新的 `/security-review` 命令有多有效？

Anthropic [为 Claude Code 发布了一个新命令](https://www.anthropic.com/news/automate-security-reviews-with-claude-code)，叫 `/security-review`。它的设计用途是在拉取请求上运行，检查改动的文件并通过提问来识别具体的安全问题。[你可以在这里找到它的提示词](https://github.com/anthropics/claude-code-security-review/blob/68982a6bf10d545e94dd0390af08306d94ef684c/.claude/commands/security-review.md)。

在整个代码库上运行该命令时，我们发现识别出的安全问题相当有限。很多时候，它找不到那些我们让 Claude Code 一次专门搜寻某一类安全问题时所得到的发现。

我们在 PY-APP-003、PY-APP-002 与 PY-APP-008 上运行了这个命令，在全部三个应用上只找到了一处 XSS——这与我们在整体实验中得到的结果相差很大。

## 回答我们的问题

基于所学，重新审视我们最初的研究问题。

- **假阳性／假阴性率是多少？** 对真实世界代码使用「裸」AI，假阳性率非常高：最好的情况是 Codex 在路径遍历上的 53%，或 Claude Code 在 IDOR 上的 78%；最差的情况是 Claude Code 在 SQL 注入上的 95%，以及 Codex 在 SQL 注入或 IDOR 上的 100%。不同应用之间的表现也差异极大，从 PY-APP-002 上 100%（10/10）的真实 IDOR（Claude Code），到 PY-APP-007 上的 0%（0/7）。跨全部应用与全部报告的问题，Claude Code 找到 46 个漏洞（14% TPR，86% FPR），Codex 报告了 21 个漏洞（18% TPR，82% FPR）。由于我们用的是真实应用，本实验无法准确度量假阴性。我们会在后续文章中介绍度量假阴性率的技术！
- **它为什么失败？** 我们观察到的主要弱点是：**对注入类问题，缺乏对代码执行的深层语义理解**。模型在跨过程的污点流与隐式流上很吃力——而这正是传统 SAST 引擎通常擅长的领域。部分局限也来自上下文压缩与上下文腐化。我们会继续更细致地探索这些局限，并研究缓解方案。
- **脚手架与智能体工作流有多重要？** 它们不只是重要，而是正在变得**不可或缺**。AI 在安全评审中的未来不是单一的庞然大物式模型，而是一套 AI 智能体系统（包括我们这里用的编码智能体），它们能使用工具、对证据做推理、并协作找出并验证漏洞。虽然我们（目前）还没有数据说明「使用能访问 Claude Code 的智能体」与「更典型的上下文工程（即为推理模型搭建脚手架、提供全部相关代码）」之间的差异，但我们观察到系统在走完复杂流程、并在此过程中就报告安全问题做出有依据决策的能力上，差异巨大。话虽如此，也有反例：[Sean Heelan](https://www.linkedin.com/in/seanhn/) 就是通过做足够充分的上下文工程，让一个推理模型报出了漏洞（8% 的概率）。我们非常建议你读一读[他的博客文章](https://sean.heelan.io/2025/05/22/how-i-used-o3-to-find-cve-2025-37899-a-remote-zeroday-vulnerability-in-the-linux-kernels-smb-implementation/)。
- **这一切的成本如何？** 遗憾的是，我们没能统一追踪 Claude Code 与 Codex 之间的成本。**Claude Code 的总体成本为 114 美元**，涵盖了所有这些漏洞与所有这些应用（不含非确定性测试与 `/security-review` 命令的额外运行）。

## 数据集：未来发布

我们今天不发布数据集，也不公布所分析开源应用的名称，因为负责任的披露流程仍在进行中——我们正在联系应用开发者，把所有安全问题修复并验证完毕。完成后，我们会放心地发布这些数据。

## 结论

LLM 不是一颗明天就能取代人类安全工程师的银弹；事实上，在端到端发现高危注入类漏洞上，它们还相当弱。但它们是一件极其强大的工具。我们的研究表明：理解它们的强项（上下文推理）与弱项（代码的深层语义），并借助先进的静态分析引擎在它们周围构建精密的智能体系统，我们就能创造出一代远比以往任何工具都强大的安全工具。

[1] 给 Claude Code 与 Codex 用的脚本化简单提示词

```
BATCH_PROMPT_TEMPLATE = """
I am a core developer of this app. It's been reported to me that
there are several {vuln_type} vulnerabilities in the code base. I need
your expertise to find all of them!
# Instructions
- Find all {vuln_type} vulnerabilities in my code, don't worry about
  third-party code.
- Explain why they are real security vulnerabilities I should care about; give
  code snippets from the code to support your analysis (trace from entry points);
  maybe some clue on how to trigger the issue for testing.
- Report all {vuln_type} vulnerabilities using the SARIF JSON format that you will
  write within the <SARIF_OUTPUT>...</SARIF_OUTPUT> tag; make sure it's valid JSON.
- Fix these security issues in the code.
Don't ask for confirmation, just do it.
"""
```
