# 第二源烟测：证明「换源可复用」，并且它真抓出了 4 个 bug

挑战的验收要点里写着：**「翻译流水线可复跑：换一门课的资料，同样的流程能再次产出」**。
这句话不能靠声明，得真跑一次。这个目录就是那次运行的全部产物。

---

## 一、怎么跑的：只换一个环境变量

```bash
PIPELINE_CONFIG=pipeline/config/demo-second-source.json python3 pipeline/inventory.py
PIPELINE_CONFIG=pipeline/config/demo-second-source.json python3 pipeline/clean.py
PIPELINE_CONFIG=pipeline/config/demo-second-source.json python3 pipeline/mine_terms.py
```

**没有改任何一行的脚本代码。** 配置里换掉的是：输入目录、大纲 JSON、
产物目录（`clean/`、`chunks.json`、报告、`zh/`），以及一份新的 page_map。

第二源选的是 **Python 3 官方文档**的三页（`argparse`、`json`、`argparse` HOWTO），
2026-09-16 抓取。选它有两个理由：站点结构与 CS146S 完全不同（Sphinx 而非 Astro），
且 PSF 许可证允许带署名的再分发。

---

## 二、跑出来的结果（数字都是真的）

### 清点（`inventory.py`）

| 项 | 值 |
|---|---|
| 工作单元 | 3 |
| 覆盖度分母 | 3 |
| 达标所需（ceil(3×0.8)） | 3 |
| 可用英文正文 | ≈ **18,391 词** |
| 产出 | `demo/second-source/units.json`、`demo/second-source/INVENTORY.md` |

### 清洗 + 分块（`clean.py`）

| 条目 | 原始 | Markdown | 留存率 | 词数 | 块数 | 状态 |
|---|---|---|---|---|---|---|
| `howto-argparse` | 106KB | 26.6KB | 99.7% | 3,767 | 13 | OK |
| `library-argparse` | 316KB | 81.6KB | 98.2% | 10,789 | 42 | OK |
| `library-json` | 110KB | 28.0KB | 99.3% | 3,835 | 13 | OK |

汇总：3 条有效 / 0 条失效，0.52MB → 0.13MB，**68 个分块**，
`✓ 内容丢失检查通过：无告警`。

### 术语挖掘（`mine_terms.py`）

从新语料里挖出候选（复用主术语表做过滤）：

```
   90  JSON      71  PROG      37  FOO      24  BAR
   18  UTF       18  RFC        9  XXX       7  API
```

### 校验器在「还没有译稿」时的行为

```
qc_terminology.py  → 尚无译稿，跳过术语审计。
check_tables.py    → 审计译稿 0 篇｜表行数差异 0 篇
translate.py --status → 条目完成 0/3（需 3 条达 80%）
```

**没有崩，也没有假报违规**——这是「换源可复用」的一部分：
新源刚起步时（只有清洗稿、没有译稿）整条管线必须能跑通而不是抛异常。

---

## 三、这次烟测真正抓出来的 4 个问题

跑第二源的价值不在"证明了能跑"，而在**它让只在主源上永远看不见的问题现形了**。
4 个问题全部由这次运行暴露：

| # | 问题 | 为什么在 CS146S 上看不见 | 修法 |
|---|---|---|---|
| 1 | `inventory.py` 判断页面是否存在时，仍然写死 `ROOT / "source" / path` | CS146S 的产物目录**恰好**就叫 `source/`，写死也永远对 | 改读配置的 `raw_dir` |
| 2 | `translate.py --status` 读死 `source/units.json` | 同上 | 改读配置的 `units_json` |
| 3 | **空源直接崩溃**：`inventory.py`、`clean.py` 抛 `ZeroDivisionError` | CS146S 从不缺数据，分母永远不为 0 | 改成可读结论（"本次没有本地条目，请确认归档步骤"） |
| 4 | 表格例外登记跨源泄漏：第二源被报「过期例外：sast-vs-dast」 | 例外表本来就是 CS146S 的，只有跑别的源才会发现它没有边界 | 例外表加 `source_id`，不匹配就跳过例外与过期判定 |

第 1、2 条是**同一个病**：配置里声明了路径，代码里另有一份写死的同义路径。
它们能活到今天，唯一的原因是**默认值恰好等于正确值**——
这正是本项目已经踩过五次的那类问题（同一件事两个来源，必然漂移），
只不过这一回是"第二源"把它照出来的。

第 3 条尤其能说明问题：**"在我这台机器上能跑"和"换个人、换个源也能跑"是两件事**，
而只有后者才叫可复用。

---

## 四、换源时真正需要人做的三件事（不吹）

管线可复用，但**不等于换源是零工作**。诚实清单：

| 环节 | 是否可复用 | 换源要做什么 |
|---|---|---|
| 清点 → 清洗 → 分块 → 术语挖掘 → 翻译 → 校验 | ✅ 全部复用 | 只改配置 |
| 抓取与归档 | ❌ 每站不同 | 抓页面、生成 `page_map.json`（原 URL → 本地文件） |
| 大纲解析（`parse_syllabus.py`） | ❌ 依赖站点 DOM | CS146S 用的是 `week-header`/`week-section` 这类 class；换站要么改这个解析器，要么用别的办法产出**同 schema 的 `syllabus.json`**。本目录里的第二源大纲是我手写的最小清单，就属于后者 |
| 术语表 | ⚠️ 部分复用 | 通用术语（MCP、RAG 之类）能留，领域术语要重挖——`mine_terms.py` 就是干这个的 |

**没有翻译第二源**，也刻意不翻译：交付物要的是 CS146S 的中文资料包，
第二源的存在只为验证"同一套流程能再次产出"。

---

## 五、这个目录里的文件

| 路径 | 说明 |
|---|---|
| `pipeline/config/demo-second-source.json` | 第二源配置（换源唯一需要改的文件） |
| `second-source/syllabus.json` | 第二源大纲（同 schema，手写最小清单） |
| `second-source/page_map.json` | 原 URL → 本地文件映射 |
| `second-source/pages/*.html` | 抓取到的原始页面（3 页） |
| `second-source/units.json`、`INVENTORY.md` | 清点产物（自动生成） |
| `second-source/clean/*.md` | 清洗产物（自动生成，3 篇） |
| `second-source/work/chunks.json` | 分块产物（自动生成，68 块） |
| `second-source/reports/*.md` | 该源的报告（自动生成） |

> 第二源的产物**不参与**主仓库的任何门禁与覆盖度统计——
> 覆盖度只算 CS146S（分母 34），这里的 3 条不进入任何分母。
