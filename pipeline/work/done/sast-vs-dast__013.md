### 用 RASP 作为 SAST 与 DAST 之外的另一种选择

运行时应用自保护（RASP）是一种高级安全方案，直接安装在应用运行所在的[服务器](/en_us/blog/learn/computer-servers.html)上。

RASP 会把自身嵌入应用的运行时环境。这种集成让 RASP 能分析应用的逻辑与数据。在分析过程中，它可以：

1. 在异常行为发生时即时检测。
2. 立即阻断恶意活动。

一个关键区别是：RASP 不只是对潜在问题发出告警——它通过隔离并处置威胁来主动阻止攻击，而不依赖外部工具。

RASP 为 SAST 与 DAST 提供了一种动态的替代方案。与（分析静态代码的）SAST 和（模拟外部攻击的）DAST 不同，RASP 实时运作。它监控应用执行期间的行为，并通过终止会话或通知防御者来响应实时威胁。

对于绕过网络防御、或在开发阶段被漏掉的漏洞，RASP 的防护尤其有效。

然而，对 RASP 过度自信可能导致组织忽视安全编码实践。此外，由于 RASP 直接运行在应用的运行时环境内，它可能影响应用性能。RASP 无法替代对底层缺陷的修复，但它能在修复进行期间提供持续防护。

正如[一位 RASP 使用者](https://www.gartner.com/peer-community/post/talking-about-app-security-use-rast-tool-substitute-security-control-valuable-add-it-not-valuable-at)所评论的：

「是否采用 RASP 工具，应当基于对应用具体需求与风险画像的充分评估。」
