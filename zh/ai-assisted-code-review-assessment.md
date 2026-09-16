<!-- source: source/pdfs/ai-assisted-code-review-assessment.pdf -->
<!-- week: 7 | chunks: 9 -->

<!-- page 1 -->
arXiv:2405.13565v1 [cs.SE] 22 May 2024
Permission to make digital or hard copies of all or part of this work for personal or
classroom use is granted without fee provided that copies are not made or distributed
for profit or commercial advantage and that copies bear this notice and the full citation
on the first page. Copyrights for third-party components of this work must be honored.
For all other uses, contact the owner/author(s).
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
© 2024 Copyright held by the owner/author(s).
ACM ISBN 979-8-4007-0685-1/24/07
https://doi.org/10.1145/3664646.3665664
现代代码评审中的 AI 辅助编码实践评估
Manushree Vijayvergiya
manushree@google.com
Google
Zurich, Switzerland
Małgorzata Salawa
magorzata@google.com
Google
Zurich, Switzerland
Ivan Budiselić
ibudiselic@google.com
Google
Zurich, Switzerland
Dan Zheng
danielzheng@google.com
Google
Mountain View, USA
Pascal Lamblin
lamblinp@google.com
Google
Montreal, Canada
Marko Ivanković
markoi@google.com
Google
Zurich, Switzerland
Juanjo Carin
juanjocarin@google.com
Google
Sunnyvale, USA
Mateusz Lewko
mlewko@google.com
Google
Zurich, Switzerland
Jovan Andonov
jandonov@google.com
Google
Zurich, Switzerland
Goran Petrović
goranpetrovic@google.com
Google
Zurich, Switzerland
Daniel Tarlow
dtarlow@google.com
Google
Montreal, Canada
Petros Maniatis
maniatis@google.com
Google
Mountain View, USA
René Just∗
rjust@cs.washington.edu
University of Washington
Seattle, USA
摘要
现代代码评审是指：代码作者提交的增量代码贡献，在被提交到版本控制系统之前，先由一位或多位同行评审。现代代码评审的一个重要环节，是核查代码贡献是否符合最佳实践。其中一部分最佳实践可以自动核查，但另一些通常只能交给人工评审者。本文报告 AutoCommenter 的开发、部署与评估过程：这是一个由大语言模型驱动的系统，能够自动学习并落实编码最佳实践。我们为四种编程语言（C++、Java、Python 与 Go）实现了 AutoCommenter，并在一个大型工业环境中评估了它的表现与采纳情况。评估表明：一套端到端地学习并落实编码最佳实践的系统是可行的，且对开发者的工作流有正面影响。此外，本文还报告了把这样一个系统推广到数万名开发者时所遇到的挑战，以及由此得到的经验教训。

关键词
人工智能、代码评审、编码最佳实践

ACM 引用格式：
Manushree Vijayvergiya, Małgorzata Salawa, Ivan Budiselić, Dan Zheng,
Pascal Lamblin, Marko Ivanković, Juanjo Carin, Mateusz Lewko, Jovan An-
donov, Goran Petrović, Daniel Tarlow, Petros Maniatis, and René Just. 2024.
AI-Assisted Assessment of Coding Practices in Modern Code Review. In
Proceedings of the 1st ACM International Conference on AI-Powered Software
(AIware ’24), July 15–16, 2024, Porto de Galinhas, Brazil. ACM, New York,
NY, USA, 9 pages. https://doi.org/10.1145/3664646.3665664

CCS 概念
• 软件及其工程 → 软件验证与确认。

1 引言

与整体式代码评审（holistic code review）[8] 相比，现代代码评审 [21, 23] 多年来在开源与工业环境中自发演化。业界已经形成一套常见的同行评审准则 [5, 20, 21]，其中包含编码最佳实践。许多公司、项目乃至编程语言都以“风格指南”[1–4] 的形式正式定义这些准则，通常涵盖以下几个方面：

• 格式：行宽限制、空白与缩进的用法、圆括号与方括号的位置等；
• 命名：大小写、简洁性、描述性等；
• 文档：文件级、函数级及其它注释所要求的位置与内容；
• 语言特性：在不同代码场景中如何使用特定的语言特性；
• 代码惯用法：使用代码惯用法来提升代码的清晰性、模块化程度与可维护性。

开发者普遍对现代代码评审流程表示高度满意 [23, 28]。其主要收益之一，是让那些不熟悉该代码库、特定语言特性或常见代码惯用法的代码作者获得学习机会。在评审过程中，资深开发者会就最佳实践对代码作者进行指导，

∗ 本工作在 Google 完成。

<!-- page 2 -->
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil 除了评审（并了解）代码贡献及其影响之外。
静态分析工具，例如 linter [15]，可以自动核查代码是否符合某些最佳实践（例如格式规则），有些工具甚至能自动修复违规。然而，那些细微的准则、或带有例外情况的准则，很难整体自动核查（例如命名约定，以及遗留代码中经过论证的偏离），还有些准则根本无法用精确规则来表达（例如代码注释的清晰性与具体程度），只能依靠人的判断与开发者群体的共同知识。因此，通常仍然要由人工评审者来检查代码改动是否违反最佳实践。

代码评审流程最大的成本是时间，尤其是资深开发者的时间。即使有大量自动化、并且把流程尽量做轻，一位开发者每天也轻易就能在这件事上花掉好几个小时 [23]。

机器学习近来的进展——尤其是大语言模型（LLM）的能力——表明 LLM 适合用于代码评审自动化（例如 [11, 16, 17, 24–26]）。但在大规模部署端到端系统时所面临的软件工程挑战，仍未被探索。同样，这类系统在整体效能与用户接受度方面的外部评估也付之阙如。

本文考察：是否有可能部分自动化代码评审流程，具体而言是检测违反最佳实践的情况，从而为代码作者提供及时反馈，并让评审者把精力集中在整体功能上。具体来说，本文报告我们在 Google 的工业环境中开发、部署并评估 AutoCommenter——一个自动化代码评审助手——的经验；它目前每天被数万名开发者使用。

