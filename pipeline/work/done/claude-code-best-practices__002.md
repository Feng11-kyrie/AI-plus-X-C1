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
