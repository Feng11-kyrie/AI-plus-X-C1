# pipeline — 可复跑的翻译管线

本目录是 C1 挑战的核心：**信息获取与处理管线**。
每一步都是独立可执行的脚本，读取配置、产出中间产物，可重复运行。

## 设计原则

1. **零依赖**：只用 Python 3 标准库，不需要 `pip install`。降低他人复用的门槛。
2. **配置驱动**：所有路径与参数来自 `config/<源代号>.json`，脚本内不硬编码课程名。
3. **产物可核对**：生成的报告都标注了数据源与生成方式，且带"请勿手工编辑"提示——手工改过的报告无法复跑，也就失去了作为证据的价值。
4. **人工在关键节点介入**：脚本负责"提出候选"和"校验规则"，人负责"做决定"。术语译法的审定就是典型的人机分工。

## 脚本清单

| 脚本 | 输入 | 输出 | 作用 |
|---|---|---|---|
| `parse_syllabus.py` | `source/index.html` | `source/syllabus.json` | 把课程主页解析成结构化的 10 周大纲 |
| `inventory.py` | `syllabus.json`、`page_map.json` | `source/units.json`、`source/INVENTORY.md` | 清点资料、识别失效条目、**自证覆盖度分母** |
| `clean.py` | `units.json` + 页面 HTML | `clean/*.md`、`pipeline/work/chunks.json`、`reports/clean-comparison.md` | 剔除样板 → Markdown → 按标题分块 |
| `mine_terms.py` | `units.json` + 页面 HTML | 控制台 / `reports/term-candidates.csv` | 从语料挖掘术语候选（频率证据） |
| `glossary_tool.py` | `glossary/glossary.csv` | `glossary/glossary.md` | 校验术语表自身无矛盾 + 渲染人读版 |

## 执行顺序

```bash
python3 pipeline/parse_syllabus.py    # 1. 大纲 → JSON
python3 pipeline/inventory.py         # 2. 清点 → units.json + INVENTORY.md
python3 pipeline/clean.py             # 3. 清洗 + 分块（消费 units.json）
python3 pipeline/mine_terms.py        # 4. 挖掘术语候选（改术语表前跑）
python3 pipeline/glossary_tool.py     # 5. 校验 + 渲染术语表
```

顺序有依赖：`clean.py` 消费 `inventory.py` 产出的 `units.json`。

## 单一判定来源

`clean.py` 导出 `extract_markdown()` 与 `MIN_CONTENT_CHARS`，`inventory.py` **从中导入**而不是自己再写一套。

原因：清点用的"什么算正文"和清洗产物必须**同源**。两处各写一份判定逻辑，迟早会漂移，
届时 `INVENTORY.md` 声称可用的篇目与 `clean/` 里实际产出的内容就会自相矛盾——
而覆盖度数字正是建立在这个判定之上。

## 换一门课（可复用性验证）

**不需要改脚本代码**，只需新建一个配置文件：

```bash
cp pipeline/config/cs146s.json pipeline/config/<新课代号>.json
# 编辑其中的 paths.* 指向新课的资料目录
```

四个脚本即可在另一门课上产出同样的 `syllabus.json` / `units.json` / `INVENTORY.md` / 术语候选表。

> `parse_syllabus.py` 中的 HTML 解析规则依赖源站的 DOM 结构（`div.week-card` 等）。
> 换源时若 DOM 不同，需调整该脚本的解析部分——**这是有意保留的边界**：
> 资料结构的适配无法完全自动化，但它被隔离在单一脚本内，不影响其余三步。

## 质量门禁

`glossary_tool.py --check` 校验失败会返回非零退出码，可直接用于 CI：

| 规则 | 检查内容 |
|---|---|
| R1 | `id` 唯一 |
| R2 | `term_en` 唯一（大小写不敏感） |
| R3 | **禁用变体不得与任何术语的正式译法冲突** |
| R4 | `policy` 取值合法 |
| R5 | 非 `keep_en` 术语必须有中文译法 |
| R6 | 禁用变体内部不重复 |

R3 是这套校验的关键——它防止术语表**自相矛盾**（例如把"推理"列为某词的禁用变体，同时又是另一个词的正式译法）。
实际运行中 R3 抓到过 2 个真实冲突（`Inference`/`Reasoning`、`Tracing`/`Trace`），已修正。
