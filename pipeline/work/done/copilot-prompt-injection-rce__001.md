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
