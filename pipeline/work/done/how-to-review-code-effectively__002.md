### 用评审者团队管理通知

你不会希望代码改动去 ping 一个庞大的团队，以致团队里每个人都觉得评审这个改动**[不是自己的责任](https://en.wikipedia.org/wiki/Diffusion_of_responsibility)**。那会导致拉取请求要么无人评审地搁置，要么在本该再等等的时候就被合并——因为关键评审者在一大堆通知里错过了它。这两种情况都会影响产品质量。

如果可以，我建议精简你所加入的[代码所有者](https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)团队数量，让你的通知保持在可管理的范围内。这样，落进你收件箱的拉取请求就不只是噪声，而是你真心觉得该去评审的东西。宽泛的「万能」代码所有者团队作为兜底尚可，但不适合作为自动评审请求的第一线默认选择。把仓库的 CODEOWNERS 文件维护得井井有条，并配合定义清晰的代码边界，既能限制通知量，也能帮评审者避免通知疲劳。

限制团队通知的另一个办法是：建立一个「一线响应者」团队，然后用自动化按排班增删团队成员。这样你的团队可以专注于日常的代码库，而被排入值班的一线响应者会收到本团队服务区域内拉取请求的通知。例如，你可以用 [PagerDuty API](https://developer.pagerduty.com/api-reference/3f03afb2c84a4-get-a-schedule) 判断某一天谁是一线响应者，再用 [Octokit 库](https://docs.github.com/rest/using-the-rest-api/libraries-for-the-rest-api?apiVersion=2022-11-28#official-github-libraries)来增删团队成员。
