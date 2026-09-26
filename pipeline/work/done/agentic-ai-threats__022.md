## 结论

智能体应用既继承了 LLM 的漏洞，也继承了外部工具的漏洞，同时通过复杂工作流、自主决策与动态工具调用进一步扩大了攻击面。这放大了被攻陷后的潜在影响，可能从信息泄露、未授权访问一路升级到远程代码执行与整个基础设施被接管。正如我们的模拟攻击所示，各式各样的提示词载荷都能触发同一个弱点，凸显出这些威胁的灵活与隐蔽。

保护 AI 智能体需要的不是零敲碎打的修补，而是一套覆盖提示词加固、输入校验、安全工具集成与健壮运行时监控的纵深防御策略。

仅靠通用安全机制并不足够。组织必须采用专门构建的方案——例如 Palo Alto Networks [Prisma AIRS](https://www.paloaltonetworks.com/prisma/prisma-ai-runtime-security)——来**发现、评估与防护**智能体应用特有的威胁。

Palo Alto Networks 客户可通过以下产品更好地防范上文讨论的威胁：

[Unit 42 AI 安全评估](https://www.paloaltonetworks.com/unit42/assess/ai-security-assessment) 可帮助你主动识别最有可能针对你的 AI 环境的威胁。

如果你认为自己可能已被攻陷，或有紧急事项，请联系 [Unit 42 事件响应团队](https://start.paloaltonetworks.com/contact-unit42.html)，或致电：

- 北美：免费电话：+1 (866) 486-4842 (866.4.UNIT42)
- 英国：+44.20.3743.3660
- 欧洲与中东：+31.20.299.3130
- 亚洲：+65.6983.8730
- 日本：+81.50.1790.0200
- 澳大利亚：+61.2.4062.7950
- 印度：00080005045107

Palo Alto Networks 已与 Cyber Threat Alliance（CTA）成员分享这些发现。CTA 成员利用这些情报，快速为自身客户部署防护，并系统性地瓦解恶意网络行为者。可在 [Cyber Threat Alliance](https://www.cyberthreatalliance.org) 了解更多。
