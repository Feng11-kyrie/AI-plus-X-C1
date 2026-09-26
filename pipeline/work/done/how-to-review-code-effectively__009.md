### 使用草稿拉取请求

创建新的拉取请求时，你可以选择把它设为草稿。我大量依赖[草稿阶段](https://docs.github.com/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request)来表达我是否需要评审。例如，如果某个必需的 CI 构建正失败，或我还没写完，我就把它保持在草稿状态。我也倾向于对别人的拉取请求抱同样预期：如果是草稿，我默认作者还没准备好接受评审；如果标为「可以评审了」，我默认他们距离部署只差拿到足够的批准。

草稿状态意味着拉取请求尚未完成，所以在解决合并冲突或处理评审者反馈时，我会把拉取请求退回草稿。如果必须改动代码，我会先把拉取请求标为草稿，以免打扰那些已经评审过的人。当我把它改回「就绪」时，GitHub 会给那些评审者发通知，让他们能再看一遍。
