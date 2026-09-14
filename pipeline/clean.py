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

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
P = CFG["paths"]
CLEAN_DIR = ROOT / "clean"
CHUNKS_PATH = ROOT / "pipeline/work/chunks.json"
REPORT_PATH = ROOT / "reports/clean-comparison.md"
MAX_CHUNK_CHARS = CFG["translation"]["max_chunk_chars"]
# 剔除样板后正文少于此字符数，视为"有文件但没内容"（SPA 壳 / 付费墙 / JS 渲染页）。
# 唯一定义处：inventory.py 从这里导入，避免两处阈值各自漂移。
MIN_CONTENT_CHARS = 1500

# 需要整棵剔除的样板标签
BOILERPLATE = {
    "script", "style", "noscript", "nav", "header", "footer", "aside",
    "form", "iframe", "svg", "button", "select", "option", "template",
    "figure", "video", "audio", "canvas", "map", "object", "embed",
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


def _list(node: Node, lines: list, depth: int, ordered: bool) -> None:
    idx = 0
    for c in node.children:
        if not isinstance(c, Node) or c.tag != "li":
            continue
        idx += 1
        marker = f"{idx}." if ordered else "-"
        pad = "  " * depth
        # li 的首段作为行，其余子块缩进
        head, subs = [], []
        for ch in c.children:
            if isinstance(ch, str):
                head.append(re.sub(r"\s+", " ", ch))
            elif ch.tag in ("ul", "ol"):
                subs.append(ch)
            elif ch.tag == "pre":
                subs.append(ch)
            else:
                head.append(inline(ch))
        txt = re.sub(r"\s+", " ", "".join(head)).strip()
        lines.append(f"{pad}{marker} {txt}".rstrip())
        for s in subs:
            if s.tag in ("ul", "ol"):
                _list(s, lines, depth + 1, ordered=(s.tag == "ol"))
            else:
                code = s.text().rstrip()
                if code.strip():
                    lines.append("")
                    lines.extend("  " * (depth + 1) + x for x in code.split("\n"))
                    lines.append("")


def _table(node: Node, lines: list) -> None:
    rows = []
    for tr in node.find_all(["tr"]):
        cells = []
        for td in tr.children:
            if isinstance(td, Node) and td.tag in ("td", "th"):
                cells.append(re.sub(r"\s+", " ", inline(td)).strip().replace("|", "\\|"))
        if cells:
            rows.append(cells)
    if len(rows) < 2:
        return
    width = max(len(r) for r in rows)
    rows = [r + [""] * (width - len(r)) for r in rows]
    lines.append("")
    lines.append("| " + " | ".join(rows[0]) + " |")
    lines.append("|" + "---|" * width)
    for r in rows[1:]:
        lines.append("| " + " | ".join(r) + " |")
    lines.append("")


def tidy(md: str) -> str:
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"[ \t]+\n", "\n", md)
    return md.strip() + "\n"


def extract_markdown(raw: str) -> str:
    """从原始 HTML 提取正文并转成 Markdown。供本模块与 inventory.py 共用。

    单独暴露出来是为了让「什么算正文」只有一个判定来源——
    清点用的度量与清洗用的产物必须一致，否则覆盖率数字会自相矛盾。
    """
    tb = TreeBuilder()
    tb.feed(raw)
    tb.close()
    prune(tb.root)
    return tidy("\n".join(render(pick_main(tb.root))))


# ---------------------------------------------------------------- 分块

def split_chunks(unit_id: str, title: str, md: str) -> list:
    """按二级/三级标题切块；超长块再按段落切。"""
    parts = re.split(r"\n(?=#{2,3} )", md)
    chunks, buf, head_path = [], "", title

    def flush():
        nonlocal buf
        t = buf.strip()
        if not t:
            buf = ""
            return
        if len(t) <= MAX_CHUNK_CHARS:
            chunks.append({"heading_path": head_path, "text": t})
        else:
            # 段落级再切
            cur = ""
            for para in t.split("\n\n"):
                if len(cur) + len(para) + 2 > MAX_CHUNK_CHARS and cur.strip():
                    chunks.append({"heading_path": head_path, "text": cur.strip()})
                    cur = ""
                cur += para + "\n\n"
            if cur.strip():
                chunks.append({"heading_path": head_path, "text": cur.strip()})
        buf = ""

    for seg in parts:
        m = re.match(r"(#{2,3}) (.+)", seg)
        if m:
            flush()
            head_path = m.group(2).strip()
        buf += seg
    flush()

    for i, c in enumerate(chunks):
        c["index"] = i
        c["unit_id"] = unit_id
        c["chars"] = len(c["text"])
    return chunks


# ---------------------------------------------------------------- 主流程

