#!/usr/bin/env python3
"""
资料清点与缺口报告生成器。

输入：source/syllabus.json（课程大纲）、source/page_map.json（URL→本地文件映射）
输出：source/units.json（机器可读的工作单元清单 = 翻译管线的工作队列）
      source/INVENTORY.md（人读的清点与缺口报告，含覆盖度分母自证）

设计意图：
  覆盖度必须"分母自证"——不能只说"覆盖 80%"，要说清 80% 是相对什么算的。
  本脚本把分母的定义固化在代码里，任何人可复跑核对。

用法：python3 pipeline/inventory.py
"""
import json
import re
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
P = CFG["paths"]

SYLLABUS = json.loads((ROOT / "source/syllabus.json").read_text(encoding="utf-8"))
PAGES_DIR = ROOT / P["pages_dir"]
PDFS_DIR = ROOT / P["pdfs_dir"]

# 判定阈值：小于此字节数的 HTML 视为占位/抓取失败
PLACEHOLDER_MAX_BYTES = 2000

WEEK_TITLES_ZH = {
    1: "编码 LLM 与 AI 开发导论",
    2: "编码智能体的解剖学",
    3: "AI IDE",
    4: "Claude Code 与智能体编程",
    5: "Warp 与 AI 终端",
    6: "AI 安全与漏洞检测",
    7: "AI 驱动的代码评审",
    8: "全栈 AI 开发与部署",
    9: "SRE、可观测性与智能体值班",
    10: "AI 在软件工程中的未来",
}


def html_text(p: Path) -> tuple:
    """返回 (可见文本, 标题)。用于估算字数和识别真伪页面。"""
    raw = p.read_text(encoding="utf-8", errors="replace")
    title = ""
    m = re.search(r"<title[^>]*>(.*?)</title>", raw, re.S | re.I)
    if m:
        title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip()
    body = re.sub(r"<(script|style|nav|footer|header)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", body)
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    return text, title


def classify(url: str) -> tuple:
    """把 reading 的 url 分类为 local / external。"""
    if url.startswith("pages/") or url.startswith("pdfs/"):
        return "local", url
    if url.startswith("http"):
        return "external", url
    return "unknown", url


