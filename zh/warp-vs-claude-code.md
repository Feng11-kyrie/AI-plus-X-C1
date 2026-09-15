<!-- source: source/pages/warp-vs-claude-code.html -->
<!-- week: 5 | translated: 2026-09-15T15:27:41+0800 | chunks: 4 -->

Warp 是一个**智能体化的开发环境**，把现代终端与强大的智能体结合起来，帮助你构建、测试、部署和调试代码。Warp 的 AI 由 **Oz** 驱动——这是面向云端智能体的编排平台。

![Warp，智能体化的开发环境：Warp 终端（为与智能体协同编码而打造的现代终端）与 Oz（面向云端智能体的编排平台）](https://docs.warp.dev/~gitbook/image?url=https%3A%2F%2F4009768362-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252FPsjNxoJ0NFCXW6rRdHH3%252Fuploads%252Fgit-blob-6224a456c2508188d8d7035e3f03d6d8f6cd732a%252Fwarp-oz-welcome.png%3Falt%3Dmedia&width=768&dpr=3&quality=100&sign=59ed190c&sv=2)Warp 把现代终端与 Oz——面向云端智能体的编排平台——合二为一

## Warp

Warp 就是你工作的地方——一个快速的现代终端，为与智能体协同编码而打造。

**核心能力：**

-

   [**智能体模式**](https://docs.warp.dev/agent-platform/local-agents/interacting-with-agents/agent-modality)：在用于执行命令的纯净终端与用于多轮智能体工作流的专用对话视图之间切换。

-

   [**现代终端体验**](/terminal/editor)：光标移动、基于块的导航、多行编辑、语法高亮和丰富的补全。使用 Rust 构建，性能出色。

-

   [**代码编辑器**](/code/overview)：文件树、支持 LSP 的代码编辑器，以及可交互的代码评审体验。

-

   [**编码智能体集成**](https://docs.warp.dev/agent-platform/local-agents/third-party-cli-agents)：语音输入、用 @ 选择终端图片等功能。兼容 Oz，或 Claude Code、Codex 等智能体。

深入探索 Warp 的核心功能

## Oz：面向云端智能体的编排平台

Oz 是面向云端智能体的编排平台，为 Warp 的全部智能能力提供支撑。Oz 的设计目标是规模化的智能体编排——理解你的代码库、自主执行任务、并适配你的工作流。Oz 从设计上就支持多模型，让你可以为每个任务灵活选择最合适的 LLM。

Oz 有两种运行模式：

### 本地智能体

直接在 Warp 应用内运行，提供实时、可交互的编码辅助。

-

   跨代码库编写与重构代码

-

   调试问题并修复错误

-

   运行命令并解读结果

-

   规划并执行多步骤任务

本地智能体让你始终掌握控制权。你可以检查改动、在任务进行中调整智能体方向、并在动作执行前予以批准。

→ [开始使用本地智能体](https://docs.warp.dev/agent-platform/local-agents/overview)

### 云端智能体

Oz 云端智能体在 Warp 的基础设施（或你自己的基础设施）上后台运行，用于规模化自动化。

-

   **触发器**：响应来自 Slack、Linear、GitHub 或自定义 Webhook 的事件

-

   **定时计划**：运行依赖更新、死代码清理等周期性任务

-

   **并行能力**：跨仓库或跨任务并发运行大量智能体

-

   **可观测性**：每一次运行都被追踪、可审计，并可分享给团队

云端智能体适合那些无需你即时关注的工作，例如 PR 评审、Issue 分级处置、例行维护，以及由集成驱动的工作流。

→ [了解云端智能体](https://docs.warp.dev/agent-platform/cloud-agents/overview)

## 二者如何协同

Warp 与 Oz 在本地与云端开发之间提供统一体验：

-

   **同一个智能体，随处可用**：无论你是在 Warp 中交互式工作，还是在云端运行智能体，用的都是同一套底层智能体能力。

-

   **无缝交接**：在云端启动任务，需要亲自动手时再在本地 Warp 中接手，进度与上下文都不会丢失。

-

   **共享上下文**：[Warp Drive](/knowledge-and-collaboration/warp-drive)、[Rules](https://docs.warp.dev/agent-platform/capabilities/rules) 与 [MCP 服务器](https://docs.warp.dev/agent-platform/capabilities/mcp) 在本地与云端智能体上都可用，因此团队的知识与工具始终触手可及。

-

   **团队协作**：分享智能体会话、检查智能体的动作、调整正在运行的任务，无论任务是谁发起的。

## 多模型支持

Oz 从设计上就支持多模型。你可以从一组精选的顶级模型中[选择偏好的 LLM](https://docs.warp.dev/agent-platform/capabilities/model-choice)。

## 隐私与安全

Warp 符合 **SOC 2** 标准，并与所有签约的 LLM 供应商执行**零数据留存**政策。客户的 AI 数据不会被留存、存储或用于训练。

Warp 的 AI 功能可在 **Settings** > **AI** 中全局关闭。

→ [进一步了解数据隐私](https://www.warp.dev/privacy)

## 后续步骤

-

   [**快速入门指南**](/getting-started/readme-1)：安装 Warp 并开始编码

-

   [**本地智能体概览**](https://docs.warp.dev/agent-platform/local-agents/overview)：探索 Warp 中可用的全部 AI 功能

-

   [**云端智能体概览**](https://docs.warp.dev/agent-platform/cloud-agents/overview)：配置后台自动化

-

   [**Oz 平台**](https://docs.warp.dev/agent-platform/cloud-agents/platform)：了解 CLI、API、SDK 与基础设施