概括而言，本文的贡献是：

• 一套基于 LLM 的代码评审助手系统的通用架构（第 3 节）。
• 工具校准与向数万名开发者推广的说明（第 4 节）。
• 对该系统的评估（第 5 节）。
• 经验教训的总结与讨论（第 6 节）。

2 背景

AutoCommenter 是在 Google 的大型工业环境中开发的。Google 的现代代码评审实践与其它工业项目和开源项目类似 [23]。

2.1 代码评审流程

Google 的代码评审流程成熟、以变更（change）为单位、并有工具辅助。Ivanković 等人 [12] 与 Petrović 等人 [18] 对该流程做了详细总结。对代码库的每一次改动都必须至少由另一位开发者评审。每天有数万次代码库改动走完评审流程，数万名开发者以代码作者与评审者两种身份参与其中。

作者与评审者通过代码评审系统交换意见，一次评审会随着受该改动影响的文件快照逐轮推进。每条评审意见都附着在某个特定文件快照中的特定行列范围上。作者要解决一条意见，通常是在本地副本中修改该文件

Manushree Vijayvergiya 等

图 1：人工评审者发布的一条示例意见。

并导出新快照，进入下一轮代码评审。当作者与所有评审者都满意、且没有任何自动化分析在阻塞合并时，代码就被合入代码库。

代码评审流程中最费钱的部分，是代码作者与评审者“护送”一次改动所花的时间（从最初写代码，到处理评审意见、确保所有自动化分析通过，最后把改动合入代码库）。尽管流程已经用自动化系统在评审前分析代码做了优化（尤其是无需人工介入的自动代码格式化），代码评审每年仍要消耗数千开发者年。因此，哪怕只是把开销降低个位数百分点，也会转化为可观的业务影响。

2.2 最佳实践

最佳实践是指某种被认为更优的编程语言用法；最佳实践文档则描述它应当如何应用、能带来什么好处。**最佳实践 URL** 指某份最佳实践文档或其中的特定小节；**违反最佳实践**指某段没有遵循最佳实践、但可以改到遵循的代码。在上下文清楚时，我们分别用 **URL** 与 **违规** 来指代最佳实践 URL 与违反最佳实践。

Google 的中心代码库包含多种语言的代码，其中 C++、Java、Python 与 Go 各自都超过一亿行 [19]。有 15 种语言备有面向全体开发者开放的正式风格指南。其中许多语言还有额外的语言入门材料、核心库文档，以及“每周小技巧”式的通讯。这些材料虽然不像风格指南那样被严格执行，但在代码评审中被频繁引用。有些语言的这类文档多达数百页。代码作者与评审者都被要求核查代码是否遵循了全部最佳实践。

十多年前引入的一套正式机制叫“可读性（readability）”，用于确保最佳实践被一致地遵循。某种语言里专门的风格专家被称为“可读性导师”，他们指导经验不足的开发者达到对该语言的熟练 [23]。可读性导师通常用几句话概括一条最佳实践，并在意见末尾附上一个 URL 供改动作者参考。图 1 给出了一条由可读性导师发布的意见示例。

<!-- page 3 -->
AI-Assisted Assessment of Coding Practices in Modern Code Review AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

大规模预处理（周期性）　　数据集整理（按需）
训练与微调（按需）

Comment
storage
Source
repository
Input/target
format
Tensorboard
Scheduler
Worker Worker Workers
Relevant
code
comments
Worker Worker Workers Examples
(temporal
splits)
Worker Worker TPU pods
Model
checkpoints

图 2：模型训练管线的架构。

可读性流程也存在一些缺点。对作者而言，它因增加评审轮次而拉长了开发时间。对可读性导师而言，这会变成一项单调且耗时的工作。它要求掌握数百条不断演进的的最佳实践，包括识别并废弃过时的规则，并把它们（连同相关链接）记录到代码评审系统中。此外，它还要求持续跟进——有时要经过多轮迭代——以确保所有违规都已纠正。

3 方法

针对 2.1 节与 2.2 节所述的挑战，我们开发了 AutoCommenter：一个自动检测违反最佳实践情况的代码分析工具。它的目标是为代码作者提供及时反馈，并减轻人工做最佳实践评审的负担，从而让评审者能把精力放在代码功能上。

3.1 模型与任务定义

要自动化最佳实践分析，模型必须能够表示源代码、精确定位违规位置，并识别出被违反的是哪条最佳实践。我们采用传统的 transformer 思路、基于 T5 与 T5X [22]，做文本到文本的转换。

最佳实践分析是一个多任务大序列模型中的一项任务。除 T5 的标准预训练任务——跨度去噪（预测被遮蔽的 token）——之外，用于训练该模型的其它任务还包括：代码评审意见的解决、下一次编辑预测、变量重命名，以及构建错误修复 [9]。训练语料包含 30 亿条以上样本，其中最佳实践分析数据集贡献约 80 万条。模型用此类模型常见的标准交叉熵损失训练，并以最大化序列准确率指标——即对每条样本预测出完全正确的目标文本——为调优目标。

在最佳实践分析任务中，模型的输入是一个任务提示词加上源代码，目标是一个源代码位置加上一个指向被违反的最佳实践的 URL。任务提示词被格式化成一段固定文本的代码注释，使用该编程语言相应的注释风格。它用自然语言描述任务，并放在源代码之前；源代码是某个文件的直接文本表示。如果输入超过模型的上下文窗口，就会被截断。位置是源代码中的字节偏移量，URL 指向被违反的那条最佳实践。目标格式由一套领域特定语言定义，其中一种特殊情况是“空”目标——表示没有任何违规。除目标之外，模型还会输出一个 0 到 1 之间的置信度分数。

以下以 Go 语言为例给出输入/目标示例。

输入

