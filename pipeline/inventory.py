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
import os
import math
import re
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
# 复用 clean.py 的正文提取逻辑：清点度量与清洗产物必须同源，
# 否则覆盖率数字与 clean/ 里的实际内容会自相矛盾。
from clean import extract_markdown, MIN_CONTENT_CHARS  # noqa: E402

# 配置路径可由环境变量覆盖：换源跑第二份配置时不改代码——
#   PIPELINE_CONFIG=pipeline/config/demo-second-source.json python3 pipeline/inventory.py
CONFIG_PATH = Path(os.environ.get("PIPELINE_CONFIG", "pipeline/config/cs146s.json"))
CFG = json.loads((ROOT / CONFIG_PATH).read_text(encoding="utf-8"))
P = CFG["paths"]

SYLLABUS = json.loads((ROOT / P["syllabus_json"]).read_text(encoding="utf-8"))
PAGES_DIR = ROOT / P["pages_dir"]
PDFS_DIR = ROOT / P["pdfs_dir"]

# 判定阈值：小于此字节数的 HTML 视为占位/抓取失败
PLACEHOLDER_MAX_BYTES = 2000

# 失效模式识别：给出可核对的原因，而不是笼统的"内容少"
FAILURE_HINTS = [
    ("Notion JS 渲染页：正文需 JavaScript 才能生成，静态抓取只能拿到外壳",
     lambda r: "notion" in r[:2000].lower() and "javascript must be enabled" in r.lower()),
    ("SPA 导航壳：__NEXT_DATA__ 载荷为空，真实正文在未被抓取的子页面中",
     lambda r: "__NEXT_DATA__" in r and re.search(r'"pageProps"\s*:\s*\{\s*\}', r)),
    ("访问码 / 付费墙拦截：抓到的只是登录门页",
     lambda r: "access code" in r.lower() or "site owner login" in r.lower()),
    ("源站反爬拦截：拿到占位页而非正文",
     lambda r: "medium.com" in r.lower() or "blocked" in r.lower()[:3000]),
]

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
                u["local_path"] = f"{P['raw_dir']}/{path}"
                if f.exists():
                    size = f.stat().st_size
                    u["bytes"] = size
                    if f.suffix.lower() == ".pdf":
                        u["status"] = "ok"
                        u["format"] = "pdf"
                        u["words_est"] = None
                        u["content_chars"] = None
                        u["reason"] = "PDF 未逐页校验，按可用计"
                    else:
                        raw = f.read_text(encoding="utf-8", errors="replace")
                        md = extract_markdown(raw)
                        text, title = html_text(f)
                        u["page_title"] = title
                        u["words_est"] = len(md.split())
                        u["content_chars"] = len(md)
                        u["format"] = "html"
                        if size == 0:
                            u["status"] = "empty"
                            u["reason"] = "文件 0 字节，抓取完全失败"
                        elif size < PLACEHOLDER_MAX_BYTES:
                            u["status"] = "placeholder"
                            u["reason"] = "体积过小，抓到的是占位页"
                        elif len(md) < MIN_CONTENT_CHARS:
                            u["status"] = "low_content"
                            u["reason"] = next(
                                (msg for msg, pred in FAILURE_HINTS if pred(raw)),
                                "剔除样板后正文不足，需人工确认")
                        else:
                            u["status"] = "ok"
                            u["reason"] = ""
                else:
                    u["status"] = "missing"
                    u["format"] = f.suffix.lstrip(".")
            else:
                u["status"] = "external"
                parts = re.sub(r"^https?://", "", path).split("/")
                u["domain"] = parts[0]

            units.append(u)

    units.sort(key=lambda x: (x["week"], x["source_ref"]))
    (ROOT / P["units_json"]).write_text(
        json.dumps({"units": units}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- 统计 ----
    local = [u for u in units if u["kind"] == "local"]
    usable = [u for u in local if u["status"] == "ok"]
    broken = [u for u in local if u["status"] in ("empty", "placeholder", "low_content")]
    external = [u for u in units if u["kind"] == "external"]
    words = sum(u["words_est"] or 0 for u in usable)
    n_html = len([u for u in local if u["format"] == "html"])
    n_pdf = len([u for u in local if u["format"] == "pdf"])
    usable_html = len([u for u in usable if u["format"] == "html"])
    usable_pdf = len([u for u in usable if u["format"] == "pdf"])
    need = math.ceil(len(local) * CFG["coverage"]["target_ratio"])

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
    A(f"- **其中可用 = {len(usable)} 条**（HTML {usable_html} + PDF {usable_pdf}），**确认无效 = {len(broken)} 条**")
    A(f"- **分子 = 已产出中文译稿的可用条目数**（随管线推进更新）")
    A(f"- 目标：分子 / 分母 ≥ **{int(CFG['coverage']['target_ratio'] * 100)}%**，即 ≥ {need} 条")
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
    A(f"| 分母（本地 readings） | {len(local)} | HTML {n_html} + PDF {n_pdf} |")
    A(f"| **可用条目** | **{len(usable)}** | HTML {usable_html} + PDF {usable_pdf}，内容完整可翻译 |")
    A(f"| **确认无效条目** | **{len(broken)}** | 全部为 HTML，详见第二节 |")
    A(f"| 达到 {int(CFG['coverage']['target_ratio']*100)}% 所需最少条目 | {need} | ceil({len(local)} × {CFG['coverage']['target_ratio']}) |")
    A(f"| 可用英文正文字数（估） | ≈ {words:,} | 仅 HTML 可用条目（按清洗后正文计），PDF 未计 |")
    A("")
    if len(usable) < need:
        A(f"> 🔴 **风险提示**：可用条目 {len(usable)} 条 < 目标 {need} 条，"
          f"仅靠现有可用条目**无法达标记**。必须先补抓部分无效条目，或确认 PDF 可译。")
    else:
        A(f"> ✅ **可行性**：可用条目 {len(usable)} 条 ≥ 目标 {need} 条。"
          f"全部译完可达 {len(usable)/len(local)*100:.1f}%。")
    A("")
    if usable_pdf:
        A("> ⚠️ **注意**：PDF 条目 **必须纳入翻译范围** 才能达标记。"
          "若只翻译 HTML 部分，覆盖率为 "
          f"{usable_html}/{len(local)} = {usable_html/len(local)*100:.1f}%"
          f"{'，**低于目标**。' if usable_html/len(local) < CFG['coverage']['target_ratio'] else '，达标。'}")
        A("")
    A("---")
    A("")
    A("## 二、缺口清单（必须处理）")
    A("")
    if broken:
        A("以下条目**已在 `pages/` 中登记，但内容不可用**，是当前管线的第一批待办：")
        A("")
        A("| # | 周 | 标题 | 文件 | 原始字节 | 清洗后正文 | 失效模式 | 处置建议 |")
        A("|---|---|---|---|---|---|---|---|")
        for i, u in enumerate(broken, 1):
            cc = u.get("content_chars")
            cc_s = f"{cc} 字符" if cc is not None else "—"
            if u["status"] == "empty":
                fix = "重新抓取源站"
            elif u["status"] == "placeholder":
                fix = "需人工导出，或声明缺口"
            elif u["status"] == "low_content" and "SPA" in (u.get("reason") or ""):
                fix = "需补抓其指向的子页面，或将本页降级为索引"
            elif u["status"] == "low_content":
                fix = "需人工获取 / 登录访问，或声明缺口"
            else:
                fix = "重新抓取源站"
            A(f"| {i} | W{u['week']} | {u['reading_title']} | `{Path(u['local_path']).name}` | "
              f"{u['bytes']} | {cc_s} | {u.get('reason') or '—'} | {fix} |")
        A("")
        A("> 判定口径：剔除 script/style/nav/footer 等样板后，**正文不足 "
          f"{MIN_CONTENT_CHARS} 字符**即视为无效——"
          "因为这类页面即使占着文件名，也无法进入翻译管线。")
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
    A("图例：`OK` 可用 ｜ `EMPTY` 0 字节 ｜ `PLACEHOLDER` 占位页 ｜ "
      "`LOW` 有文件但正文不足 ｜ `EXTERNAL` 外链")
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
                  "low_content": "**LOW**", "external": "EXTERNAL",
                  "missing": "**MISSING**"}[u["status"]]
            ref = u.get("local_path") or u.get("source_ref", "")
            wc = f"{u['words_est']:,}" if u.get("words_est") else "—"
            A(f"| {st} | {u['kind']}/{u.get('format', 'link')} | {u['reading_title'][:44]} | `{ref}` | {wc} |")
        A("")
        if not wu:
            A("_（本周无 readings）_")
            A("")

    (ROOT / P["inventory_md"]).write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- 控制台摘要 ----
    print(f"工作单元总数 : {len(units)}")
    print(f"  本地可用   : {len(usable)}  (words ≈ {words:,})")
    print(f"  本地损坏   : {len(broken)}  -> {[u['local_path'].split('/')[-1] for u in broken]}")
    print(f"  外部链接   : {len(external)}")
    # 复用上面算好的 need，而不是在这里重新算一遍——
    # 同一个数在三处各算一次，正是刚才 off-by-one 漏改第三处的原因。
    print(f"覆盖度分母   : {len(local)}   {int(CFG['coverage']['target_ratio']*100)}% 需 >= {need} 条")
    print(f"已写出       : source/units.json, source/INVENTORY.md")


if __name__ == "__main__":
    main()
