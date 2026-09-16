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

✅ 0 篇译稿的表行数与清洗稿完全一致，无差异。

## 差异明细

无。

