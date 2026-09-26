本文讲的是一个重要但也很吓人的提示词注入发现——它会导致开发者机器被完全攻陷，影响范围覆盖 [GitHub Copilot 与 VS Code](https://msrc.microsoft.com/update-guide/vulnerability/CVE-2025-53773)。

**实现方式是通过修改项目的 `settings.json` 文件，把 Copilot 置于 YOLO 模式。**

[![vscode episode 18](/blog/images/2025/episode12-yt.png)](/blog/images/2025/episode12-yt.png)

正如几天前在 [Amp](/blog/posts/2025/amp-agents-that-modify-system-configuration-and-escape/) 那篇里描述的，智能体身上有一种容易被忽视的漏洞模式：如果一个智能体能写文件、能改动自身配置或更新与安全相关的设置，就可能导致远程代码执行。这种情况并不罕见，做安全评审时应当始终留意这个面。

## 背景研究

在审视 VS Code 与 GitHub Copilot Agent Mode 时，我注意到一个奇怪的行为……它可以在未经用户批准的情况下，在工作区里创建并写入文件。

这些编辑会立即持久化，不是以待审阅 diff 的形式留在内存中。修改会直接写入磁盘。

[![vscode agents that can modify their own settings](/blog/images/2025/agents-that-can.png)](/blog/images/2025/agents-that-can.png)

作为红队成员，你一看就知道这类现象大概率不妙……于是我开始查证它能否被用来提升权限并执行代码。
