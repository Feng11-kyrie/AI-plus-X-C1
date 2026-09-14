# AI➕X C1｜CS146S 课程资料获取与翻译

> 把 Stanford **CS146S: The Modern Software Developer**（Fall 2025）的公开课程资料，
> 通过一条**可复跑的信息获取与翻译管线**，产出完整中文资料包，让下一批同学零成本复用。

本仓库是 **AI➕X 挑战 C1「课程资料获取与翻译」** 的交付物。
挑战编号：`ch-20260717031336-pxzwy0` ｜ 截止：2026-12-31 23:59

---

## 📌 当前状态

> **本仓库正在建设中。** 下表如实反映进度，不做任何完成度上的夸大。

| 阶段 | 状态 | 说明 |
|---|---|---|
| ① 资料获取与归档 | ✅ 完成 | 21MB 一手资料已归档至 `source/` |
| ② 资料清点与缺口识别 | ✅ 完成 | `source/INVENTORY.md`（自动生成，含覆盖度分母自证） |
| ③ 术语表建设 | ✅ 完成 | **170 条**（要求 ≥50），经校验器通过 |
| ④ 清洗管线（HTML→Markdown） | ✅ 完成 | `pipeline/clean.py`：6.13MB HTML → 0.43MB MD，**发现 5 篇失效** |
| ⑤ 翻译管线 | ⬜ 未开始 | 计划 `pipeline/translate.py` |
| ⑥ 术语一致性自动校验 | ⬜ 未开始 | 计划 `pipeline/qc_terminology.py` + CI |
| ⑦ 中文译稿产出 | ⬜ 未开始 | 目标 ≥80% 覆盖度（≥27 条） |
| ⑧ 发布与复盘 | ⬜ 未开始 | 含 AAR、拿来说明 |

**已交付**：`source/INVENTORY.md`、`glossary/glossary.csv`、`reports/clean-comparison.md`、`clean/`（26 篇英文底稿）、`pipeline/` 五支可跑脚本

---

## 🎯 覆盖度：分母是这么定义的

覆盖率不能只报一个数字——**必须先说清分母是什么**，否则无法核对。本项目的定义：

> **分母 = 课程大纲中指向本地文件的 readings = 34 条**
> （即 `source/pages/` 与 `source/pdfs/` 中有实体文件的条目）
> **目标：中文译稿 / 34 ≥ 80%，即 ≥ 27 条**

| 口径 | 数量 |
|---|---|
| 分母（本地 readings） | **34**（HTML 31 + PDF 3） |
| 其中可用 | **29**（HTML 26 + PDF 3） |
| **其中确认失效** | **5**（全部为 HTML） |
| 达到 80% 所需 | ≥ 27 条 |
| 可用英文正文规模 | ≈ 65,156 词（清洗后正文，PDF 未计） |
| 大纲中的外部链接 | 10 条（**不计入分母**，理由见下） |

**⚠️ 一个关键的可行性约束**：29/34 = **85.3%**，达标。但如果**只翻译 HTML 部分**，覆盖率仅 26/34 = **76.5%，低于目标**。因此 **3 份 PDF 必须纳入翻译范围**。

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
| 5 | `lessons-from-ai-code-reviews` | W7 | **0 字节** | 抓取完全失败 |

另有系统性缺失：

| 缺口 | 影响 | 现状 |
|---|---|---|
| **讲义（Slides）完全缺失** | 10 周讲义均无 | 全部为 Google Slides/Drive，需 Google 账号，自动化不可行 |
| **视频字幕完全缺失** | 3 个 YouTube 视频无字幕 | 需额外获取步骤，当前不纳入分母 |

> 讲义与视频的完整链接清单（含每一周的 Google Slides URL）见 `source/INVENTORY.md` 第 2.1、2.2 节。
> 逐篇失效明细见 **[`reports/clean-comparison.md`](reports/clean-comparison.md)**。

---

## 📚 术语表（术语一致性的强制保障）

**170 条术语**，覆盖 7 个领域，含 **370 条禁用变体**。

