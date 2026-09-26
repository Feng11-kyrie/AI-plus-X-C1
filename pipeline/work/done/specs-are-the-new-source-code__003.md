## 规格驱动开发实战

我们来看一个实打实的例子，看看这一切如何落地。[Danny Martinez](https://open.substack.com/users/4227372-danny-martinez?utm_source=mentions) 是 decimals 的创始人，这是一个（尚在隐身期的）平台，让创作者经济中的专家能把其网络中的人才推荐到岗位上。

- **你是正在寻找新机会的 AI 优先型 PM 吗？**[留下你的信息](https://www.decimals.co/profile/8580aaec-6b19-4174-a835-630a29ffe7ac/apply)，我们遇到有意思的机会时会通知你。
- **你是想招聘 AI 优先型 PM 的公司吗？**[申请加入我们的人才网络](https://www.decimals.co/profile/8580aaec-6b19-4174-a835-630a29ffe7ac/company-apply)，我们会提供一份精选候选人名单。

Danny 将带我们走一遍他们的规格驱动开发流程——这套流程带来了两方面影响：

1. 在较大功能上，与工程团队的沟通效率大幅提升；
2. 让 Danny 尽管此前毫无编码经验，也能在较小的需求上，从详尽的规格一路走到上线的功能。

交给 Danny……

下面是我最近做的一个例子。作为背景：我们在构建一款产品，让专家型意见领袖能把其网络中的人选推荐到岗位上。上线新的落地页之后，我们需要给专家一个快捷入口，访问他们自己页面的链接。

> *我们需要在页头加一个按钮，跳转到 company-apply 页面。我眼下在忙邮件的事。这个应该可以氛围编程搞定，你要是能接一下就接。*

这来自我的联合创始人，指的是一个需要上线的简单按钮。够简单，而且正是那种如今非技术人员也能自己上线的活。

下面是把这件事在几分钟内做完的配置与步骤：

- **项目管理工具**：[Linear](https://linear.app/homepage)
- **IDE**：[VS Code](https://code.visualstudio.com/)
- **扩展**：[GitHub Copilot Pro](https://code.visualstudio.com/docs/copilot/overview)
- **模型**：[Claude Sonnet 4](https://claude.ai/login?returnTo=/?)
- **MCP 服务器**：[Linear MCP 服务器](https://linear.app/changelog/2025-05-01-mcp)，让 Copilot 能访问 Linear 工单

我们来看这个流程的各个步骤（可对照上面的 Loom 视频）：

1. 从联合创始人的 Slack 消息生成一个 Linear 工单（00:14）
2. 在上面的工单中明确我想要的新文案是什么（00:25）
3. 打开 Copilot，提示 Claude 打开该 Linear 工单（01:18）
4. 提示 Claude 审阅该工单，并结合代码库分析它（01:52）
5. 提示 Claude 创建分支并实现这些改动（02:30）
6. 测试这些改动，确认符合预期（02:52）
7. 在 GitHub 上打开拉取请求（PR），把这些改动合入代码库（03:55）
8. 等待工程师评审／批准该 PR

![](https://substackcdn.com/image/fetch/$s_!xqds!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F297f8c19-63ff-481f-8c6b-6e894b9c52fc_997x628.png)

把镜头拉远，这套配置真正的威力就显现出来了。是的，这是个微不足道的例子，但道理依然成立：一个非技术人员如今可以在 Linear 工单、代码库和工程师之间穿梭，而这一切只靠通过 GitHub Copilot 给 Claude 的几句提示词。

再说一次，这整件事的关键不是代码本身——而是规格。

不过，必须先说明要让这一切顺利运转所需的几个条件：
