### 用自动化在各团队间统一代码评审

仓库级别的配置与自动化，例如使用 [CODEOWNERS 文件](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-file-location)与[分支保护规则](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)，有助于在各团队间强制执行评审流程标准。而另一些标准——比如拉取请求里什么值得评论——则必须由我们人来维护。把你们团队内部的代码评审运作方式写下来，确保任何参与代码评审或提交拉取请求的人都知道：如何让自己的拉取请求被评审、预期的评审周转时间是多久，以及有哪些自动化在辅助评审。

有些团队用项目看板来跟踪有哪些拉取请求进入评审；我见过这在管理共享 API 的团队里效果很好——那类区域经常被团队之外的人修改。另一些团队只依赖 GitHub 通知，我见过这在代码所有权边界清晰、且团队能严格做到「来了就评」时效果很好。

如果你遵循的是本团队特有的流程，自动化可以帮助你向团队之外的人传达预期。例如，如果有很多其他团队依赖你团队的评审，你可以用机器人自动在任何请求你团队评审的拉取请求下留言，告诉作者大概什么时候能收到回复。