| 分类 | 条数 | 分类 | 条数 |
|---|---|---|---|
| 核心 LLM 与提示词 | 28 | 安全 | 32 |
| 智能体与工具调用 | 15 | SRE 与可观测性 | 25 |
| 软件工程 | 35 | 产品与流程 | 13 |
| 工具与专有名词（不译） | 23 | | |

**为什么是 `csv` 而不是一张 Markdown 表格**：`glossary/glossary.csv` 是**机器可读的唯一真源**，管线直接消费它；`glossary/glossary.md` 是自动渲染的展示版。禁用变体字段（`forbidden_zh`）让"术语统一"从一句自我声明变成**可脚本校验的事实**。

📄 **[`glossary/glossary.md`](glossary/glossary.md)**（人读）｜ **[`glossary/glossary.csv`](glossary/glossary.csv)**（机器读）

---

## 🗂 目录结构

```
AI-plus-X-C1/
├── README.md                  ← 你在这里
├── NOTICE.md                  版权、出处与使用边界
├── AAR.md                     七维复盘（待产出）
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
│   ├── parse_syllabus.py      解析 index.html → syllabus.json
│   ├── inventory.py           清点与缺口报告生成
│   ├── clean.py               HTML → Markdown 清洗 + 分块
│   ├── mine_terms.py          从语料挖掘术语候选
│   └── glossary_tool.py       术语表校验 + 渲染
│
├── clean/                     清洗后的英文 Markdown 底稿（26 篇，可人工抽检）
├── zh/                        中文译稿（待产出）
├── reports/                   清洗对比报告（已有）
│                              + 覆盖度/术语一致率/抽检报告（待产出）
├── logs/ai-journal.md         AI 协作日志（待产出）
└── notes/拿来说明/            至少 3 个"拿来说明"（待产出）
```

---

## 🚀 如何使用本仓库

### 只是想读中文资料的同学

译稿将放在 `zh/` 下，按周组织（`zh/week01/` … `zh/week10/`）。
**当前译稿尚未产出**，请先看英文原始资料：直接打开 `source/index.html`，它是一份完整的离线课程主页（含导航、大纲与全部本地化的阅读链接），无需联网。

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
```

> 注意执行顺序：`inventory.py` 产出 `units.json`，`clean.py` 消费它。
> 全部脚本零依赖，只用 Python 3 标准库；复跑后 `git status` 应无差异（产物是确定性的）。

术语表校验可以作为质量门禁单独运行（校验失败返回非零退出码）：

```bash
python3 pipeline/glossary_tool.py --check
```

### 🔁 换一门课怎么办？（管线的可复用性）

这是本管线的核心设计目标。**不需要改任何脚本代码**，只需：

1. 新建 `pipeline/config/<新课代号>.json`，指向新课的 `index_html` / `pages_dir` / `pdfs_dir` / `page_map`；
2. 其余五个脚本读取配置即可运行，产出新课的 `syllabus.json` / `units.json` / `INVENTORY.md` / `clean/` / 术语候选。

> 已用这套结构在 **CS146S** 上完整跑通。第二门课的复跑演示见 `reports/`（待产出）。

---

## 📦 交付物对照

| 挑战要求的交付物 | 本仓库对应位置 | 状态 |
|---|---|---|
| `README.md` | `README.md`（本文件） | ✅ |
| 资料包说明（来源/范围/流程/用法/缺口） | 本文件 + `source/INVENTORY.md` | ✅ |
| 术语表 ≥50 条 | `glossary/glossary.csv`（170 条） | ✅ |
| 可复跑的翻译管线 | `pipeline/`（5 支脚本，已跑通「获取→清点→清洗」） | 🚧 进行中 |
| 清洗后英文底稿 | `clean/`（26 篇）+ `reports/clean-comparison.md` | ✅ |
| 完整中文资料包 | `zh/` | ⬜ |
| `*AI日志*` | `logs/ai-journal.md` | ⬜ |
| `*AAR*`（七维复盘） | `AAR.md` | ⬜ |
| `*拿来说明*` ≥3 个 | `notes/拿来说明/` | ⬜ |

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
