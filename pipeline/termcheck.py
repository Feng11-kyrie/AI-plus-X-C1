#!/usr/bin/env python3
"""
术语匹配的唯一判定来源。

**为什么单独抽一个模块**：
逐块校验（translate.py）与全量审计（qc_terminology.py）都需要判断
「这段中文有没有违反术语表」。一开始我各写了一份，结果：

  translate.py 的版本已经消除了子串误报，
  qc_terminology.py 的版本没有 —— 于是全量审计报出 52 次违规，
  而其中绝大多数是早就解决过的假阳性。

同一个判断两处实现，必然漂移。这在本项目已经是第三次同类问题
（前两次：状态键与文件名不一致、覆盖度目标三处各算一遍）。
所以这次不是再修一遍副本，而是抽出单一来源。

两条中文特有的判定规则：
  1. **被正式译法包含的变体一律跳过**——「上下文协议」是
     「模型上下文协议（MCP）」的子串，子串匹配必然误报。
  2. **硬性 / 提示级分级**——「记录」「流程」「代理」这类词在中文里
     本身常用，或是**另一个英文词**的合法译法，只提示不拦截。
"""
from __future__ import annotations

import re


def approved_forms(term: dict) -> list:
    """正式译法的可接受形式。

    缩写类术语（如「大语言模型（LLM）」）行文中可能只写中文、
    也可能只写缩写，两者都算正确。
    """
    zh = (term.get("term_zh") or "").strip()
    forms = {zh} if zh else set()
    m = re.match(r"^(.+?)[（(]([A-Za-z0-9/\-\. ]+)[）)]$", zh)
    if m:
        forms.add(m.group(1).strip())
        forms.add(m.group(2).strip())
    return sorted(f for f in forms if f)


def count_forms(text: str, forms: list) -> int:
    """统计可接受形式的出现次数。长形式优先替换，避免嵌套重复计数。"""
    t, n = text, 0
    for f in sorted(forms, key=len, reverse=True):
        n += t.count(f)
        t = t.replace(f, "\x00")
    return n


def variants(term: dict, key: str) -> list:
    return [x.strip() for x in (term.get(key) or "").split("|") if x.strip()]


def visible_variants(term: dict, key: str) -> list:
    """剔除「被正式译法包含」的变体——它们在任何译文中都会误报。"""
    approved = (term.get("term_zh") or "").strip()
    out = []
    for v in variants(term, key):
        if approved and v in approved:
            continue
        out.append(v)
    return out


def find_hits(text: str, term: dict) -> tuple:
    """在一段中文里查找术语违规，返回 (硬性命中, 提示级命中)。

    两个列表的元素为 (变体, 出现次数)。
    """
    hard, soft = [], []
    for key, bucket in (("forbidden_zh", hard), ("forbidden_soft", soft)):
        for v in visible_variants(term, key):
            c = text.count(v)
            if c:
                bucket.append((v, c))
    return hard, soft
