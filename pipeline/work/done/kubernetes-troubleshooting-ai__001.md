### Kubernetes 排障之困

Kubernetes 自动化了大量工作，但它动态且短暂易逝的特性，给 [DevOps](https://resolve.ai/glossary/what-is-the-future-of-devops) 与 SRE 团队带来了新的挑战。以下是我们见到的最常见场景：

**1. 谎报军情的吵闹告警**

Kubernetes 的控制平面不停地把工作负载调整到期望状态。像 Pod 重启这样的小插曲，往往会触发在你来得及反应之前就已自愈的告警。结果就是告警疲劳。而在这片噪声之下，配置错误的自动扩缩器、隐藏的瓶颈等真问题无人察觉，直到滚雪球般演变成线上故障。

**2. 短暂的 Pod，丢失的上下文**

Pod 崩溃时，会把宝贵的排查上下文一并带走。事后对 [Pod 执行 `kubectl describe` 往往看不出什么](https://resolve.ai/glossary/how-to-debug-kubernetes-pod-pending-state)。来不及挂上调试器，Kubernetes 资源与状态早已重置。等你开始排查时，关键线索已经消失了。这就像在证据被清扫干净之后才赶到案发现场。

**3. 可观测性数据的迷宫**

日志散落在各个节点、Pod 与容器之间，让[调试](https://resolve.ai/glossary/what-is-debugging)变成一件令人沮丧的苦差。Kubernetes 产生海量指标与遥测，但对某一条具体告警而言，其中只有极小一部分是相关的。翻遍无穷无尽的仪表盘、在命令行里反复执行 kubectl 命令、跨命名空间比对 CPU 与内存用量以找出相关数据——这些都在浪费时间、拖延处置，让团队被噪声淹没，而不是专注于解决方案。
