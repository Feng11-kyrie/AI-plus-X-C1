#!/usr/bin/env python3
"""
交付物命名检查：挑战的 `required_deliverables` 是**通配符**，逐个真匹配一遍。

**为什么需要这个检查**

挑战包 `challenge.json` 里的 `required_deliverables` 是：

```
README.md,*AI日志*,*AAR*,*拿来说明*
```

这四个是**通配符**，不是文件名。而本仓库的 AI 日志原先叫 `logs/ai-journal.md`——
路径里没有「AI日志」四个字。于是：

```python
glob.glob("*AI日志*", recursive=True)   # → []   0 项
```

**内容一字不少，但在检查器眼里这份交付物不存在。** 而 rubric 的红线是
`missing_artifacts`（核心交付物缺失 → 产物完整性 ≤ 5），
`no_ai_log`（无 AI 日志/AAR → 复盘质量 ≤ 5）。名字对不上，等于自己踩红线。

同理 `*拿来说明*`：挑战要求「**至少 3 个**」，如果四个文件名叫
`01-xxx.md` 而只有外层目录叫「拿来说明」，那么按文件计数只有 1 项，判不达标。

**结论：交付物的名字是规格的一部分，必须机械校验，不能靠"我写了"来确认。**

用法
----
  python3 pipeline/check_deliverables.py           # 产出 reports/deliverables-check.md
  python3 pipeline/check_deliverables.py --check   # 不满足时返回非零退出码（CI 门禁）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "reports/deliverables-check.md"

# 直接抄自挑战包（challenge.json 的 required_deliverables），不自己改写。
# 同时保留原始字符串作为证据，避免"检查器自己定义需求"。
SPEC_FILE = Path.home() / "AI➕X挑战/C1_课程资料获取与翻译/challenge.json"
SPEC_FALLBACK = "README.md,*AI日志*,*AAR*,*拿来说明*"

# 每个通配符的最少匹配**文件**数（目录不算数——挑战说的是"至少 3 个"）
MIN_FILES = {"README.md": 1, "*AI日志*": 1, "*AAR*": 1, "*拿来说明*": 3}


def load_spec() -> tuple:
    """返回 (required_deliverables 原文, 来源说明)。"""
    try:
        d = json.loads(SPEC_FILE.read_text(encoding="utf-8"))
        return d.get("required_deliverables", SPEC_FALLBACK), f"`{SPEC_FILE.name}` 的 `required_deliverables`"
    except Exception:
        return SPEC_FALLBACK, "内置回退值（挑战包不在本机）"


def matches(pattern: str) -> list:
    """按通配符找匹配项：顶层与递归两种写法取并集。"""
    hits = set(ROOT.glob(pattern)) | set(ROOT.glob(f"**/{pattern}"))
    out = []
    for h in sorted(hits):
        rel = h.relative_to(ROOT).as_posix()
        if any(part.startswith(".") or part == ".git" for part in h.relative_to(ROOT).parts):
            continue
        out.append((rel, h.is_dir(), h.stat().st_size if h.is_file() else 0))
    return out


def main() -> int:
    spec, origin = load_spec()
    patterns = [p.strip() for p in spec.split(",") if p.strip()]

    rows, failures = [], []
    for pat in patterns:
        hits = matches(pat)
        files = [h for h in hits if not h[1]]
        need = MIN_FILES.get(pat, 1)
        ok = len(files) >= need
        empty = [h[0] for h in files if h[2] == 0]
        if not ok:
            failures.append(f"`{pat}` 需要 ≥{need} 个文件，实际匹配到 {len(files)} 个文件"
                            f"（另有 {len(hits) - len(files)} 个目录）")
        if empty:
            failures.append(f"`{pat}` 匹配到空文件：{', '.join(empty)}")
        rows.append({"pat": pat, "need": need, "hits": hits, "files": files, "ok": ok})

    L = ["# 交付物检查报告（DELIVERABLES）", "",
         "> 由 `pipeline/check_deliverables.py` 自动生成，**请勿手工编辑**。", "",
         "## 判定依据", "",
         f"要求的交付物（原文，来自 {origin}）：", "",
         f"```\n{spec}\n```", "",
         "这四个是**通配符**。所以检查方式不是「我写了没有」，而是"
         "**拿通配符在仓库里真匹配一遍**，并按文件计数。", "",
         "| 通配符 | 最少文件数 | 实际文件数 | 结论 |", "|---|---|---|---|"]
    for r in rows:
        L.append(f"| `{r['pat']}` | {r['need']} | {len(r['files'])} | {'✅' if r['ok'] else '❌'} |")
    L += ["", "## 匹配到的文件", ""]
    for r in rows:
        L.append(f"### `{r['pat']}`")
        L.append("")
        for rel, is_dir, size in r["hits"]:
            kind = "目录" if is_dir else f"{size:,} 字节"
            L.append(f"- `{rel}`（{kind}）")
        if not r["hits"]:
            L.append("- **无匹配**")
        L.append("")
    L += ["## 结论", ""]
    if failures:
        L.append("❌ 不满足挑战要求：")
        L.append("")
        for f in failures:
            L.append(f"- {f}")
        L.append("")
        L.append("> 注意：**交付物改名不是小事。** 内容再全，通配符匹配不到就等于缺失，"
                 "而 rubric 红线 `missing_artifacts` / `no_ai_log` 会把对应维度直接压到 5 分。")
    else:
        L.append("✅ 挑战要求的四项交付物全部按通配符匹配成功，且无空文件。")
    L.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"交付物通配符 {len(rows)} 个｜不满足 {len(failures)} 项")
    for r in rows:
        print(f"  {'✅' if r['ok'] else '❌'} {r['pat']}：{len(r['files'])} 个文件"
              f"（要求 ≥{r['need']}）")
    for f in failures:
        print(f"  ⚠️ {f}")
    print(f"报告：{REPORT.relative_to(ROOT)}")
    return 1 if ("--check" in sys.argv and failures) else 0


if __name__ == "__main__":
    sys.exit(main())
