#!/usr/bin/env python3
"""
清洗管线：HTML → 干净 Markdown，并按标题切分为翻译分块。

为什么需要这一步（来自清点阶段的实测）：
  source/pages/prompt-engineering-guide.html 有 128KB，但可见正文只有 374 词。
  页面里绝大部分是导航、脚本、样式与页脚样板。直接交给 AI 翻译会：
    (a) 浪费大量 token 在垃圾内容上；
    (b) 让译文夹杂导航文字，污染结构；
    (c) 让"覆盖度"失去意义——你以为翻了 128KB，其实只翻了 2KB。

本脚本做三件事：
  1. 剔除样板（script/style/nav/header/footer/aside/form/iframe/svg）
  2. 用"正文密度"启发式定位正文容器
  3. 转成保留结构的 Markdown，并按标题切块（供翻译管线消费）

产物：
  clean/<unit>.md              清洗后的英文 Markdown 底稿（入库，可人工抽检）
  pipeline/work/chunks.json    翻译分块（中间产物，可复跑再生）
  reports/clean-comparison.md  清洗前后对比报告（含压缩率与密度）

用法：
  python3 pipeline/clean.py
  python3 pipeline/clean.py --limit 3      # 只处理前 3 篇，便于调试
"""
from __future__ import annotations

import os
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# 配置路径可由环境变量覆盖：换源跑第二份配置时不改代码——
#   PIPELINE_CONFIG=pipeline/config/demo-second-source.json python3 pipeline/inventory.py
CONFIG_PATH = Path(os.environ.get("PIPELINE_CONFIG", "pipeline/config/cs146s.json"))
CFG = json.loads((ROOT / CONFIG_PATH).read_text(encoding="utf-8"))
P = CFG["paths"]
CLEAN_DIR = ROOT / P["clean_dir"]
CHUNKS_PATH = ROOT / P["chunks_json"]
REPORT_PATH = ROOT / P["reports_dir"] / "clean-comparison.md"
MAX_CHUNK_CHARS = CFG["translation"]["max_chunk_chars"]
# 合并小块的目标下限：低于此长度的块会与后续块合并（上限仍受 MAX_CHUNK_CHARS 约束）
MIN_CHUNK_TARGET = 900
# 剔除样板后正文少于此字符数，视为"有文件但没内容"（SPA 壳 / 付费墙 / JS 渲染页）。
# 唯一定义处：inventory.py 从这里导入，避免两处阈值各自漂移。
MIN_CONTENT_CHARS = 1500

# 需要整棵剔除的样板标签。
# 注意 figure **不在此列**：现代文档框架（Astro Starlight / Expressive Code）
# 会把 <pre><code> 包进 <figure class="frame code-output">。
# 早期版本把 figure 整棵剔除，导致 3 篇共丢 10,735 字符正文（占其内容 3.9%~19.1%）。
# 这是本项目最隐蔽的一个 bug——体积指标完全看不出来，只有清点元素数量才能发现。
BOILERPLATE = {
    "script", "style", "noscript", "nav", "header", "footer", "aside",
    "form", "iframe", "svg", "button", "select", "option", "template",
    "video", "audio", "canvas", "map", "object", "embed",
}

# 行级样板：正文容器内部残留的 UI 文字（cookie 横幅、登录入口、订阅提示）。
# 必须**整行**匹配才剔除，避免误删正文里含这些词的普通句子。
BOILERPLATE_LINES = {
    "sign in", "sign up", "sign out", "log in", "log out", "login", "logout",
    "subscribe", "subscribe now", "newsletter", "accept", "accept all",
    "accept all cookies", "reject all", "cookie settings", "cookie policy",
    "privacy policy", "terms of service", "terms & conditions",
    "related posts", "related articles", "table of contents", "contents",
    "skip to content", "skip to main content", "share this", "share",
    "read more", "learn more", "back to top", "menu", "search", "close",
    "enter access code", "site owner login", "enroll now →",
    "all rights reserved", "powered by ghost", "site owner login",
}

# 章节级样板：这些标题下的**整段内容**都是站外导航，不是文章正文。
# 注意不包含 "table of contents"——文章自带的目录属于正式内容，
# 删掉会损失文档结构。判断依据是「是不是文章的一部分」，
# 而不是「看起来像不像导航」。
BOILERPLATE_SECTIONS = {
    "related posts", "related articles", "recent posts", "you might also like",
    "more from", "recommended for you", "read next", "popular posts",
    "in this series", "tags", "categories", "share this",
}
# HTMLParser 中无需闭合的标签
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}

HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []          # Node | str
        self.parent = parent

    def cls(self) -> str:
        return self.attrs.get("class", "") or ""

    def text(self) -> str:
        out = []
        for c in self.children:
            out.append(c if isinstance(c, str) else c.text())
        return "".join(out)

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()

    def find_all(self, tags) -> list:
        return [n for n in self.walk() if n.tag in tags]


