# 表格完整性报告（TABLE INTEGRITY）

> 由 `pipeline/check_tables.py` 自动生成，**请勿手工编辑**。

## 判定口径

| 项 | 说明 |
|---|---|
| 比对对象 | `clean/<篇目>.md` 与 `zh/<篇目>.md` 的 Markdown 表格行数（以 `|` 开头的行） |
| A 类差异 | 源文有表、行数不同 → 丢行 / 并行嫌疑 |
| B 类差异 | 源文 0 行表、译文有表 → 清洗管线漏识别表格的嫌疑 |
| 例外 | 逐条登记在 `pipeline/config/table-exceptions.json`，含证据与处置决定 |

## 结论

审计 30 篇译稿，1 篇存在差异：1 篇已登记例外，0 篇未登记。

## 差异明细

| 篇目 | 源表行 | 译表行 | 类型 | 状态 | 处置 |
|---|---|---|---|---|---|
| `sast-vs-dast` | 0 | 12 | B_清洗稿漏识别表格 | 已登记例外 | 保留译文的表格形式，不压回扁平行——压回去会丢掉原页面明确的结构。清洗管线的这个盲区（div 表格）记在 README 的已知缺口与 拿来说明/04。 |

### `sast-vs-dast`

- **类型**：B_清洗稿漏识别表格
- **证据**：source/pages/sast-vs-dast.html 里「SAST vs. DAST: key differences」那张表用的是 <div class="table no-header"> 嵌套 div 画的，页面里没有任何 <table> 元素（grep '<table' 命中 0 次）。clean.py 的表提取器只认 <table>，所以只能把每个 div 输出成一行平文本：clean/sast-vs-dast.md 第 110–150 行是 33 行连续文本，没有 | 号。译稿按原页面的表格结构把它重建成了 12 行 Markdown 表。
- **复核日期**：2026-09-16
- **处置决定**：保留译文的表格形式，不压回扁平行——压回去会丢掉原页面明确的结构。清洗管线的这个盲区（div 表格）记在 README 的已知缺口与 拿来说明/04。


