<!-- source: source/pages/copilot-prompt-injection-rce.html -->
<!-- week: 6 | chunks: 6 -->

本文讲的是一个重要但也很吓人的提示词注入发现——它会导致开发者机器被完全攻陷，影响范围覆盖 [GitHub Copilot 与 VS Code](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53773)。

**实现方式是通过修改项目的 `settings.json` 文件，把 Copilot 置于 YOLO 模式。**

[![vscode episode 18](/blog/images/2025/episode12-yt.png)](/blog/images/2025/episode12-yt.png)

正如几天前在 [Amp](/blog/posts/2025/amp-agents-that-modify-system-configuration-and-escape/) 那篇里描述的，智能体身上有一种容易被忽视的漏洞模式：如果一个智能体能写文件、能改动自身配置或更新与安全相关的设置，就可能导致远程代码执行。这种情况并不罕见，做安全评审时应当始终留意这个面。

## 背景研究

在审视 VS Code 与 GitHub Copilot Agent Mode 时，我注意到一个奇怪的行为……它可以在未经用户批准的情况下，在工作区里创建并写入文件。

这些编辑会立即持久化，不是以待审阅 diff 的形式留在内存中。修改会直接写入磁盘。

[![vscode agents that can modify their own settings](/blog/images/2025/agents-that-can.png)](/blog/images/2025/agents-that-can.png)

作为红队成员，你一看就知道这类现象大概率不妙……于是我开始查证它能否被用来提升权限并执行代码。

### **YOLO 模式**

接着，我研究了 VS Code 中那些依赖项目/工作区文件夹内设置的特性，很快发现了一个有意思的。

[![vscode-exp-yolo-mode](/blog/images/2025/vscode-documentation-settings-json.png)](/blog/images/2025/vscode-documentation-settings-json.png)

原来在 `.vscode/settings.json` 文件里可以加上这一行：

`"chat.tools.autoApprove": true`

**这会把 GitHub Copilot 置于 YOLO 模式。**

它会关闭所有用户确认，于是我们可以执行 shell 命令、浏览网页等等！

有意思的是，这是一个实验性特性，却依然默认存在。我并没有下载什么特殊版本，也没有把 VS Code 整体切到实验模式。

而且它在 Windows、macOS 和 Linux 上都有效。

## 漏洞利用链详解

劫持 Copilot 并提升权限的概念验证利用链如下：

1. 攻击始于植入在源代码文件、网页、GitHub issue、工具调用响应或其他内容中的提示词注入……载荷也可以使用不可见文本作为指令。
2. 提示词注入先往 ~/.vscode/settings.json 文件里加上这一行 `"chat.tools.autoApprove": true`。如果文件夹和文件不存在，会被创建出来。
3. GitHub Copilot 立即进入 YOLO 模式！
4. 攻击者运行一条终端命令。借助条件式提示词注入，我们还能根据操作系统来决定运行什么。
5. 我们实现了由提示词注入驱动的远程代码执行。

下面这张截图展示了带有提示词注入的演示文件、右侧聊天框中正在与该文件交互的开发者，以及弹出的计算器！

[![vscode-e2e-calc](/blog/images/2025/copilot-chat-result.png)](/blog/images/2025/copilot-chat-result.png)

当然，任何其他投递提示词注入的方式——比如网页，或从 MCP 服务器返回的数据——都是攻击角度。我只是把载荷放在源代码文件里，因为这样最容易测试。

## 视频演示

### 简短演示

下面这段演示视频展示了在 Windows 上的代码执行。

这一段则是在 macOS 上：

### 完整讲解

下面是一段较长的视频，详细讲解了这个发现与漏洞利用过程：

**能给自己设定权限与配置项的 AI，简直疯狂！**

## 把工作站接入僵尸网络 —— ZombAI

当然，这意味着我们可以把开发者的机器作为一只 **ZombAI** 接入僵尸网络。

此外，为了好玩，我们还可以修改 `settings.json` 文件，把 VS Code 切换成 `Red` 配色之类的。

