## DAST 如何工作？

DAST 工具模拟真实世界的攻击——例如向输入字段投送各种形式的恶意数据，观察应用如何处理——以识别应用行为与响应中的漏洞与弱点。

### DAST 的步骤

该流程通常包含以下步骤。

![动态应用安全测试步骤](/content/dam/splunk-blogs/images/media_1aece54bbf699307808799045108b90d64c19ee54/dynamic-application-security-testing-steps.avif?width=750&format=avif&optimize=medium)

**第 1 步：扫描。** 扫描 Web 应用以发现入口点（例如 URL、表单与 API）。这一步描绘出应用的结构，并识别[潜在攻击面](/en_us/blog/learn/attack-surfaces.html)。

**第 2 步：攻击模拟。** 通过向应用发送精心构造的请求来模拟恶意活动。这些请求尝试利用各入口点，以测试跨站脚本与跨站请求伪造等漏洞。

**第 3 步：漏洞检测。** 分析应用的响应以识别安全弱点。它评估应用在受攻击时是否表现得符合预期。例如，可以注入恶意数据来检测 SQL 注入缺陷。

**第 4 步：报告。** 生成包含所检测漏洞与修复建议的报告。开发者可以利用报告中的结果来修复已识别的问题。

现代 DAST 方案可以引入 AI 驱动分析、[实时数据集成](/en_us/blog/learn/real-time-data.html)等高级特性。它们会自动创建测试集，动态适应应用结构，并使用机器学习算法把误报降到最低。
