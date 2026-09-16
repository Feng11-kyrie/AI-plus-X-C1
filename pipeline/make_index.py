#!/usr/bin/env python3
"""
生成中文译稿入口索引 `zh/README.md`。

**为什么需要它**

交付物是「让下一批同学零成本复用的中文资料包」。但仓库里原先没有任何**入口**：
`zh/` 下 28 个文件全部以英文单元名命名（`agentic-ai-threats.md` 之类），
README 只有一句「译稿在 `zh/` 下」。

于是出现了最不该出现的情况——**东西都在，但读者找不到**：
有人打开仓库，看到的是 README 里一堆覆盖度数字，却看不到"我该从哪一篇开始读"。

索引按**周**组织，每篇给出：中文标题、原始英文标题、指向译稿的链接、
原文归档链接、中文字数、以及**哪些还没译**（缺口写在明面，不藏）。

索引由脚本生成而不是手写：手写的索引一定会过期（本项目已经因为"手写/声明"
而不是"生成/校验"栽过好几次）。`--check` 模式在 CI 里比对，
索引与仓库实际内容不一致就判失败。

用法
----
  python3 pipeline/make_index.py           # 生成/更新 zh/README.md
  python3 pipeline/make_index.py --check   # 索引与实际内容不一致时返回非零（CI 门禁）
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
P = CFG["paths"]
ZH_DIR = ROOT / P["zh_dir"]
CLEAN_DIR = ROOT / P["clean_dir"]
OUT = ZH_DIR / "README.md"

UNIT_TITLES_ZH = CFG.get("unit_titles_zh", {})

WEEK_ZH = {
    1: "导论：编码 LLM 与 AI 开发", 2: "智能体的解剖学", 3: "AI IDE",
    4: "Claude Code 与智能体编程", 5: "现代终端", 6: "AI 安全与漏洞检测",
    7: "AI 驱动的代码评审", 8: "全栈 AI 开发与部署",
    9: "SRE、可观测性与智能体值班", 10: "AI 软件工程的未来",
}


def plain_len(path: Path) -> int:
    return len(re.sub(r"\s+", "", path.read_text(encoding="utf-8")))


def zh_title(path: Path) -> str:
    """中文标题直接从译稿本身的第一个标题取——不另存一份，避免两处漂移。"""
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^#{1,3}\s+(.*)$", line.strip())
        if m:
            t = re.sub(r"[*`\[\]]|\([^)]*\)", "", m.group(1)).strip()
            return t or "—"
    return "—"


def build() -> str:
    units = json.loads((ROOT / P["units_json"]).read_text(encoding="utf-8"))["units"]
    zh_files = {p.stem: p for p in ZH_DIR.glob("*.md") if p.name != "README.md"}

    done = [u for u in units if u["kind"] == "local"
            and Path(u["local_path"]).stem in zh_files]
    pending = [u for u in units if u["kind"] == "local"
               and Path(u["local_path"]).stem not in zh_files]
    total_chars = sum(plain_len(p) for p in zh_files.values())

    L = ["# 中文资料包（索引）", "",
         "> **本文件由 `pipeline/make_index.py` 自动生成，请勿手工编辑。**", "",
         f"CS146S: The Modern Software Developer（Stanford University, Fall 2025）"
         f"的公开课程资料中文译稿，**{len(done)} 篇**，约 "
         f"**{total_chars:,}** 个中文字符。", "",
         "每一篇都同时提供三种对应关系，便于核对：", "",
         "| 你想看的 | 路径 |", "|---|---|",
         "| 中文译稿 | `zh/<单元名>.md`（下表已直接给出链接） |",
         "| 清洗后的英文底稿 | `clean/<单元名>.md` |",
         "| 原始网页归档 | `source/pages/<单元名>.html` |", "",
         "> 分词块数、覆盖度明细等运行期统计不写进本文件：它们来自 `pipeline/work/` 下的",
         "> **中间产物**（未入库），而 CI 是在全新 checkout 上跑门禁的——索引不能建立在",
         "> 中间产物上，否则门禁会在别人机器上无故变红。逐条状态见 `reports/coverage.md`。", "",
         "> 译稿与底稿**同名**，只是目录不同——想把中英对照阅读时，"
         "两边的章节结构、代码块、表格都是逐块对齐的。", "",
         "---", ""]

    for week in sorted({u["week"] for u in done + pending}):
        L.append(f"## 第 {week} 周：{WEEK_ZH.get(week, '')}")
        L.append("")
        L.append("| 中文标题 | 原文标题 | 译稿 | 中文字数 |")
        L.append("|---|---|---|---|")
        for u in [x for x in done + pending if x["week"] == week]:
            stem = Path(u["local_path"]).stem
            # 中文标题优先取配置里人工审定的译名（单一来源），
            # 其次取译稿本身的第一个标题，避免手写索引过期
            title_zh = UNIT_TITLES_ZH.get(stem) or (
                zh_title(zh_files[stem]) if stem in zh_files else "")
            if stem in zh_files:
                link = f"[`{stem}.md`]({stem}.md)"
                chars = f"{plain_len(zh_files[stem]):,}"
            else:
                link = "**未译**（见下方缺口说明）"
                chars = "—"
            L.append(f"| {title_zh or '—'} | {u['reading_title']} | {link} | {chars} |")
        L.append("")

    L += ["---", "", "## 还没译的部分（如实列出）", ""]
    if pending:
        L.append("| 原文标题 | 周 | 原因 |")
        L.append("|---|---|---|")
        reason = {"empty": "原始缓存就是 0 字节（该条目实为大纲里的一段 YouTube 视频）",
                  "low_content": "抓取到的是 SPA 导航壳 / 登录门页 / JS 外壳，没有正文可译",
                  "placeholder": "抓到的是反爬占位页（源站 Medium，自动访问被 403 拦截）"}
        for u in pending:
            L.append(f"| {u['reading_title']} | W{u['week']} | "
                     f"{reason.get(u.get('status'), u.get('reason') or u.get('status', '—'))} |")
    else:
        L.append("无。")
    L += ["", "另有**不进入本资料包**的部分（讲义 Slides、视频字幕），"
          "原因见根目录 [`README.md`](../README.md) 的「已知缺口」。", "",
          "## 覆盖度口径", "",
          "覆盖率 = 已译条目 / 大纲中指向本地文件的 readings（分母 **34**）。",
          f"当前 **{len(done)}/34 = {len(done)/34*100:.1f}%**，目标 ≥ 80%（≥ 28 条）。",
          "逐条状态见 [`reports/coverage.md`](../reports/coverage.md)。", "",
          "## 怎么用", "",
          "```bash",
          "# 直接读：打开 zh/<单元名>.md（上表有链接）",
          "# 中英对照：同时打开 clean/<单元名>.md",
          "# 想看原始网页：source/pages/<单元名>.html（离线快照，无需联网）",
          "```", "",
          "想把这份资料包**重新生成一遍**（而不是只读）：见根目录 README 的"
          "「如何使用本仓库 → 想复跑或接续这条管线的同学」。", ""]
    return "\n".join(L)


def main() -> int:
    text = build()
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else None
    if "--check" in sys.argv:
        if old != text:
            print("❌ zh/README.md 与实际内容不一致——运行 `python3 pipeline/make_index.py` 重新生成")
            return 1
        print(f"✅ zh/README.md 与仓库实际内容一致（{text.count(chr(10))+1} 行）")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    print(f"已生成 {OUT.relative_to(ROOT)}（{text.count(chr(10))+1} 行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
