## 建议与修复

实际上，除了我分享的 YOLO 模式这个例子之外，还有更多攻击角度。当 Microsoft 问我是否还有更多信息时，我又多查了一些，注意到还有其他有问题的位置，例如 AI 可以写入的 `.vscode/tasks.json`，或者添加伪造的恶意 MCP 服务器等等，都可能导致代码执行。而且 AI 还能重新配置项目的用户界面与配置项。

**最近我注意到开发者常常同时使用多个智能体，因此还存在覆盖其他智能体配置文件的威胁（允许列表中的 bash 命令、添加 MCP 服务器……），因为这些文件通常也放在项目文件夹里。**

理想情况下，AI 在未获人工批准之前不应能修改文件。许多其他编辑器确实会展示 diff，再由开发者批准。

## 负责任披露

在 2025 年 6 月 29 日报告该漏洞后，Microsoft 确认了复现结果并追问了几个后续问题。几周后，MSRC 指出这是他们已经在跟踪的问题，并将在 8 月修复。随着 8 月的 Patch Tuesday 发布，该问题现已修复。

感谢来自 [Persistent Security](https://persistent-security.net/) 的 [Markus Vervier](https://x.com/marver)，他也识别并向 Microsoft 报告了这个漏洞。你可以在这里找到他们的分析文章：[此处](https://www.persistent-security.net/post/part-iii-vscode-copilot-wormable-command-execution-via-prompt-injection)。同时也要感谢 [Ari Marzuk](https://x.com/Ari_MaccariTA)，他看起来也平行地发现了该问题。

感谢 MSRC 与产品团队的成员在缓解该问题过程中提供的帮助。
