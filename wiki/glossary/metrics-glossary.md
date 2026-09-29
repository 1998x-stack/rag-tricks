---
title: Metrics Glossary
type: glossary
evidence: synthesis
verified_at: 2026-09-29
---

# Metrics Glossary

| 指标 | 主要回答的问题 | 常见误读 |
|---|---|---|
| Precision@K | 返回结果有多少是相关的？ | 高 Precision 不代表没有漏召回 |
| Recall@K | 相关证据找回了多少？ | 需要相对完整的 relevance 标注 |
| Hit Rate@K | 是否至少命中一个相关结果？ | 无法衡量多证据覆盖 |
| MRR | 第一个相关结果有多靠前？ | 不关心后续相关结果排序 |
| nDCG@K | 分级相关结果排序是否合理？ | relevance grade 质量决定指标质量 |
| Groundedness | 回答是否被上下文支持？ | 不代表上下文本身正确 |
| Completeness | 应答信息是否遗漏？ | 与 groundedness 不是同一维度 |
| Citation precision | 引用是否支持对应 claim？ | 不代表重要 claim 都有引用 |
| Citation coverage | 重要 claim 是否被引用覆盖？ | 不代表引用本身正确 |
| P95 latency | 95% 请求在该时间内完成 | 不能用平均 latency 替代 |
| TTFT | 用户多久看到第一 token？ | 不代表完整响应时间 |
| cost/query | 单请求完整系统成本 | 必须统一 token、infra、cache 等口径 |

## 指标选择原则

不要用单指标定义“RAG 质量”。至少同时看 retrieval、generation、latency、cost；生产场景再增加 reliability 与业务结果。

详细定义见 [[../evaluation/evaluation]]。

## 来源与证据

- Evidence: Synthesis
- 指标定义来自仓库 Evaluation Center 已登记的外部/工程来源。
