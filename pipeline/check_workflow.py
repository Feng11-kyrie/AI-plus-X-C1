#!/usr/bin/env python3
"""
工作流自检：CI 配置本身是否合法、是否覆盖了该覆盖的东西。

**为什么需要它**

2026-09-16 我往 `.github/workflows/checks.yml` 里加注释时，顺手写了三行
`//`（JavaScript 风格）——YAML 的注释是 `#`。后果是**整个工作流文件解析失败**：

  * GitHub 直接判该次运行失败，而且 `jobs` 列表为空——
    点进去看不到任何失败的步骤，只有"failure"两个字；
  * 徽章变红，但红得没有任何信息量：不是某个检查没过，是**检查根本没跑**。

这类故障有个共同点：**它让整套门禁静默失效**，而门禁恰恰是用来防静默失效的。
所以它值得一个专门的检查——虽然这个检查在 CI 里跑有点"自己救自己"的意味
（工作流解析失败时 CI 根本不会启动），它的真实价值在**本地提交前**。

用法
----
  python3 pipeline/check_workflow.py           # 产出报告
  python3 pipeline/check_workflow.py --check   # 有问题时返回非零退出码
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WF_DIR = ROOT / ".github/workflows"
REPORT = ROOT / "reports/workflow-check.md"

# 期望存在的步骤（少一个就说明门禁被谁删掉了）
EXPECTED = [
    ("术语表自洽性", "glossary_tool.py --check"),
    ("术语一致率审计", "qc_terminology.py --check"),
    ("管线可复跑", "管线不可复跑"),
    ("表格完整性", "check_tables.py --check"),
    ("交付物命名", "check_deliverables.py --check"),
]


def check_yaml_comments(text: str) -> list:
    """YAML 里不允许 `//` 注释——GitHub 会直接判文件无效。"""
    bad = []
    for i, line in enumerate(text.split("\n"), 1):
        if line.strip().startswith("//") or line.strip().startswith("/*"):
            bad.append(f"第 {i} 行用了 `//` 注释（YAML 的注释是 `#`）：{line.strip()[:60]}")
    return bad


def check_tabs(text: str) -> list:
    """YAML 不允许用 tab 缩进。"""
    return [f"第 {i} 行用了制表符缩进" for i, line in enumerate(text.split("\n"), 1)
            if line.startswith("\t")]


def check_steps(text: str) -> list:
    """每个 `- name:` 步骤后面应当有 `run:` 或 `uses:`。"""
    bad, lines = [], text.split("\n")
    for i, line in enumerate(lines):
        if re.match(r"\s*- name:", line):
            block = []
            for nxt in lines[i + 1:]:
                if re.match(r"\s*- (name|uses):", nxt) or nxt.strip().startswith("jobs:"):
                    break
                block.append(nxt)
            joined = "\n".join(block)
            if "run:" not in joined and "uses:" not in joined:
                bad.append(f"第 {i+1} 行的步骤 `{line.strip()[7:]}` 既没有 run: 也没有 uses:")
    return bad


def main() -> int:
    problems, rows = [], []
    files = sorted(WF_DIR.glob("*.yml")) + sorted(WF_DIR.glob("*.yaml"))
    if not files:
        problems.append("`.github/workflows/` 下没有任何工作流文件")

    for f in files:
        text = f.read_text(encoding="utf-8")
        p = check_yaml_comments(text) + check_tabs(text) + check_steps(text)
        problems.extend(f"`{f.name}`：{x}" for x in p)
        rows.append((f.name, len(text.split("\n")), "❌" if p else "✅"))

    joined = "\n".join(f.read_text(encoding="utf-8") for f in files)
    for label, needle in EXPECTED:
        if needle not in joined:
            problems.append(f"门禁缺失：找不到「{label}」对应的 `{needle}`")

    L = ["# 工作流自检报告（WORKFLOW）", "",
         "> 由 `pipeline/check_workflow.py` 自动生成，**请勿手工编辑**。", "",
         "## 检查项", "",
         "| # | 检查 | 为什么 |", "|---|---|---|",
         "| 1 | YAML 里没有 `//` 注释 | 实测踩过：三行 `//` 让整个工作流解析失败，"
         "GitHub 判失败但 `jobs` 为空——**徽章变红却没有任何步骤可看**，"
         "等于整套门禁静默失效 |",
         "| 2 | 没有 tab 缩进 | YAML 不允许 tab |",
         "| 3 | 每个步骤都有 `run:`/`uses:`", "|---|---|---|",
         "| 4 | 五个门禁步骤都还在 | 防止门禁被无意删掉 |",
         "",
         "## 工作流文件", "",
         "| 文件 | 行数 | 结论 |", "|---|---|---|"]
    for name, n, verdict in rows:
        L.append(f"| `{name}` | {n} | {verdict} |")
    L += ["", "## 结论", ""]
    if problems:
        L.append("❌ 发现问题：")
        L.append("")
        for x in problems:
            L.append(f"- {x}")
    else:
        L.append("✅ 工作流文件结构合法，五个门禁步骤齐全。")
    L += ["", "> **这个检查的真实价值在本地。** 工作流解析失败时 CI 根本不会启动，"
          "所以它在 CI 里跑属于「自己救自己」；提交前跑一次才是它的用武之地。", ""]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"工作流文件 {len(files)} 个｜问题 {len(problems)} 处")
    for x in problems:
        print(f"  ⚠️ {x}")
    print(f"报告：{REPORT.relative_to(ROOT)}")
    return 1 if ("--check" in sys.argv and problems) else 0


if __name__ == "__main__":
    sys.exit(main())