/ / [∗ ] T a s k : C h e c k / / P a c k a g e a d d i t i o n package a d d i t i o n
l a n g u a g e p r o v i d e s b e s t Add
/ / R e t u r n a sum
func Add ( value1 , v a l u e 2 i n t ) i n t {
r e t u r n v a l u e 1 + v a l u e 2
}
p r a c t i c e s .

目标

INSERT 153 COMMENT h t t p s : / / go . d e v / d o c / comment # f u n c

输入的第一行是固定文本的任务提示词，其余部分是源代码。目标给出了位置（字节偏移 153 对应 Add 函数的起始处）以及一个 go.dev 的 URL，指向 Go 语言风格指南中该函数注释所违反的确切部分（此例中是“注释应以函数名开头”这一惯常做法）。注意，目标可能包含零个、一个或多个（拼接起来的）位置—URL 对，取决于源代码中有多少处违规。

3.2 模型训练

图 2 展示了模型训练管线的架构，它由三部分组成。我们把数据集构建拆成两步（预处理与整理），因为第一步要处理的数据量大得多，成本也显著更高。预处理这一步的产出与模型的输入/目标表示无关。这样的拆分提升了功能迭代速度——示例表示与其它示例层面的调整都能快速迭代。预处理这一步使用容错的调度系统，并周期性地抽取相关代码注释，以保证新数据随时可用。

3.2.1 大规模预处理。训练样本来自真实的代码评审数据，但并非所有代码注释都适合用于模型训练。因此，预处理这一步会识别**相关代码注释**——即人写的、包含指向某份最佳实践文档的 URL 的注释。对每条注释，预处理这一步随后收集对应的源代码与相关元数据，包括注释在源代码中的位置及其创建时间。这一步的产出是一组相关代码注释，每条都带有为模型训练整理样本所需的全部数据。

<!-- page 4 -->
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil 3.2.2 数据集整理。数据集整理是一个按需执行的单步处理，实现为 Beam1 管线。它按照 3.1 节所述的输入/目标格式，把每条相关代码注释转换成标准的 TensorFlow Example 数据结构。

3.2.3 训练与微调。整理好的样本直接用于模型训练与评估。我们在一个 TPU 集群上使用 T5X 框架 [22]，每 1000 步保存一次模型检查点，并用 Tensorboard 监控训练。

3.3 模型选择

在历史数据上做的两项内在评估，决定了我们如何选择模型检查点、置信度阈值与解码策略。第一项是在验证集与测试集上的评估，给出以文件为单位的精确率与召回率估计。第二项是在完整过往代码评审上的评估，给出每次代码评审的评论总数估计，从而指示开发者与 AutoCommenter 打交道的频繁程度。

3.3.1 在验证集与测试集上的评估。我们按时间切分数据集，以确保模型没有在验证集与测试集中代码注释的**未来**评审快照上训练过。在我们的数据集里，85% 的文件恰好只有一条相关代码注释，11% 有两条，4% 有三条及以上。

如果预测出的代码位置与 URL 与期望值一致（不计顺序），我们就认为该预测正确。

回忆一下，模型会为每个预测给出置信度分数，这引入了另一个参数：置信度低于某个阈值 𝑡 的预测可以被抑制。我们定义 𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛𝑡 为置信度大于 𝑡 的正确预测数，除以置信度大于 𝑡 的全部预测数；𝑅𝑒𝑐𝑎𝑙𝑙𝑡 的定义类似。有了这些定义，我们就能估计出：作为 𝑡 的函数，会有多少（不）正确结果被展示给用户。在训练期间，我们用 𝑃𝑟𝑒𝑐𝑖𝑠𝑖𝑜𝑛𝑡 与 𝑅𝑒𝑐𝑎𝑙𝑙𝑡 来比较模型检查点。

这种评估避免了数据泄漏，也让我们能自动评估模型表现，但它有一个局限：虽然可以合理假定某个代码评审快照上的人工注释是正确的，但它们并不完备。换句话说，某个评审快照里的代码可能按多条最佳实践都还有改进空间，而人工评审者并没有对每一条都发表（带 URL 的）评论。这可能有几个原因：

• 缺少引用：评审者可能对某个问题发表了评论，但没有附上 URL 作为引用。
• 有选择地评论：评审者可能只就某个问题评论一次，期望作者在全局范围内一并修复。
• 专长或关注点不同：评审者可能并不熟悉所有最佳实践，或者在具体某次代码评审中干脆选择不评论某个问题（例如只关注改动过的代码）。

虽然我们数据集中大多数文件只有一条相关注释，但人工检查那些“不正确”的预测后得到的零星证据表明：由于上述原因，通常可能存在多条最佳实践评论。鉴于我们的基准数据并不完备，精确率与召回率这两个度量是有噪声的。

1 https://beam.apache.org/

Manushree Vijayvergiya 等

因此我们采用下一节所述的补充评估，以增强对模型整体表现的信心。

3.3.2 在完整过往代码评审上的评估。为了准确估计真实环境中的潜在评论量，我们用某个特定的模型检查点与阈值，在一批过往代码评审上评估 AutoCommenter。预测出的评论不会被追溯地发布到代码评审系统中，而是记录进数据库以供分析。这样我们就能估计预期的发布频率——既包括以文件为粒度，也包括以整次代码评审为粒度。

由于开发者面对的 AutoCommenter 会作用于一次代码评审所涉及的全部代码改动，这项评估是投产部署前的重要一步。额外的好处是，这一步还能进一步优化并评估不同用户群体、不同编程语言等的发布频率。

3.4 推理基础设施

AutoCommenter 的核心是一个中心化的最佳实践分析服务。该服务以一个或多个待分析源文件作为输入。对每个文件，它构造模型输入（3.1 节），把它编码为标准的 TensorFlow Example 数据结构，然后查询模型。模型本身由一个模型服务提供，该服务使用 TensorFlow 的 Example 数据结构作为与领域无关的输入输出格式。最后，最佳实践分析服务执行一系列过滤步骤（第 4 节），抑制低质量预测，并返回其余预测。

3.5 IDE 与代码评审集成

