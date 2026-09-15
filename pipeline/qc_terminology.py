#!/usr/bin/env python3
"""
全量术语一致率检查：对**已完成的全部译稿**做术语审计。

与 translate.py 的逐块校验的分工：
  translate.py  —— 翻译过程中逐块拦截（即时反馈，但只见单块）
  qc_terminology.py —— 完成后对全量译稿做审计（全局视图，可作 CI 门禁）

三项检查：

  1. **一致性**：358 个硬性禁用变体在全部译稿中是否出现过。
     出现过 → 判违规，给出文件名与上下文。这是主判据。

  2. **覆盖率**：源文中出现的术语，其正式译法是否在译文中出现。
     能抓到「漏译某个术语」或「整段丢失」——这类问题逐块校验看不见，
     因为单块内部可能自洽。

  3. **提示级**：10 个提示级变体只统计不判违规。
     它们多是「另一个英文词的合法译法」（如 proxy → 代理），
     一律判违规会逼出错误的译文。

产出：reports/terminology-consistency.md
用法：python3 pipeline/qc_terminology.py [--check]
      --check 模式在有硬性违规时返回非零退出码，可直接用作 CI 门禁。
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from termcheck import find_hits, approved_forms, count_forms, variants  # noqa: E402
CFG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
GLOSSARY = ROOT / CFG["paths"]["glossary"]
ZH_DIR = ROOT / CFG["paths"].get("zh_dir", "zh")
CLEAN_DIR = ROOT / "clean"
REPORT = ROOT / "reports/terminology-consistency.md"

CODE_FENCE = re.compile(r"^[ \t]*```.*?^[ \t]*```", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """去掉代码块与行内代码。

    代码按约定逐字保留原文，里面的英文术语（如代码注释中的 agent）
    不应参与术语覆盖率判定，否则会大量误报。
    """
    t = CODE_FENCE.sub("\n", text)
    return INLINE_CODE.sub(" ", t)


def context_of(text: str, needle: str, width: int = 34) -> str:
    i = text.find(needle)
    if i < 0:
        return ""
    seg = text[max(0, i - width): i + len(needle) + width]
    return re.sub(r"\s+", " ", seg).strip()


def main() -> int:
    with GLOSSARY.open(encoding="utf-8") as f:
        glossary = [r for r in csv.DictReader(f)]

    zh_files = sorted(ZH_DIR.glob("*.md")) if ZH_DIR.exists() else []
    if not zh_files:
        print("尚无译稿，跳过术语审计。")
        return 0

    # 读取译稿与对应源文
    docs = []
    for f in zh_files:
        zh = f.read_text(encoding="utf-8")
        src = CLEAN_DIR / f.name
        docs.append({
            "unit": f.stem,
            "zh": zh,
            "zh_plain": strip_code(zh),
            "src_plain": strip_code(src.read_text(encoding="utf-8")) if src.exists() else "",
            "has_src": src.exists(),
        })

    rows, violations, omissions, soft_hits = [], [], [], []
    total_approved = total_violations = 0

    for term in glossary:
        if term["policy"] == "keep_en":
            continue
        forms = approved_forms(term)
        if not forms:
            continue

        used = 0

        # --- 一致性：硬性禁用变体 ---
        for d in docs:
            h, _s = find_hits(d["zh_plain"], term)   # 共享判定：含包含关系过滤
            for v, c in h:
                total_violations += c
                violations.append({
                    "term": term["term_en"], "approved": term["term_zh"],
                    "variant": v, "unit": d["unit"], "count": c,
                    "context": context_of(d["zh_plain"], v),
                })

        # --- 提示级：只统计 ---
        for d in docs:
            _h, s = find_hits(d["zh_plain"], term)
            for v, c in s:
                soft_hits.append({"term": term["term_en"], "variant": v,
                                  "unit": d["unit"], "count": c})

        # --- 覆盖率：源文出现该术语，译文是否用正式译法 ---
        src_units = [d for d in docs if d["has_src"]
                     and re.search(r"\b" + re.escape(term["term_en"].split(" (")[0]) + r"\b",
                                   d["src_plain"], re.I)]
        for d in src_units:
            pass
        for d in docs:
            if not d["has_src"]:
                continue
            used += count_forms(d["zh_plain"], forms)
        total_approved += used

        for d in src_units:
            if count_forms(d["zh_plain"], forms) == 0:
                omissions.append({"term": term["term_en"], "approved": term["term_zh"],
                                  "unit": d["unit"]})

        rows.append({
            "term": term["term_en"], "approved": term["term_zh"],
            "used": used, "n_src": len(src_units),
            "n_viol": sum(v["count"] for v in violations if v["term"] == term["term_en"]),
            "policy": term["policy"], "category": term["category"],
        })

    # ---- 报告 ----
    denom = total_approved + total_violations
    rate = (total_approved / denom * 100) if denom else 100.0
    used_terms = [r for r in rows if r["used"] > 0]
    clean_terms = [r for r in used_terms if r["n_viol"] == 0]

    L, A = [], None
    L.append("# 术语一致率报告（TERMINOLOGY CONSISTENCY）")
    L.append("")
    L.append("> 由 `pipeline/qc_terminology.py` 自动生成，**请勿手工编辑**。")
    L.append("")
    A = L.append
    A("## 检查范围")
    A("")
    A("| 项 | 值 |")
    A("|---|---|")
    A(f"| 术语表条目 | {len(glossary)} 条（其中需翻译 {len([r for r in glossary if r['policy'] != 'keep_en'])} 条） |")
    A(f"| 审计译稿 | {len(docs)} 条 |")
    A(f"| 硬性禁用变体 | {sum(len(variants(t,'forbidden_zh')) for t in glossary)} 个 |")
    A(f"| 提示级变体 | {sum(len(variants(t,'forbidden_soft')) for t in glossary)} 个（只统计不判违规） |")
    A("")
    A("## 一致率")
    A("")
    A("**口径**：一致率 = 正式译法出现次数 /（正式译法出现次数 + 硬性违规次数）")
    A("")
    n_soft = sum(s["count"] for s in soft_hits)
    A("| 指标 | 数值 |")
    A("|---|---|")
    A(f"| 正式译法出现次数 | {total_approved:,} |")
    A(f"| **硬性违规次数** | **{total_violations}** |")
    A(f"| **术语一致率（硬性口径）** | **{rate:.2f}%** |")
    A(f"| 提示级命中次数 | {n_soft}（**不计入一致率**，见第三节） |")
    A(f"| 实际用到的术语 | {len(used_terms)} 条 |")
    A(f"| 其中零违规 | {len(clean_terms)} 条 |")
    A("")
    A("> ⚠️ **这个百分比只统计硬性禁用变体。** 术语表另有一批提示级变体，"
      "它们是中文常用词或**其它英文词**的合法译法（如 proxy → 代理、"
      "dashboard → 控制台），一律判违规会逼出错误的译文。"
      "读数时请把两者一起看——**单看 100% 会高估实际的一致性**。")
    A("")
    if total_violations == 0:
        A("✅ **全部硬性禁用变体零出现。**")
    else:
        A(f"❌ 发现 {total_violations} 处违规，详见下方。")
    A("")
    A("## 一、违规明细（硬性）")
    A("")
    if violations:
        A("| 术语 | 应为 | 出现的违规写法 | 篇目 | 次数 | 上下文 |")
        A("|---|---|---|---|---|---|")
        for v in violations:
            A(f"| {v['term']} | {v['approved']} | **{v['variant']}** | `{v['unit']}` "
              f"| {v['count']} | …{v['context']}… |")
    else:
        A("无。")
    A("")
    A("## 二、覆盖率缺口（参考项，不作门禁）")
    A("")
    A("源文中出现某术语，但译文中完全没有出现它的正式译法。")
    A("")
    A("**为什么只作参考而不判违规**——这个检查的误报率偏高，已知至少三类：")
    A("")
    A("1. **正式译法依上下文而变**：`Agentic` 的正式译法是「智能体化的」，"
      "但在 `Agentic AI` 里按术语表应译「智能体 AI」，于是「智能体化的」"
      "自然不出现——这不是漏译。")
    A("2. **英文术语被有意保留**：如 `prompt`、`diff` 在中文技术写作里常保留英文，"
      "这类确实值得人工看一眼，但不必然算错。")
    A("3. **词边界匹配的局限**：英文词可能出现在短语内部。")
    A("")
    A("按本项目的原则——**天天误报的校验器最终会被忽略**——因此只列出、不拦截。")
    A("")
    if omissions:
        A("| 术语 | 应为 | 篇目 |")
        A("|---|---|---|")
        for o in omissions:
            A(f"| {o['term']} | {o['approved']} | `{o['unit']}` |")
    else:
        A("无。所有源文中出现的术语，译文中都使用了正式译法。")
    A("")
    A("## 三、提示级变体（仅统计）")
    A("")
    A("这些变体在中文里本身是常用词，或是**另一个英文词**的合法译法，"
      "因此只统计、不判违规。例如 `proxy` 的标准译法就是「代理」，"
      "而「代理」是 Agent 的提示级变体。")
    A("")
    if soft_hits:
        A("| 术语 | 变体 | 篇目 | 次数 |")
        A("|---|---|---|---|")
        for s in soft_hits:
            A(f"| {s['term']} | {s['variant']} | `{s['unit']}` | {s['count']} |")
    else:
        A("无。")
    A("")
    A("## 四、逐术语统计")
    A("")
    A("| 术语 | 正式译法 | policy | 出现次数 | 源文篇数 | 违规 |")
    A("|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: -x["used"]):
        if r["used"] == 0 and r["n_src"] == 0:
            continue
        flag = "✅" if r["n_viol"] == 0 else f"❌ {r['n_viol']}"
        A(f"| {r['term']} | {r['approved']} | `{r['policy']}` | {r['used']:,} "
          f"| {r['n_src']} | {flag} |")
    A("")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- 控制台 ----
    print(f"审计译稿 {len(docs)} 条 ｜ 术语表 {len(glossary)} 条")
    print(f"正式译法出现 {total_approved:,} 次 ｜ 硬性违规 {total_violations} 次")
    print(f"术语一致率 {rate:.2f}%")
    if violations:
        print(f"\n违规明细已写入 {REPORT.relative_to(ROOT)}")
        for v in violations[:10]:
            print(f"  ❌ {v['unit']}: 「{v['variant']}」应为「{v['approved']}」")
    if omissions:
        print(f"\n覆盖率缺口 {len(omissions)} 处（详见报告）")
    print(f"报告：{REPORT.relative_to(ROOT)}")

    if "--check" in sys.argv and total_violations:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
