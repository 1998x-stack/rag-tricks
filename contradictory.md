# 设计权衡与决策中心

> 本页面保留原 `contradictory.md` 路径作为兼容入口。原先的“观点 A vs 观点 B”已经迁移为结构化 [RAG Decision Center](./wiki/decisions/decision-center.md)。

RAG 工程中很多看似矛盾的观点并不真正互斥，而是适用于不同约束。新的 Decision Record 不再给出脱离上下文的单一答案，而是要求明确 SLO、成本、失败风险和验证实验。

## 12 个核心决策

| 原权衡 | 新 Decision Record |
|---|---|
| 语义检索 vs 关键词检索 | [Sparse / Dense / Hybrid Retrieval](./wiki/decisions/retrieval-strategy.md) |
| 大参数模型 vs 小参数模型 | [Model Size Decision](./wiki/decisions/model-size.md) |
| 768 vs 1024 向量维度 | [Embedding Dimension](./wiki/decisions/embedding-dimension.md) |
| 实时索引 vs 批量构建 | [Index Freshness](./wiki/decisions/index-freshness.md) |
| 无条件 vs 条件触发检索 | [Retrieval Trigger](./wiki/decisions/retrieval-trigger.md) |
| FP32 vs FP16 / INT8 | [Vector Precision](./wiki/decisions/vector-precision.md) |
| 固定长度 vs 动态语义分块 | [Chunking Strategy](./wiki/decisions/chunking-strategy.md) |
| 全文上下文 vs 压缩 | [Context Compression](./wiki/decisions/context-compression.md) |
| 技术中台 vs 业务定制 | [Platform vs Custom](./wiki/decisions/platform-vs-custom.md) |
| 单地域 vs 多地域 | [Multi-region Deployment](./wiki/decisions/multi-region.md) |
| GPU 独占 vs 共享 | [GPU Scheduling](./wiki/decisions/gpu-scheduling.md) |
| 大模型 vs 大语料库 | [Model vs Corpus Investment](./wiki/decisions/model-vs-corpus.md) |

## 决策模板

每个决策建议记录：

    Context
      ↓
    Constraints / SLO
      ↓
    Alternatives
      ↓
    Evaluation metrics
      ↓
    Minimum experiment
      ↓
    Decision
      ↓
    Review trigger

评估方法统一使用 [Evaluation Center](./wiki/evaluation/evaluation.md)。

## 为什么不再保留原来的“结论式分析”

原页面中有不少类似“默认使用 X”“Y 一定更优”“提升 Z%”的写法。这些内容混合了来源材料中的局部案例、整理者总结和工程推导，很容易被误读为通用结论。

新的 Decision Center 将数字放回它们的实验/业务上下文中，并优先回答：

- 什么条件下候选方案会更合适？
- 哪些指标会发生 tradeoff？
- 怎么设计最小实验验证？
- 什么变化会触发重新决策？

## 来源与证据

- Evidence: Derived / Synthesis
- 旧页面中的部分案例数字可在原始材料中定位，但本页面不再复述它们作为通用默认值。
- 各 Decision Record 单独标记来源范围与推导边界。
