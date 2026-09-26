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
