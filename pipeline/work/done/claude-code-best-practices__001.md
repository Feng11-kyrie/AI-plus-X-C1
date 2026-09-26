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
