# NOTICE — 版权、出处与使用边界

## 一、原始资料的版权归属

本仓库 `source/` 目录下的全部英文原始资料，版权归**原始作者与出版方**所有，
本项目**不主张任何权利**。具体包括：

| 内容 | 版权归属 |
|---|---|
| 课程大纲、站点结构、讲义链接 | Stanford University ／ 课程讲师 Mihail Eric |
| `source/pages/` 下 31 篇文章 | 各自原始站点（Google Cloud、Anthropic、OWASP、Splunk、Semgrep、Coding Horror、GitHub Blog、Graphite、Google SRE、Chroma、Resolve AI、Warp、Devin 等） |
| `source/pdfs/` 下 3 份 PDF | Anthropic ／ OpenAI ／ 相应出版方 |
| 课程名称、讲师姓名、机构标识 | Stanford University |

这些资料原本散落在公开互联网上。本仓库将其**归档**，目的是：

1. 让译稿的**溯源可核对**（每个译文单元对应哪个原始来源）；
2. 让翻译管线**可复跑**（没有原始输入，管线无法重跑验证）；
3. 抵御源站失效——课程站点或文章下线后，归档仍有价值。

## 二、翻译与衍生作品

`zh/` 目录下的中文译稿是对上述原始资料的**衍生作品**，
其版权状态**从属于原始作品**，本项目不对译稿主张独立版权。

译稿仅用于**学习与交流**，**不得用于商业用途**。

## 三、本项目的原创部分

以下内容为本项目原创，采用 **MIT 许可**：

- `pipeline/` — 全部脚本（大纲解析、资料清点、术语挖掘、术语表校验）
- `glossary/` — 术语表（译法选择与禁用变体规则是本项目的整理成果）
- `README.md`、`AAR.md`、`logs/`、`notes/`、`reports/` — 项目文档与过程记录

## 四、免责与撤回承诺

- 本项目为**课程作业**（AI➕X 挑战 C1），非官方翻译，与 Stanford University 无隶属关系。
- 译稿可能存在错误，**不应作为权威参考**；引用请以原始英文资料为准。
- **若任何版权方对本仓库的内容有异议，请通过 Issue 或邮件联系，将立即移除相关内容。**

## 五、如何正确引用

引用本课程的原始内容时，请引用官方来源：

```
CS146S: The Modern Software Developer
Stanford University, Fall 2025
Instructor: Mihail Eric
https://themodernsoftware.dev/
```

引用本仓库的术语表或管线工具时：

```
AI➕X C1 课程资料获取与翻译
https://github.com/Feng11-kyrie/AI-plus-X-C1
```
