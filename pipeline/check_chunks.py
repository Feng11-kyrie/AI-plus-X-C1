#!/usr/bin/env python3
"""
分块清单：列出某单元的分块编号与实际 done 文件的对应关系。

**为什么是清单工具，而不是自动门禁**：
我原本想用「中文长度 / 源文长度」的比例来自动判定「一个文件里写了多个分块」。
实测证明**这个启发式不可靠**：

  合并两个分块后的比例 ≈ 0.8–1.0（因为中文产出本约为源文的 0.4 倍）
  而合法的表格密集块比例可达 0.78
  → 两类完全重叠，无论阈值定在哪里都会误报或漏报

所以退回到一个**辅助清单**：把「该有哪些块、实际有哪些块」摆出来，
由人在 ingest 之前扫一眼。这比一个天天误报的自动门禁更实用。

**背景**：我按「内容主题」而非 chunk 索引切分译文，已导致 3 次合并：
  specs-are-the-new-source-code  （#2+#3）
  owasp-top-ten                  （#2+#3）
  context-rot                    （#3+#4+#5）
每次都是 ingest 报「某块未通过」才发现——那时已白写几千字。

用法：
  python3 pipeline/check_chunks.py                # 全部单元概览
  python3 pipeline/check_chunks.py context-rot    # 某单元的逐块清单
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = ROOT / "pipeline/work/chunks.json"
DONE = ROOT / "pipeline/work/done"


def main() -> int:
    chunks = json.loads(CHUNKS.read_text(encoding="utf-8"))["chunks"]
    by_unit = defaultdict(list)
    for c in chunks:
        by_unit[c["unit_id"]].append(c)

    if len(sys.argv) > 1:
        uid = sys.argv[1]
        items = sorted(by_unit.get(uid, []), key=lambda c: c["index"])
        if not items:
            print(f"未找到单元 {uid}")
            return 1
        print(f"=== {uid}：{len(items)} 个分块 ===")
        print(f"{'块':>4} {'源字符':>7} {'中文':>7} {'比例':>6}  标题")
        for c in items:
            f = DONE / f"{uid}__{c['index']:03d}.md"
            if f.exists():
                zh = len(re.sub(r"\s+", "", f.read_text(encoding="utf-8")))
                ratio = f"{zh / max(c['chars'], 1):.2f}"
                zh_s = str(zh)
            else:
                zh_s, ratio = "—", "—"
            print(f"{c['index']:>4} {c['chars']:>7} {zh_s:>7} {ratio:>6}  "
                  f"{c['heading_path'][:34]}")
        missing = [c["index"] for c in items
                   if not (DONE / f"{uid}__{c['index']:03d}.md").exists()]
        print(f"\n缺失块编号: {missing if missing else '无'}")
        return 0

    # 概览模式
    total = written = 0
    print(f"{'单元':<44} {'块':>4} {'已写':>5}  缺失编号")
    for uid in sorted(by_unit):
        items = sorted(by_unit[uid], key=lambda c: c["index"])
        have = [c["index"] for c in items
                if (DONE / f"{uid}__{c['index']:03d}.md").exists()]
        total += len(items)
        written += len(have)
        miss = [c["index"] for c in items if c["index"] not in have]
        if 0 < len(have) < len(items):
            print(f"{uid:<44} {len(items):>4} {len(have):>5}  {miss}")
    print(f"\n合计 {written} / {total} 块已写")
    return 0


if __name__ == "__main__":
    sys.exit(main())
