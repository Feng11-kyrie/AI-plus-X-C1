## Claude Code 新的 `/security-review` 命令有多有效？

Anthropic [为 Claude Code 发布了一个新命令](https://www.anthropic.com/news/automate-security-reviews-with-claude-code)，叫 `/security-review`。它的设计用途是在拉取请求上运行，检查改动的文件并通过提问来识别具体的安全问题。[你可以在这里找到它的提示词](https://github.com/anthropics/claude-code-security-review/blob/68982a6bf10d545e94dd0390af08306d94ef684c/.claude/commands/security-review.md)。

在整个代码库上运行该命令时，我们发现识别出的安全问题相当有限。很多时候，它找不到那些我们让 Claude Code 一次专门搜寻某一类安全问题时所得到的发现。

我们在 PY-APP-003、PY-APP-002 与 PY-APP-008 上运行了这个命令，在全部三个应用上只找到了一处 XSS——这与我们在整体实验中得到的结果相差很大。
