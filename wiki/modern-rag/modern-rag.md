---
title: Modern RAG
type: hub
evidence: external
verified_at: 2026-09-29
---

# Modern RAG

本模块专门收录**原《字节跳动 RAG 实践手册》之外**的现代 RAG 方法。它与 `source-manual` 内容严格隔离：页面只使用明确登记的外部来源，不把后来方法倒写成原手册内容。

## 方法地图

| 方法 | 主要解决的问题 | 工程提醒 |
|---|---|---|
| [[contextual-retrieval]] | chunk 脱离原文上下文导致检索失败 | 增加索引预处理与生成成本，需要离线回归 |
| [[hyde]] | query 与目标文档语义表达错位 | 适合零样本检索候选，需要防止伪文档细节被误当事实 |
| [[self-rag]] | 何时检索、何时反思和修正 | 更接近 research pattern，不应直接当作生产默认架构 |
| [[graphrag]] | 全局主题、实体关系、整体性问题 | 方法值得研究；Microsoft GraphRAG 开源实现当前主要处于维护模式 |
| [[reranking-late-interaction]] | 初始召回已有候选，但最终排序仍不够好 | Cross-Encoder 与 Late Interaction 都要支付额外计算/索引成本 |

## 按 failure mode 选方法

    检索不到
      ├─ chunk 缺上下文 → Contextual Retrieval
      ├─ query 表达弱 / 零样本 → HyDE
      ├─ 需要动态检索与自检 → Self-RAG pattern
      ├─ 全局主题 / 图关系 → GraphRAG
      └─ 候选已存在但排序差 → Reranking / Late Interaction

不要因为一个方法更新、论文分数高或社区热度高就直接采用。统一通过 [[../evaluation/evaluation]] 与 [[../benchmarks/benchmark-standard]] 在自己的 corpus、query distribution、成本和延迟约束下验证。

## 与原手册内容的边界

- `wiki/modern-rag/`：只收录外部现代方法；
- 原有 `wiki/indexing/`、`wiki/retrieval/` 等页面：保留手册来源与历史整理；
- 需要跨模块比较时，使用 [[../decisions/decision-center]]，不要混写来源。

## 来源与证据

- Evidence: External + Derived
- 外部来源见各专题页面和 `sources/source-map.json`。
- 本页的方法选择树属于仓库工程化整理。
