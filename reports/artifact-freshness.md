# 产物新鲜度报告（ARTIFACT FRESHNESS）

> 由 `pipeline/check_staleness.py` 自动生成，**请勿手工编辑**。

## 这个检查在防什么

CI 的确定性检查是「连跑两遍比对彼此」，它**发现不了提交产物过期**——
两遍都自洽，只是都与仓库里提交的那份不一致。实测撞上过：
`source/units.json` / `INVENTORY.md` 的字数统计停留在一次代码改动之前，
同一份仓库里存在两套数字。

## 口径

| 项 | 说明 |
|---|---|
| 比对对象 | 提交到 HEAD 的产物 vs 工作区里**现在**跑出来的产物 |
| 范围 | 只比 `units.json` 里 **format != pdf** 的条目 |
| 为什么排除 PDF | PDF 文本提取依赖 macOS PDFKit，在 Linux 上必然不同，比它等于把假告警制度化 |

## 结果

| 产物 | 结论 | 说明 |
|---|---|---|
| `source/units.json` | 一致 | 比对 41 个非 PDF 条目 |

✅ 提交的产物与现在跑出来的完全一致。

