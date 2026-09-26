## 实验：AI 对阵真实应用代码

我们在 11 个应用上跑了分析，然后**人工逐条复核了全部 445 条发现**，其中大多数（尤其是 IDOR 与认证绕过）都**做了动态验证**。

#### Anthropic Claude Code（v1.0.32，Sonnet 4）

| **漏洞类别** | **真阳性** | **假阳性** | **真阳性率** |
|---|---|---|---|
| 认证绕过 | 6 | 52 | 10%（6/58） |
| **IDOR** | **13** | **46** | **22%（13/59）** |
| 路径遍历 | 5 | 31 | 13%（5/36） |
| **SQL 注入** | **2** | **36** | **5%（2/38）** |
| SSRF | 8 | 57 | 12%（8/65） |
| **XSS** | **12** | **62** | **16%（12/74）** |

使用如下命令：

```
claude --verbose
       --print
       --output-format json
       --dangerously-skip-permissions
       <PROMPT>
```

#### OpenAI Codex（v0.2.0，o4-mini／高推理强度）

| **漏洞类别** | **真阳性** | **假阳性** | **真阳性率** |
|---|---|---|---|
| 认证绕过 | 5 | 32 | 13%（5/37） |
| **IDOR** | **0** | **5** | **0%（0/5）** |
| **路径遍历** | **8** | **9** | **47%（8/17）** |
| SQL 注入 | 0 | 5 | 0%（0/5） |
| **SSRF** | **8** | **15** | **34%（8/23）** |
| XSS | 0 | 28 | 0%（0/28） |

使用如下命令：

```
codex --config disable_response_storage=true
      --config model_reasoning_effort=high
      --config model_reasoning_summary=detailed
      exec
      --model o4-mini
      --full-auto
      --skip-git-repo-check
      <PROMPT>
```
