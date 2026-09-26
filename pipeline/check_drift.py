#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_drift.py —— 手写交付物里的关键数字必须与生成物一致。

背景（见仓库 AAR / 拿来说明）：
  本项目反复撞上「同一件事写在两处、慢慢漂移」的问题。最典型的一次是补译
  最后一篇论文（覆盖度 28/34=82.4% → 29/34=85.3%）后，README / AAR /
  拿来说明 / CI 注释里有若干处仍残留旧的「28 篇 / 82.4% / 10 支脚本 / 5 份报告」。
  这些不是笔误，而是「手写文档没跟着生成物走」的系统病。

本门禁把那几条**必须同源**的数字固化成断言：
  - 管线脚本数（pipeline/*.py）              ↔ 文档里写的「N 支 Python」
  - 中文译稿数（zh/*.md，不含 README）        ↔ 文档里写的「N 条中文译稿 / N 篇译稿」
  - 自动生成报告数（reports/*）               ↔ 文档里写的「N 份自动生成报告」
  - 覆盖率（reports/coverage.md）             ↔ 文档里写的「29/34 = 85.3%」

只读取**已入库**的文件（zh/ reports/ pipeline/ README.md AAR.md 拿来说明/），
不依赖 macOS 才有的 PDF 提取、不依赖未入库的 pipeline/work/ —— 因此可以作硬门禁。

用法：
  python3 pipeline/check_drift.py --check     # 退出码 0 通过 / 1 漂移
  python3 pipeline/check_drift.py             # 同上（默认 --check）
"""

import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def count_zh_units():
    """中文译稿数 = zh/*.md 中排除 README.md 的文件数。"""
    files = [f for f in glob.glob(os.path.join(ROOT, "zh", "*.md"))
             if os.path.basename(f) != "README.md"]
    return len(files)


def count_reports():
    """自动生成报告数 = reports/ 下的文件数。"""
    return len([f for f in glob.glob(os.path.join(ROOT, "reports", "*"))
                if os.path.isfile(f)])


def count_pipeline_py():
    """管线 Python 脚本数 = pipeline/*.py。"""
    return len(glob.glob(os.path.join(ROOT, "pipeline", "*.py")))


def parse_coverage():
    """从 reports/coverage.md 解析 (分母, 已完成条目, 可用条目)。"""
    path = os.path.join(ROOT, "reports", "coverage.md")
    den = num = avail = None
    text = open(path, encoding="utf-8").read()
    # 两种写法都能抓：``分母 = ... readings = **34** 条`` 或 ``分母为 34 条``
    m = re.search(r"readings\s*=\s*\*\*(\d+)\*\*\s*条", text)
    if not m:
        m = re.search(r"分母[^\d]{0,30}(\d+)\s*条", text)
    if m:
        den = int(m.group(1))
    m = re.search(r"可用（可翻译）\s*=\s*\*\*(\d+)\*\*", text)
    if m:
        avail = int(m.group(1))
    m = re.search(r"已完成条目\s*\|\s*\*\*(\d+)\*\*\s*/\s*(\d+)", text)
    if m:
        num = int(m.group(1))
    return den, num, avail


def main():
    errors = []

    # ---- 真实值（来自生成物）----
    zh_units = count_zh_units()
    reports = count_reports()
    py_scripts = count_pipeline_py()
    den, num, avail = parse_coverage()

    print(f"真实值（生成物）：译稿 {zh_units} 篇 ｜ 报告 {reports} 份 ｜ "
          f"管线脚本 {py_scripts} 支 ｜ 覆盖度 {num}/{den}（可用 {avail}）")

    # 真实值自身先自洽
    if den and num is not None and avail is not None:
        if num != avail:
            errors.append(f"覆盖率自相矛盾：已完成 {num} ≠ 可用 {avail}")
        if den and num is not None:
            pct = num / den * 100
            if abs(pct - 85.3) > 0.05:
                errors.append(f"覆盖率 {num}/{den} = {pct:.1f}%，期望 85.3%")

    # ---- 受检文档 ----
    doc_files = (
        [os.path.join(ROOT, "README.md"), os.path.join(ROOT, "AAR.md"),
         os.path.join(ROOT, ".github", "workflows", "checks.yml")]
        + sorted(glob.glob(os.path.join(ROOT, "拿来说明", "*.md")))
    )

    # 手写文档里出现的数字必须与真实值一致。
    # 每个正则只匹配「数量 + 单位」的明确写法，避免误伤「≥28 条达标线」这类合法表述。
    patterns = {
        "支 Python 脚本数": (r"(\d+)\s*支\s*Python", py_scripts),
        "条中文译稿数":     (r"(\d+)\s*条中文译稿", zh_units),
        "篇译稿数":         (r"(\d+)\s*篇译稿", zh_units),
        "篇中文译稿数":     (r"(\d+)\s*篇中文译稿", zh_units),
        "份自动生成报告数": (r"(\d+)\s*份自动生成报告", reports),
    }

    for doc in doc_files:
        name = os.path.relpath(doc, ROOT)
        text = open(doc, encoding="utf-8").read()
        for label, (pat, expected) in patterns.items():
            for m in re.finditer(pat, text):
                val = int(m.group(1))
                if val != expected:
                    ctx = text[max(0, m.start() - 25): m.start() + len(m.group(0)) + 10].replace("\n", " ")
                    errors.append(
                        f"[{name}] {label} 写成 {val}，应为 {expected}｜…{ctx}…"
                    )

    # ---- README 主口径必须是 29/34 = 85.3%，且不得残留 28/34 = 82.4% ----
    readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    if "29/34 = 85.3%" not in readme:
        errors.append("[README.md] 未出现主口径「29/34 = 85.3%」")
    # 仅查 README：AAR 里「82.4% → 85.3%」是合法的历史过渡叙述，不动它。
    if "28/34 = 82.4%" in readme:
        errors.append("[README.md] 残留旧主口径「28/34 = 82.4%」（应为 29/34 = 85.3%）")

    # ---- AAR 过程事实里的覆盖率必须写 29/34 = 85.3% ----
    aar = open(os.path.join(ROOT, "AAR.md"), encoding="utf-8").read()
    if "29/34 = 85.3%" not in aar:
        errors.append("[AAR.md] 过程事实未写「29/34 = 85.3%」")

    # ---- 输出 ----
    if errors:
        print("\n❌ 发现数字漂移（手写文档与生成物不一致）：")
        for e in errors:
            print(f"  - {e}")
        print(f"\n共 {len(errors)} 处漂移。请回源改文档，不要为了好看改分母/口径。")
        return 1

    print("\n✅ 文档关键数字与生成物一致，无漂移。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
