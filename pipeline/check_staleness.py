#!/usr/bin/env python3
"""
提交产物新鲜度检查：仓库里**提交过的**产物，是否等于管线**现在**能跑出来的产物。

**为什么需要这个检查**

CI 的第 3 项（确定性）是「连跑两遍、比对彼此」，测的是"同样的输入是否得到同样的输出"。
它刻意**不比对 git**——因为 CI 跑在 Ubuntu 上、PDF 提取依赖 macOS PDFKit，
直接 diff 会因平台差异失败，那是假告警。

但这个设计有一个已知代价，今天真被撞上了：

  `source/units.json` 与 `source/INVENTORY.md` 里的 **字数统计是过期的**。
  代码在某个时点改过正文度量（`extract_markdown`），`clean/*.md` 随之重生成，
  但这两个文件没有跟着重生成。于是仓库里同时存在两套数字：

    提交的 INVENTORY.md：可用英文正文 ≈ 66,679 词
    现在跑出来的       ：可用英文正文 ≈ 65,487 词

  两遍互测永远发现不了它——两遍都很自洽，只是**都与提交的那份不一致**。

**口径（为什么只比 HTML，不比 PDF）**

只比对**平台无关**的部分：`source/units.json` 里 format != pdf 的条目。
PDF 条目的度量依赖 macOS PDFKit，在 Linux 上必然不同，比它就是把假告警制度化。

用法
----
  python3 pipeline/check_staleness.py           # 本地比对，产出报告
  python3 pipeline/check_staleness.py --check   # 有过期产物时返回非零（本地提交前用）

  # CI 里作为**信息性**检查运行：先跑一遍管线，再比对
  python3 pipeline/parse_syllabus.py && python3 pipeline/inventory.py >/dev/null
  python3 pipeline/check_staleness.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
P = CFG["paths"]
REPORT = ROOT / P["reports_dir"] / "artifact-freshness.md"

# 只比对平台无关的产物。PDF 相关度量在 Linux 上必然不同，排除。
CHECKED = [P["units_json"]]


def head_version(rel: str):
    """取 HEAD 里该文件的内容；文件尚未提交时返回 None。"""
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT,
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def html_entries(text: str) -> dict:
    """从 units.json 里取平台无关（非 PDF）条目的度量。"""
    try:
        units = json.loads(text)["units"]
    except Exception:
        return {}
    out = {}
    for u in units:
        if u.get("format") == "pdf" or str(u.get("local_path", "")).endswith(".pdf"):
            continue
        out[u.get("source_ref") or u.get("reading_title")] = {
            "words_est": u.get("words_est"),
            "content_chars": u.get("content_chars"),
            "status": u.get("status"),
            "bytes": u.get("bytes"),
        }
    return out


def main() -> int:
    rows, stale = [], []
    for rel in CHECKED:
        cur_path = ROOT / rel
        old = head_version(rel)
        if old is None or not cur_path.exists():
            rows.append((rel, "跳过", "文件未提交或不存在"))
            continue
        a, b = html_entries(old), html_entries(cur_path.read_text(encoding="utf-8"))
        diff = [(k, a.get(k), b.get(k)) for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)]
        for k, o, n in diff:
            stale.append({"file": rel, "unit": k, "committed": o, "current": n})
        rows.append((rel, f"{len(diff)} 处不同" if diff else "一致",
                     f"比对 {len(b)} 个非 PDF 条目"))

    L = ["# 产物新鲜度报告（ARTIFACT FRESHNESS）", "",
         "> 由 `pipeline/check_staleness.py` 自动生成，**请勿手工编辑**。", "",
         "## 这个检查在防什么", "",
         "CI 的确定性检查是「连跑两遍比对彼此」，它**发现不了提交产物过期**——",
         "两遍都自洽，只是都与仓库里提交的那份不一致。实测撞上过：",
         "`source/units.json` / `INVENTORY.md` 的字数统计停留在一次代码改动之前，",
         "同一份仓库里存在两套数字。", "",
         "## 口径", "",
         "| 项 | 说明 |", "|---|---|",
         "| 比对对象 | 提交到 HEAD 的产物 vs 工作区里**现在**跑出来的产物 |",
         "| 范围 | 只比 `units.json` 里 **format != pdf** 的条目 |",
         "| 为什么排除 PDF | PDF 文本提取依赖 macOS PDFKit，在 Linux 上必然不同，"
         "比它等于把假告警制度化 |",
         "",
         "## 结果", "",
         "| 产物 | 结论 | 说明 |", "|---|---|---|"]
    for rel, verdict, note in rows:
        L.append(f"| `{rel}` | {verdict} | {note} |")
    L.append("")
    if stale:
        L.append("### 过期条目明细")
        L.append("")
        L.append("| 产物 | 条目 | 提交值 | 现在的值 |")
        L.append("|---|---|---|---|")
        for s in stale:
            L.append(f"| `{s['file']}` | `{s['unit']}` | {s['committed']} | {s['current']} |")
        L.append("")
        L.append("> 处理方式：重跑管线并提交新产物（**不要**改回旧数字——代码是判据，产物是结果）。")
    else:
        L.append("✅ 提交的产物与现在跑出来的完全一致。")
    L.append("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"产物新鲜度：比对 {len(CHECKED)} 个文件｜过期条目 {len(stale)} 处")
    for s in stale[:10]:
        print(f"  ⚠️ {s['unit']}: 提交 {s['committed']} → 现在 {s['current']}")
    print(f"报告：{REPORT.relative_to(ROOT)}")
    return 1 if ("--check" in sys.argv and stale) else 0


if __name__ == "__main__":
    sys.exit(main())
