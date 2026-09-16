#!/usr/bin/env python3
"""
表格完整性检查：源文清洗稿的表格行数 vs 中译稿的表格行数。

**为什么加这个检查**

逐块校验（translate.py）只比代码围栏数和链接数，**不比表格行数**。
于是「整行被吃掉」这类丢内容的行为可以完全通过校验。实测就是这样：

  * `agentic-ai-threats` 第 6 块：源文表 12 行，我译出来 10 行——
    两行重复载荷行（HTML 里引用角标单独成行）被我当噪声删了，
    同时单元格里重复的载荷文本也被我「顺手规范化」掉了。
  * `mcp-introduction` 第 6 块：源文表 10 行，我译出来 6 行——
    4 行 colSpan 分节行（原页面里横跨 4 列的分节标题）被我并进了数据行。
  * `sast-vs-dast`：源文清洗稿里 **0 行**表格，译文里却有 12 行——
    反方向的差异，原因是清洗管线没识别出那张表（见下）。

三处都不是自动校验发现的，是我在拼装译稿时手工数行数发现的。
**手工发现的问题必须变成机制**，否则下次还会发生。这个脚本就是那个机制。

**两类差异**

  A. 源文有表、译文行数不同        → 丢行或并行的嫌疑
  B. 源文 0 行表、译文有表          → 清洗管线漏识别表格的嫌疑
     （实测：原页面用 `<div class="table">` 嵌套 div 画表，
       不是 `<table>` 元素，clean.py 的表提取器匹配不到，
       只能把每个 div 输出成一行平文本。）

**例外要显式登记**，不能靠脚本里写 if：见 pipeline/config/table-exceptions.json，
每条都必须写清证据、复核日期与处置决定。数字对不上（源/译行数变了）也算失败——
这样例外不会悄悄过期。

用法
----
  python3 pipeline/check_tables.py           # 产出 reports/table-integrity.md
  python3 pipeline/check_tables.py --check   # 有未登记差异时返回非零退出码（CI 门禁）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
ZH_DIR = ROOT / CFG["paths"].get("zh_dir", "zh")
CLEAN_DIR = ROOT / "clean"
EXC_FILE = ROOT / "pipeline/config/table-exceptions.json"
REPORT = ROOT / "reports/table-integrity.md"


def table_rows(text: str) -> int:
    """Markdown 表格行数（以 | 开头的行）。"""
    return sum(1 for line in text.split("\n") if line.startswith("|"))


def main() -> int:
    exceptions = json.loads(EXC_FILE.read_text(encoding="utf-8")) if EXC_FILE.exists() else {}

    rows, unexplained, stale = [], [], []
    for zh_file in sorted(ZH_DIR.glob("*.md")):
        src_file = CLEAN_DIR / zh_file.name
        if not src_file.exists():
            continue
        src_n = table_rows(src_file.read_text(encoding="utf-8"))
        zh_n = table_rows(zh_file.read_text(encoding="utf-8"))
        if src_n == zh_n:
            continue
        unit = zh_file.stem
        kind = "B_清洗稿漏识别表格" if src_n == 0 and zh_n > 0 else "A_行数不符"
        exc = exceptions.get(unit)
        if exc and exc.get("src_rows") == src_n and exc.get("zh_rows") == zh_n:
            rows.append((unit, src_n, zh_n, kind, "已登记例外", exc))
        else:
            rows.append((unit, src_n, zh_n, kind, "**未登记**", exc or {}))
            unexplained.append(unit)

    # 例外的数字若已经不再匹配当前代码状态，也算过期，必须重新复核
    for unit, exc in exceptions.items():
        if unit not in {r[0] for r in rows}:
            stale.append(unit)

    L = ["# 表格完整性报告（TABLE INTEGRITY）", "",
         "> 由 `pipeline/check_tables.py` 自动生成，**请勿手工编辑**。", "",
         "## 判定口径", "",
         "| 项 | 说明 |", "|---|---|",
         "| 比对对象 | `clean/<篇目>.md` 与 `zh/<篇目>.md` 的 Markdown 表格行数（以 `|` 开头的行） |",
         "| A 类差异 | 源文有表、行数不同 → 丢行 / 并行嫌疑 |",
         "| B 类差异 | 源文 0 行表、译文有表 → 清洗管线漏识别表格的嫌疑 |",
         "| 例外 | 逐条登记在 `pipeline/config/table-exceptions.json`，含证据与处置决定 |",
         "",
         "## 结论", ""]
    n_units = len(list(ZH_DIR.glob("*.md")))
    if not rows:
        L.append(f"✅ {n_units} 篇译稿的表行数与清洗稿完全一致，无差异。")
    else:
        L.append(f"审计 {n_units} 篇译稿，{len(rows)} 篇存在差异："
                 f"{len(rows) - len(unexplained)} 篇已登记例外，"
                 f"{len(unexplained)} 篇未登记。")
    L += ["", "## 差异明细", ""]
    if rows:
        L += ["| 篇目 | 源表行 | 译表行 | 类型 | 状态 | 处置 |", "|---|---|---|---|---|---|"]
        for unit, s, z, kind, state, exc in rows:
            decision = exc.get("decision", "—") if state == "已登记例外" else "待处理"
            L.append(f"| `{unit}` | {s} | {z} | {kind} | {state} | {decision} |")
        L.append("")
        for unit, s, z, kind, state, exc in rows:
            if state != "已登记例外":
                continue
            L += [f"### `{unit}`", "",
                  f"- **类型**：{kind}",
                  f"- **证据**：{exc.get('evidence', '—')}",
                  f"- **复核日期**：{exc.get('reviewed', '—')}",
                  f"- **处置决定**：{exc.get('decision', '—')}",
                  ""]
    else:
        L.append("无。")
    if stale:
        L += ["", "## 已过期的例外登记", "",
              "下列篇目在例外表里，但当前并不存在差异——说明登记已过期，"
              "需要删掉或复核（防止例外悄悄覆盖新问题）。", ""]
        for unit in stale:
            L.append(f"- `{unit}`")
    L.append("")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"审计译稿 {n_units} 篇｜表行数差异 {len(rows)} 篇"
          f"（已登记例外 {len(rows) - len(unexplained)}，未登记 {len(unexplained)}）")
    for unit, s, z, kind, state, _e in rows:
        print(f"  {'⚠️ ' if state == '**未登记**' else '  '}{unit}: 源 {s} → 译 {z}（{kind}，{state}）")
    if stale:
        print(f"  ⚠️ 过期例外登记：{', '.join(stale)}")
    print(f"报告：{REPORT.relative_to(ROOT)}")

    if "--check" in sys.argv and (unexplained or stale):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
