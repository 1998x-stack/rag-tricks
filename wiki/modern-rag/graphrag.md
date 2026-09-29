---
title: GraphRAG
type: concept
evidence: external
verified_at: 2026-09-29
---

# GraphRAG

## 核心思想

GraphRAG 类方法从非结构化文本中抽取实体、关系和高层结构，用图及其派生摘要为问答构造更有针对性的 context。它尤其适合普通 Top-k chunk retrieval 难以回答的**全局主题、跨实体关系、整体性问题**。

## 不是什么

- 不是“把向量数据库替换成图数据库”这么简单；
- 不是所有 query 都需要图；
- 图构建质量、实体消歧、社区/摘要策略本身会成为新的错误源。

## 成本结构

需要额外考虑：

- entity/relation extraction；
- graph build/update；
- community/summary artifacts；
- incremental freshness；
- graph query + text evidence 的联合追溯。

## 当前实现状态提醒

截至 2026-09-29，Microsoft `microsoft/graphrag` README 明确说明该开源项目**largely in maintenance mode**，主要做 bug fix、依赖更新和 CVE 处理，不再接收新功能 PR。

这不意味着 GraphRAG 方法失效；它意味着评估“GraphRAG 方法论”和选择“Microsoft GraphRAG 具体实现”是两个不同决策。

## 最小实验

挑选真正需要 global reasoning 的 query，与传统 hybrid RAG 比较：answer correctness、evidence coverage、construction cost、index freshness、query latency。不要只用普通 factoid QA 得出结论。

## 来源与证据

- Evidence: External
- Microsoft GraphRAG GitHub README，状态核验日期 2026-09-29。
- Microsoft 将项目描述为利用图形成 targeted context 的研究项目，并在 README 标明当前主要处于 maintenance mode。
