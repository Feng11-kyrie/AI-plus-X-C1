# 资料清点与缺口报告（INVENTORY）

> 本文件由 `pipeline/inventory.py` 自动生成，**请勿手工编辑**（改脚本后重跑）。
> 数据源：`source/syllabus.json` + `source/page_map.json`。

课程：**Python 3 标准库与指南（第二源烟测）**（Python Software Foundation，3.x docs）
讲师：— ｜ 原始站点：https://docs.python.org/3/ ｜ 缓存于 2026-09-16

---

## 一、覆盖度分母（自证）

覆盖度不能只报一个百分比，必须先说清**分母是什么**。本报告采用的定义：

- **分母 = 大纲中指向本地文件的 readings = 3 条**（即 `pages/` 与 `pdfs/` 中有实体文件的条目）
- **其中可用 = 3 条**（HTML 3 + PDF 0），**确认无效 = 0 条**
- **分子 = 已产出中文译稿的可用条目数**（随管线推进更新）
- 目标：分子 / 分母 ≥ **80%**，即 ≥ 3 条

> **为什么不把外链算进分母**：大纲另有 0 条指向外部站点（YouTube / GitHub / X / 第三方博客），它们不受本地缓存控制，其可获得性取决于对方站点与账号权限，属于**扩展范围**，计入分母会让覆盖率失去可比性。详见第四节。

### 换算成硬指标

| 口径 | 数量 | 说明 |
|---|---|---|
| 分母（本地 readings） | 3 | HTML 3 + PDF 0 |
| **可用条目** | **3** | HTML 3 + PDF 0，内容完整可翻译 |
| **确认无效条目** | **0** | 全部为 HTML，详见第二节 |
| 达到 80% 所需最少条目 | 3 | ceil(3 × 0.8) |
| 可用英文正文字数（估） | ≈ 18,391 | 仅 HTML 可用条目（按清洗后正文计），PDF 未计 |

> ✅ **可行性**：可用条目 3 条 ≥ 目标 3 条。全部译完可达 100.0%。

---

## 二、缺口清单（必须处理）

无损坏条目。

### 2.1 讲义（Slides）——**完全缺失**

`slides_info/` 为空目录：**课程 10 周的讲义元数据一条都未抓取到**。
大纲中登记的讲义链接如下（全部为 Google Slides/Drive，**需 Google 账号**，自动化抓取不可行）：

| 周 | 讲义 | 类型 | 链接 |
|---|---|---|---|

### 2.2 视频字幕——**完全缺失**

大纲中的视频均为 YouTube 外链，**无任何字幕文件被获取**。
若要把视频字幕纳入覆盖范围，需额外的一手获取步骤（yt-dlp 等），
且需评估网络可达性与版权边界。**当前决定：不纳入分母，列为扩展范围。**

---

## 三、逐周工作单元清单

图例：`OK` 可用 ｜ `EMPTY` 0 字节 ｜ `PLACEHOLDER` 占位页 ｜ `LOW` 有文件但正文不足 ｜ `EXTERNAL` 外链

### Week 1：标准库文档（第二源烟测） ／ 编码 LLM 与 AI 开发导论

Topics：HTML → Markdown 清洗、表格与代码块保留、分块

| 状态 | 类型 | 标题 | 本地路径 / 来源 | 字数 |
|---|---|---|---|---|
| OK | local/html | 如何使用 argparse（HOWTO） | `demo/second-source/pages/howto-argparse.html` | 3,767 |
| OK | local/html | argparse — 命令行选项解析 | `demo/second-source/pages/library-argparse.html` | 10,789 |
| OK | local/html | json — JSON 编解码 | `demo/second-source/pages/library-json.html` | 3,835 |

