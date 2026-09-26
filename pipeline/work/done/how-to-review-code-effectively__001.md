## 什么是代码评审？

严格来说，代码评审——在 GitHub 上体现为[拉取请求评审](https://docs.github.com/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)——允许协作者对拉取请求中提出的改动发表评论、表示赞同，或在合并之前要求进一步修改。

我把拉取请求看作一场对话的开端。我把它读成作者在说「我认为这比我们现在的做法更好」。代码评审是塑造产品实现方式的绝佳机会。作为代码评审者，我的职责是与作者来回讨论，通过提问、质疑假设、以及总体上充当第二双眼睛来改进他们的代码。

## 微调你的代码评审流程

### 如何找到待评审的拉取请求

我就住在我的 [GitHub 通知收件箱](https://github.com/notifications?query=is:unread)里。它是我浏览器里固定打开的少数几个标签页之一，所以随时可用。每当我在等 CI、在两个任务之间、刚开始一天工作，或者手头正好有点空，我都会去看一眼收件箱。我评审的多数拉取请求都是在那里发现的。GitHub 的各团队往往有一个当作大本营的 Slack 频道，那是分享「待评审」拉取请求的好地方——这也是我发现拉取请求的另一条主要途径。

我还常用 [GitHub Slack 集成](https://slack.github.com/)把某个 Slack 频道订阅到我团队相关的新拉取请求上，效果不错。为了筛选哪些拉取请求会出现在 Slack 里，我会用一个团队专属标签，然后在 Slack 里用类似 `/github subscribe your/repo pulls +label:"your-team-label"` 的命令来订阅。

我喜欢用这样的查询去找可能需要评审的未决拉取请求：`is:open archived:false is:pr org:github -is:draft team-review-requested:github/relevant-codeowner-team`。用这个查询，我能找到 GitHub 组织内[处于打开状态](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-open-or-closed-state)、[未归档](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-based-on-whether-a-repository-is-archived)的[拉取请求](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-only-issues-or-pull-requests)，[且位于 GitHub 组织之内](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-within-a-users-or-organizations-repositories)、不是[草稿](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-for-draft-pull-requests)，并且[把相关代码所有者团队列为被请求的评审者](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer)。我通常会省掉 [`review:required`](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer) 这个搜索限定符，因为即使同事已经评审过，我也有兴趣自己看一遍。毕竟评审代码不只是帮作者，也帮我自己跟上那些影响我所负责代码的变更。
