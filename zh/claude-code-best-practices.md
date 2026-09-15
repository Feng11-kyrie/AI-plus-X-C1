<!-- source: source/pages/claude-code-best-practices.html -->
<!-- week: 4 | chunks: 4 -->

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

## 你可以用它做什么

以下是使用 Claude Code 的一些方式：

自动化你一直拖着没做的事

Claude Code 会处理那些吃掉你一天时间的琐碎任务：为没有测试的代码写测试、修复整个项目里的 lint 错误、解决合并冲突、更新依赖、撰写发布说明。

```
claude "write tests for the auth module, run them, and fix any failures"
```

构建功能、修复 bug

用大白话描述你想要什么。Claude Code 会规划方案、跨多个文件编写代码，并验证它能正常工作。
遇到 bug 时，粘贴错误信息或描述症状即可。Claude Code 会在你的代码库中追踪问题、定位根因并实现修复。更多示例见
常见工作流
。

创建提交与拉取请求

Claude Code 直接与 git 协作。它会暂存改动、撰写提交信息、创建分支并打开拉取请求。

```
claude "commit my changes with a descriptive message"
```

在 CI 中，你可以用
GitHub Actions
或
GitLab CI/CD
自动化代码评审与 issue 分级处置。

用 MCP 连接你的工具

模型上下文协议（MCP）
是连接 AI 工具与外部数据源的开放标准。借助 MCP，Claude Code 可以读取 Google Drive 里的设计文档、更新 Jira 工单、拉取 Slack 数据，或使用你自己的定制工具。

用指令、技能与钩子做定制

`CLAUDE.md`
是一个放在项目根目录的 markdown 文件，Claude Code 会在每次会话开始时读取它。用它来设定编码规范、架构决策、偏好的库以及评审清单。Claude 还会在工作过程中建立
自动记忆
，跨会话保存构建命令、调试心得等经验，无需你写任何东西。
创建
自定义命令
，把团队可共享的可重复工作流打包起来，例如
/review-pr
或
/deploy-staging
。
钩子
让你在 Claude Code 动作前后运行 shell 命令，例如每次文件编辑后自动格式化，或提交前运行 lint。

运行智能体团队、构建自定义智能体

派生
多个 Claude Code 智能体
，同时处理同一任务的不同部分。由一个主导智能体协同这些工作、分配子任务并合并结果。
对于完全自定义的工作流，
Agent SDK
让你构建由 Claude Code 的工具与能力驱动的自有智能体，并完全掌控编排、工具访问与权限。

用 CLI 做管道、脚本与自动化

Claude Code 是可组合的，遵循 Unix 哲学。把日志管道进来、在 CI 中运行它，或与其他工具链式调用：

```
# Analyze recent log output
tail -200 app.log | claude -p "Slack me if you see any anomalies"

# Automate translations in CI
claude -p "translate new strings into French and raise a PR for review"

# Bulk operations across files
git diff main --name-only | claude -p "review these changed files for security issues"
```

完整命令与参数见
CLI 参考
。

安排周期性任务

按计划运行 Claude，自动化重复性工作：早晨的 PR 评审、夜间的 CI 失败分析、每周的依赖审计，或在 PR 合并后同步文档。

- 云端定时任务运行在 Anthropic 托管的基础设施上，因此即使你的电脑关机也会继续执行。可从 Web、桌面应用创建，或在 CLI 中运行 /schedule。
- 桌面定时任务运行在你的机器上，可直接访问本地文件与工具
- `/loop` 在 CLI 会话内重复某个 prompt，用于快速轮询

随时随地工作

会话并不绑定在某个单一入口上。随着上下文变化，你可以在不同环境之间迁移工作：

- 离开工位后，用 Remote Control 从手机或任意浏览器继续工作
- Message Dispatch 从手机派发任务，并打开它创建的桌面会话
- 在 Web 或 iOS 应用上启动长时间运行的任务，然后用 claude --teleport 把它拉到终端里
- 用 /desktop 把终端会话交接给桌面应用，做可视化 diff 审阅
- 从团队聊天中路由任务：在 Slack 里 @Claude 并附上 bug 报告，然后收到一个拉取请求

## 处处可用 Claude Code

每个入口都连接到同一个底层 Claude Code 引擎，因此你的 CLAUDE.md 文件、设置与 MCP 服务器在所有入口上都通用。
除了上面的
终端
、
VS Code
、
JetBrains
、
桌面
与
Web
环境之外，Claude Code 还能与 CI/CD、聊天和浏览器工作流集成：

| 我想要…… | 最佳选择 |
|---|---|
| 从手机或其他设备继续本地会话 | [Remote Control](/docs/en/remote-control) |
| 把 Telegram、Discord、iMessage 或自定义 webhook 的事件推入会话 | [Channels](/docs/en/channels) |
| 在本地启动任务，在移动端继续 | [Web](/docs/en/claude-code-on-the-web) 或 [Claude iOS 应用](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| 按周期运行 Claude | [云端定时任务](/docs/en/web-scheduled-tasks) 或 [桌面定时任务](/docs/en/desktop#schedule-recurring-tasks) |
| 自动化 PR 评审与 issue 分级处置 | [GitHub Actions](/docs/en/github-actions) 或 [GitLab CI/CD](/docs/en/gitlab-ci-cd) |
| 让每个 PR 都获得自动代码评审 | [GitHub 代码评审](/docs/en/code-review) |
| 把 Slack 里的 bug 报告转成拉取请求 | [Slack](/docs/en/slack) |
| 调试线上 Web 应用 | [Chrome](/docs/en/chrome) |
| 为自己的工作流构建自定义智能体 | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) |

## 后续步骤

安装好 Claude Code 之后，下面这些指南能帮你更进一步。

- 快速上手：走完你的第一个真实任务，从浏览代码库到提交修复
- 存储指令与记忆：用 CLAUDE.md 文件与自动记忆给 Claude 持久化指令
- 常见工作流与最佳实践：充分发挥 Claude Code 价值的模式
- 设置：按你的工作流定制 Claude Code
- 故障排查：常见问题的解决方案
- code.claude.com：演示、定价与产品详情
