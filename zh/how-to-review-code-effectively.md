<!-- source: source/pages/how-to-review-code-effectively.html -->
<!-- week: 7 | chunks: 13 -->

作为 GitHub 的一名资深工程师，[代码评审](https://github.com/features/code-review)是我日常工作中主要关注的领域之一。过去八年里，我评审了超过 7,000 个拉取请求。为什么这么多？因为代码评审对构建优质软件至关重要，而**另一双眼睛**往往能发现你本来会漏掉的问题。

我把代码评审视为自己工作中最重要的部分之一。事实上，每当我看到同事有拉取请求等待评审，我宁愿放下自己手头的分支，先去评审他们提出的改动。毕竟，他们的拉取请求已经闯过了持续集成（CI）的重重关卡，也达到了作者自己判断的「完成」标准，所以它大概比我那些还在进行中的工作更接近可交付状态。与其在自己代码上再多耗上无法预估的时间，我更愿意先把他们的代码送上终点线。

我越早给出反馈——「这里可能是 nil，会导致报错」「这看起来是个 n+1 查询」「这里最好能有个方法签名」——这些反馈就能越早被处理，bug 就越早被消灭，功能就越早发布。

我想分享自己是怎么做代码评审的，希望我们都能交出更好的代码。

## 什么是代码评审？

严格来说，代码评审——在 GitHub 上体现为[拉取请求评审](https://docs.github.com/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews)——允许协作者对拉取请求中提出的改动发表评论、表示赞同，或在合并之前要求进一步修改。

我把拉取请求看作一场对话的开端。我把它读成作者在说「我认为这比我们现在的做法更好」。代码评审是塑造产品实现方式的绝佳机会。作为代码评审者，我的职责是与作者来回讨论，通过提问、质疑假设、以及总体上充当第二双眼睛来改进他们的代码。

## 微调你的代码评审流程

### 如何找到待评审的拉取请求

我就住在我的 [GitHub 通知收件箱](https://github.com/notifications?query=is:unread)里。它是我浏览器里固定打开的少数几个标签页之一，所以随时可用。每当我在等 CI、在两个任务之间、刚开始一天工作，或者手头正好有点空，我都会去看一眼收件箱。我评审的多数拉取请求都是在那里发现的。GitHub 的各团队往往有一个当作大本营的 Slack 频道，那是分享「待评审」拉取请求的好地方——这也是我发现拉取请求的另一条主要途径。

我还常用 [GitHub Slack 集成](https://slack.github.com/)把某个 Slack 频道订阅到我团队相关的新拉取请求上，效果不错。为了筛选哪些拉取请求会出现在 Slack 里，我会用一个团队专属标签，然后在 Slack 里用类似 `/github subscribe your/repo pulls +label:"your-team-label"` 的命令来订阅。

我喜欢用这样的查询去找可能需要评审的未决拉取请求：`is:open archived:false is:pr org:github -is:draft team-review-requested:github/relevant-codeowner-team`。用这个查询，我能找到 GitHub 组织内[处于打开状态](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-open-or-closed-state)、[未归档](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-based-on-whether-a-repository-is-archived)的[拉取请求](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-only-issues-or-pull-requests)，[且位于 GitHub 组织之内](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests#search-within-a-users-or-organizations-repositories)、不是[草稿](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-for-draft-pull-requests)，并且[把相关代码所有者团队列为被请求的评审者](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer)。我通常会省掉 [`review:required`](https://docs.github.com/search-github/searching-on-github/searching-issues-and-pull-requests#search-by-pull-request-review-status-and-reviewer) 这个搜索限定符，因为即使同事已经评审过，我也有兴趣自己看一遍。毕竟评审代码不只是帮作者，也帮我自己跟上那些影响我所负责代码的变更。

### 用评审者团队管理通知

你不会希望代码改动去 ping 一个庞大的团队，以致团队里每个人都觉得评审这个改动**[不是自己的责任](https://en.wikipedia.org/wiki/Diffusion_of_responsibility)**。那会导致拉取请求要么无人评审地搁置，要么在本该再等等的时候就被合并——因为关键评审者在一大堆通知里错过了它。这两种情况都会影响产品质量。

如果可以，我建议精简你所加入的[代码所有者](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)团队数量，让你的通知保持在可管理的范围内。这样，落进你收件箱的拉取请求就不只是噪声，而是你真心觉得该去评审的东西。宽泛的「万能」代码所有者团队作为兜底尚可，但不适合作为自动评审请求的第一线默认选择。把仓库的 CODEOWNERS 文件维护得井井有条，并配合定义清晰的代码边界，既能限制通知量，也能帮评审者避免通知疲劳。

限制团队通知的另一个办法是：建立一个「一线响应者」团队，然后用自动化按排班增删团队成员。这样你的团队可以专注于日常的代码库，而被排入值班的一线响应者会收到本团队服务区域内拉取请求的通知。例如，你可以用 [PagerDuty API](https://developer.pagerduty.com/api-reference/3f03afb2c84a4-get-a-schedule) 判断某一天谁是一线响应者，再用 [Octokit 库](https://docs.github.com/rest/using-the-rest-api/libraries-for-the-rest-api?apiVersion=2022-11-28#official-github-libraries)来增删团队成员。

### 用自动化在各团队间统一代码评审

仓库级别的配置与自动化，例如使用 [CODEOWNERS 文件](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners#codeowners-file-location)与[分支保护规则](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/managing-a-branch-protection-rule)，有助于在各团队间强制执行评审流程标准。而另一些标准——比如拉取请求里什么值得评论——则必须由我们人来维护。把你们团队内部的代码评审运作方式写下来，确保任何参与代码评审或提交拉取请求的人都知道：如何让自己的拉取请求被评审、预期的评审周转时间是多久，以及有哪些自动化在辅助评审。

有些团队用项目看板来跟踪有哪些拉取请求进入评审；我见过这在管理共享 API 的团队里效果很好——那类区域经常被团队之外的人修改。另一些团队只依赖 GitHub 通知，我见过这在代码所有权边界清晰、且团队能严格做到「来了就评」时效果很好。

如果你遵循的是本团队特有的流程，自动化可以帮助你向团队之外的人传达预期。例如，如果有很多其他团队依赖你团队的评审，你可以用机器人自动在任何请求你团队评审的拉取请求下留言，告诉作者大概什么时候能收到回复。

## 什么样的代码评审算好，什么样算差？

好的代码评审带来清晰度，并推动代码走向比原先更好的状态。

作为评审者，**沟通清晰是关键**。你要让人清楚哪些评论属于个人偏好、哪些是批准前的阻塞项。为你想建议的做法给出示例，能提升评审质量、也让你的意思更清楚。如果你能给出与拉取请求同一个仓库里的例子，那就更好了——它通过鼓励一致的实现方式，进一步支撑你的建议。

相比之下，糟糕的代码评审缺乏清晰度。例如，不带任何评论的一揽子批准或否决，会让拉取请求作者怀疑这次评审到底有没有认真做。哪怕只是在批准时重述一遍你对作者意图的理解，也能暴露出你和作者的理解是否一致。

如果一次代码评审没说清建议应该在什么时候落实，对作者来说体验也会很差。指出「现有未改动的代码应当重构」或「还应处理另一种情况」都没问题，但**必须说明这些是否是批准的前置条件**。如果这个拉取请求不采纳你的建议也可以合入，一定要说清楚。保持较小的 diff、把这些改动作为单独的拉取请求分别交付，可能更稳妥。

**下面这条评审评论既具体，又清楚传达了建议的实现方式：**

*「我看到你的新方法沿用了这个文件里现有的风格，接收了 [X] 个参数。参数这么多会损害可读性，也意味着这个函数做的事太多了。你觉得在后续的拉取请求里把这个方法以及现有的几个一起重构、减少参数数量怎么样？」*

**这条评论好在哪：**

- 给出了具体细节。
- 引用了具体的代码或问题。
- 提出了问题的解决方向。
- 引用了证据或给出了解释

**在光谱的另一端，以下是一些本可以更好的评审评论示例：**

*「我不喜欢这个。」*——评审者不喜欢什么？他心里有没有一个可以明确说出来的替代方案？

**可能的改进：**

- 「这一行做的事太多了，我们能不能简化它来提升可读性？」
- 「我觉得这会有性能问题，因为是个 n+1 查询。」
- 「我们能不能用[首选框架]自带的方案，而不是自己写一套实现？」

*「这样不行。」*——为什么这些改动不行？

**可能的改进：**

- 「这样不行，因为 [X]，参见相关 issue：[issue 链接]。」
- 「这个之前在[拉取请求链接]里试过，因为 [X] 没成功。」
- 「如果你在 [X] 上遇到问题，可以试试[替代方案]。」

*「我觉得这修好了一个 bug。」*——我很喜欢这种点名，但有没有更多上下文，比如一个 issue 链接，能让它更清楚？

**可能的改进：**

- 「我觉得这修好了[issue 链接]。」
- 「这是在修[issue 链接]里的那个 bug 吗？」
- 「这看起来就是我们遇到过的那个 bug[失败构建的链接]。谢谢修复！」

## 如何给出好的代码评审

### 提问题

我把拉取请求作者看作对这次改动掌握最多上下文的人。我可以基于自己的经历指出我看到的问题——我在 Ruby on Rails 单体应用、TypeScript、或高流量数据库上的经验——但我信任作者对我问题的回答。我把他们对具体细节的理解放在比我更高的位置。

我也很喜欢问那些涉及代码中所做假设的问题。他们处理的数据长什么样？是否存在与该形状不符的数据？代码能很好地应对吗？这段代码是否资源密集？它的性能会好吗？作为评审者，我最喜欢的回应是作者提供一个自动化测试来验证这些场景下的行为。第二喜欢的回应是经验数据，比如来自数据仓库的查询结果，或一张 Datadog 图表，说明为什么这些场景不成问题。

作为拉取请求作者，我很感激收到提问。有人提问，就给了我空间去解释自己为什么对这次改动有信心，并在必要时引用 issue、查询或图表。它也让我能把自己的知识和经验分享给别人。作者不仅能看到我的回应，其他评审者以及未来那些想追溯某个过往决策来龙去脉的读者也能看到。

### 给出肯定

除了提问，对你赞同的部分发表评论也是好习惯。这类评论能表明你读懂了正在改什么，或验证了代码中的某个假设。以下是几个例子：

- 「看起来这与本模块其它类所用的模式一致。」
- 「谢谢你为这个加了测试！」
- 「这比之前可读性强多了。」

以我的经验，处在接收端的人也会觉得这种评论很舒服。收到代码评审有时会让人感到消耗。当我要应付来自好几方的问题与建议时，收到几条不向我索取任何东西、只是支持并肯定我已经投入的工作的评论，会是很好的提振。

### 注意偏见与假设

我们很容易让对评审者、或对其所改代码区域的偏见影响自己的评审。你会习惯某个人在某个领域工作、或有某种资历，然后默认他们知道自己在做什么——但**每个人**都会犯错。你对这些改动的审视、你那些核查对方假设或验证自己假设的问题，可能在部署之前就抓住问题。

我很推崇写测试，因为测试能去掉一部分偏见。当你写一个测试来检查代码是否正常工作时，[你不必只听作者的一面之词](https://www.youtube.com/watch?v=NIKAsGC1Iy8)，只需看测试有没有通过——当然，前提是你的测试本身写对了。😅

我也很推崇初级开发者在代码评审中向资深开发者提问，哪怕他们觉得自己的问题很傻、或答案显而易见。如果对你来说不明显，那就是合理的。对别人来说同样不会明显！把问题问出来，给作者留出写下答案的空间，也把这一点教育留给后来的人。

### 批准还是不批准

我把自己的评审看作一道**阻塞闸门**，能拦住别人改进我们的产品，因此我会非常慎重地扣下批准。我常常会有个人偏好，也会建议一些我乐于看到作者做出的可选改动，但我不会仅凭这些就扣着批准不给。如果我对某人的拉取请求有建议，但按其现状并不会搞坏生产环境、不会对用户造成负面影响、也不会引起其它问题，我就会带着这些评论批准。作者可以选择在合并之前处理我的反馈，也可以在另一个分支里跟进。

评审代码时，请留意你的建议有多重要。它值得为了被落实而推迟发布吗？它值得走完整个循环吗——作者看到反馈、做出建议的改动、等 CI、重新评审、部署，最后合并？**如果某个建议不被采纳也不会让谁的日子更难过，那就让作者自己决定改不改、什么时候改。**

[「请求修改」选项](https://docs.github.com/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request#submitting-your-review)会阻止拉取请求被合并，直到评审者回来批准它。我极少用它，因为通常感觉过于强硬。我信任我的团队知道什么时候该批准一个拉取请求，所以同事的批准可以代替我的。同样，我也信任拉取请求作者会尊重并考虑我的反馈，而不是因为别人批准了就盲目合并。我唯一会选「请求修改」的情况，是我认为存在**紧迫的安全问题**、并担心他们合并之前看不到我的顾虑。

## 如何从代码评审中获得最大收获

### 评审自己的代码

GitHub 高级软件工程师 [Paul Smith](https://github.com/paulcsmith) 教会我在请别人评审之前先评审自己的拉取请求，我也建议你这么做。先自己过一遍，对那些不明显、或如果出现在别人的拉取请求里你会追问的改动，直接在行内留言。自评审还能帮你判断一个拉取请求是不是太大了、[拆开](https://github.blog/2020-05-21-github-protips-tips-tricks-hacks-and-secrets-from-sarah-vessels/)会更好。

**特别推荐：**如果你在意让拉取请求保持小巧，可以用 [lerebear/sizeup-action](https://github.com/lerebear/sizeup-action) 自动给拉取请求打上标签，标明其复杂度与规模。

### 欢迎合并后的评审

如果我碰巧在别人来得及评审之前就合并了拉取请求，我依然欢迎他们的评审。如果我的拉取请求搞坏了什么、或有意外后果，在拉取请求上留言就等于留下线索，帮未来的读者追溯当时发生了什么！

如果我收到的是对已合并拉取请求的评审，我会像它还没合入时那样处理反馈。可能是一条评论解释我的视角，可能是开新的拉取请求来迭代我原先交付的代码，也可能是开新 issue 来记录待做的工作。

### 使用草稿拉取请求

创建新的拉取请求时，你可以选择把它设为草稿。我大量依赖[草稿阶段](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request)来表达我是否需要评审。例如，如果某个必需的 CI 构建正失败，或我还没写完，我就把它保持在草稿状态。我也倾向于对别人的拉取请求抱同样预期：如果是草稿，我默认作者还没准备好接受评审；如果标为「可以评审了」，我默认他们距离部署只差拿到足够的批准。

草稿状态意味着拉取请求尚未完成，所以在解决合并冲突或处理评审者反馈时，我会把拉取请求退回草稿。如果必须改动代码，我会先把拉取请求标为草稿，以免打扰那些已经评审过的人。当我把它改回「就绪」时，GitHub 会给那些评审者发通知，让他们能再看一遍。

### 保持风度

「用蜂蜜能抓到比醋更多的苍蝇」这句话浮现在我脑海中。我希望自己的拉取请求能得到评审，所以我乐于回复自己拉取请求下的评论——尤其当我不同意评审者的意见时。即便我不写回复，我也常常会用 👍 表示同意，或用 ❤ 说声谢谢。

我希望评审者相信他们的建议不会被遗忘，所以我通过评论让他们保持在信息流里。如果我同意他们的建议——比如进一步重构现有代码——我可能会这么说，同时也会说明为什么这次拉取请求里先不做这个改动。当我在后续的拉取请求里处理了他们的反馈，我会回来给出链接，让评审者知道他们的反馈没有被忽视。

在后续实现这些建议改动时，我也会 @ 他们，并附上一句「这处理了 @某某 在 <之前拉取请求的 URL> 中提出的反馈」。这既为其他读者提供了上下文，也是对被点名评审者的致意，把功劳归给他。

当你兑现了「稍后在别的分支处理反馈」的承诺，这有助于建立与评审者之间的信任，也让他们更放心地批准你未来的拉取请求——因为他们知道你不会留下半成品。

## 总结

代码评审对产品质量的重要性怎么强调都不过分，在 AI 生成代码的时代尤其如此。在我的职业生涯中，有许多次仅仅因为多了那双眼睛，一个 bug 被抓住了、一起故障被避免了。代码评审绝对值得投入时间，无论是花在日常评审上、梳理流程上，还是构建辅助自动化上。对开发者而言，**现在就把拉取请求评审透彻，比日后处理一个已经上线到生产环境的问题更快、也更少痛苦**。

感谢你对代码质量如此在意，愿意读我这套关于代码评审的理念。你最近查看过[自己的评审队列](https://github.com/search?q=review-requested:@me+is:open+archived:false&type=pullrequests)吗？也许现在正是把这些想法付诸行动的好时机。

如果你想进一步了解如何在 GitHub 上使用拉取请求评审，可以看看 GitHub Community 上资深 DevOps 架构师 [Mickey Gousset](https://github.com/mickeygousset) 与资深 DevOps 架构师 [Joshua Johanning](https://github.com/joshjohanning) 的这篇文章，讨论[评审拉取请求的 5 个技巧](https://github.com/orgs/community/discussions/130771)。

## 标签：

- 代码评审

## 作者

![Sarah Vessels](https://avatars.githubusercontent.com/u/82317?v=4&s=200)

资深软件工程师，GitHub
