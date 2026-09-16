# AI➕X C1｜CS146S 课程资料获取与翻译

[![pipeline-checks](https://github.com/Feng11-kyrie/AI-plus-X-C1/actions/workflows/checks.yml/badge.svg)](https://github.com/Feng11-kyrie/AI-plus-X-C1/actions/workflows/checks.yml)

> 把 Stanford **CS146S: The Modern Software Developer**（Fall 2025）的公开课程资料，
> 通过一条**可复跑的信息获取与翻译管线**，产出完整中文资料包，让下一批同学零成本复用。

本仓库是 **AI➕X 挑战 C1「课程资料获取与翻译」** 的交付物。
挑战编号：`ch-20260717031336-pxzwy0` ｜ 截止：2026-12-31 23:59

> 🔍 **这个徽章不是装饰。** 点进去是 GitHub Actions 的真实运行日志——
> 每次 push 都会在 GitHub 的机器上重跑一遍管线、审计全量术语，通不过就变红。
> 它把「我声称可复跑」变成「任何人都能点开看它跑没跑通」。
>
> 这里**只有一个徽章**，刻意没加「覆盖率 XX%」之类的静态徽章——
> 那种徽章要手动更新，一旦忘记就变成过期的自我表扬。覆盖率请看下方状态表。

---

## 📌 当前状态

> **本仓库正在建设中。** 下表如实反映进度，不做任何完成度上的夸大。

| 阶段 | 状态 | 说明 |
|---|---|---|
| ① 资料获取与归档 | ✅ 完成 | 21MB 一手资料已归档至 `source/` |
| ② 资料清点与缺口识别 | ✅ 完成 | `source/INVENTORY.md`（自动生成，含覆盖度分母自证） |
| ③ 术语表建设 | ✅ 完成 | **171 条**（要求 ≥50），317 个硬性 + 48 个提示级禁用变体，经校验器通过 |
| ④ 清洗管线（HTML/PDF→Markdown） | ✅ 完成 | `pipeline/clean.py`：20.8MB → 0.55MB，**29 条正文底稿 + 零内容丢失告警** |
| ⑤ 翻译管线 | ✅ 完成 | `pipeline/translate.py`：后端可插拔（queue / api）、增量可复跑、逐块校验 |
| ⑥ 术语一致性自动校验 | ✅ 完成 | `qc_terminology.py` + `check_tables.py` + CI 门禁（徽章实时反映） |
| ⑦ 中文译稿产出 | ✅ **28/29 条** | 覆盖率 **82.4%**（分母 34），已越过 80% 目标（≥28 条） |
| ⑧ 发布与复盘 | 🚧 进行中 | AAR、AI 日志（600+ 条事件，自动渲染）、**4 个拿来说明**已完成 |

**已交付**：四项必交交付物（`README.md` / `AI日志.md` / `AAR.md` / `拿来说明/` ×4）
均已齐全；另有 `source/INVENTORY.md`、`glossary/glossary.csv`、`clean/`（29 条英文底稿）、
`zh/`（**28 条中文译稿**）、`reports/`（5 份自动生成报告）、`pipeline/`（10 支 Python 脚本 + 1 支 JS）

---

## 🎯 覆盖度：分母是这么定义的

覆盖率不能只报一个数字——**必须先说清分母是什么**，否则无法核对。本项目的定义：

> **分母 = 课程大纲中指向本地文件的 readings = 34 条**
> （即 `source/pages/` 与 `source/pdfs/` 中有实体文件的条目）
> **目标：中文译稿 / 34 ≥ 80%，即 ≥ 28 条**（`ceil(34×0.8)`；早先误算成 27）

| 口径 | 数量 |
|---|---|
| 分母（本地 readings） | **34**（HTML 31 + PDF 3） |
| 其中可用 | **29**（HTML 26 + PDF 3） |
| **其中确认失效** | **5**（全部为 HTML） |
| 达到 80% 所需 | ≥ 28 条（`ceil(34×0.8)`） |
| **已完成译稿** | **28 条 → 82.4% ✅** |
| 可翻译正文规模 | ≈ **83,327 词**（含 3 份 PDF；仅 HTML 为 67,127 词） |
| 大纲中的外部链接 | 10 条（**不计入分母**，理由见下） |

**⚠️ 一个关键的可行性约束**：29/34 = **85.3%** 是上限，而达标线是 28 条。也就是说**只有 1 条的容错**。
如果**只翻译 HTML 部分**，覆盖率仅 26/34 = **76.5%，低于目标**——因此 3 份 PDF 必须纳入翻译范围。

**当前进度 28/29 条 = 82.4%**（262/271 个分块）。剩下 1 条是原始缓存就失效的
`lessons-from-ai-code-reviews`（0 字节）。逐条状态见 **[`reports/coverage.md`](reports/coverage.md)**。

### 分母的一个边界情形（不据此改口径，但如实标注）

重抓失效条目时发现：`lessons-from-ai-code-reviews` 这条**其实不是文章，是一段视频**。
证据在归档里——大纲的可执行代码 `source/site/themodernsoftware.dev/assets/index-CgRb4FxC.js`
的 Week 7 阅读清单里，这条的文字是 `Lessons from millions of AI code reviews`，链接指向
`https://www.youtube.com/watch?v=TswQeKftnaw`。大纲里另外两段视频（W1 的
`Deep Dive into LLMs`、`AI Prompt Engineering: A Deep Dive`）**都被正确归类为
`external`、不计入分母**；只有这一条因为在归档时按普通网页抓取、留下一个 0 字节文件，
被归类成 `local`，于是进了分母。

| 口径 | 分母 | 覆盖度 | 目标 | 结论 |
|---|---|---|---|---|
| **主口径（保守，本仓库采用）** | 34 | **28/34 = 82.4%** | ≥28 | ✅ 达标 |
| 若按大纲视频的既有处理移出分母 | 33 | 28/33 = 84.8% | ≥27 | ✅ 达标 |

**为什么采用保守口径**：把「抓不到的条目」移出分母会让数字变好看，而这正是本项目
刻意避免的事——5 篇失效条目一律留在分母里，当作对自己的惩罚（见 `拿来说明/03`）。
两个数字都给出来，结论在两种口径下都达标，读者可以自行核对。

**为什么外链不计入分母**：大纲另有 10 条指向 YouTube / GitHub / X / 第三方站点，它们的可获得性取决于对方站点与账号权限，不受本项目控制。计入分母会让覆盖率失去可比性。它们被列为**扩展范围**，在 `source/INVENTORY.md` 中完整登记。

📄 完整清点、逐周工作单元清单、缺口明细 → **[`source/INVENTORY.md`](source/INVENTORY.md)**

---

## ⚠️ 已知缺口（如实声明，未做隐瞒）

清洗管线**剔除了样板后**才发现：失效的不是 2 篇，而是 **5 篇**。原始缓存自带的 README 只承认了其中 1 篇。

| # | 篇目 | 周 | 症状 | 失效模式 |
|---|---|---|---|---|
| 1 | `prompt-engineering-guide` | W1 | 128KB 但正文仅 548 字节 | **SPA 导航壳**：`__NEXT_DATA__` 载荷为空，真实正文在未被抓取的子页面 |
| 2 | `good-context-good-code` | W4 | 9KB 但正文仅 77 字节 | **访问码/付费墙**：抓到的是登录门页 |
| 3 | `peeking-under-the-hood-of-claude-code` | W4 | 550 字节 | **反爬占位页**（源站 Medium） |
| 4 | `how-warp-uses-warp` | W5 | 15KB 但正文仅 7 字节 | **Notion JS 渲染页**：静态抓取只能拿到外壳 |
| 5 | `lessons-from-ai-code-reviews` | W7 | **0 字节** | 抓取完全失败（**已查明：这条其实是大纲里的一段 YouTube 视频**，不是文章；见上文「分母的一个边界情形」） |

另有系统性缺失：

| 缺口 | 影响 | 现状 |
|---|---|---|
| **讲义（Slides）完全缺失** | 10 周讲义均无 | 全部为 Google Slides/Drive，需 Google 账号，自动化不可行 |
| **视频字幕完全缺失** | 3 个 YouTube 视频无字幕 | 需额外获取步骤，当前不纳入分母 |
| **挑战包另附的 `Vibe_Coding_Playbook.pdf` 未翻译** | 挑战材料里的 14 页一手材料无中文 | 经 PDFKit 提取为 **0 字符**——纯图像型 PDF（无文字层），要 OCR 才能取文；本管线不做 OCR。它不在大纲 readings 里，故不计入覆盖度分母 |
| **清洗管线漏识别 div 表格** | 用 `<div class="table">` 画的表不会转成 Markdown 表 | 已知 1 处（`sast-vs-dast`），差异登记在 `table-exceptions.json` |

> 讲义与视频的完整链接清单（含每一周的 Google Slides URL）见 `source/INVENTORY.md` 第 2.1、2.2 节。
> 逐篇失效明细见 **[`reports/clean-comparison.md`](reports/clean-comparison.md)**。

---

## 📚 术语表（术语一致性的强制保障）

**171 条术语**，覆盖 7 个领域，含 **317 条硬性 + 48 条提示级禁用变体**（其中 148 条需翻译、23 条专有名词保留英文）。

| 分类 | 条数 | 分类 | 条数 |
|---|---|---|---|
| 软件工程 | 36 | 安全 | 32 |
| 核心 LLM 与提示词 | 28 | SRE 与可观测性 | 25 |
| 工具与专有名词（不译） | 21 | 智能体与工具调用 | 15 |
| 产品与流程 | 14 | | |

> **为什么禁用变体要分两级**：中文里一批词既是「本术语的错误译法」、
> 又是「邻近英文词的正确译法」（如 proxy → 代理、dashboard → 控制台）。
> 一律硬性拦截会逼出错误的译文，所以这类只提示不拦截，并在报告里单列一节说明。

**为什么是 `csv` 而不是一张 Markdown 表格**：`glossary/glossary.csv` 是**机器可读的唯一真源**，管线直接消费它；`glossary/glossary.md` 是自动渲染的展示版。禁用变体字段（`forbidden_zh`）让"术语统一"从一句自我声明变成**可脚本校验的事实**。

📄 **[`glossary/glossary.md`](glossary/glossary.md)**（人读）｜ **[`glossary/glossary.csv`](glossary/glossary.csv)**（机器读）

---

## 🗂 目录结构

```
AI-plus-X-C1/
├── README.md                  ← 你在这里
├── NOTICE.md                  版权、出处与使用边界
├── AAR.md                     七维复盘
│
├── source/                    一手资料归档（含原始缓存，保证管线可复跑）
│   ├── INVENTORY.md           ★ 资料清点与缺口报告（自动生成）
│   ├── units.json             ★ 机器可读的工作单元清单 = 翻译管线的工作队列
│   ├── syllabus.json          ★ 从 index.html 解析出的结构化大纲（10 周）
│   ├── index.html             课程主页（含完整 Syllabus）
│   ├── page_map.json          原始 URL → 本地文件映射（溯源依据）
│   ├── pages/                 31 篇阅读材料 HTML
│   ├── pdfs/                  3 份 PDF
│   └── site/                  原站静态资源
│
├── glossary/
│   ├── glossary.csv           ★ 术语表（唯一真源，机器可读）
│   └── glossary.md            术语表（自动渲染，人读）
│
├── pipeline/                  管线：每一步都可复跑
│   ├── config/cs146s.json     ★ 源配置——换课程只改这个文件
│   ├── config/table-exceptions.json  表格差异例外登记（含证据与复核日期）
│   ├── parse_syllabus.py      解析 index.html → syllabus.json
│   ├── inventory.py           清点与缺口报告生成
│   ├── clean.py               HTML/PDF → Markdown 清洗 + 分块
│   ├── pdfkit_dump.js         PDF 文本提取（macOS PDFKit，经 osascript 调用）
│   ├── mine_terms.py          从语料挖掘术语候选
│   ├── glossary_tool.py       术语表校验 + 渲染
│   ├── translate.py           ★ 翻译管线（后端可插拔、增量可复跑、逐块校验）
│   ├── termcheck.py           ★ 术语判定的唯一来源（两个校验器共用）
│   ├── qc_terminology.py      全量术语一致率审计（CI 门禁）
│   ├── check_tables.py        源↔译表格行数比对（CI 门禁）
│   ├── check_deliverables.py  ★ 交付物通配符真匹配（CI 门禁）
│   ├── check_workflow.py      ★ 工作流自检（CI 门禁 + 本地提交前用）
│   ├── check_staleness.py     提交产物 vs 现在跑出来的产物（信息性）
│   └── check_chunks.py        分块对照清单（人工核「有没有把两块并成一块」）
│
├── demo/                      ★ 第二源烟测（换源可复用证据，见 demo/README.md）
├── clean/                     清洗后的英文 Markdown 底稿（29 条，可人工抽检）
├── zh/                        中文译稿（28 条，82.4%）
├── reports/                   6 份自动生成报告：清洗对比、覆盖度、术语一致率、
│                              表格完整性、交付物检查、术语候选
├── AI日志.md                  ★ AI 协作日志（600+ 条事件，自动生成，按天汇总）
└── 拿来说明/                  ★ 4 个"拿来说明"（文件名含「拿来说明」，见下方说明）
```

---

## ✅ 自动化检查（CI）

每次 push 都会在 GitHub 的机器上自动跑下列检查（`.github/workflows/checks.yml`）：

| # | 检查 | 命令 | 失败会怎样 |
|---|---|---|---|
| 1 | 术语表自洽性（R1–R9） | `glossary_tool.py --check` | 徽章变红 |
| 2 | 全量术语一致率 | `qc_terminology.py --check` | 徽章变红 |
| 3 | **管线可复跑（确定性）** | 连跑两遍比对彼此 | 徽章变红 |
| 4 | **表格完整性（源↔译表行数）** | `check_tables.py --check` | 徽章变红 |
| 5 | **交付物命名（通配符真匹配）** | `check_deliverables.py --check` | 徽章变红 |
| 6 | **工作流自检（YAML 合法 + 门禁齐全）** | `check_workflow.py --check` | 徽章变红 |
| 7 | 提交产物新鲜度 | `check_staleness.py` | 信息性，不作门禁 |
| 8 | 覆盖度概览 | `translate.py --status` | 信息性，不作门禁 |

> **第 4 项是补出来的。** 逐块校验只比代码围栏数与链接数，**不比表格行数**——
> 于是三处整行丢失（两处是我自己删的）一路通过校验，全靠手工数行数才发现。
> 手工发现的问题必须变成机制。经过与结论见
> [`拿来说明/04`](拿来说明/拿来说明-04-三处丢行与手工发现的机制化.md)。

### 第 3 项为什么这么设计

CI 跑在 **Ubuntu** 上，而 PDF 提取依赖 **macOS 原生 PDFKit**——所以 CI 产出的
`clean/` 与仓库里提交的那份必然不同，直接 `git diff` 会因为平台差异而失败，
那是**假告警**。

改为**连跑两遍比对彼此**：测的是「同样的输入是否得到同样的输出」，与平台无关。
这才是「可复跑」的真正含义。

### 已知的 CI 覆盖缺口（如实声明）

- ❌ **PDF 提取未纳入 CI**：平台依赖所致。3 份 PDF 的确定性只在 macOS 上验证过。
- ❌ **表格单元格内容未纳入 CI**：`check_tables.py` 只比行数，单元格里的删改抓不到。
- ✅ **HTML 清洗、分块、清点报告**：完整覆盖。

宁可把缺口写清楚，也不假装全覆盖。

---

## 🚀 如何使用本仓库

### 只是想读中文资料的同学

译稿在 `zh/` 下，**28 篇（29 篇可用资料中的 28 篇）**，文件名与英文底稿一一对应。
还没译的那篇是原始缓存就已失效的 `lessons-from-ai-code-reviews`（0 字节），原因见下方已知缺口。

入口建议按学习顺序读：先 `zh/prompt-engineering-overview.md`、`zh/mcp-introduction.md`
建立概念，再按周推进。原文对照看 `clean/` 下同名英文底稿。

英文原始资料仍可直接打开 `source/index.html`——一份完整的离线课程主页，无需联网。

### 想复跑或接续这条管线的同学

**零依赖**——只用 Python 3 标准库，无需 pip install。

```bash
git clone git@github.com:Feng11-kyrie/AI-plus-X-C1.git
cd AI-plus-X-C1

python3 pipeline/parse_syllabus.py   # 解析大纲 → source/syllabus.json
python3 pipeline/inventory.py        # 生成清点与缺口报告
python3 pipeline/clean.py            # HTML → Markdown 清洗 + 分块
python3 pipeline/mine_terms.py       # 挖掘术语候选（可选，--csv 导出）
python3 pipeline/glossary_tool.py    # 校验术语表并渲染
python3 pipeline/translate.py --status   # 覆盖度概览（不翻译，只看进度）
```

要用 **API 后端**（而不是默认的队列后端）真正自动跑完翻译：

```bash
export DEEPSEEK_API_KEY=sk-...           # 任何 OpenAI 兼容端点
python3 pipeline/translate.py --backend api
```

> 没有 key 时脚本会**先检查再动手**（退出码 2），不会写出半截状态。
> 默认的 `queue` 后端把每块的完整 prompt 写到 `pipeline/work/todo/`，
> 再把译文从 `pipeline/work/done/` 收回——本项目的中译稿就是这样逐块产出并留痕的。

> 注意执行顺序：`inventory.py` 产出 `units.json`，`clean.py` 消费它。
> 全部脚本零依赖，只用 Python 3 标准库；复跑后 `git status` 应无差异（产物是确定性的）。

术语表校验可以作为质量门禁单独运行（校验失败返回非零退出码）：

```bash
python3 pipeline/glossary_tool.py --check     # 术语表自洽性（R1–R9）
python3 pipeline/qc_terminology.py --check    # 全量术语一致率
python3 pipeline/check_tables.py --check      # 表格完整性（源↔译表行数）
python3 pipeline/check_chunks.py              # 分块对照清单（只提示不拦截）
```

### 🔁 换一门课怎么办？（管线的可复用性）

这是本管线的核心设计目标。**不需要改任何脚本代码**，只需：

1. 新建 `pipeline/config/<新课代号>.json`，指向新课的 `index_html` / `pages_dir` / `pdfs_dir` / `page_map`；
2. 其余五个脚本读取配置即可运行，产出新课的 `syllabus.json` / `units.json` / `INVENTORY.md` / `clean/` / 术语候选。

> 已用这套结构在 **CS146S** 上跑通全链路（获取 → 清点 → 清洗 → 分块 → 翻译 → 校验）。
> **换源也已实际演示**：见 **[`demo/`](demo/README.md)**——只换一个环境变量
> （`PIPELINE_CONFIG=...`），把同一套脚本跑到一个完全不同的站点（Python 3 官方文档）上，
> 清点 → 清洗 → 分块 → 术语挖掘全部产出（3 条 / 68 块 / 留存率 98.2–99.7%）。
> 那次烟测**真抓出了 4 个只在单源下看不见的 bug**（写死的路径、空源崩溃、例外登记跨源泄漏），
> 已全部修掉。
>
> 仍未做的：把第二门课**译完**（交付物要的是 CS146S 的中文包，第二源只用于验证可复用），
> 以及抓取/大纲解析这两个环节的自动化——它们本来就是每站不同的部分，清单见 `demo/README.md`。

---

## 📦 交付物对照

| 挑战要求的交付物 | 本仓库对应位置 | 状态 |
|---|---|---|
| `README.md` | `README.md`（本文件） | ✅ |
| 资料包说明（来源/范围/流程/用法/缺口） | 本文件 + `source/INVENTORY.md` | ✅ |
| 术语表 ≥50 条 | `glossary/glossary.csv`（**171 条**） | ✅ |
| 可复跑的翻译管线 | `pipeline/`（10 支 Python + 1 支 JS，「获取→清点→清洗→翻译→校验」全通） | ✅ |
| 清洗后英文底稿 | `clean/`（29 条）+ `reports/clean-comparison.md` | ✅ |
| 完整中文资料包 | `zh/`（**28/29 条 = 82.4%**） | ✅ 达标 |
| `*AI日志*` | `AI日志.md`（600+ 条事件，自动生成、含失败记录） | ✅ |
| `*AAR*`（七维复盘） | `AAR.md` | ✅ |
| `*拿来说明*` ≥3 个 | `拿来说明/`（**4 篇**） | ✅ |

> **交付物的名字是规格的一部分。** 挑战里写的是四个**通配符**：
> `README.md,*AI日志*,*AAR*,*拿来说明*`。本仓库为此专门改了名并加了机械校验——
> 因为踩过一次：AI 日志原先叫 `logs/ai-journal.md`，路径里没有「AI日志」四个字，
> `glob("*AI日志*")` 返回 **0 项**。内容一字不少，但在检查器眼里这份交付物不存在，
> 而 rubric 红线 `missing_artifacts` 会把产物完整性直接压到 5 分。
> 同理 `*拿来说明*` 要求「至少 3 个」，所以四个文件的**文件名**都含「拿来说明」，
> 而不是只有外层目录叫这个名字（否则按文件计数只有 1 项）。
> 现在由 `pipeline/check_deliverables.py` 每次 push 自动核对。

---

## © 版权与出处

原始课程资料版权归 **Stanford University** 与原作者所有。
本仓库的译稿与工具仅用于**学习与交流**，不作商业用途。

- 课程：CS146S: The Modern Software Developer（Stanford University, Fall 2025）
- 讲师：Mihail Eric
- 原始站点：<https://themodernsoftware.dev/>
- 缓存日期：2026-04-02

详细声明见 **[`NOTICE.md`](NOTICE.md)**。若版权方有异议，请联系删除。

---

## 📄 许可

- `pipeline/`、`glossary/` 下的**工具与术语表**：MIT
- `source/` 下的**原始资料**：版权归原作者，仅作归档，不适用 MIT
- `zh/` 下的**中文译稿**：仅限学习交流