开发者通过两种方式与 AutoCommenter 的分析服务交互——直接通过 IDE 插件，或间接通过代码评审系统。Google 的全体开发者都使用代码评审系统，几乎所有开发者也使用该 IDE。

AutoCommenter 的评论在 IDE 中以诊断信息的形式出现，用蓝色波浪下划线标出，覆盖相关代码片段。把鼠标悬停在带下划线的代码上，会显示完整评论以及该最佳实践的简要概括，并附有指向相关最佳实践文档的可点击链接。这些内嵌信息免去了开发者为了不熟悉的最佳实践而在 IDE 与浏览器之间来回切换的需要，从而简化了工作流。由于 IDE 中的评论需要实时生成，我们的目标是把生成评论的延迟控制在亚秒级。

在代码评审系统中，AutoCommenter 在每次更新后运行（即针对每个新的代码评审快照），一旦检测到违规就自动发布评论。自动化工具产生的评论在视觉上与人工评论相似，但背景色不同。

图 3 给出了 AutoCommenter 在代码评审系统中生成并发布的一条示例评论。注意右侧的“赞”与“踩”按钮，作者与评审者若觉得某条评论特别有用或没用，都可以点击。还要注意左侧对评审者可见的“Please fix”按钮：一旦点击，就会生成一条新评论，表示该评审者认为这条评论很重要、必须在代码合入代码库之前解决。这些反馈按钮是代码评审系统中的标准配置，出现在自动化工具（例如 [7, 13]）生成的所有评论上，为工具的用户接受度提供了信号。IDE 也提供了类似的反馈机制。

<!-- page 5 -->
AI-Assisted Assessment of Coding Practices in Modern Code Review AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

图 3：AutoCommenter 发布的一条示例评论。

4 部署

我们在 2022 年 7 月至 2023 年 10 月这段时间里，把 AutoCommenter 推广到了 Google 的全体开发者：

• 2022 年 7 月之前——团队自用（teamfooding）：即本文作者。
• 2022 年 7 月——早期采用者：约 3000 名志愿者。
• 2023 年 7 月——A/B 实验：约半数开发者。
• 2023 年 10 月起——正式可用：全体开发者。

请注意，出于工业界的保密要求，我们无法披露代码评审、开发者、文件、评论的绝对数量，也无法披露代码评审时长的分布。我们只报告相对指标（在适当之处）以及相关趋势。

我们采用迭代式改进的方式，持续评估并提升 AutoCommenter 的表现：

• 在历史数据上评估（3.3 节），以获得关于模型在该任务上表现如何的方向性认识，并据此确定阈值、选择解码策略。
• 监控并分析用户交互，以及通过反馈按钮与问题报告给出的直接反馈。
• 基于其它评估步骤中观察到的模式，做有针对性的人工评估。

图 4 展示了随时间推移，开发者对已发布的代码评审评论与 IDE 诊断信息的正负面反馈之比。虚线表示开发者每月给出的反馈点击总数。如预期的那样，在早期采用者阶段这个总数低得多。此外，由于我们在此期间主动改进 AutoCommenter，这一阶段的波动也更大。

回忆一下代码评审系统中的三个反馈按钮（图 3），它们让开发者能够对某条已发布的评论表达正面或负面情绪。我们把带“赞”或“Please fix”的评论视为正面，把带“踩”的评论视为负面；我们定义**有用率**为正面评论数与全部带反馈评论数之比。

本节其余部分描述部署过程中我们观察到的具体情况与相应的改进。

4.1 阈值与解码策略的选择

4.1.1 阈值。在部署初期，我们想谨慎地维护开发者对 AutoCommenter 的信任，于是从一个很高的置信度阈值 𝑡 = 0.98 起步。我们人工抽样了数百条结果，发现阈值以下约 80% 的预测其实仍然正确——也就是说，在 𝑡 = 0.98 时漏报率极高。此外我们观察到，Python 的预测呈现出显著不同的置信度分布，受阈值化的影响不成比例地大。我们推测原因在于训练数据集的构成（不同 URL 的数量与 URL 出现频率）以及最佳实践文档的具体程度，但更深入的探究留待未来工作。尝试按语言分别设阈值被证明无效：每种语言一个阈值，仍然无法充分刻画模型正确预测数百条不同最佳实践的能力。这导致预测出的 URL 缺乏多样性：模型倾向于对某些 URL 给出更高分数，而与其正确与否无关。这些观察促成了对 AutoCommenter 的第一次重大改动：**按 URL 设阈值**，其取值基于在验证集上的内在评估计算得出。

4.1.2 解码。在完整过往代码评审上用按 URL 阈值加贪心解码做评估后发现，AutoCommenter 在全部被改动的文件中能检测出 6% 的违规。然而其中 80% 的评论会被发布在作者并未修改的代码行上。开发者通常不会对未改动的代码采取行动。因此，AutoCommenter 会过滤掉针对未改动代码行生成的评论，把被改动文件中的评论比例降到 1.3%。为提高这一比例，我们试验了不同的解码策略：贪心（默认）、束搜索、top-k 与 top-p 采样。最终我们选定束搜索（生成 𝑛 = 4 个候选响应），它把评论发布频率提高到三倍，达到 3.9%。它还带来了显著更高的 URL 多样性：发布最频繁的 10 个 URL 占全部评论的 41%，而贪心搜索下这一比例是 80%。

在为部署选择解码策略时，延迟是另一个重要方面。虽然束搜索提高了发布频率与多样性，但推理明显变慢（延迟中位数为 2 秒）。考虑到这一延迟对于 IDE 中的交互式使用来说难以接受，我们最终决定：代码评审系统使用束搜索，IDE 使用贪心搜索。

<!-- page 6 -->
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil 4.2 抑制过时的最佳实践