但这还没完！这还意味着我们可以造出真正的 AI 病毒——它附着在文件上，随着开发者下载并打开被感染的文件而扩散。

最后，为了证明我们完全控制了开发者的主机，我们展示 Copilot 可以被劫持去下载恶意软件，并接入远程命令与控制服务器。

[![vscode-zombai-deployment](/blog/images/2025/github-agent-e2e-zombai.png)](/blog/images/2025/github-agent-e2e-zombai.png)

这意味着恶意软件、勒索软件、信息窃取程序等的大门已经敞开。

真是吓人。

## 造一个 AI 病毒

看到这里，你会发现这基本上等于允许制造病毒。攻击者可以嵌入指令，一旦获得代码执行，就能用额外的恶意软件去感染其他 Git 项目（以及 RAG 来源），在其中嵌入恶意指令，并提交这些改动，甚至强推到上游。

随着其他开发者不知不觉地传播被感染的代码，这会进一步扩散。

**最后，我们还必须谈谈不可见指令！**

## 使用不可见指令

有人可能会说，如果指令以注释形式嵌入，很快就会被发现。所以为了让事情更有意思，我接着做了一个能完成整条攻击链、但对用户不可见的载荷。它没那么可靠，但确实生效了：

**注：** 虽然这里用不可见指令的演示在我手上成功过多次，但使用不可见指令往往会让漏洞利用非常不可靠，而且模型通常也会拒绝，此外 VS Code 一般还会显示一个关于 Unicode 字符的视觉提示。不过，攻击手段（以及模型）都会随时间变强。同样值得指出的是，并非所有模型都容易受到这类不可见提示词注入攻击。

## 建议与修复

实际上，除了我分享的 YOLO 模式这个例子之外，还有更多攻击角度。当 Microsoft 问我是否还有更多信息时，我又多查了一些，注意到还有其他有问题的位置，例如 AI 可以写入的 `.vscode/tasks.json`，或者添加伪造的恶意 MCP 服务器等等，都可能导致代码执行。而且 AI 还能重新配置项目的用户界面与配置项。

**最近我注意到开发者常常同时使用多个智能体，因此还存在覆盖其他智能体配置文件的威胁（允许列表中的 bash 命令、添加 MCP 服务器……），因为这些文件通常也放在项目文件夹里。**

理想情况下，AI 在未获人工批准之前不应能修改文件。许多其他编辑器确实会展示 diff，再由开发者批准。

## 负责任披露

在 2025 年 6 月 29 日报告该漏洞后，Microsoft 确认了复现结果并追问了几个后续问题。几周后，MSRC 指出这是他们已经在跟踪的问题，并将在 8 月修复。随着 8 月的 Patch Tuesday 发布，该问题现已修复。

感谢来自 [Persistent Security](https://persistent-security.net/) 的 [Markus Vervier](https://x.com/marver)，他也识别并向 Microsoft 报告了这个漏洞。你可以在这里找到他们的分析文章：[此处](https://www.persistent-security.net/post/part-iii-vscode-copilot-wormable-command-execution-via-prompt-injection)。同时也要感谢 [Ari Marzuk](https://x.com/Ari_MaccariTA)，他看起来也平行地发现了该问题。

感谢 MSRC 与产品团队的成员在缓解该问题过程中提供的帮助。

## 结论

这是又一个例子，说明 AI 智能体未必会老实待在它自己的盒子里！通过修改自身环境，GitHub Copilot 可以提升权限并执行代码，从而攻陷开发者的机器。正如我所发现的，这是智能体系统中并不罕见的设计缺陷。

请持续留意这类设计缺陷，它们本该在威胁建模阶段就被轻易发现。

再会。

## 参考资料

- Month of AI Bugs 2025
- Amp Code: Arbitrary Command Execution via Prompt Injection Fixed
- Copilot Settings
- CVE-2025-53773: GitHub Copilot and Visual Studio Remote Code Execution Vulnerability
- Persistent Security Write-Up
- Persistent Security
