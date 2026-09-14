#!/usr/bin/env python3
"""
从 source/index.html 解析 CS146S 课程大纲，产出结构化 syllabus.json。

用途：
  1. 支撑 source/INVENTORY.md 的资料清点与缺口报告（覆盖度分母自证）
  2. 作为 pipeline 的输入配置——换源时替换本脚本即可复用同一套流程

这是 C1「信息获取与处理管线」的第一步：把非结构化的一手资料变成机器可读的清单。
"""
import json
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
INDEX = ROOT / CONFIG["paths"]["index_html"]
OUT = ROOT / "source/syllabus.json"


def strip_tags(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def parse_week(card: str) -> dict:
    header = re.search(r'<div class="week-header">(.*?)</div>', card, re.S)
    head_txt = strip_tags(header.group(1)) if header else ""

    m = re.match(r"Week\s+(\d+)\s*:\s*(.+)", head_txt)
    if not m:
        return {}
    num, title = int(m.group(1)), m.group(2).strip()

    week = {"week": num, "title": title, "topics": [], "readings": [],
            "lectures": [], "assignments": []}

    body = re.search(r'<div class="week-body">(.*)', card, re.S)
    body = body.group(1) if body else ""

    # 按 week-section 切块，保留 lecture-row 归属
    blocks = re.split(r'<div class="week-section">', body)
    for b in blocks[1:]:
        h4 = re.search(r"<h4>(.*?)</h4>", b, re.S)
        label = strip_tags(h4.group(1)) if h4 else "?"
        chunks = re.split(r'<div class="lecture-row">', b)
        content = chunks[0]
        rows = chunks[1:]
        low = label.lower()

        def links(frag):
            out = []
            for a in re.finditer(r'<a\s[^>]*href="([^"]+)"[^>]*>(.*?)</a>', frag, re.S):
                out.append({"text": strip_tags(a.group(2)), "url": a.group(1)})
            return out

        if "topic" in low:
            week["topics"] = [strip_tags(li) for li in re.findall(r"<li>(.*?)</li>", content, re.S)]
        if "reading" in low:
            for row in [content] + rows:
                week["readings"].extend(links(row))
        if "lecture" in low:
            for row in [content] + rows:
                week["lectures"].extend(links(row))
        if "assignment" in low or "exercise" in low or "design doc" in low:
            week["assignments"].extend(links(content))

    return week


def main() -> None:
    t = INDEX.read_text(encoding="utf-8", errors="replace")
    cards = re.split(r'<div class="week-card">', t)[1:]
    weeks = [w for w in (parse_week(c) for c in cards) if w]
    weeks.sort(key=lambda w: w["week"])

    data = {
        "course": "CS146S: The Modern Software Developer",
        "institution": "Stanford University",
        "term": "Fall 2025",
        "instructor": "Mihail Eric",
        "source_url": "https://themodernsoftware.dev/",
        "source_html": "index.html",
        "weeks": weeks,
    }
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"解析出 {len(weeks)} 周 -> {OUT.name}")
    for w in weeks:
        print(f"  Week {w['week']:>2} | topics {len(w['topics']):>2} | "
              f"readings {len(w['readings']):>2} | lectures {len(w['lectures']):>2} | "
              f"assignments {len(w['assignments'])} | {w['title']}")


if __name__ == "__main__":
    main()
