#!/usr/bin/env python3
"""
翻译管线：消费 chunks.json + 术语表，产出中文译稿，并把过程写进 AI 日志。

设计要点
--------
1. **后端可插拔**
   - `queue`：把每块的完整 prompt 写到 pipeline/work/todo/，
     再把译文从 pipeline/work/done/ 收回。适合由人 / agent 执行，
     也让"人工在环"这件事可见、可留痕。
   - `api`：直接调用 OpenAI 兼容的 /chat/completions 端点，
     key 从环境变量读取。任何人配上 key 就能真正自动跑完。
   两种后端走同一套 prompt 构造、校验与记录逻辑。

2. **日志是副产品，不是事后补写**
   每翻译一块就 append 一条结构化事件到 logs/journal.jsonl，
   再渲染成人读的 logs/ai-journal.md。
   包含时间、后端、prompt 哈希、规模、耗时、校验结果与失败原因。
   事后回忆补写的日志颗粒度均匀、没有失败记录——这里刻意相反。

3. **增量可复跑**
   pipeline/work/state.json 记录每块的状态。
   已完成的块不会重译；改了 prompt 模板或术语表则哈希变化、自动重译。

4. **术语注入只带相关的**
   每块只注入在该块中实际出现的术语，避免把 170 条全塞进每个 prompt。

用法
----
  python3 pipeline/translate.py --emit          # 队列模式：生成待译 prompt
  python3 pipeline/translate.py --ingest        # 队列模式：收回译文并组装
  python3 pipeline/translate.py --backend api   # API 模式：直接翻译
  python3 pipeline/translate.py --status        # 进度概览
  python3 pipeline/translate.py --render-log    # 只重渲染 AI 日志
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "pipeline/config/cs146s.json").read_text(encoding="utf-8"))
P = CFG["paths"]
T = CFG.get("translation", {})

CHUNKS_PATH = ROOT / "pipeline/work/chunks.json"
STATE_PATH = ROOT / "pipeline/work/state.json"
TODO_DIR = ROOT / "pipeline/work/todo"
DONE_DIR = ROOT / "pipeline/work/done"
ZH_DIR = ROOT / P.get("zh_dir", "zh")
JOURNAL_JSONL = ROOT / "logs/journal.jsonl"
JOURNAL_MD = ROOT / "logs/ai-journal.md"
COVERAGE_MD = ROOT / "reports/coverage.md"

PROMPT_VERSION = "v1"
DEFAULT_BACKEND = T.get("backend", "queue")
API_MODEL = T.get("api_model", "deepseek-chat")
API_BASE = T.get("api_base", "https://api.deepseek.com/v1")
API_KEY_ENV = T.get("api_key_env", "DEEPSEEK_API_KEY")


# ---------------------------------------------------------------- 工具

def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 术语表

def load_glossary() -> list:
    f = ROOT / P["glossary"]
    with f.open(encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh)]


def relevant_terms(text: str, glossary: list) -> list:
    """只挑在该块里实际出现的术语，避免每个 prompt 都塞进 170 条。"""
    low = text.lower()
    out = []
    for r in glossary:
        if r["policy"] == "keep_en":
            continue
        # 术语的英文主形，以及括号里的缩写形式，任一出现即算命中
        cands = [r["term_en"]]
        m = re.search(r"\(([A-Za-z0-9/\- ]+)\)", r["term_en"])
        if m:
            cands.append(m.group(1))
        base = re.sub(r"\s*\(.*?\)\s*", "", r["term_en"]).strip()
        cands.append(base)
        for c in cands:
            c = c.strip()
            if len(c) >= 3 and c.lower() in low:
                out.append(r)
                break
    return out


# ---------------------------------------------------------------- Prompt

def build_prompt(chunk: dict, terms: list) -> str:
    lines = [
        "你是资深技术文档译者。把下面的英文 Markdown 译成简体中文。",
        "",
        "硬性要求：",
        "1. 完整保留 Markdown 结构：标题层级、列表、表格、引用、链接、代码块围栏。",
        "2. 代码块内容逐字保留，绝不翻译，包括其中的注释与标识符。",
        "3. 链接与图片的 URL 一字不改，只翻译可见文字。",
        "4. 术语必须严格使用下表给定译法；禁用变体一律不得出现。",
        "5. 不增、不删、不加译者注、不加任何解释或前后缀。",
        "6. 只输出译文本身。",
        "",
    ]
    if terms:
        lines.append("术语表（必须遵守）：")
        lines.append("")
        lines.append("| 英文 | 中文 | 禁用变体 |")
        lines.append("|---|---|---|")
        for r in terms:
            fb = r["forbidden_zh"].replace("|", "、") or "—"
            lines.append(f"| {r['term_en']} | {r['term_zh']} | {fb} |")
        lines.append("")
    else:
        lines.append("（本段未命中术语表条目，按通用技术文档惯例翻译。）")
        lines.append("")
    lines.append(f"来源：{chunk.get('source_ref', '')} ｜ 章节：{chunk.get('heading_path', '')}")
    lines.append("")
    lines.append("待译内容：")
    lines.append("")
    lines.append(chunk["text"])
    return "\n".join(lines)


# ---------------------------------------------------------------- 校验

def variant_hits(zh: str, term: dict) -> tuple:
    """找出译文中违反术语表的写法，返回 (硬性违规, 提示级)。

    两条中文特有的判定规则——都是被真实误报逼出来的：

    1. **被正式译法包含的变体，一律跳过。**
       例：MCP 的正式译法是「模型上下文协议（MCP）」，而其禁用变体是「上下文协议」，
       显然后者是前者的子串。用子串匹配会把正确的译文判成违规。
       同理「故障事件」包含「事件」和「故障」、「检索增强生成（RAG）」包含「检索增强」。
       代价是这类变体单用时也检不出来——可接受，因为宁可漏报也不误报，
       一个天天误报的校验器最终会被忽略，那才是真正的失效。

    2. **区分硬性与提示。**
       像「记录」「流程」这种词在中文里本身就常用（"记录每一步"、"排障流程"），
       把它们一律判为违规会逼着人写出不自然的译文。
       术语表里用 forbidden_soft 列单独声明，只提示不拦截。
    """
    approved = (term.get("term_zh") or "").strip()
    hard, soft = [], []
    for key, bucket in (("forbidden_zh", hard), ("forbidden_soft", soft)):
        for fb in filter(None, (x.strip() for x in (term.get(key) or "").split("|"))):
            if approved and fb in approved:
                continue                      # 规则 1：是正式译法的组成部分
            if fb in zh:
                bucket.append(f"出现禁用变体「{fb}」（应为「{approved}」）")
    return hard, soft


def validate(src: str, zh: str, terms: list) -> dict:
    """对单块译文做机械校验，返回 (通过与否, 问题列表, 指标)。"""
    hard_issues, soft_issues = [], []
    zh = (zh or "").strip()
    if not zh:
        return False, ["译文为空"], {}

    def fences(s):
        return len(re.findall(r"^[ \t]*```", s, re.M))

    def links(s):
        return len(re.findall(r"\]\(", s))

    sf, zf = fences(src), fences(zh)
    sl, zl = links(src), links(zh)

    if sf != zf:
        hard_issues.append(f"代码围栏数不符：原文 {sf}，译文 {zf}")
    if sl != zl:
        hard_issues.append(f"链接数不符：原文 {sl}，译文 {zl}")

    for r in terms:
        h, s = variant_hits(zh, r)
        hard_issues.extend(h)
        soft_issues.extend(s)

    src_len = len(re.sub(r"\s+", "", src))
    zh_len = len(re.sub(r"\s+", "", zh))
    ratio = zh_len / src_len if src_len else 0
    if ratio < 0.25:
        hard_issues.append(f"译文过短：中英字符比 {ratio:.2f}（疑漏译）")
    elif ratio > 2.0:
        hard_issues.append(f"译文过长：中英字符比 {ratio:.2f}（疑添加内容）")

    metrics = {"src_chars": src_len, "zh_chars": zh_len, "ratio": round(ratio, 3),
               "fences": zf, "links": zl, "soft_issues": soft_issues}
    return (not hard_issues), hard_issues, metrics


# ---------------------------------------------------------------- 日志

def journal(event: dict) -> None:
    JOURNAL_JSONL.parent.mkdir(parents=True, exist_ok=True)
    event.setdefault("ts", now_iso())
    with JOURNAL_JSONL.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def render_journal() -> None:
    """把 journal.jsonl 渲染成人读的 ai-journal.md。"""
    if not JOURNAL_JSONL.exists():
        return
    events = [json.loads(l) for l in JOURNAL_JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]

    chunks = [e for e in events if e.get("event") == "chunk"]
    ok = [e for e in chunks if e.get("ok")]
    bad = [e for e in chunks if not e.get("ok")]
    units = [e for e in events if e.get("event") == "unit"]

    L, A = [], None
    L.append("# AI 协作日志")
    L.append("")
    L.append("> **本文件由 `pipeline/translate.py` 自动生成，请勿手工编辑。**")
    L.append("> 原始事件流：`logs/journal.jsonl`（append-only，每翻译一块即写入一条）。")
    L.append("")
    L.append("## 为什么是自动生成的")
    L.append("")
    L.append("事后回忆补写的日志有明显特征：颗粒度均匀、没有失败记录、没有返工。")
    L.append("这份日志反过来——它由管线在每次调用时立即落盘，**不通过人工整理**，")
    L.append("因此失败、重试、校验不通过都会如实留在里面。")
    L.append("")
    L.append("## 总览")
    L.append("")
    L.append("| 指标 | 数值 |")
    L.append("|---|---|")
    L.append(f"| 记录事件总数 | {len(events)} |")
    L.append(f"| 翻译块次 | {len(chunks)} |")
    L.append(f"| 其中通过校验 | {len(ok)} |")
    L.append(f"| **其中未通过 / 失败** | **{len(bad)}** |")
    L.append(f"| 完成条目 | {len(units)} |")
    if checks := [e for e in chunks if e.get("issues")]:
        L.append(f"| 出现过校验问题的块 | {len(checks)} |")
    L.append("")
    L.append("## 逐块记录")
    L.append("")
    L.append("| 时间 | 条目 | 块 | 后端 | prompt | 原/译字符 | 用时 | 结果 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for e in chunks:
        res = "✅" if e.get("ok") else "❌ " + "；".join(e.get("issues", []))[:60]
        secs = e.get("seconds")
        secs_s = f"{secs}s" if secs is not None else "—"
        L.append(f"| {e['ts'][11:19]} | `{e.get('unit_id','')[:26]}` | {e.get('index','')} "
                 f"| {e.get('backend','')} | `{e.get('prompt_hash','')}` "
                 f"| {e.get('src_chars',0)}/{e.get('zh_chars',0)} "
                 f"| {secs_s} | {res} |")
    L.append("")
    if bad:
        L.append("## 失败与返工记录")
        L.append("")
        L.append("这一节是日志里最有价值的部分——它记录的是**真实踩过的坑**。")
        L.append("")
        for e in bad:
            L.append(f"### `{e.get('unit_id','')}` 第 {e.get('index','')} 块")
            L.append("")
            L.append(f"- 时间：{e['ts']}　后端：{e.get('backend','')}　prompt 哈希：`{e.get('prompt_hash','')}`")
            for i in e.get("issues", []):
                L.append(f"- 问题：{i}")
            L.append("")
    if units:
        L.append("## 条目汇总")
        L.append("")
        L.append("| 条目 | 周 | 块数 | 中文字符 | 完成时间 |")
        L.append("|---|---|---|---|---|")
        for e in units:
            L.append(f"| `{e.get('unit_id','')}` | W{e.get('week','')} | {e.get('n_chunks','')} "
                     f"| {e.get('zh_chars',0):,} | {e['ts'][:19]} |")
        L.append("")
    JOURNAL_MD.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL_MD.write_text("\n".join(L) + "\n", encoding="utf-8")


# ---------------------------------------------------------------- 后端

def backend_queue_emit(pending: list, glossary: list) -> int:
    """把待译块的完整 prompt 写成文件，等外部（人或 agent）产出译文。"""
    TODO_DIR.mkdir(parents=True, exist_ok=True)
    n = 0
    for c in pending:
        terms = relevant_terms(c["text"], glossary)
        prompt = build_prompt(c, terms)
        f = TODO_DIR / f"{c['unit_id']}__{c['index']:03d}.md"
        f.write_text(prompt, encoding="utf-8")
        n += 1
    return n


def backend_queue_ingest(pending: list, glossary: list, backend: str) -> list:
    """从 done/ 收回译文，逐块校验并记账。"""
    results = []
    for c in pending:
        done = DONE_DIR / f"{c['unit_id']}__{c['index']:03d}.md"
        if not done.exists():
            continue
        zh = done.read_text(encoding="utf-8").strip()
        terms = relevant_terms(c["text"], glossary)
        ok, issues, metrics = validate(c["text"], zh, terms)
        results.append((c, zh, ok, issues, metrics))
    return results


def backend_api(prompt: str) -> tuple:
    """调用 OpenAI 兼容端点。返回 (译文, 错误)。"""
    key = os.environ.get(API_KEY_ENV, "")
    if not key:
        return "", f"环境变量 {API_KEY_ENV} 未设置"
    payload = json.dumps({
        "model": API_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE.rstrip('/')}/chat/completions", data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"], ""
    except urllib.error.HTTPError as e:
        return "", f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}"
    except (urllib.error.URLError, KeyError, json.JSONDecodeError) as e:
        return "", f"调用失败: {e}"


# ---------------------------------------------------------------- 组装与报告

def assemble_unit(unit_id: str, chunks: list, translations: dict) -> str:
    """把某条目的分块译文按序拼成完整中文底稿。"""
    parts = [translations[c["index"]] for c in sorted(chunks, key=lambda x: x["index"])
             if c["index"] in translations]
    first = sorted(chunks, key=lambda x: x["index"])[0]
    # 头部刻意不含时间戳：含了的话每次重跑都会产生假 diff，
    # 而「复跑后 git status 干净」正是本项目用来证明可复跑的手段。
    # 翻译时间在 logs/journal.jsonl 里有精确记录，不必在两个地方各记一份。
    header = (f"<!-- source: {first.get('source_ref','')} -->\n"
              f"<!-- week: {first.get('week','')} | chunks: {len(parts)} -->\n\n")
    return header + "\n\n".join(parts) + "\n"


def write_coverage(state: dict, chunks_by_unit: dict) -> None:
    """产出覆盖度报告——分母自证，与 INVENTORY.md 口径一致。"""
    units = load_json(ROOT / "source/units.json", {"units": []})["units"]
    local = [u for u in units if u["kind"] == "local"]
    usable = [u for u in local if u["status"] == "ok"]
    target = CFG["coverage"]["target_ratio"]
    need = -(-int(len(local) * target))

    def unit_done(u) -> bool:
        cs = chunks_by_unit.get(Path(u["local_path"]).stem, [])
        # 注意：all() 对空序列返回 True，会把没有分块的条目误判为完成
        if not cs:
            return False
        return all(state.get(f"{Path(u['local_path']).stem}__{c['index']}", {}).get("ok")
                   for c in cs)

    done = [u for u in usable if unit_done(u)]

    L, A = [], None
    L.append("# 覆盖度报告（COVERAGE）")
    L.append("")
    L.append("> 由 `pipeline/translate.py` 自动生成，**请勿手工编辑**。")
    L.append("")
    L.append("## 分母定义（与 INVENTORY.md 一致）")
    L.append("")
    L.append(f"- 分母 = 大纲中指向本地文件的 readings = **{len(local)}** 条")
    L.append(f"- 可用（可翻译）= **{len(usable)}** 条")
    L.append(f"- 目标 = {int(target * 100)}% ⇒ ≥ **{need}** 条")
    L.append("")
    A = L.append
    A("## 当前进度")
    A("")
    A("| 指标 | 数值 |")
    A("|---|---|")
    A(f"| 已完成条目 | **{len(done)}** / {len(usable)} |")
    A(f"| 覆盖率（分母 {len(local)}） | **{len(done)/len(local)*100:.1f}%** |")
    A(f"| 是否达标 | {'✅ 达标' if len(done) >= need else f'⬜ 未达标（还差 {need - len(done)} 条）'} |")
    A("")
    A("## 逐条状态")
    A("")
    A("| 条目 | 周 | 格式 | 块数 | 已完成块 | 状态 |")
    A("|---|---|---|---|---|---|")
    for u in sorted(usable, key=lambda x: (x["week"], x["local_path"])):
        uid = Path(u["local_path"]).stem
        cs = chunks_by_unit.get(uid, [])
        n_ok = len([c for c in cs if state.get(f"{uid}__{c['index']}", {}).get("ok")])
        st = "✅ 完成" if cs and n_ok == len(cs) else (f"🚧 {n_ok}/{len(cs)}" if n_ok else "⬜ 未开始")
        A(f"| `{uid}` | W{u['week']} | {u.get('format','')} | {len(cs)} | {n_ok} | {st} |")
    A("")
    A("> 覆盖度按**整条**计：一条条目只有全部分块译完才算完成。")
    COVERAGE_MD.parent.mkdir(parents=True, exist_ok=True)
    COVERAGE_MD.write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(done), len(usable), need


# ---------------------------------------------------------------- 主流程

def main() -> None:
    data = load_json(CHUNKS_PATH, {"chunks": []})
    chunks = data["chunks"]
    if not chunks:
        print("没有分块。请先运行：python3 pipeline/clean.py", file=sys.stderr)
        return 1
    glossary = load_glossary()
    state = load_json(STATE_PATH, {})

    by_unit = {}
    for c in chunks:
        by_unit.setdefault(c["unit_id"], []).append(c)

    args = sys.argv[1:]
    backend = DEFAULT_BACKEND
    if "--backend" in args:
        backend = args[args.index("--backend") + 1]

    if "--render-log" in args:
        render_journal()
        print(f"已重渲染 {JOURNAL_MD.relative_to(ROOT)}")
        return 0

    def key(c):
        return f"{c['unit_id']}__{c['index']}"

    pending = []
    for c in chunks:
        terms = relevant_terms(c["text"], glossary)
        h = sha(build_prompt(c, terms))
        if state.get(key(c), {}).get("ok") and state[key(c)].get("prompt_hash") == h:
            continue          # 已完成且 prompt 未变 —— 跳过
        pending.append(c)

    # ---- 状态概览 ----
    if "--status" in args:
        n_ok = len([1 for c in chunks if state.get(key(c), {}).get("ok")])
        print(f"分块总数 {len(chunks)}｜已完成 {n_ok}｜待处理 {len(chunks) - n_ok}")
        done_units, total_units, need = write_coverage(state, by_unit)
        print(f"条目完成 {done_units}/{total_units}（需 {need} 条达 80%）")
        print(f"报告已更新：{COVERAGE_MD.relative_to(ROOT)}")
        return 0

    if "--emit" in args:
        n = backend_queue_emit(pending, glossary)
        print(f"已生成 {n} 份待译 prompt -> {TODO_DIR.relative_to(ROOT)}/")
        print("把译文写到 pipeline/work/done/<unit>__<idx>.md 后，运行 --ingest 收回。")
        return 0

    if not pending:
        print("没有待处理的块（全部已完成且 prompt 未变）。")
        render_journal()
        write_coverage(state, by_unit)
        return 0

    # 队列后端下，done/ 里可能还没有任何译文。此时直接返回，不写
    # run_start / run_end——否则反复执行 --ingest 会往日志里灌入大量
    # 「什么都没做」的事件，把真正的记录淹没。
    if backend != "api" and not any(
            (DONE_DIR / f"{c['unit_id']}__{c['index']:03d}.md").exists() for c in pending):
        print(f"done/ 中暂无新译文（待处理 {len(pending)} 块）。")
        print(f"把译文写到 {DONE_DIR.relative_to(ROOT)}/<unit>__<idx>.md 后再运行 --ingest。")
        render_journal()
        write_coverage(state, by_unit)
        return 0

    t0 = time.time()
    journal({"event": "run_start", "backend": backend, "pending": len(pending),
             "prompt_version": PROMPT_VERSION})

    if backend == "api":
        # 预检：配置错误必须在动手之前中止。
        # 否则会为每一块写一条失败记录——把 265 条配置噪声灌进日志，
        # 而日志的「失败与返工记录」本该只保留真实的翻译问题。
        if not os.environ.get(API_KEY_ENV):
            print(f"中止：后端 api 需要环境变量 {API_KEY_ENV}，当前未设置。\n"
                  f"  1) 导出密钥：export {API_KEY_ENV}=<your-key>\n"
                  f"  2) 或改用队列后端：python3 pipeline/translate.py --emit",
                  file=sys.stderr)
            return 2
        results = []
        limit = int(args[args.index("--limit") + 1]) if "--limit" in args else len(pending)
        for c in pending[:limit]:
            terms = relevant_terms(c["text"], glossary)
            prompt = build_prompt(c, terms)
            st = time.time()
            zh, err = backend_api(prompt)
            ok, issues, metrics = validate(c["text"], zh, terms) if zh else (False, [err], {})
            results.append((c, zh, ok, issues, metrics, round(time.time() - st, 2), sha(prompt)))
    else:
        results = []
        for c, zh, ok, issues, metrics in backend_queue_ingest(pending, glossary, backend):
            results.append((c, zh, ok, issues, metrics, None,
                            sha(build_prompt(c, relevant_terms(c["text"], glossary)))))

    # ---- 记账 ----
    translations = {}
    for c in chunks:
        if state.get(key(c), {}).get("ok"):
            t = ROOT / "pipeline/work/zh" / f"{key(c)}.md"
            if t.exists():
                translations[key(c)] = t.read_text(encoding="utf-8").strip()

    n_ok = 0
    for item in results:
        c, zh, ok, issues, metrics, secs, ph = item
        if ok:
            d = ROOT / "pipeline/work/zh"
            d.mkdir(parents=True, exist_ok=True)
            (d / f"{key(c)}.md").write_text(zh + "\n", encoding="utf-8")
            translations[key(c)] = zh
            n_ok += 1
        state[key(c)] = {
            "ok": ok, "prompt_hash": ph, "issues": issues,
            "backend": backend, "ts": now_iso(), **metrics,
        }
        journal({"event": "chunk", "unit_id": c["unit_id"], "index": c["index"],
                 "week": c["week"], "backend": backend, "prompt_hash": ph, "ok": ok,
                 "issues": issues, "seconds": secs, **metrics})

    save_json(STATE_PATH, state)

    # ---- 组装完成的条目 ----
    ZH_DIR.mkdir(parents=True, exist_ok=True)
    for uid, cs in by_unit.items():
        if not all(state.get(key(c), {}).get("ok") for c in cs):
            continue
        tr = {c["index"]: translations[key(c)] for c in cs if key(c) in translations}
        if len(tr) != len(cs):
            continue
        out = ZH_DIR / f"{uid}.md"
        body = assemble_unit(uid, cs, tr)
        if not out.exists() or out.read_text(encoding="utf-8") != body:
            out.write_text(body, encoding="utf-8")
            journal({"event": "unit", "unit_id": uid, "week": cs[0]["week"],
                     "n_chunks": len(cs), "zh_chars": len(re.sub(r"\s+", "", body))})

    journal({"event": "run_end", "backend": backend, "processed": len(results),
             "ok": n_ok, "failed": len(results) - n_ok,
             "seconds": round(time.time() - t0, 2)})
    render_journal()
    done_units, total_units, need = write_coverage(state, by_unit)

    print(f"本轮处理 {len(results)} 块：通过 {n_ok}，未通过 {len(results) - n_ok}")
    print(f"条目完成 {done_units}/{total_units}（需 {need} 条达 80%）")
    if len(results) - n_ok:
        print(f"未通过明细见 {JOURNAL_MD.relative_to(ROOT)} 的「失败与返工记录」")
    print(f"日志：{JOURNAL_MD.relative_to(ROOT)} ｜ 覆盖度：{COVERAGE_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
