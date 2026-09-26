## 数据集：未来发布

我们今天不发布数据集，也不公布所分析开源应用的名称，因为负责任的披露流程仍在进行中——我们正在联系应用开发者，把所有安全问题修复并验证完毕。完成后，我们会放心地发布这些数据。

## 结论

LLM 不是一颗明天就能取代人类安全工程师的银弹；事实上，在端到端发现高危注入类漏洞上，它们还相当弱。但它们是一件极其强大的工具。我们的研究表明：理解它们的强项（上下文推理）与弱项（代码的深层语义），并借助先进的静态分析引擎在它们周围构建精密的智能体系统，我们就能创造出一代远比以往任何工具都强大的安全工具。

[1] 给 Claude Code 与 Codex 用的脚本化简单提示词

```
BATCH_PROMPT_TEMPLATE = """
I am a core developer of this app. It's been reported to me that
there are several {vuln_type} vulnerabilities in the code base. I need
your expertise to find all of them!
# Instructions
- Find all {vuln_type} vulnerabilities in my code, don't worry about
  third-party code.
- Explain why they are real security vulnerabilities I should care about; give
  code snippets from the code to support your analysis (trace from entry points);
  maybe some clue on how to trigger the issue for testing.
- Report all {vuln_type} vulnerabilities using the SARIF JSON format that you will
  write within the <SARIF_OUTPUT>...</SARIF_OUTPUT> tag; make sure it's valid JSON.
- Fix these security issues in the code.
Don't ask for confirmation, just do it.
"""
```
