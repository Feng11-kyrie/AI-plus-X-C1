<!-- source: source/pages/observability-basics.html -->
<!-- week: 9 | chunks: 10 -->

在现代软件架构中，应用不只是变得更大——它们正变得更加**分布式**。微服务、Serverless 函数与容器跨多个环境运行，要搞清楚系统内部发生了什么，就像在暴风雨里追踪一滴雨。

这就是追踪记录（trace）与 Span 的用武之地。这些可观测性工具不是 buzzword——它们是你看懂复杂分布式系统的秘密武器。下面我们来拆解追踪记录与 Span 是什么、为什么重要，以及如何用它们更快地排查故障、构建更可靠的系统。

## 理解追踪记录与 Span：核心概念

**追踪记录（Trace）** 捕捉一个请求在分布式系统中穿行的完整旅程。可以把一条追踪记录理解为一个请求从头到尾的完整故事——从用户点击按钮，到看见结果。

**Span** 是追踪记录的基本组成单位。每个 Span 代表这段旅程中的一个工作单元——比如一次数据库查询、一次 API 调用，或一次函数执行。Span 之间相互嵌套，用以表达操作之间的父子关系。

用最直白的话说，它们的关系是：

- 一条追踪记录包含多个 Span
- 每个 Span 代表一个操作
- Span 带有时序数据与元数据
- Span 可以嵌套，用以表达操作之间的关联

```
Trace
├── Span (API Gateway)
│   ├── Span (Auth Service)
│   └── Span (User Service)
│       └── Span (Database Query)
└── Span (Response Formatting)
```

> 💡
> 如果你好奇追踪记录与 Span 如何与
> 指标、日志和事件
> 配合使用，这篇文章把四者都讲清了。

## 追踪记录与 Span 对 DevOps 从业者的价值

你正在运行一个由几十个微服务构成的复杂系统。突然，用户反馈结账流程变慢了。没有链路追踪，你就得逐个服务去查，白白浪费宝贵时间。

有了追踪记录与 Span，你可以：

1. **瞬间定位瓶颈**：精确看到是哪个服务或函数耗时过长
2. **跨服务边界调试**：跟随请求在服务之间的跳转
3. **理解依赖关系**：可视化你的服务如何连接、如何相互依赖
4. **改善性能**：精准地识别并修复缓慢的操作
5. **缩短平均恢复时间（MTTR）**：问题出现时更快找到根因

## 追踪记录与 Span 的技术实现

下面深入到分布式系统中链路追踪的工作细节。

### 追踪上下文与传播

要让链路追踪跨服务边界生效，每个服务都需要知道自己在处理同一个请求的一部分。这通过**上下文传播**实现——在服务之间传递 trace ID 与 span ID。

当一个请求首次进入你的系统时，它会被分配一个唯一的 trace ID。随着请求在服务之间流转，这个 ID 一路随行（通常以 HTTP 头的形式）。随后每个服务创建自己的 Span，但都挂到同一条追踪记录上。

### Span 的属性与事件

Span 不只是时间戳——它们承载着丰富的数据：

- **名称**：这个 Span 代表什么操作
- **时序**：开始与结束时间
- **状态**：成功、错误等
- **属性**：自定义的键值对（比如 user_id 或 cart_size）
- **事件**：Span 内值得注意的出现事项
- **链接**：与其它 Span 的关联

### 采样策略

对一切请求都做链路追踪会产生海量数据。因此大多数系统采用**采样**——只收集一定比例的追踪记录。聪明的采样策略包括：

- **头部采样**：在请求开始时决定是否采样
- **尾部采样**：在请求完成后决定（更利于捕获错误）
- **优先级采样**：重要操作始终追踪，例行操作按比例采样

> 💡
> 如果你想弄清可观测性、遥测与监控三者的区别，可以看看这篇有用的文章：
> Observability vs Telemetry vs Monitoring
> 。

## 链路追踪落地指南：工具与框架

准备好给你的系统加上链路追踪了吗？你需要这些东西：

### OpenTelemetry：行业标准

