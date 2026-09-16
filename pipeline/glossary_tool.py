#!/usr/bin/env python3
"""
术语表工具：校验 glossary.csv 并渲染 glossary.md。

校验规则（术语表自身的质量门禁）：
  R1 id 唯一
  R2 term_en 唯一（大小写不敏感）
  R3 禁用变体不得与任何术语的正式译法冲突
  R4 policy 取值合法
  R5 非 keep_en 的术语必须有中文译法
  R6 禁用变体内部不得重复

用法：
  python3 pipeline/glossary_tool.py            # 校验 + 渲染
  python3 pipeline/glossary_tool.py --check     # 只校验（CI 用，失败返回非零）
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 配置路径可由环境变量覆盖：换源跑第二份配置时不改代码——
#   PIPELINE_CONFIG=pipeline/config/demo-second-source.json python3 pipeline/inventory.py
CONFIG_PATH = Path(os.environ.get("PIPELINE_CONFIG", "pipeline/config/cs146s.json"))
CFG = json.loads((ROOT / CONFIG_PATH).read_text(encoding="utf-8"))
CSV_PATH = ROOT / CFG["paths"]["glossary"]
MD_PATH = (ROOT / CFG["paths"]["glossary"]).with_suffix(".md")

POLICIES = {"translate", "keep_en", "keep_en_first", "acronym"}
CATEGORIES = {
    "core-llm": "核心 LLM 与提示词",
    "agent": "智能体与工具调用",
    "swe": "软件工程",
    "security": "安全",
    "sre": "SRE 与可观测性",
    "process": "产品与流程",
    "tool": "工具与专有名词（不译）",
}


def load():
    with CSV_PATH.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def validate(rows):
    errs, warns = [], []

    ids = [r["id"] for r in rows]
    for k, v in Counter(ids).items():
        if v > 1:
            errs.append(f"R1 id 重复: {k} × {v}")

    ens = Counter(r["term_en"].lower() for r in rows)
    for k, v in ens.items():
        if v > 1:
            errs.append(f"R2 term_en 重复: {k} × {v}")

    # R3 禁用变体 vs 正式译法冲突（硬性与提示级都要查）
    approved = defaultdict(list)
    for r in rows:
        if r["term_zh"]:
            approved[r["term_zh"].strip()].append(r["term_en"])
    forbidden_map = defaultdict(list)
    for r in rows:
        for col in ("forbidden_zh", "forbidden_soft"):
            for fb in filter(None, (x.strip() for x in (r.get(col) or "").split("|"))):
                forbidden_map[fb].append(r["term_en"])
    for fb, owners in forbidden_map.items():
        if fb in approved:
            errs.append(f"R3 冲突: 禁用变体「{fb}」（{owners}）同时是 "
                        f"「{approved[fb]}」的正式译法")

    for r in rows:
        if r["policy"] not in POLICIES:
            errs.append(f"R4 policy 非法: {r['id']} = {r['policy']}")
        if r["policy"] != "keep_en" and not r["term_zh"].strip():
            errs.append(f"R5 缺译法: {r['id']} {r['term_en']}")
        if r["category"] not in CATEGORIES:
            warns.append(f"未知分类: {r['term_en']} = {r['category']}")

        def varis(col):
            return [x.strip() for x in (r.get(col) or "").split("|") if x.strip()]

        # R6：硬性与提示级变体内部及彼此之间都不得重复
        for k, v in Counter(varis("forbidden_zh") + varis("forbidden_soft")).items():
            if v > 1:
                errs.append(f"R6 禁用变体重复: {r['term_en']} -> {k}")
        # R7：同一变体不应既是硬性又是提示级
        for k in set(varis("forbidden_zh")) & set(varis("forbidden_soft")):
            errs.append(f"R7 变体同时标为硬性与提示级: {r['term_en']} -> {k}")
        # R8：提示级变体若是正式译法的子串则毫无意义——包含关系判定会先跳过它
        approved_zh = (r["term_zh"] or "").strip()
        for fb in varis("forbidden_soft"):
            if approved_zh and fb in approved_zh:
                warns.append(f"R8 提示级变体「{fb}」是「{approved_zh}」的子串，"
                             f"会被包含关系判定跳过，标记无意义")

    # R9：硬性禁用变体不得是**其它术语正式译法**的组成部分。
    # 起因：False Positive -> 误报 把「假阳性」列为硬性禁用，
    # 而 False Positive Rate -> 假阳性率（FPR）——速率形式恰恰用了那个词。
    # R1–R8 都查不出这类「同一份表里两条规则互相冲突」。
    approved_terms = [(r["term_zh"].strip(), r["term_en"]) for r in rows if r["term_zh"].strip()]
    for r in rows:
        for col in ("forbidden_zh", "forbidden_soft"):
            for fb in filter(None, (x.strip() for x in (r.get(col) or "").split("|"))):
                for azh, aen in approved_terms:
                    if fb != azh and fb in azh:
                        warns.append(
                            f"R9 潜在冲突: 「{fb}」是 {r['term_en']} 的禁用变体，"
                            f"但它是 {aen} 的正式译法「{azh}」的组成部分")
    return errs, warns


def render(rows):
    L, A = [], None
    L.append("# 术语表（Glossary）")
    L.append("")
    L.append("> 本文件由 `pipeline/glossary_tool.py` 从 `glossary.csv` 自动渲染，**请勿手工编辑**。")
    L.append("> **唯一真源是 `glossary.csv`**（机器可读，管线直接消费）。")
    L.append("")
    L.append("## 使用政策")
    L.append("")
    L.append("| policy | 含义 |")
    L.append("|---|---|")
    L.append("| `translate` | 译成中文，全文统一使用该译法 |")
    L.append("| `acronym` | 保留缩写，首次出现时给出中文全称 |")
    L.append("| `keep_en_first` | 首次出现写「中文（English）」，之后用中文 |")
    L.append("| `keep_en` | 专有名词/产品名，保留英文不译 |")
    L.append("")
    L.append("## 禁用变体的两个等级")
    L.append("")
    L.append("| 列 | 等级 | 校验行为 |")
    L.append("|---|---|---|")
    L.append("| `forbidden_zh` | **硬性** | 译文中出现即判该块不通过，必须返工 |")
    L.append("| `forbidden_soft` | 提示级 | 只记录不拦截——用于「记录」「流程」这类"
             "在中文里本身就常用、单用也说得通的词 |")
    L.append("")
    L.append("另有两条中文特有的判定规则（见 `pipeline/translate.py` 的 `variant_hits`）：")
    L.append("")
    L.append("1. **被正式译法包含的变体一律跳过**——「上下文协议」是"
             "「模型上下文协议（MCP）」的子串，子串匹配会把正确译文判成违规。")
    L.append("2. 宁可漏报也不误报：一个天天误报的校验器最终会被忽略。")
    L.append("")
    n_hard = sum(len([x for x in (r.get("forbidden_zh") or "").split("|") if x.strip()]) for r in rows)
    n_soft = sum(len([x for x in (r.get("forbidden_soft") or "").split("|") if x.strip()]) for r in rows)
    L.append(f"**术语总数：{len(rows)} 条**"
             f"（硬性禁用变体 {n_hard} 条 + 提示级 {n_soft} 条，"
             "由 `pipeline/translate.py` 逐块强制校验）")
    L.append("")

    by_cat = defaultdict(list)
    for r in rows:
        by_cat[r["category"]].append(r)

    for cat, label in CATEGORIES.items():
        items = by_cat.get(cat, [])
        if not items:
            continue
        L.append(f"## {label}（{len(items)} 条）")
        L.append("")
        L.append("| 英文 | 中文 | policy | 禁用变体（硬性） | 提示级 | 语料频次 |")
        L.append("|---|---|---|---|---|---|")
        for r in sorted(items, key=lambda x: -int(x["freq_in_corpus"] or 0)):
            fb = r["forbidden_zh"].replace("|", "、") or "—"
            fs = r.get("forbidden_soft", "").replace("|", "、") or "—"
            f = r["freq_in_corpus"]
            freq = f if f and f != "0" else "—"
            L.append(f"| {r['term_en']} | {r['term_zh']} | `{r['policy']}` | {fb} | {fs} | {freq} |")
        L.append("")

    return "\n".join(L) + "\n"


def main():
    rows = load()
    errs, warns = validate(rows)

    if errs:
        print("✗ 术语表校验失败：", file=sys.stderr)
        for e in errs:
            print(f"   - {e}", file=sys.stderr)
        return 1

    print(f"✓ 术语表校验通过：{len(rows)} 条")
    terms = [r for r in rows if r["policy"] != "keep_en"]
    keepe = [r for r in rows if r["policy"] == "keep_en"]
    fbs = sum(len([x for x in (r.get("forbidden_zh") or "").split("|") if x.strip()]) for r in rows)
    soft = sum(len([x for x in (r.get("forbidden_soft") or "").split("|") if x.strip()]) for r in rows)
    print(f"   需翻译      : {len(terms)}")
    print(f"   保留英文    : {len(keepe)}")
    print(f"   硬性禁用变体: {fbs}")
    print(f"   提示级变体  : {soft}")
    print(f"   分类        : {len({r['category'] for r in rows})}")
    for w in warns:
        print(f"   ! {w}")

    if "--check" not in sys.argv:
        MD_PATH.write_text(render(rows), encoding="utf-8")
        print(f"   已渲染      : {MD_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