在把 AutoCommenter 发布给约 3000 名自愿的早期采用者之后，我们注意到几天之内用户就提交了大量问题报告。其中许多都对应同一个 URL2，它描述的是与 Python 导入相关的最佳实践。然而在 Python 3.9 中，某些类型名的规范来源已经变了，那条最佳实践也在 2022 年初发生了变化。由于我们的训练数据延伸到 2022 年之前，其中包含了不少已经不再适用的最佳实践评论。我们意识到这是一个反复出现的模式：随着语言演进、或引入新的库，最佳实践也在演进。缓解这个问题的一种办法是：每当规则变化时，就把这类数据过滤掉并重新训练模型。但这既费时又费资源：需要完整地重新生成数据、训练模型、评估并上线。而在那之前，“过时”的模型要么必须关掉——这会造成系统停摆——要么必须抑制受影响的预测；否则系统很快就会失去开发者的信任。我们选择用条件过滤（对源代码做正则匹配）来抑制特定最佳实践的预测，原因有两个：第一，它可以动态部署并立即生效；第二，它支持对预测做细粒度过滤。

4.3 对选定评论的独立评分

早期使用几个月后，我们观察到有用率在约 54% 处进入平台期。为了弄清原因、找出改进空间并为更大范围推广做准备，我们在 2023 年 4 月做了一项独立的人工评分研究，分析了约 370 条在早期采用者部署阶段收到开发者反馈的已发布评论。

为了获得关于评论有用性的多元视角，我们招募了 15 位评分者——来自合作团队的开发者。我们请他们为 AutoCommenter 那些收到过明确用户反馈的评论打分。我们没有把原始的用户反馈展示给评分者，以免影响其评价。评分者依据所链接的最佳实践与周边代码来评估每条评论的有用性。我们要求他们关注评论的正确性，同时也考虑这条评论作为作者是否可执行（例如，一条技术上正确、但在具体场景下看起来不值得处理的评论，他们会不会去解决）。我们鼓励他们对每条评论给出自由形式的反馈。

评分者评估得出的有用率是 60%，略高于同一批评论上开发者反馈给出的 54%，但远低于我们为更大范围推广设定的 80% 目标。

这项研究最有趣的发现是：那些“没用”的评论存在清晰的模式。举几个例子：

**同时涉及多个主题、或主题过于复杂**：例如，某个 URL 指向的小节描述了与 Python linter 交互的多条准则，包括它经常触发的情形以及抑制它的办法。作者可能很难弄清某条已发布的评论究竟指的是哪一条准则、又该如何解决。类似地，C++ 中关于如何写好函数文档的指导是满满一页的密集文字。评分者经常指出：最佳实践（以及 AutoCommenter 的简要概括）与实际代码之间存在脱节，即使代码确实包含相关违规。

2 https://github.com/google/styleguide/blob/gh-pages/pyguide.md#22-imports

Manushree Vijayvergiya 等

**高质量概括的重要性**：评分者常常发现，AutoCommenter 的概括（通过抓取文档源生成，且有时缺失）未能充分说明所引准则与评论/代码之间的相关性。

**主观且有争议的主题**：一个例子是避免在库代码中使用 flag。flag 用在库里可能出问题，但有些库本身就是设计成通过 flag 配置大量特性的。此外，遗留代码可能并不遵循这条准则，评审者也不会去强制。模型没有学到这些细微差别，有时会在作者给既有库新增一个 flag 时预测出违规。

**某些准则上的系统性模型错误**：一个有趣的例子是那条提倡在 C++ vector 上优先使用成员函数 push_back 而非 emplace_back 的准则（当两个函数可用相同实参达到同样效果时）。模型学会了预测它，但在 emplace_back 确实更合适的情况下也会预测，甚至在某个无关类型恰好有一个叫 push_back 的成员函数时也会预测。

**正确但价值很低**：代码注释里句末少个句号，人工评审者通常是可以接受的。这虽然技术上正确，但让作者回到 IDE 去修，净价值可能是负的。

评分者研究带来的洞见促成了对 AutoCommenter 的两处改动。第一，该研究识别出 17 个不可执行的 URL，抑制它们之后，历史有用率在开发者反馈上从 54% 升到 66%，在评分者反馈上从 60% 升到 74%。我们又进一步分析了与这些 URL 相似、但未被评分的 URL 所关联的评论，额外抑制了 5 个。第二，我们审查并人工更新了所有高频发布 URL 的概括。这些改动加在一起，足以让我们达到下一阶段推广所需的 80% 有用率目标。

4.4 A/B 实验

2023 年 7 月，我们以 A/B 实验的形式把 AutoCommenter 部署给约半数开发者。我们把开发者随机分配到实验组（启用 AutoCommenter）与对照组（关闭 AutoCommenter）。随机化依据是开发者邮箱地址 SHA256 哈希的最后几位数字；我们还确认了两组在规模与构成上没有差异，包括任职年限、职级、编程语言与业务部门的分布。我们也确认了实验开始前，实验期间所测量的各项变量在对照组与实验组之间没有差异。实验期间的评论发布频率与预期一致（4.1 节）。

我们没有在以下任何一项上检测到统计上显著的变化：代码评审的总时长、开发者实际花在代码评审上的时间、作者与评审者之间评论—回复的轮次。但我们确实检测到编码速度略有提升。我们推测，减少为了查文档而发生的上下文切换带来了这一正面效果。更深入的探究留待未来工作。

基于这些结果，我们得出结论：没有不良影响，并于 2023 年 10 月把 AutoCommenter 部署给了全体开发者。

<!-- page 7 -->
AI-Assisted Assessment of Coding Practices in Modern Code Review 图 5：AutoCommenter 在生产环境中生成的自动评论，与训练数据里的人工评论，按 URL 统计评论数的累积分布。

5 评估

基于自 2023 年 3 月以来收集的有用率与用户反馈，我们得出结论：开发者总体对 AutoCommenter 生成的评论是满意的。我们通过分析用户反馈，持续改进数据集准备、阈值、URL 抑制与概括，以确保 AutoCommenter 对开发者工作流产生高度的正面影响。

除开发者满意度之外，在向全体 Google 开发者发布数月之后，我们还评估了 AutoCommenter 表现的另外三个方面：