def main() -> None:
    units = []
    seen = set()

    for w in SYLLABUS["weeks"]:
        for r in w["readings"]:
            kind, path = classify(r["url"])
            if path in seen:
                continue
            seen.add(path)

            u = {
                "week": w["week"],
                "week_title": w["title"],
                "week_title_zh": WEEK_TITLES_ZH.get(w["week"], ""),
                "reading_title": r["text"],
                "kind": kind,
                "source_ref": r["url"],
            }

            if kind == "local":
                f = ROOT / "source" / path
                u["local_path"] = f"source/{path}"
                if f.exists():
                    size = f.stat().st_size
                    u["bytes"] = size
                    if f.suffix.lower() == ".pdf":
                        u["status"] = "ok"
                        u["format"] = "pdf"
                        u["words_est"] = None
                    else:
                        text, title = html_text(f)
                        u["page_title"] = title
                        u["words_est"] = len(text.split())
                        if size == 0:
                            u["status"] = "empty"          # 抓取完全失败
                        elif size < PLACEHOLDER_MAX_BYTES:
                            u["status"] = "placeholder"    # 反爬占位页
                        else:
                            u["status"] = "ok"
                        u["format"] = "html"
                else:
                    u["status"] = "missing"
                    u["format"] = f.suffix.lstrip(".")
            else:
                u["status"] = "external"
                parts = re.sub(r"^https?://", "", path).split("/")
                u["domain"] = parts[0]

            units.append(u)

    units.sort(key=lambda x: (x["week"], x["source_ref"]))
    (ROOT / "source/units.json").write_text(
        json.dumps({"units": units}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- 统计 ----
    local = [u for u in units if u["kind"] == "local"]
    usable = [u for u in local if u["status"] == "ok"]
    broken = [u for u in local if u["status"] in ("empty", "placeholder")]
    external = [u for u in units if u["kind"] == "external"]
    words = sum(u["words_est"] or 0 for u in usable)

    # ---- 生成 INVENTORY.md ----
    L = []
    A = L.append
    A("# 资料清点与缺口报告（INVENTORY）")
    A("")
    A("> 本文件由 `pipeline/inventory.py` 自动生成，**请勿手工编辑**（改脚本后重跑）。")
    A("> 数据源：`source/syllabus.json` + `source/page_map.json`。")
    A("")
    A(f"课程：**{SYLLABUS['course']}**（{SYLLABUS['institution']}，{SYLLABUS['term']}）")
    A(f"讲师：{SYLLABUS['instructor']} ｜ 原始站点：{SYLLABUS['source_url']} ｜ 缓存于 {CFG['cached_on']}")
    A("")
    A("---")
    A("")
    A("## 一、覆盖度分母（自证）")
    A("")
    A("覆盖度不能只报一个百分比，必须先说清**分母是什么**。本报告采用的定义：")
    A("")
    A(f"- **分母 = 大纲中指向本地文件的 readings = {len(local)} 条**（即 `pages/` 与 `pdfs/` 中有实体文件的条目）")
    A(f"- **其中可用 = {len(usable)} 条**，**已损坏 = {len(broken)} 条**")
    A(f"- **分子 = 已产出中文译稿的可用条目数**（随管线推进更新）")
    A(f"- 目标：分子 / 分母 ≥ **{int(CFG['coverage']['target_ratio'] * 100)}%**")
    A("")
    A("> **为什么不把外链算进分母**：大纲另有 "
      f"{len(external)} 条指向外部站点（YouTube / GitHub / X / 第三方博客），"
      "它们不受本地缓存控制，其可获得性取决于对方站点与账号权限，属于**扩展范围**，"
      "计入分母会让覆盖率失去可比性。详见第四节。")
    A("")
    A("### 换算成硬指标")
    A("")
    A("| 口径 | 数量 | 说明 |")
    A("|---|---|---|")
    A(f"| 分母（本地 readings） | {len(local)} | pages {len([u for u in local if u['format']=='html'])} + pdf {len([u for u in local if u['format']=='pdf'])} |")
    A(f"| 可用条目 | {len(usable)} | 内容完整，可进入翻译管线 |")
    A(f"| 损坏条目 | {len(broken)} | 需补抓或声明缺口 |")
    A(f"| 达到 80% 所需最少条目 | {-(-int(len(local) * 0.8))} | ceil({len(local)} × 0.8) |")
    A(f"| 可用英文正文字数（估） | ≈ {words:,} | 仅 HTML 可用条目，PDF 未计 |")
    A("")
    A("---")
    A("")
    A("## 二、缺口清单（必须处理）")
    A("")
    if broken:
        A("以下条目**已在 `pages/` 中登记，但内容不可用**，是当前管线的第一批待办：")
        A("")
        A("| # | 周 | 标题 | 文件 | 字节 | 症状 | 处置建议 |")
        A("|---|---|---|---|---|---|---|")
        for i, u in enumerate(broken, 1):
            sym = "0 字节，抓取完全失败" if u["status"] == "empty" else "占位页，源站反爬拦截"
            fix = "重新抓取源站（见 page_map 中的原始 URL）" if u["status"] == "empty" \
                else "源站为 Medium，自动化访问被拦；需人工导出或声明缺口"
            A(f"| {i} | W{u['week']} | {u['reading_title']} | `{u['local_path']}` | "
              f"{u['bytes']} | {sym} | {fix} |")
        A("")
    else:
        A("无损坏条目。")
        A("")

    # 已知缺失的讲义/视频
    A("### 2.1 讲义（Slides）——**完全缺失**")
    A("")
    A("`slides_info/` 为空目录：**课程 10 周的讲义元数据一条都未抓取到**。")
    A("大纲中登记的讲义链接如下（全部为 Google Slides/Drive，**需 Google 账号**，自动化抓取不可行）：")
    A("")
    A("| 周 | 讲义 | 类型 | 链接 |")
    A("|---|---|---|---|")
    for w in SYLLABUS["weeks"]:
        for lec in w["lectures"]:
            u = lec["url"]
            kind = "Google Slides/Drive" if "docs.google.com" in u else \
                   ("YouTube" if "youtube" in u or "youtu.be" in u else "其它外部")
            A(f"| W{w['week']} | {lec['text'][:40]} | {kind} | {u[:96]} |")
    A("")
    A("### 2.2 视频字幕——**完全缺失**")
    A("")
    A("大纲中的视频均为 YouTube 外链，**无任何字幕文件被获取**。")
    A("若要把视频字幕纳入覆盖范围，需额外的一手获取步骤（yt-dlp 等），")
    A("且需评估网络可达性与版权边界。**当前决定：不纳入分母，列为扩展范围。**")
    A("")

    A("---")
    A("")
    A("## 三、逐周工作单元清单")
    A("")
    A("图例：`OK` 可用 ｜ `EMPTY` 0 字节 ｜ `PLACEHOLDER` 占位页 ｜ `EXTERNAL` 外链")
    A("")
    for w in SYLLABUS["weeks"]:
        wu = [u for u in units if u["week"] == w["week"]]
        ok = len([u for u in wu if u["status"] == "ok"])
        A(f"### Week {w['week']}：{w['title']} ／ {WEEK_TITLES_ZH.get(w['week'], '')}")
        A("")
        A(f"Topics：{'、'.join(w['topics']) if w['topics'] else '—'}")
        A("")
        A(f"| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |")
        A("|---|---|---|---|---|")
        for u in wu:
            st = {"ok": "OK", "empty": "**EMPTY**", "placeholder": "**PLACEHOLDER**",
                  "external": "EXTERNAL", "missing": "**MISSING**"}[u["status"]]
            ref = u.get("local_path") or u.get("source_ref", "")
            wc = f"{u['words_est']:,}" if u.get("words_est") else "—"
            A(f"| {st} | {u['kind']}/{u.get('format', 'link')} | {u['reading_title'][:44]} | `{ref}` | {wc} |")
        A("")
        if not wu:
            A("_（本周无 readings）_")
            A("")

    (ROOT / "source/INVENTORY.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- 控制台摘要 ----
    print(f"工作单元总数 : {len(units)}")
    print(f"  本地可用   : {len(usable)}  (words ≈ {words:,})")
    print(f"  本地损坏   : {len(broken)}  -> {[u['local_path'].split('/')[-1] for u in broken]}")
    print(f"  外部链接   : {len(external)}")
    print(f"覆盖度分母   : {len(local)}   80% 需 >= {-(-int(len(local)*0.8))} 条")
    print(f"已写出       : source/units.json, source/INVENTORY.md")


if __name__ == "__main__":
    main()