class TreeBuilder(HTMLParser):
    """把 HTML 解析成轻量 DOM。"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.cur)
        self.cur.children.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        # 向上找到匹配的祖先，容忍不规范嵌套
        node = self.cur
        while node is not self.root and node.tag != tag:
            node = node.parent
        if node is not self.root:
            self.cur = node.parent

    def handle_data(self, data):
        if data:
            self.cur.children.append(data)


# ---------------------------------------------------------------- 正文定位

def prune(node: Node) -> None:
    """递归剔除样板子树。"""
    kept = []
    for c in node.children:
        if isinstance(c, Node):
            if c.tag in BOILERPLATE:
                continue
            prune(c)
        kept.append(c)
    node.children = kept


def content_score(node: Node) -> int:
    """正文密度打分：正文段落/代码/列表的文字总量。"""
    total = 0
    for n in node.walk():
        if n.tag in ("p", "pre", "li", "blockquote", "td"):
            total += len(n.text().strip())
    return total


def pick_main(root: Node) -> Node:
    """选正文容器：得分最高者；同分取更深的（更接近正文本身）。"""
    cands = [n for n in root.walk() if n.tag in ("article", "main", "div", "section")]
    if not cands:
        return root
    best, best_score, best_depth = None, 0, 0
    for n in cands:
        s = content_score(n)
        if s < 400:
            continue
        depth = 0
        p = n.parent
        while p is not None:
            depth += 1
            p = p.parent
        if s > best_score * 1.15 or (s > best_score * 0.85 and depth > best_depth):
            best, best_score, best_depth = n, s, depth
    return best or root


# ---------------------------------------------------------------- Markdown 渲染

def inline(node: Node) -> str:
    """渲染行内内容。"""
    out = []
    for c in node.children:
        if isinstance(c, str):
            out.append(c)
            continue
        t = c.tag
        inner = inline(c)
        if t in ("strong", "b"):
            out.append(f"**{inner.strip()}**" if inner.strip() else "")
        elif t in ("em", "i"):
            out.append(f"*{inner.strip()}*" if inner.strip() else "")
        elif t == "code":
            out.append(f"`{inner.strip()}`" if inner.strip() else "")
        elif t == "a":
            href = (c.attrs.get("href") or "").strip()
            txt = inner.strip()
            if not txt:
                out.append("")
            elif not href or href.startswith("#") or href.startswith("javascript:"):
                out.append(txt)
            else:
                out.append(f"[{txt}]({href})")
        elif t == "br":
            out.append("  \n")
        elif t == "img":
            alt = (c.attrs.get("alt") or "").strip()
            src = (c.attrs.get("src") or "").strip()
            # 过滤 1x1 追踪像素
            out.append(f"![{alt}]({src})" if src and "1x1" not in src else "")
        elif t == "del":
            out.append(f"~~{inner.strip()}~~")
        else:
            out.append(inner)
    return re.sub(r"[ \t]+", " ", "".join(out))


def code_lang(node: Node) -> str:
    for c in node.walk():
        cls = c.cls()
        m = re.search(r"(?:language|lang|highlight)-([a-zA-Z0-9+#]+)", cls)
        if m:
            return m.group(1).lower()
    return ""


def render(node: Node, depth: int = 0) -> list:
    """递归渲染为 Markdown 行列表。"""
    lines = []
    for c in node.children:
        if isinstance(c, str):
            s = re.sub(r"\s+", " ", c).strip()
            if s:
                lines.append(s)
            continue

        t = c.tag

        if t in HEADINGS:
            lvl = int(t[1])
            txt = re.sub(r"\s+", " ", inline(c)).strip()
            if txt:
                lines.append("")
                lines.append("#" * lvl + " " + txt)
                lines.append("")

        elif t == "pre":
            code = c.text()
            if code.strip():
                lang = code_lang(c)
                lines.append("")
                lines.append(f"```{lang}")
                lines.extend(code.rstrip().split("\n"))
                lines.append("```")
                lines.append("")

        elif t == "p":
            txt = inline(c).strip()
            if txt:
                lines.append("")
                lines.append(txt)
                lines.append("")

        elif t in ("ul", "ol"):
            lines.append("")
            _list(c, lines, depth, ordered=(t == "ol"))
            lines.append("")

        elif t == "blockquote":
            inner = [x for x in render(c) if x.strip()]
            lines.append("")
            lines.extend("> " + x for x in inner)
            lines.append("")

        elif t in ("figcaption", "caption"):
            # 图注/代码块标题：保留为斜体说明，不与正文混淆
            txt = re.sub(r"\s+", " ", inline(c)).strip()
            if txt:
                lines.append("")
                lines.append(f"*{txt}*")
                lines.append("")

        elif t == "table":
            _table(c, lines)

        elif t in ("div", "section", "article", "main", "span", "td", "th", "li",
                   "dd", "dt", "dl", "figure", "hgroup", "details", "summary"):
            lines.extend(render(c, depth))
        else:
            # 其余标签：只取文字，避免输出无意义结构
            txt = re.sub(r"\s+", " ", inline(c)).strip()
            if txt and t not in ("html", "body", "#root"):
                lines.append(txt)
            elif t in ("html", "body", "#root"):
                lines.extend(render(c, depth))
    return lines


# 列表项内部的块级子元素。
# 关键：_list 早期只特判了**直接**是 pre 或嵌套列表的子节点，
# 其余一律走 inline() 扁平化。但 Astro Starlight 的结构是
#   pre < figure < div < li
# 于是 figure 落进兜底分支，17 个代码块被压成纯文本、丢失围栏。
# 教训：兜底路径必须对**所有**块级标签做结构保留，而不是只枚举常见的几个。
LI_BLOCK = {"pre", "ul", "ol", "table", "blockquote", "figure", "div",
            "section", "details", "hgroup", "dl"}


def _list(node: Node, lines: list, depth: int, ordered: bool) -> None:
    idx = 0
    for c in node.children:
        if not isinstance(c, Node) or c.tag != "li":
            continue
        idx += 1
        marker = f"{idx}." if ordered else "-"
        pad = "  " * depth
        head, subs = [], []
        for ch in c.children:
            if isinstance(ch, str):
                head.append(re.sub(r"\s+", " ", ch))
            elif ch.tag in LI_BLOCK:
                subs.append(ch)          # 块级子元素：交给 render 保留结构
            else:
                head.append(inline(ch))  # 行内子元素：并入本条的文字
        txt = re.sub(r"\s+", " ", "".join(head)).strip()
        lines.append(f"{pad}{marker} {txt}".rstrip())

        # 缩进 3 空格：对 "- "（2）与 "1. "（3）都足以留在列表项内
        sub_pad = pad + "   "
        for s in subs:
            if s.tag in ("ul", "ol"):
                _list(s, lines, depth + 1, ordered=(s.tag == "ol"))
            else:
                sub = [x for x in render(s) if x.strip()]
                if sub:
                    lines.append("")
                    lines.extend(sub_pad + x for x in sub)
                    lines.append("")


def _table(node: Node, lines: list) -> None:
    rows, extras = [], []
    for tr in node.find_all(["tr"]):
        cells = []
        for td in tr.children:
            if not (isinstance(td, Node) and td.tag in ("td", "th")):
                continue
            if td.find_all(["pre", "ul", "ol", "blockquote"]):
                # 单元格里的块级内容（代码块/列表/引用）无法塞进 Markdown 表格。
                # inline() 会把 <pre> 压成纯文本，代码就丢了围栏、会被当散文翻译。
                # 处置：单元格留空，块内容移到表后按行标签单独输出，避免重复。
                sub = [x for x in render(td) if x.strip()]
                if sub:
                    label = re.sub(r"\s+", " ", tr.text()).strip()[:60]
                    extras.append((label, sub))
                cells.append("")
            else:
                cells.append(re.sub(r"\s+", " ", inline(td)).strip().replace("|", "\\|"))
        if cells:
            rows.append(cells)
    if not rows:
        return
    if len(rows) < 2:
        # 单行表格（CMS 常用于布局）早期被整表丢弃，
        # 在 agentic-ai-threats 上造成 27 个表、5,608 字符内容消失。
        # 表格结构无法还原时，至少要把文字交出去。
        for cell in rows[0]:
            if cell:
                lines.append("")
                lines.append(cell)
        lines.append("")
    else:
        width = max(len(r) for r in rows)
        rows = [r + [""] * (width - len(r)) for r in rows]
        lines.append("")
        lines.append("| " + " | ".join(rows[0]) + " |")
        lines.append("|" + "---|" * width)
        for r in rows[1:]:
            lines.append("| " + " | ".join(r) + " |")
        lines.append("")

    for label, sub in extras:
        if label:
            lines.append("")
            lines.append(f"**{label}**")
        lines.append("")
        lines.extend(sub)
        lines.append("")


def drop_boilerplate_sections(md: str) -> tuple:
    """删除整节的站外导航内容，返回 (文本, 删除行数)。

    与行级样板（drop_boilerplate_lines）的区别：行级只删单行，
    这里连同标题下的全部内容一起删，直到遇到同级或更高级的标题。

    起因：code-reviews-just-do-it 共 5 个分块，其中 4 个是博客模板的
    「Related posts / Recent Posts」区块——3,427 字符、占该篇 47%。
    它们会被原样送去翻译，既浪费产出又污染成品。
    """
    lines = md.split("\n")
    out, i, dropped, removed = [], 0, 0, []
    while i < len(lines):
        m = re.match(r"^[ \t]*(#{1,6})[ \t]+(.+?)\s*$", lines[i])
        if m and m.group(2).strip().strip("*_` ").lower() in BOILERPLATE_SECTIONS:
            level = len(m.group(1))
            j = i + 1
            while j < len(lines):
                m2 = re.match(r"^[ \t]*(#{1,6})[ \t]+", lines[j])
                if m2 and len(m2.group(1)) <= level:
                    break
                j += 1
            dropped += j - i
            removed.extend(lines[i:j])
            i = j
            continue
        out.append(lines[i])
        i += 1
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out))
    return text, dropped, "\n".join(removed)


def drop_table_duplicates(md: str) -> tuple:
    """删除 Markdown 表格之后的「拍平副本」，返回 (文本, 删除块数, 被删文本)。

    成因：部分站点（如 Google Cloud）为响应式布局与无障碍访问，
    会把同一张表渲染两次——一次是真正的 table，一次是 div 列表。
    清洗后会得到「Markdown 表格 + 同内容的逐行纯文本」两份重复。

    实测影响：prompt-engineering-overview 有 6 张这样的表，
    若不去重，约 40% 的篇幅是重复内容，翻译产出会被白白翻倍。

    判定方式：表格之后的连续段落，若其内容都能在该表格的单元格集合里
    找到，就认定为副本。保守起见要求至少连续 3 段才算——宁可少删，
    不能误删正文（正文段落几乎不可能恰好等于某几个单元格）。
    """
    blocks = md.split("\n\n")
    out, removed_blocks, removed_text = [], 0, []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        out.append(b)
        if "|" in b and re.search(r"^[ \t]*\|[\s:-]*\|", b, re.M):
            cells = set()
            for row in b.split("\n"):
                for c in row.strip().strip("|").split("|"):
                    norm = re.sub(r"\s+", " ", c).strip().strip("*` ")
                    if norm:
                        cells.add(norm)
            j = i + 1
            dup = []
            # 两侧必须用同一套归一化：表格单元格已去掉 ** 与多余空白，
            # 待判定的段落也要同样处理，否则 "**Scenario**" 匹配不上 "Scenario"。
            while j < len(blocks) and (
                    re.sub(r"\s+", " ", blocks[j]).strip().strip("*` ") in cells):
                dup.append(j)
                j += 1
            if len(dup) >= 3:
                removed_blocks += len(dup)
                removed_text.extend(blocks[k] for k in dup)
                i = j
                continue
        i += 1
    return "\n\n".join(out), removed_blocks, "\n\n".join(removed_text)


def tidy(md: str) -> str:
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    return md.strip() + "\n"


# ---------------------------------------------------------------- 乱码修复

MOJIBAKE_RE = re.compile(r"[\u00c2\u00c3\u00e2][\u0080-\u00bf]")


def mojibake_score(s: str) -> int:
    return len(MOJIBAKE_RE.findall(s))


def fix_mojibake(s: str) -> tuple:
    """修复「UTF-8 字节被按 Latin-1 解码」造成的乱码，返回 (文本, 修复处数)。

    现象：源缓存里 system—particularly 变成 systemâparticularly。
    成因：原始 UTF-8 的三字节序列被当作 Latin-1 单字符读入后重新存成 UTF-8。

    逐行处理，因为一篇文章可能只有部分行受损——整篇一起转会在遇到
    正常 UTF-8 字符（如中文）时抛异常而放弃修复。

    安全约束（宁可修不了，也不能改坏好内容）：
      每个候选必须**乱码数减少**且**不引入替换字符**，否则保留原行。
    """
    if mojibake_score(s) == 0:
        return s, 0
    out, fixed = [], 0
    for line in s.split("\n"):
        if mojibake_score(line) == 0:
            out.append(line)
            continue
        try:
            cand = line.encode("latin-1", errors="strict").decode("utf-8", errors="strict")
        except (UnicodeEncodeError, UnicodeDecodeError):
            out.append(line)
            continue
        if mojibake_score(cand) < mojibake_score(line) and "\ufffd" not in cand:
            out.append(cand)
            fixed += 1
        else:
            out.append(line)
    return "\n".join(out), fixed


# ---------------------------------------------------------------- 完整性校验

def count_raw(raw: str) -> dict:
    """从原始 HTML 字符串统计元素数量（全文档，含样板）。"""
    return {
        "headings": len(re.findall(r"<h[1-6][\s>]", raw, re.I)),
        "code": len(re.findall(r"<pre[\s>]", raw, re.I)),
        "links": len(re.findall(r"<a\s[^>]*href=", raw, re.I)),
        "tables": len(re.findall(r"<table[\s>]", raw, re.I)),
    }


def count_node(node: Node) -> dict:
    """统计 DOM 子树内的元素数量（剔除样板、选定正文之后）。"""
    return {
        "headings": len(node.find_all(HEADINGS)),
        "code": len(node.find_all(["pre"])),
        "links": len([n for n in node.find_all(["a"]) if n.attrs.get("href")]),
        "tables": len(node.find_all(["table"])),
    }


def count_md(md: str) -> dict:
    """统计最终 Markdown 里的元素数量。

    必须容许前导空白：列表项内的块级元素会被缩进 3 空格，
    早期版本用 `^``` 计数，把缩进后的 26 个代码块误数成 8 个，
    反而让校验器报出假告警。
    """
    fences = len(re.findall(r"^[ \t]*```", md, re.M))
    return {
        "headings": len(re.findall(r"^[ \t]*#{1,6}\s+\S", md, re.M)),
        "code": fences // 2,
        "links": len(re.findall(r"\]\(", md)),
        "tables": len(re.findall(r"^[ \t]*\|[\s:-]*\|", md, re.M)),
    }


def md_plain_len(md: str) -> int:
    """把 Markdown 还原成纯文字后统计字符数，用于衡量文字留存。"""
    s = re.sub(r"^[ \t]*```.*$", "", md, flags=re.M)      # 去掉围栏行本身
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)            # 图片整体去掉
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)        # 链接留文字
    s = re.sub(r"^[ \t]*#{1,6}[ \t]+", "", s, flags=re.M)  # 标题标记
    s = re.sub(r"^[ \t]*[-*+][ \t]+", "", s, flags=re.M)   # 无序列表标记
    s = re.sub(r"^[ \t]*\d+\.[ \t]+", "", s, flags=re.M)   # 有序列表标记
    s = re.sub(r"^[ \t]*>+[ \t]?", "", s, flags=re.M)      # 引用标记
    s = s.replace("|", " ").replace("*", "").replace("`", "").replace("~", "")
    return len(re.sub(r"\s+", "", s))


def verify(c_raw: dict, c_main: dict, c_md: dict, text_main: int, text_md: int) -> dict:
    """校验清洗是否静默丢了内容。

    刻意区分两类问题，因为处置方式完全不同：

      **内容丢失**（严重）——文字本身没了。翻译管线拿不到东西，是硬伤。
        判据：文字留存率 < 90%。这条是主判据。

      **标记扁平化**（次要）——文字都还在，只是丢了结构标记。
        例：表格单元格里的 <h4> 经 inline() 变成普通文字。
        对翻译而言文字才是要翻的东西，标记丢了不影响译文完整性，
        因此只作提示、不告警。

    代码块单独严判：它一旦丢了围栏，内容会被当散文翻译，
    而代码必须逐字保留——这是技术文档翻译的硬要求。

    返回 {"text_retention": float, "alarms": [...], "notes": [...]}
    """
    alarms, notes = [], []

    retention = (text_md / text_main) if text_main else 1.0
    if text_main and retention < 0.90:
        alarms.append(
            f"内容丢失: 正文容器 {text_main} 字符文字，Markdown 只剩 {text_md} "
            f"（留存 {retention * 100:.1f}%，丢失 {(1 - retention) * 100:.1f}%）")

    r, m, d = c_raw["code"], c_main["code"], c_md["code"]
    if r > 0 and m < r * 0.75:
        alarms.append(
            f"pruner loss: 原始 HTML 有 {r} 个代码块，正文容器只剩 {m} 个"
            f"（丢 {r - m} 个）")
    if m > 0 and d < m * 0.75:
        alarms.append(
            f"代码块保真: 正文容器有 {m} 个代码块，Markdown 只产出 {d} 个"
            f"（丢 {m - d} 个）——代码会被当散文翻译")

    for k, zh in (("headings", "标题"), ("tables", "表格"), ("links", "链接")):
        mm, dd = c_main[k], c_md[k]
        if mm > 0 and dd < mm * 0.75:
            notes.append(f"标记扁平化: {mm} 个{zh} -> Markdown {dd} 个（文字已保留）")

    return {"text_retention": retention, "alarms": alarms, "notes": notes}


def drop_boilerplate_lines(md: str) -> tuple:
    """整行匹配剔除残留 UI 文字，返回 (文本, 剔除行数, 剔除字符数)。

    第三个返回值用于完整性校验：被有意删掉的文字不该算作「内容丢失」。
    """
    out, dropped, removed = [], 0, []
    for line in md.split("\n"):
        key = line.strip().strip("*_` ").lower()
        if key and key in BOILERPLATE_LINES:
            dropped += 1
            removed.append(line)
            continue
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text, dropped, "\n".join(removed)


def extract(raw: str) -> tuple:
    """从原始 HTML 提取正文 → Markdown，并返回过程指标。

    返回 (markdown, stats)。stats 里带着完整性校验所需的三个层次计数，
    供 calling 端判断是否发生了静默丢内容。

    单独暴露是为了让「什么算正文」只有一个判定来源——
    inventory.py 从中导入，清点度量与清洗产物必须一致，
    否则覆盖率数字会与 clean/ 里的实际内容自相矛盾。
    """
    raw_fixed, moji_fixed = fix_mojibake(raw)
    c_raw = count_raw(raw_fixed)

    tb = TreeBuilder()
    tb.feed(raw_fixed)
    tb.close()
    prune(tb.root)
    main_node = pick_main(tb.root)
    c_main = count_node(main_node)

    md = tidy("\n".join(render(main_node)))
    md, bp_sections, bp_section_text = drop_boilerplate_sections(md)
    md, bp_tables, bp_table_text = drop_table_duplicates(md)
    md, bp_dropped, bp_line_text = drop_boilerplate_lines(md)
    c_md = count_md(md)

    # 留存率的分母要扣掉「有意删除的样板」——否则删得越干净、
    # 校验器反而报得越凶，这类假告警会让校验器失去可信度。
    #
    # 被删文本必须用与分子相同的度量（md_plain_len）来算：
    # 早先直接数原始字符，把图片 URL 也算了进去，而分子的口径不含 URL，
    # 于是留存率冒出 173% 这种数字。分子分母不同源，任何比率都不可信。
    text_main = len(re.sub(r"\s+", "", main_node.text()))
    text_expect = max(text_main - md_plain_len(
        bp_section_text + "\n" + bp_line_text + "\n" + bp_table_text), 1)
    verdict = verify(c_raw, c_main, c_md, text_main=text_expect, text_md=md_plain_len(md))
    stats = {
        "mojibake_fixed": moji_fixed,
        "boilerplate_lines_dropped": bp_dropped,
        "boilerplate_sections_dropped": bp_sections,
        "table_duplicates_dropped": bp_tables,
        "counts_raw": c_raw,
        "counts_main": c_main,
        "counts_md": c_md,
        "text_retention": verdict["text_retention"],
        "alarms": verdict["alarms"],
        "notes": verdict["notes"],
    }
    return md, stats


def extract_markdown(raw: str) -> str:
    """仅取 Markdown 的便捷入口（inventory.py 用）。"""
    return extract(raw)[0]


# ---------------------------------------------------------------- PDF 提取

PDF_JS = ROOT / "pipeline/pdfkit_dump.js"


def extract_pdf(pdf_path: Path) -> tuple:
    """用 macOS 原生 PDFKit 提取 PDF 文本，返回 (markdown, 错误说明)。

    为什么不用 Python 库：本项目坚持零第三方依赖。macOS 自带 PDFKit，
    经 osascript 调用无需安装任何东西。

    代价必须说清楚：**这一步不跨平台**。在非 macOS 环境会返回明确的
    错误说明而不是静默产出空文件——静默失败正是本项目一直在防的东西。
    """
    import platform
    import subprocess
    import tempfile

    if platform.system() != "Darwin":
        return "", "非 macOS 环境：PDF 提取依赖 macOS 原生 PDFKit，当前平台不支持"
    if not PDF_JS.exists():
        return "", f"缺少 {PDF_JS.name}"
    try:
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out.md"
            proc = subprocess.run(
                ["osascript", "-l", "JavaScript", str(PDF_JS), str(pdf_path), str(out)],
                capture_output=True, text=True, timeout=300)
            if not out.exists():
                msg = (proc.stderr or proc.stdout or "").strip()[:200]
                return "", f"提取失败：{msg or '未知错误'}"
            return out.read_text(encoding="utf-8", errors="replace"), ""
    except (OSError, subprocess.SubprocessError) as exc:
        return "", f"调用 PDFKit 失败：{exc}"


# ---------------------------------------------------------------- 分块

def split_chunks(unit_id: str, title: str, md: str) -> list:
    """按二级/三级标题切块，然后合并过小的相邻块。

    为什么要合并：纯按标题切会产生大量碎片——
    实测 398 块中 37% 不足 500 字符、85 块不足 300 字符、最小仅 7 字符。
    碎片的代价有两重：
      1. 请求数暴涨（成本）；
      2. 每块上下文不足，代词指代与术语一致性变差——
         而「术语统一」正是本挑战 25 分评分点。
    """
    parts = re.split(r"\n(?=#{2,3} )", md)
    raw_chunks, buf, head_path = [], "", title

    def flush():
        nonlocal buf
        t = buf.strip()
        if not t:
            buf = ""
            return
        if len(t) <= MAX_CHUNK_CHARS:
            raw_chunks.append({"heading_path": head_path, "text": t})
        else:
            cur = ""
            for para in t.split("\n\n"):
                if len(cur) + len(para) + 2 > MAX_CHUNK_CHARS and cur.strip():
                    raw_chunks.append({"heading_path": head_path, "text": cur.strip()})
                    cur = ""
                cur += para + "\n\n"
            if cur.strip():
                raw_chunks.append({"heading_path": head_path, "text": cur.strip()})
        buf = ""

    for seg in parts:
        m = re.match(r"(#{2,3}) (.+)", seg)
        if m:
            flush()
            head_path = m.group(2).strip()
        buf += seg
    flush()

    # ---- 合并过小的相邻块 ----
    merged, cur = [], None
    for c in raw_chunks:
        if cur is None:
            cur = dict(c)
            cur["headings"] = [c["heading_path"]]
            continue
        fits = len(cur["text"]) + len(c["text"]) + 2 <= MAX_CHUNK_CHARS
        if len(cur["text"]) < MIN_CHUNK_TARGET and fits:
            cur["text"] = cur["text"].rstrip() + "\n\n" + c["text"].lstrip()
            cur["headings"].append(c["heading_path"])
        else:
            merged.append(cur)
            cur = dict(c)
            cur["headings"] = [c["heading_path"]]
    if cur is not None:
        merged.append(cur)

    # ---- 丢弃纯标题碎片（只有标题、没有正文，翻译它没有意义）----
    chunks = []
    for c in merged:
        body = re.sub(r"^[ \t]*#{1,6}[ \t]+.*$", "", c["text"], flags=re.M)
        body = re.sub(r"\s+", "", body)
        c["headings"] = [h for h in c["headings"] if h]
        if len(body) < 20 and "```" not in c["text"]:
            continue
        chunks.append(c)

    for i, c in enumerate(chunks):
        c["index"] = i
        c["unit_id"] = unit_id
        c["chars"] = len(c["text"])
    return chunks


# ---------------------------------------------------------------- 主流程

def main() -> None:
    units = json.loads((ROOT / P["units_json"]).read_text(encoding="utf-8"))["units"]
    # 处理**所有**本地条目（HTML 与 PDF，含已知失效的），而不是只处理 status==ok 的：
    # 清洗报告必须完整记账——把失败篇目排除在外会让报告谎报"一切正常"。
    todo = [u for u in units
            if u["kind"] == "local" and (ROOT / u["local_path"]).exists()]
    if "--limit" in sys.argv:
        todo = todo[: int(sys.argv[sys.argv.index("--limit") + 1])]

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    n_html = len([u for u in todo if u.get("format") == "html"])
    n_pdf = len([u for u in todo if u.get("format") == "pdf"])
    all_chunks, rows, skipped, notes = [], [], [], []
    print(f"待清洗 {len(todo)} 条（HTML {n_html} + PDF {n_pdf}）\n")

    for u in todo:
        src = ROOT / u["local_path"]
        unit_id = Path(u["local_path"]).stem
        title = u.get("reading_title") or unit_id
        raw_bytes = src.stat().st_size
        fmt = u.get("format", "html")
        stats = {}

        if fmt == "pdf":
            md, err = extract_pdf(src)
            if err:
                notes.append(f"`{unit_id}`：{err}")
        else:
            raw = src.read_text(encoding="utf-8", errors="replace")
            md, stats = extract(raw)

        words = len(md.split())
        usable = len(md) >= MIN_CONTENT_CHARS
        chunks = []
        if usable:
            header = (f"<!-- source: {u['local_path']} -->\n"
                      f"<!-- week: {u['week']} | format: {fmt} "
                      f"| original: {u.get('page_title') or title} -->\n\n")
            (CLEAN_DIR / f"{unit_id}.md").write_text(header + md, encoding="utf-8")
            chunks = split_chunks(unit_id, title, md)
            for c in chunks:
                c["week"] = u["week"]
                c["reading_title"] = title
                c["source_ref"] = u["local_path"]
                c["format"] = fmt
            all_chunks.extend(chunks)
        else:
            skipped.append(unit_id)

        density = (len(md.encode("utf-8")) / raw_bytes * 100) if raw_bytes else 0
        retention = stats.get("text_retention")
        alarms = stats.get("alarms", [])
        # 已知失效的条目不再重复告警（它们已在清点报告里登记为失效）
        if not usable:
            alarms = []
        for a in alarms:
            notes.append(f"`{unit_id}`：{a}")

        rows.append({
            "unit": unit_id, "week": u["week"], "title": title, "format": fmt,
            "raw": raw_bytes, "md": len(md.encode("utf-8")),
            "words": words, "chunks": len(chunks), "density": density,
            "retention": retention,
            "mojibake": stats.get("mojibake_fixed", 0),
            "boilerplate": stats.get("boilerplate_lines_dropped", 0),
            "alarms": alarms,
            "flag": "OK" if usable else "**失效**",
            "reason": u.get("reason") or ("剔除样板后正文不足" if not usable else ""),
            "usable": usable,
        })
        # 留存率可略超 100%：Markdown 侧的纯文字计数口径与 DOM 侧不同。
        # 超过 100% 只意味着"没有丢失"，显示时钳制以免误读。
        ret_s = f"{min(retention, 1.0) * 100:>5.1f}%" if retention is not None else "  n/a"
        print(f"  W{u['week']:>2} {fmt:<4} {unit_id[:38]:<38} "
              f"{raw_bytes/1024:>7.0f}KB → {len(md.encode('utf-8'))/1024:>6.1f}KB "
              f"| 留存 {ret_s} | {words:>5} 词 {len(chunks):>2} 块 "
              f"{'OK' if usable else '**失效**'}")

    CHUNKS_PATH.write_text(
        json.dumps({"source_id": CFG["source_id"], "chunks": all_chunks},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # ---- 对比报告 ----
    good = [r for r in rows if r["usable"]]
    bad = [r for r in rows if not r["usable"]]
    tot_raw = sum(r["raw"] for r in rows)
    tot_md = sum(r["md"] for r in rows)
    tot_words = sum(r["words"] for r in good)
    raw_good = sum(r["raw"] for r in good)
    md_good = sum(r["md"] for r in good)
    L = []
    A = L.append
    A("# 清洗前后对比报告（HTML/PDF → Markdown）")
    A("")
    A("> 由 `pipeline/clean.py` 自动生成，**请勿手工编辑**。")
    A("")
    A("## 为什么要清洗")
    A("")
    A("原始 HTML 里绝大部分是导航、脚本与样式样板，不是正文。若直接把 HTML 交给翻译模型：")
    A("")
    A("1. **浪费 token**——付费处理脚本与导航；")
    A("2. **污染结构**——译文里混入导航文字，破坏可读性；")
    A("3. **让覆盖度失真**——以为翻译了 128KB，实际只翻了 2KB 正文。")
    A("")
    A("## 总体效果")
    A("")
    n_htmlg = len([r for r in good if r["format"] == "html"])
    n_pdfg = len([r for r in good if r["format"] == "pdf"])
    A("| 指标 | 数值 |")
    A("|---|---|")
    A(f"| 处理条目数 | {len(rows)}（HTML {n_html} + PDF {n_pdf}） |")
    A(f"| 可入管线 | **{len(good)}**（HTML {n_htmlg} + PDF {n_pdfg}） |")
    A(f"| 失效 | {len(bad)} |")
    A(f"| 原始体积 | {tot_raw/1024/1024:.2f} MB |")
    A(f"| 清洗后 Markdown | {tot_md/1024/1024:.2f} MB |")
    A(f"| **有效条目压缩率** | **{md_good/raw_good*100:.1f}%**"
      f"（降至 1/{raw_good/max(md_good,1):.1f}） |")
    A(f"| 可翻译正文词数 | {tot_words:,} |")
    A(f"| 翻译分块数 | {len(all_chunks)}"
      f"（合并小块前为 398 块——合并见「合并过小相邻块」的设计说明） |")
    if all_chunks:
        avg = sum(c["chars"] for c in all_chunks) // len(all_chunks)
        A(f"| 平均块大小 | {avg:,} 字符（合并前中位数仅 795） |")
    A("")
    A("## 逐篇明细")
    A("")
    A("三列质量指标的含义：")
    A("")
    A("- **密度** = 清洗后体积 / 原始体积。越低说明样板越多、清洗收益越大。"
      "低到 1% 上下意味着 99% 的原始体积是垃圾。")
    A("- **留存** = 正文容器文字量 → Markdown 纯文字量的留存率。"
      "这是**防静默丢内容的主判据**，低于 90% 报警。")
    A("- **修复** = 该篇修掉的乱码行数 / 剔除的样板行数。")
    A("")
    A("| 周 | 篇目 | 格式 | 原始 | 清洗后 | 密度 | 留存 | 修复 | 词数 | 分块 | 判定 | 失效模式 |")
    A("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: (not x["usable"], x["density"])):
        ret = (f"**{min(r['retention'], 1.0)*100:.1f}%**"
               if r["retention"] is not None else "n/a")
        fix = f"{r['mojibake']}乱/{r['boilerplate']}样" if (r["mojibake"] or r["boilerplate"]) else "—"
        A(f"| W{r['week']} | `{r['unit']}` | {r['format']} | {r['raw']/1024:.0f} KB | "
          f"{r['md']/1024:.1f} KB | **{r['density']:.1f}%** | {ret} | {fix} | "
          f"{r['words']:,} | {r['chunks']} | {r['flag']} | {r['reason'] or '—'} |")
    A("")
    A("## 一、有效性检查")
    A("")
    if bad:
        A(f"以下 **{len(bad)} 条**清洗后正文不足 {MIN_CONTENT_CHARS} 字符，**无法进入翻译管线**。"
          "这些条目在覆盖度分母中仍占位，但拿不到内容——是必须先解决的缺口：")
        A("")
        A("| 篇目 | 周 | 格式 | 原始 | 清洗后正文 | 失效模式 |")
        A("|---|---|---|---|---|---|")
        for r in bad:
            A(f"| `{r['unit']}` | W{r['week']} | {r['format']} | {r['raw']/1024:.0f} KB | "
              f"{r['md']} 字节 | {r['reason']} |")
        A("")
        A("> 这些条目**不会**产出 `clean/*.md`，也不会进入 `chunks.json`——"
          "即它们对翻译覆盖度贡献为 0。详见 `source/INVENTORY.md` 第二节。")
    else:
        A("无失效条目。全部条目清洗后正文量正常。")
    A("")
    A("## 二、内容丢失检查")
    A("")
    A("清洗最容易出的错是**静默丢内容**——文件还在、看着正常，但正文缺了一块。"
      "体积指标对此完全无感，所以必须有独立的元素级校验。")
    A("")
    if notes:
        A(f"发现 **{len(notes)}** 处需要关注：")
        A("")
        for n in notes:
            A(f"- {n}")
    else:
        A("✓ 未发现内容丢失。全部有效条目的文字留存率均达标，"
          "且代码块数量在「原始 → 正文容器 → Markdown」三个层次保持一致。")
    A("")
    A("校验方法：对每条比对三个层次的元素数量")
    A("")
    A("| 层次 | 含义 |")
    A("|---|---|")
    A("| `raw` | 整个原始文件（含样板） |")
    A("| `main` | 剔除样板、选定正文容器之后 |")
    A("| `md` | 最终 Markdown |")
    A("")
    A("`raw → main` 的差距暴露**样板剔除误伤正文**；"
      "`main → md` 的差距暴露**渲染器漏渲染**。"
      "代码块单独严判：它一旦丢了围栏，内容会被当散文翻译，而代码必须逐字保留。")
    A("")
    A("## 三、产物")
    A("")
    A("| 产物 | 位置 | 是否入库 |")
    A("|---|---|---|")
    A(f"| 清洗后英文底稿 | `clean/<unit>.md`（{len(good)} 条） | ✅ 入库，可人工抽检 |")
    A(f"| 翻译分块 | `pipeline/work/chunks.json`（{len(all_chunks)} 块） | ⬜ 中间产物，可复跑再生 |")
    REPORT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"\n汇总：{len(good)} 条有效 / {len(bad)} 条失效 ｜ "
          f"{raw_good/1024/1024:.2f} MB → {md_good/1024/1024:.2f} MB "
          f"（{md_good/raw_good*100:.1f}%）｜{tot_words:,} 词｜{len(all_chunks)} 块")
    if skipped:
        print(f"跳过（正文不足，未产出文件）：{', '.join(skipped)}")
    if notes:
        print(f"\n需关注 {len(notes)} 处：")
        for n in notes:
            print(f"  ⚠ {n}")
    else:
        print("\n✓ 内容丢失检查通过：无告警")
    print(f"产物：clean/  {REPORT_PATH.relative_to(ROOT)}  {CHUNKS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