（1）**评论解决率**：开发者多常修改自己的代码来解决 AutoCommenter 发布的评论？
（2）**AutoCommenter 与人工评论的对比**：AutoCommenter 的评论在多大程度上覆盖了人工评审者在评论中引用的最佳实践文档？
（3）**AutoCommenter 与 linter 的对比**：AutoCommenter 的产出在多大程度上超出了传统静态分析工具的能力？

5.1 评论解决率

开发者很少通过点击代码评审系统与 IDE 中的“赞/踩”按钮、以及代码评审系统中的“Please fix”按钮（图 3）来对 AutoCommenter 的评论给出明确反馈：代码评审系统中约 10% 的自动评论、IDE 中约 2% 的诊断信息收到了明确反馈，这与 Google 其它自动化分析的情况相当。与此同时，开发者会悬停查看 AutoCommenter 约 50% 的 IDE 诊断信息；而既有工作表明，开发者常常在不给出明确反馈的情况下就解决了自动评论 [18]。为评估开发者多常解决 AutoCommenter 的评论，我们做了一次离线分析，估计被后续代码改动解决的评论比例。

为分析评论解决情况，我们抽取了以「含有 AutoCommenter 自动评论的文件」为中心的历史改动。对每一次改动，我们抽取评论被发布时的初始快照，以及开发者最终合入代码库的那个快照。每条评论覆盖特定的行范围。我们在这两个快照之间使用基于 AST 的自动化行映射方法 [18]，以识别出模型原本

AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil

图 6：预测最频繁的前 50 个 URL 按类型分类。Linter 一列表示是否已存在、或容易构建出能检测该违规的 linter。

在第一个快照上预测过、但在合并后的快照上不再预测的评论。这样的快照对表明该评论可能已被解决；但也存在这种可能：无关的代码改动导致某条特定评论不再被预测出来。

对 6000 对快照的自动化分析显示，在 50% 的情况下，该评论在提交的快照中、于其原先发布的行位置上已不复存在。我们人工抽查了其中 40 对随机样本。我们发现，在 80% 的情况下，作者所做的改动直接解决了该已发布评论所描述的问题。因此我们估计评论解决率约为 40%，明显高于「有明确正面反馈的评论」占全部评论的比例。

5.2 AutoCommenter 与人工评论的对比

图 5 比较了 AutoCommenter 在生产环境中生成的自动评论，与训练数据中的人工评论，按（指向最佳实践文档的）唯一 URL 统计评论数的累积分布。横轴是把自动评论中曾用过的全部 URL 按频率排序后该 URL 的排名。例如，使用最频繁的 URL 排名第 1，它占全部自动评论的 9.9%。同一个 URL 在训练数据里人工撰写的评论中出现了 4.3%。总体而言，AutoCommenter 为 330 个不同 URL 创建过评论。AutoCommenter 用到的 URL 集合覆盖了历史上带最佳实践 URL 的人工评论的 68%。这是个好结果：它表明 AutoCommenter 并没有把重点放在评审者很少引用的冷门最佳实践上。

另一方面，尽管使用了束搜索，URL 多样性仍然相对偏低。前 85 个 URL 占了 AutoCommenter 创建的全部评论的 90%。同一组 URL 覆盖了带最佳实践 URL 的人工评论的 35%。在保持准确率与低延迟的同时，提升自动评论的 URL 多样性以及对最佳实践的覆盖，是我们的首要任务之一。

5.3 AutoCommenter 与 linter 的对比

为了解 AutoCommenter 在多大程度上提供了超越 linter 的价值（linter 能高效而精确地检查其中一部分最佳实践），我们抽样了预测最频繁的前 50 个违规——即图 5 中排名前 50 的 URL。对每一个抽到的

<!-- page 8 -->
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil URL，我们都检视了它的最佳实践文档，并判定 (1) 该最佳实践的类型（第 1 节），以及 (2) 是否存在、或是否容易构建出能检测相应违规的 linter。具体而言，三位在构建静态分析工具方面各自有 10 年以上经验的作者阅读了文档，并独立地对这些 URL 做了分类。关于最佳实践的类型没有分歧，但对于约 15% 的 URL 是否可以轻易构建出 linter 存在分歧。三位作者通过多数表决与讨论解决了这些分歧。分歧源自最佳实践本身含糊不清，以及那些包含多条准则的情况。例如，检查代码文档是否存在相对直截了当，但判断例外情况是否有正当理由、内容是否清晰，就未必如此。

图 6 展示了这 50 个抽样 URL 的分布，按类型、以及违规能否被 linter 检测来划分。其中 33/50（66%）的最佳实践，其违规检测超出了传统静态分析的范围。

6 经验教训

基于我们开发与部署 AutoCommenter 的经验，我们总结出几条关键教训：

• **补充传统分析**：AutoCommenter 基于 LLM 的方法能为人工评审者频繁引用的 68% 的最佳实践生成评论。其中许多超出了传统静态分析的范围。

• **内在评估与真实世界表现**：内在评估与真实世界表现可能显著背离：我们的内在评估使用真实世界人工评论的数据集，配上当时最先进的模型架构与训练方式，指向一个很有希望的模型；但最终证明，外部评估与系统改进才是成功部署的关键。

• **监控用户接受度至关重要**：哪怕只有少数几次糟糕的用户体验，也会侵蚀对自动化系统的信任。持续监控并分析真实世界反馈，对于发现这类情况并找到补救办法至关重要。就 AutoCommenter 而言，一个简单的抑制机制就足以把用户接受度大幅提升到 80% 以上，而无须在效能上做出重大牺牲。

7 相关工作

