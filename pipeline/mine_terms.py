#!/usr/bin/env python3
"""
术语候选挖掘：从语料中自动提取候选术语，供人工审定后写入 glossary。

设计意图（对应 rubric 的 pipelineAutomation「换源可复用」）：
  本脚本不绑定具体课程。换一门课只需改 pipeline/config/<source>.json 的 paths，
  同样的挖掘逻辑即可产出新语料的候选术语表。

它只负责"提出候选"，不负责"定译法"——译法由人审定后写入 glossary/glossary.csv。
这个人机分工本身就是一次可记录的 AI 协作决策（见 拿来说明/）。

用法：
  python3 pipeline/mine_terms.py            # 打印候选
  python3 pipeline/mine_terms.py --csv      # 导出 reports/term-candidates.csv
"""
import csv
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 配置路径可由环境变量覆盖：换源跑第二份配置时不改代码——
#   PIPELINE_CONFIG=pipeline/config/demo-second-source.json python3 pipeline/inventory.py
CONFIG_PATH = Path(os.environ.get("PIPELINE_CONFIG", "pipeline/config/cs146s.json"))
CFG = json.loads((ROOT / CONFIG_PATH).read_text(encoding="utf-8"))

# 噪音表：HTML/网页样板中高频但无翻译价值的词
STOP = set("""
the a an and or but if then this that these those it its is are was were be been being
to of in on at for with by from as into over under about after before
you your we our they their he she his her i me my
can could will would shall should may might must do does did done have has had
not no nor so such than too very just also more most other some any each
one two three four five six seven eight nine ten
new use used using make makes made get gets got go goes going
here there when where why how what which who whom whose
https http www com org net html pdf github com
""".split())

ACRO_STOP = {"HTML", "HTTP", "URL", "CSS", "JS", "OK", "US", "AI", "ID", "UI", "PDF", "FAQ"}



def main() -> None:
    units = json.loads((ROOT / CFG["paths"]["units_json"]).read_text(encoding="utf-8"))["units"]

    # 语料取 clean/ 下的清洗产物，而**不是**原始 HTML。
    # 早期版本自己写了一套 visible_text() 直接读 HTML，于是：
    #   1. 术语频次被导航栏与页脚文字污染（"Slides"/"Subscribe" 之类会被算进去）；
    #   2. 出现了第三份「HTML→文本」实现，与 clean.py 的判定各自演化，
    #      恰恰违反本项目在 pipeline/README.md 里写明的「单一判定来源」原则。
    # 清洗产物是管线的既定中间结果，术语挖掘理应消费它。
    corpus_parts, used = [], 0
    for u in units:
        if u["kind"] != "local" or u.get("status") != "ok":
            continue
        f = ROOT / CFG["paths"]["clean_dir"] / (Path(u["local_path"]).stem + ".md")
        if f.exists():
            corpus_parts.append(f.read_text(encoding="utf-8"))
            used += 1
    corpus = "\n".join(corpus_parts)
    total_words = len(corpus.split())
    print(f"语料：{used} 篇 clean/ 产物（HTML+PDF），约 {total_words:,} 词\n", file=sys.stderr)

    # ---- 1. 缩写词 ----
    acro = Counter(re.findall(r"\b[A-Z][A-Z0-9]{1,7}\b", corpus))
    acro = {k: v for k, v in acro.items() if k not in ACRO_STOP and v >= 3}

    # ---- 2. 首字母大写的多词短语（1~4 词）----
    phrases = Counter()
    for n in (1, 2, 3, 4):
        pat = r"\b(?:" + r"\s+".join([r"[A-Z][a-zA-Z0-9\-\.\+#]*"] * n) + r")\b"
        for m in re.findall(pat, corpus):
            w = m.strip()
            words = w.lower().split()
            if any(x in STOP for x in words):
                continue
            if len(w) < 4 or (n == 1 and len(w) < 6):
                continue
            phrases[w] += 1

    # ---- 3. 技术术语中的常见小写搭配 ----
    lower = Counter()
    for pat in (r"\bprompt engineering\b", r"\bcontext engineering\b", r"\bvibe coding\b",
                r"\bcode review\w*\b", r"\bprompt injection\b", r"\bsecurity review\b",
                r"\btool use\b", r"\bfunction calling\b", r"\bchain of thought\b",
                r"\bretrieval[- ]augmented generation\b", r"\bcontext window\b",
                r"\bcontext rot\b", r"\bagentic\b", r"\bsub-?agent\w*\b",
                r"\bscaffolding\b", r"\bguardrail\w*\b", r"\bsystem prompt\b",
                r"\bfew-?shot\b", r"\bzero-?shot\b", r"\bfine-?tun\w+\b",
                r"\bhallucinat\w+\b", r"\blatency\b", r"\bthroughput\b",
                r"\bobservability\b", r"\btelemetry\b", r"\btracing\b", r"\bspans?\b",
                r"\bincident\b", r"\bon-?call\b", r"\bpostmortem\b", r"\bSLO\b",
                r"\bdeploy\w*\b", r"\bartifact\w*\b", r"\bworkflow\w*\b",
                r"\bagent\w*\b", r"\bIDE\b", r"\bterminal\b", r"\brefactor\w*\b"):
        for m in re.findall(pat, corpus, re.I):
            lower[m.lower()] += 1

    def show(title, items, k=45):
        print(f"===== {title} =====")
        for w, c in items[:k]:
            print(f"{c:>5}  {w}")
        print()

    a_items = sorted(acro.items(), key=lambda x: -x[1])
    p_items = sorted(phrases.items(), key=lambda x: -x[1])
    l_items = sorted(lower.items(), key=lambda x: -x[1])

    show("缩写词（候选）", a_items, 50)
    show("首字母大写短语（候选）", p_items, 70)
    show("技术搭配（候选）", l_items, 45)

    if "--csv" in sys.argv:
        out = ROOT / CFG["paths"]["reports_dir"] / "term-candidates.csv"
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["candidate", "count", "type"])
            for x, c in a_items:
                w.writerow([x, c, "acronym"])
            for x, c in p_items:
                w.writerow([x, c, "capitalized_phrase"])
            for x, c in l_items:
                w.writerow([x, c, "tech_collocation"])
        print(f"已导出 -> {out.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