def main() -> None:
    units = json.loads((ROOT / "source/units.json").read_text(encoding="utf-8"))["units"]
    # 处理**所有**本地 HTML（含已知失效的），而不是只处理 status==ok 的：
    # 清洗报告必须完整记账——把失败篇目排除在外会让报告谎报"一切正常"。
    todo = [u for u in units
            if u["kind"] == "local" and u.get("format") == "html"
            and (ROOT / u["local_path"]).exists()]
    if "--limit" in sys.argv:
        todo = todo[: int(sys.argv[sys.argv.index("--limit") + 1])]

    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    all_chunks, rows, skipped = [], [], []
    print(f"待清洗 {len(todo)} 篇 HTML\n")

    for u in todo:
        src = ROOT / u["local_path"]
        unit_id = Path(u["local_path"]).stem
        raw = src.read_text(encoding="utf-8", errors="replace")
        raw_bytes = len(raw.encode("utf-8", errors="replace"))

        md = extract_markdown(raw)
        title = u.get("reading_title") or unit_id
        words = len(md.split())

        usable = len(md) >= MIN_CONTENT_CHARS
        chunks = []
        if usable:
            header = (f"<!-- source: {u['local_path']} -->\n"
                      f"<!-- week: {u['week']} | original: {u['page_title'] or title} -->\n\n")
            (CLEAN_DIR / f"{unit_id}.md").write_text(header + md, encoding="utf-8")
            chunks = split_chunks(unit_id, title, md)
            for c in chunks:
                c["week"] = u["week"]
                c["reading_title"] = title
                c["source_ref"] = u["local_path"]
            all_chunks.extend(chunks)
        else:
            skipped.append(unit_id)

        density = (len(md.encode("utf-8")) / raw_bytes * 100) if raw_bytes else 0
        rows.append({
            "unit": unit_id, "week": u["week"], "title": title,
            "raw": raw_bytes, "md": len(md.encode("utf-8")),
            "words": words, "chunks": len(chunks),
            "density": density,
            "flag": "OK" if usable else "**失效**",
            "reason": u.get("reason") or ("剔除样板后正文不足" if not usable else ""),
            "usable": usable,
        })
        print(f"  W{u['week']:>2} {unit_id[:42]:<42} "
              f"{raw_bytes/1024:>7.0f}KB → {len(md.encode('utf-8'))/1024:>6.1f}KB "
              f"({density:>5.1f}%) {words:>5} 词 {len(chunks):>2} 块 "
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
    A("# 清洗前后对比报告（HTML → Markdown）")
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
    A("| 指标 | 数值 |")
    A("|---|---|")
    A(f"| 处理篇数 | {len(rows)}（其中可入管线 {len(good)} 篇，失效 {len(bad)} 篇） |")
    A(f"| 原始 HTML 总量 | {tot_raw/1024/1024:.2f} MB |")
    A(f"| 清洗后 Markdown | {tot_md/1024/1024:.2f} MB（可入管线部分 {md_good/1024/1024:.2f} MB） |")
    A(f"| **有效篇目压缩率** | **{md_good/raw_good*100:.1f}%**"
      f"（体积降至 1/{raw_good/max(md_good,1):.1f}） |")
    A(f"| 可翻译正文词数 | {tot_words:,} |")
    A(f"| 翻译分块数 | {len(all_chunks)} |")
    A("")
    A("## 逐篇明细")
    A("")
    A("`密度` = 清洗后体积 / 原始 HTML 体积。"
      "**密度越低，说明原始 HTML 里样板越多、清洗收益越大**——低到 1% 上下意味着"
      "99% 的原始体积都是垃圾，不清洗就等于把 99% 的 token 预算烧在导航和脚本上。")
    A("")
    A("| 周 | 篇目 | 原始 HTML | 清洗后 | 密度 | 词数 | 分块 | 判定 | 失效模式 |")
    A("|---|---|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: x["density"]):
        A(f"| W{r['week']} | `{r['unit']}` | {r['raw']/1024:.0f} KB | "
          f"{r['md']/1024:.1f} KB | **{r['density']:.1f}%** | {r['words']:,} | "
          f"{r['chunks']} | {r['flag']} | {r['reason'] or '—'} |")
    A("")
    A("## 异常提示")
    A("")
    if bad:
        A(f"以下 **{len(bad)} 篇**清洗后正文不足 {MIN_CONTENT_CHARS} 字符，**无法进入翻译管线**。")
        A("这些条目在覆盖度分母中仍占位，但拿不到内容——是必须先解决的缺口：")
        A("")
        A("| 篇目 | 周 | 原始 HTML | 清洗后正文 | 失效模式 |")
        A("|---|---|---|---|---|")
        for r in bad:
            A(f"| `{r['unit']}` | W{r['week']} | {r['raw']/1024:.0f} KB | "
              f"{r['md']} 字节 | {r['reason']} |")
        A("")
        A("> 这些篇目**不会**产出 `clean/*.md`，也不会进入 `chunks.json`——"
          "即它们对翻译覆盖度贡献为 0。详见 `source/INVENTORY.md` 第二节。")
    else:
        A("无。全部篇目清洗后正文量正常。")
    A("")
    A("## 产物")
    A("")
    A("| 产物 | 位置 | 是否入库 |")
    A("|---|---|---|")
    A(f"| 清洗后英文底稿 | `clean/<unit>.md`（{len(good)} 篇） | ✅ 入库，可人工抽检 |")
    A(f"| 翻译分块 | `pipeline/work/chunks.json`（{len(all_chunks)} 块） | ⬜ 中间产物，可复跑再生 |")
    REPORT_PATH.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"\n汇总：{len(good)} 篇有效 / {len(bad)} 篇失效 ｜ "
          f"{raw_good/1024/1024:.2f} MB → {md_good/1024/1024:.2f} MB "
          f"（{md_good/raw_good*100:.1f}%）｜{tot_words:,} 词｜{len(all_chunks)} 块")
    if skipped:
        print(f"跳过（正文不足，未产出文件）：{', '.join(skipped)}")
    print(f"产物：clean/  {REPORT_PATH.relative_to(ROOT)}  {CHUNKS_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