Johnson [15] 在近 50 年前的 1977 年提出了 C linter。在这 50 年里，围绕自动化静态分析产生了大量研究：Heckman 与 Williams [10] 最近的一篇文献综述识别出 17,571 篇论文。许多研究探讨开发者如何与静态分析交互。Johnson 等人 [14] 探讨了开发者在使用静态分析时面临的挑战。他们的研究结果凸显了良好集成到既有开发者工作流中的重要性，以及建立并维护对工具之信任的重要性。Vassallo 等人 [27] 探讨了开发者在不同场景（包括编码与代码评审）中如何与静态分析交互。他们同样发现，集成到既有工作流对开发者是否愿意使用这些工具起着主要作用，而结果的高质量极其重要。Beller 等人 [6] 研究了大量开源项目中静态代码分析的使用情况。除其它发现之外，他们

Manushree Vijayvergiya 等

强调：自动化分析的使用方式与应当使用的方式，会因编程语言而异。

相比之下，把机器学习用于代码分析是一个相对较新、理解也更少的领域。近期有不少公开文献（例如 Hong 等人 [11]、Li 等人 [16]、Li 等人 [17]、Thongtanunam 等人 [24]、Tufano 等人 [25]，以及 Tufano 等人 [26]）报告了模型评估并提出自动化代码评审的工具。虽然这些模型与评论文本生成任务和本文提出的模型非常相似，但其评估大多集中在历史数据集上。正如 3.3.1 节所讨论的，仅基于历史评论的内在评估有其局限，有时无法预测真实世界表现。Frömmgen 等人 [9] 最近的另一篇文献给出了一个在线系统的评估，但做的是相反的任务：从评论生成代码，而不是从代码生成评论。

8 结论

核查代码是否遵循最佳实践，是现代代码评审流程中的常见任务。有些最佳实践可以用 linter 之类的传统工具自动核查，但许多最佳实践需要资深开发者的知识与判断，这就要花时间和精力。

本文报告了我们开发、部署并评估 AutoCommenter 这一基于 LLM 的代码评审助手系统的经验。具体而言，它铺陈了从任务与模型设计，到内在评估与系统校准，再到分阶段上线与终端用户评估的整个过程。

评估结果表明：开发一套端到端系统、使其能力远超传统工具、同时获得高度的终端用户接受度，是可行的。这些结果是把复杂的代码评审助手与自动化代码评审推向部署的、令人鼓舞的第一步。

我们的首要目标是确保良好的开发者体验，因此在设计 AutoCommenter 时追求非常高的精确率。召回率虽非主要关注点，但我们认识到它的重要性，并计划探索模型与系统架构上的哪些改动可以提升召回率。例如，我们 2022 年使用的模型在当时是最先进的，但它的上下文窗口只有 2048 个 token，仅够容纳约 200 行代码。当前最先进的模型在训练时上下文窗口达数万 token，推理时超过一百万 token。这一跃升为新增功能、以及显著改进既有功能打开了空间。

9 致谢

本工作是 Google Core Systems 与 Google DeepMind 多个团队多年协作的成果。我们感谢所有团队成员与领导的支持和建议，包括 Alberto Elizondo、Alexander Frömmgen、Ballie Sandhu、Chandu Thekkath、Chris Gorgolewski、David Tattersall、Ilya Cherny、Jacob Austin、Katja Grünwedel、Kristóf Molnár、Lera Kharatyan、Luka Rimanic、Madhura Dudhgaonkar、Marc Brockschmidt、Marcus Revaj、Maxim Tabachnyk、Nina Chen、Niranjan Tulpule、Nitya Ramani、Paige Bailey、Pavel Sychev、Pierre-Antoine Manzagol、Quinn Madison、Roger Fleig、Satish Chandra、Savinee Dancs、Stoyan Nikolov、Subhodeep Moitra，以及 Vaibhav Tulsyan。

