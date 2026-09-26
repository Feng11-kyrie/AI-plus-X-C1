Claude Code 是一款 AI 驱动的编码助手，帮助你构建功能、修复 bug、自动化开发任务。它理解你的整个代码库，能跨多个文件与工具协作完成任务。

## 开始使用

选择你的环境开始。大多数入口都需要
Claude 订阅
或
Anthropic Console
账号。终端 CLI 与 VS Code 也支持
第三方供应商
。

-

   终端

-

   VS Code

-

   桌面应用

-

   Web

-

   JetBrains

功能完整的 CLI，让你直接在终端中使用 Claude Code。在命令行里编辑文件、运行命令，管理整个项目。
安装 Claude Code，可用以下任一方式：

-

   原生安装（推荐）

-

   Homebrew

-

   WinGet

macOS、Linux、WSL：

```
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell：

```
irm https://claude.ai/install.ps1 | iex
```

Windows CMD：

```
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

如果你看到
The token '&&' is not a valid statement separator
，说明你在 PowerShell 而不是 CMD 里。请改用上面的 PowerShell 命令。当你在 PowerShell 中时，提示符会显示
PS C:\
。
Windows 需要 [Git for Windows](https://git-scm.com/downloads/win)。
如果尚未安装，请先装好。
原生安装会在后台自动更新，让你始终使用最新版本。

```
brew install --cask claude-code
```

Homebrew 安装不会自动更新。请定期运行
brew upgrade claude-code
以获取最新功能与安全修复。

```
winget install Anthropic.ClaudeCode
```

WinGet 安装不会自动更新。请定期运行
winget upgrade Anthropic.ClaudeCode
以获取最新功能与安全修复。
然后在任意项目中启动 Claude Code：

```
cd your-project
claude
```

首次使用时会提示你登录。就这样！
继续阅读快速上手 →
安装方式、手动更新或卸载说明见
高级设置
。遇到问题请访问
故障排查
。
VS Code 扩展把行内 diff、@ 提及、方案审阅与对话历史直接带到你的编辑器里。

- 为 VS Code 安装
- 为 Cursor 安装

也可以在扩展视图（Mac 上
Cmd+Shift+X
，Windows/Linux 上
Ctrl+Shift+X
）中搜索「Claude Code」。安装完成后打开命令面板（
Cmd+Shift+P
/
Ctrl+Shift+P
），输入「Claude Code」，选择
Open in New Tab
。
开始使用 VS Code →
一款独立应用，让你在 IDE 或终端之外运行 Claude Code。可视化审阅 diff、并行运行多个会话、安排周期性任务，并启动云端会话。
下载并安装：

- macOS（Intel 与 Apple Silicon）
- Windows（x64）
- Windows ARM64（仅远程会话）

安装后启动 Claude、登录，点击
Code
标签页即可开始编码。需要
付费订阅
。
进一步了解桌面应用 →
在浏览器中运行 Claude Code，无需本地安装。启动长时间运行的任务，稍后回来查看结果；处理本地没有的仓库；或并行执行多个任务。支持桌面浏览器与 Claude iOS 应用。
访问
claude.ai/code
开始编码。
开始使用 Web 版 →
一款用于 IntelliJ IDEA、PyCharm、WebStorm 及其他 JetBrains IDE 的插件，支持交互式 diff 查看与选区上下文共享。
从 JetBrains Marketplace 安装
Claude Code 插件
并重启 IDE。
开始使用 JetBrains →
