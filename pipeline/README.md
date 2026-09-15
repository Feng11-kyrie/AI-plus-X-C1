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
| `clean.py` | `units.json` + 原始文件 | `clean/*.md`、`pipeline/work/chunks.json`、`reports/clean-comparison.md` | 剔除样板 → Markdown → 完整性校验 → 分块 |
| `pdfkit_dump.js` | PDF 文件 | Markdown 文本 | 经 `osascript` 调用 macOS 原生 PDFKit 提取 PDF 文本（由 `clean.py` 调用） |
| `mine_terms.py` | `clean/*.md` | 控制台 / `reports/term-candidates.csv` | 从清洗产物挖掘术语候选（频率证据） |
| `glossary_tool.py` | `glossary/glossary.csv` | `glossary/glossary.md` | 校验术语表自身无矛盾 + 渲染人读版 |
| `qc_terminology.py` | `zh/*.md` + 术语表 | `reports/terminology-consistency.md` | **全量**术语一致率审计（可作 CI 门禁） |
| `termcheck.py` | — | — | **术语匹配的唯一判定来源**（被 translate.py 与 qc_terminology.py 共用） |

## 执行顺序

```bash
python3 pipeline/parse_syllabus.py    # 1. 大纲 → JSON
python3 pipeline/inventory.py         # 2. 清点 → units.json + INVENTORY.md
python3 pipeline/clean.py             # 3. 清洗 + 校验 + 分块（消费 units.json）
python3 pipeline/mine_terms.py        # 4. 挖掘术语候选（改术语表前跑）
python3 pipeline/glossary_tool.py     # 5. 校验 + 渲染术语表
python3 pipeline/qc_terminology.py    # 6. 全量术语一致率审计（译稿完成后跑）
```

顺序有依赖：`clean.py` 消费 `inventory.py` 产出的 `units.json`；
`mine_terms.py` 消费 `clean.py` 产出的 `clean/*.md`。

## 单一判定来源

`clean.py` 导出 `extract_markdown()` 与 `MIN_CONTENT_CHARS`，`inventory.py` **从中导入**而不是自己再写一套。

原因：清点用的"什么算正文"和清洗产物必须**同源**。两处各写一份判定逻辑，迟早会漂移，
届时 `INVENTORY.md` 声称可用的篇目与 `clean/` 里实际产出的内容就会自相矛盾——
而覆盖度数字正是建立在这个判定之上。

同理，`mine_terms.py` 早期自带第三份 `visible_text()` 直接读原始 HTML，
导致术语频次被导航文字污染，也违反了同一条原则。现已改为消费 `clean/*.md`。

**第三次违反，也是最典型的一次**：术语匹配逻辑被写了两份——
`translate.py` 的逐块校验与 `qc_terminology.py` 的全量审计各有一套。
前者已经消除了子串误报，后者没有，于是全量审计报出 52 次违规，
其中绝大多数是早已解决过的假阳性。现已抽出 `termcheck.py` 作为唯一来源，
两个校验器都从它导入。

## 完整性校验（防静默丢内容）

`clean.py` 对每条比对三个层次的元素数量：

| 层次 | 含义 |
|---|---|
| `raw` | 整个原始文件（含样板） |
| `main` | 剔除样板、选定正文容器之后 |
| `md` | 最终 Markdown |

- `raw → main` 的差距 → **样板剔除误伤正文**
- `main → md` 的差距 → **渲染器漏渲染**
- **留存率**（正文容器文字量 → Markdown 纯文字量）是主判据，低于 90% 报警
- 代码块单独严判：丢了围栏就会被当散文翻译，而代码必须逐字保留

这套校验不是装饰。它在开发中实际抓到了 4 个 bug：

| # | Bug | 症状 | 靠什么发现 |
|---|---|---|---|
| 1 | `<figure>` 被整棵剔除 | 3 篇丢 10,735 字符（最多 19.1%） | 元素计数（raw vs main） |
| 2 | `_list()` 兜底分支扁平化块级子元素 | 17 个代码块丢失围栏 | 代码块计数（main vs md） |
| 3 | 单行表格被整表丢弃 | `agentic-ai-threats` 丢 5,608 字符 | 表格计数 |
| 4 | 代码块藏在表格单元格里被压成纯文本 | 1 个代码块失效 | 代码块计数 |

前 3 个在**体积指标下完全不可见**——文件大小正常、看着也正常，只能靠元素级校验发现。

## 平台限制（必须说明）

PDF 提取依赖 **macOS 原生 PDFKit**（经 `osascript` 调用），因此：

- ✅ macOS：开箱可用，无需安装任何东西
- ❌ 其它平台：`extract_pdf()` 会返回明确的错误说明并记录进报告，
  **不会静默产出空文件**

这是本项目"零第三方依赖"原则的代价。若要跨平台，需引入 `pypdf` 之类的库——
但那会破坏「clone 下来就能跑」这一目标，因此当前选择明确报错而非静默降级。

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