<!-- page 9 -->
现代代码评审中的 AI 辅助编码实践评估 参考文献
[1] 2024. Google Style Guides. https://google.github.io/styleguide/. Accessed:
2024-03-15.
[2] 2024. Linux kernel coding style. https://www.kernel.org/doc/html/v4.10/process/
coding-style.html. Accessed: 2024-03-15.
[3] 2024. PEP 8 – Style Guide for Python Code. https://peps.python.org/pep-0008/.
Accessed: 2024-03-15.
[4] 2024. Rust Style Guide. https://doc.rust-lang.org/nightly/style-guide/. Accessed:
2024-03-15.
[5] Alberto Bacchelli and Christian Bird. 2013. Expectations, outcomes, and chal-
lenges of modern code review. In 2013 35th International Conference on Software
Engineering (ICSE). 712–721. https://doi.org/10.1109/ICSE.2013.6606617
[6] Moritz Beller, Radjino Bholanath, Shane McIntosh, and Andy Zaidman. 2016.
Analyzing the state of static analysis: A large-scale evaluation in open source soft-
ware. In 2016 IEEE 23rd International Conference on Software Analysis, Evolution,
and Reengineering (SANER), Vol. 1. IEEE, 470–481.
[7] Zimin Chen, Małgorzata Salawa, Manushree Vijayvergiya, Goran Petrović, Marko
Ivanković, and René Just. 2023. MuRS: Mutant Ranking and Suppression using
Identifier Templates. In Proceedings of the Symposium on the Foundations of
Software Engineering (FSE). 1798–1808.
[8] M. E. Fagan. 1976. Design and code inspections to reduce errors in program
development. IBM Systems Journal 15, 3 (1976), 182–211. https://doi.org/10.1147/
sj.153.0182
[9] Alexander Frömmgen, Jacob Austin, Peter Choy, Nimesh Ghelani, Lera Kharatyan,
Gabriela Surita, Elena Khrapko, Pascal Lamblin, Pierre-Antoine Manzagol, Marcus
Revaj, Maxim Tabachnyk, Daniel Tarlow, Kevin Villela, Daniel Zheng, Satish
Chandra, and Petros Maniatis. 2024. Resolving Code Review Comments with
Machine Learning. In International Conference on Software Engineering: Software
Engineering in Practice (ICSE-SEIP).
[10] Sarah Heckman and Laurie Williams. 2011. A systematic literature review of
actionable alert identification techniques for automated static code analysis.
Information and Software Technology 53, 4 (2011), 363–387. https://doi.org/10.
1016/j.infsof.2010.12.007 Special section: Software Engineering track of the 24th
Annual Symposium on Applied Computing.
[11] Yang Hong, Chakkrit Tantithamthavorn, Patanamon Thongtanunam, and Aldeida
Aleti. 2022. Commentfinder: a simpler, faster, more accurate code review com-
ments recommendation. In Proceedings of the Joint Meeting of the European Soft-
ware Engineering Conference and the Symposium on the Foundations of Software
Engineering (ESEC/FSE). 507–519.
[12] Marko Ivanković, Goran Petrović, René Just, and Gordon Fraser. 2019. Code
Coverage at Google. In Proceedings of the Joint Meeting of the European Soft-
ware Engineering Conference and the Symposium on the Foundations of Software
Engineering (ESEC/FSE). 955–963.
[13] Marko Ivanković, Goran Petrović, Yana Kulizhskaya, Mateusz Lewko, Luka Kali-
novčić, René Just, and Gordon Fraser. 2024. Productive Coverage: Improving
the Actionability of Code Coverage. In International Conference on Software
Engineering: Software Engineering in Practice (ICSE-SEIP).
[14] Brittany Johnson, Yoonki Song, Emerson Murphy-Hill, and Robert Bowdidge.
2013. Why don’t software developers use static analysis tools to find bugs?. In
2013 35th International Conference on Software Engineering (ICSE). IEEE, 672–681.
[15] Stephen C Johnson. 1977. Lint, a C program checker. Bell Telephone Laboratories
Murray Hill.
[16] Lingwei Li, Li Yang, Huaxi Jiang, Jun Yan, Tiejian Luo, Zihan Hua, Geng Liang,
and Chun Zuo. 2022. Auger: Automatically generating review comments with
AIware ’24, July 15–16, 2024, Porto de Galinhas, Brazil
pre-training models. In Proceedings of the Joint Meeting of the European Soft-
ware Engineering Conference and the Symposium on the Foundations of Software
Engineering (ESEC/FSE). 1009–1021.
[17] Zhiyu Li, Shuai Lu, Daya Guo, Nan Duan, Shailesh Jannu, Grant Jenks, Deep
Majumder, Jared Green, Alexey Svyatkovskiy, Shengyu Fu, and Neel Sundaresan.
2022. Automating code review activities by large-scale pre-training. In Proceedings
of the 30th ACM Joint European Software Engineering Conference and Symposium
on the Foundations of Software Engineering (<conf-loc>, <city>Singapore</city>,
<country>Singapore</country>, </conf-loc>) (ESEC/FSE 2022). Association for
Computing Machinery, New York, NY, USA, 1035–1047. https://doi.org/10.1145/
3540250.3549081
[18] Goran Petrović, Marko Ivanković, Gordon Fraser, and René Just. 2023. Please fix
this mutant: How do developers resolve mutants surfaced during code review?. In
International Conference on Software Engineering: Software Engineering in Practice
(ICSE-SEIP). 150–161.
[19] Rachel Potvin and Josh Levenberg. 2016. Why Google Stores Billions of Lines
of Code in a Single Repository. Communications of the ACM (CACM) 59 (2016),
78–87. http://dl.acm.org/citation.cfm?id=2854146
[20] Peter Rigby, Brendan Cleary, Frederic Painchaud, Margaret-Anne Storey, and
Daniel German. 2012. Contemporary Peer Review in Action: Lessons from Open
Source Development. IEEE Software 29, 6 (2012), 56–61. https://doi.org/10.1109/
MS.2012.24
[21] Peter C. Rigby and Christian Bird. 2013. Convergent contemporary software peer
review practices. In Proceedings of the 2013 9th Joint Meeting on Foundations of
Software Engineering (Saint Petersburg, Russia) (ESEC/FSE 2013). Association for
Computing Machinery, New York, NY, USA, 202–212. https://doi.org/10.1145/
2491411.2491444
[22] Adam Roberts, Hyung Won Chung, Gaurav Mishra, Anselm Levskaya, James
Bradbury, Daniel Andor, Sharan Narang, Brian Lester, Colin Gaffney, Afroz
Mohiuddin, et al. 2023. Scaling up models and data with t5x and seqio. Journal
of Machine Learning Research 24, 377 (2023), 1–8.
[23] Caitlin Sadowski, Emma Söderberg, Luke Church, Michal Sipko, and Alberto
Bacchelli. 2018. Modern Code Review: A Case Study at Google. In International
Conference on Software Engineering: Software Engineering in Practice (ICSE-SEIP).
181–190.
[24] Patanamon Thongtanunam, Chanathip Pornprasit, and Chakkrit Tantithamtha-
vorn. 2022. Autotransform: Automated code transformation to support modern
code review process. In Proceedings of the International Conference on Software
Engineering (ICSE). 237–248.
[25] Rosalia Tufano, Ozren Dabić, Antonio Mastropaolo, Matteo Ciniselli, and Gabriele
Bavota. 2024. Code Review Automation: Strengths and Weaknesses of the State
of the Art. IEEE Transactions on Software Engineering (TSE) (2024).
[26] Rosalia Tufano, Simone Masiero, Antonio Mastropaolo, Luca Pascarella, Denys
Poshyvanyk, and Gabriele Bavota. 2022. Using pre-trained models to boost code
review automation. In Proceedings of the International Conference on Software
Engineering (ICSE). 2291–2302.
[27] Carmine Vassallo, Sebastiano Panichella, Fabio Palomba, Sebastian Proksch, Har-
ald C Gall, and Andy Zaidman. 2020. How developers engage with static analysis
tools in different contexts. Empirical Software Engineering 25 (2020), 1419–1457.
[28] T. Winters, T. Manshreck, and H. Wright. 2020. Software Engineering at Google:
Lessons Learned from Programming Over Time. O’Reilly Media. https://books.
google.ch/books?id=TyIrywEACAAJ
收稿日期 2024-04-05；录用日期 2024-05-04