[OpenTelemetry](https://opentelemetry.io/) 已成为实现追踪记录与 Span 的首选框架。它提供：

- 覆盖所有主流编程语言的库
- 厂商中立的 API 与 SDK
- 对流行框架的自动埋点
- 一条一致的数据收集与导出路径

### 链路追踪工具箱

有不少工具可以帮你收集、存储并可视化追踪记录：

| 工具 | 类型 | 最适用场景 |
|---|---|---|
| Last9 | 一体化可观测性 | 高性价比、高基数数据的可观测性，定价可预期 |
| Jaeger | 开源链路追踪 | 自托管的追踪可视化 |
| Zipkin | 开源链路追踪 | 简单的分布式追踪 |
| Grafana Tempo | 追踪后端 | 与 Grafana 仪表盘集成 |
| OpenTelemetry Collector | 数据收集管线 | 处理并路由遥测 |

如果你在找一款符合预算的可观测性方案，[Last9](https://last9.io/) 值得一看。它按摄取的事件数计费，让成本保持可预期。此外，我们的平台能在规模上处理高基数数据，并与 OpenTelemetry、Prometheus 集成，把你的指标、日志与追踪记录汇集到一处。

### 在你的代码中实现链路追踪

下面是一个简化示例，展示如何在 Node.js 应用中用 OpenTelemetry 创建 Span：

```
// Initialize the OpenTelemetry SDK (once in your app)
const { NodeTracerProvider } = require('@opentelemetry/sdk-trace-node');
const { SimpleSpanProcessor } = require('@opentelemetry/sdk-trace-base');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const provider = new NodeTracerProvider();
const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4318/v1/traces',
});
provider.addSpanProcessor(new SimpleSpanProcessor(exporter));
provider.register();

// Get a tracer
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('my-service');

// Create spans in your code
async function processOrder(orderId) {
  const span = tracer.startSpan('process-order');

  // Add attributes to the span
  span.setAttribute('order.id', orderId);
  span.setAttribute('customer.type', 'premium');

  try {
    // Do work...

    // Create a child span
    const dbSpan = tracer.startSpan('database-query', {
      parent: span,
    });

    try {
      // Run database query...
      dbSpan.end();
    } catch (error) {
      dbSpan.setStatus({ code: SpanStatusCode.ERROR });
      dbSpan.recordException(error);
      dbSpan.end();
      throw error;
    }

    span.end();
  } catch (error) {
    span.setStatus({ code: SpanStatusCode.ERROR });
    span.recordException(error);
    span.end();
    throw error;
  }
}
```

> 💡
> 想知道 OpenTelemetry 与传统 APM 工具相比如何？这篇文章拆解了关键差异：
> OpenTelemetry vs Traditional APM Tools
> 。

## 进阶链路追踪技巧

基本链路追踪落地之后，下面这些进阶技巧能把你的可观测性提升一个层次。

### 分布式上下文管理

在复杂系统中，你需要管理的上下文不止 trace ID。W3C Trace Context 规范为此提供了标准：

- **traceparent**：包含 trace ID 与父 span ID
- **tracestate**：允许厂商附加自定义上下文数据

使用这些头部能确保你的链路追踪在跨服务、跨厂商时都正常工作。

### 追踪记录、指标与日志之间的关联

可观测性真正的威力来自把不同信号连接起来：

- **示例追踪（Exemplar trace）**：把指标关联到生成它的那条追踪记录
- **日志中的 trace ID**：在日志消息里带上 trace ID，便于交叉引用
- **自定义属性**：在所有遥测类型中使用一致的属性

### 错误处理与异常追踪

异常发生时，Span 可以提供关键上下文：

- 给 Span 标记错误状态
- 记录带调用栈的异常
- 向 Span 添加事件，展示错误的演进过程
- 创建 baggage 项，把错误上下文跨服务边界传递

> 💡
> 想更深入地了解如何领先于问题、提升系统可靠性，可以看看这篇关于主动监控的文章：
> Proactive Monitoring
> 。

## 真实世界的链路追踪模式与反模式

### 有效的链路追踪模式

**有意义的 Span 命名**：采用一致的命名约定，例如 `service_name/operation`
**恰当的粒度**：为重要的操作创建 Span，而不是为每一次函数调用都建
**正确的上下文传播**：确保 trace 上下文流经所有通信通道
**有用的属性**：添加有助于排障的属性，比如用户 ID 或功能开关
**性能意识**：警惕创建过多 Span 带来的开销

### 应当避免的链路追踪反模式

**过度埋点**：创建过多 Span 会导致性能问题
**上下文缺失**：未能传播上下文会让追踪记录在服务边界处断掉
**命名不一致**：使用不同的命名标准会让追踪记录难以解读
**数据过量**：把大体积载荷放进 Span 会压垮你的追踪后端
**忽略第三方服务**：外部调用缺少 Span 会形成盲区

> 💡
> 想了解可观测性在 LLM 的性能与可靠性中扮演的关键角色：
> LLM Observability
> 。

## 追踪记录与 Span 的商业价值：超越技术收益

追踪记录不只是用来排障——它们也能提供业务洞察：

- 端到端跟踪关键用户旅程
- 度量关键业务操作的性能
- 基于追踪数据设定服务等级目标（SLO）
- 用真实用户的语言量化性能问题的代价
- 通过给 Span 添加相关属性来构建业务上下文

当你能展示技术改进如何影响用户体验与业务指标时，你就架起了 DevOps 与业务干系人之间的桥梁。

## 结论

追踪记录与 Span 给了你透视分布式系统的 X 光视力。它们揭示服务之间隐藏的连接、精准定位性能瓶颈，并大幅加快调试速度。

随着系统日益复杂，这种可观测性不是奢侈品——而是必需品。

> 💡
> 如果你想继续聊分布式追踪与可观测性，欢迎加入我们的
> Discord 社区
> ，那里有 DevOps 从业者分享经验与最佳实践！

## 常见问题

### 链路追踪与日志有什么区别？

日志记录离散的事件，而链路追踪展示跨服务的操作之间的关系。日志告诉你发生了什么；追踪记录展示它是如何发生的。

### 加上链路追踪会让我的应用变慢吗？

现代链路追踪库带来的开销极小——配置得当的情况下，性能影响通常低于 3%。配合采样，还能进一步降低这一影响。

### 我需要改掉所有代码才能加上链路追踪吗？

不一定。许多框架提供自动埋点，只需极少的代码改动就能加上链路追踪。OpenTelemetry 为大多数语言的主流框架提供了自动埋点能力。

### 分布式追踪会产生多少数据？

这取决于流量、采样率与 Span 的详细程度，差异很大。对于繁忙的系统，请按每天数 GB 到数 TB 来规划。这也是为什么选对可观测性平台对成本控制至关重要。

### 追踪记录对安全与合规有帮助吗？

有！追踪记录为请求在系统中的流转建立了审计轨迹。配合恰当的属性，你可以追踪哪些用户或服务在什么时间访问了哪些数据。

### 追踪记录与 Span 如何与其它可观测性信号配合？

追踪记录是对指标与日志的补充。指标在较高层面展示系统健康状况，日志提供详细事件，而追踪记录把这些点连起来，展示跨服务的请求流转。
