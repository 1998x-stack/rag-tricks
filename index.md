---
layout: handbook
title: RAG Tricks · RAG 工程知识库
description: 可追溯、可验证、面向生产实践的 RAG 工程知识库
---

# RAG Tricks

> 从“资料整理”升级为“工程决策手册”：学习概念、设计系统、排查问题、理解权衡，并尽可能追溯每个关键结论的来源。

[下载 EPUB 电子书与详细 XMind 导图](./downloads/index.md) · [部署与维护说明](./docs/github-pages.md)

## 你现在想做什么？

| 目标 | 入口 |
|---|---|
| **Learn**：系统学习 RAG | [学习路径](#学习路径) |
| **Build**：设计生产 RAG | [系统架构设计](./wiki/architecture/architecture.md) |
| **Debug**：排查效果/性能问题 | [问题排查入口](#问题排查入口) |
| **Evaluate**：建立评估与回归体系 | [Evaluation Center](./wiki/evaluation/evaluation.md) |
| **Decide**：做技术选型 | [Decision Center](./wiki/decisions/decision-center.md) |
| **Verify**：核验来源和证据 | [来源与证据规范](./SOURCE_POLICY.md) |

---

## 学习路径

推荐按端到端链路学习，而不是按文件数量浏览：

1. [RAG 基础](./wiki/introduction/rag-basics.md)
2. [整体架构](./wiki/architecture/overview.md)
3. [数据处理](./wiki/data-layer/data-layer.md)
4. [索引构建](./wiki/indexing/indexing.md)
5. [检索策略](./wiki/retrieval/retrieval.md)
6. [生成优化](./wiki/generation/generation.md)
7. [Evaluation Center](./wiki/evaluation/evaluation.md)
8. [运维与可靠性](./wiki/ops-and-reliability/ops-and-reliability.md)
9. [成本与效率](./wiki/cost-and-efficiency/cost-and-efficiency.md)
10. [高级专题](./wiki/advanced-topics/advanced-topics.md)

---

## 问题排查入口

先按[分层排障流程](./wiki/evaluation/troubleshooting.md)保留失败样本、定位证据在哪一阶段丢失，再查阅以下专题。

### 召回率低 / 找不到正确内容

优先检查：

- [文本预处理](./wiki/data-layer/text-preprocessing.md)
- [嵌入模型选型](./wiki/indexing/embedding-model-selection.md)
- [向量生成策略](./wiki/indexing/vector-generation-strategy.md)
- [查询理解](./wiki/retrieval/query-understanding.md)
- [混合检索](./wiki/retrieval/hybrid-retrieval.md)
- [检索评估](./wiki/retrieval/retrieval-evaluation.md)

### 回答相关但不可信 / 幻觉高

优先检查：

- [检索结果处理](./wiki/retrieval/result-processing.md)
- [Prompt Engineering](./wiki/generation/prompt-engineering.md)
- [生成质量控制](./wiki/generation/generation-quality.md)
- [生成评估](./wiki/generation/generation-evaluation.md)

### 延迟高 / 成本高

优先检查：

- [索引性能优化](./wiki/indexing/index-performance-optimization.md)
- [生成效率](./wiki/generation/generation-efficiency.md)
- [成本拆解](./wiki/cost-and-efficiency/cost-breakdown.md)
- [成本优化](./wiki/cost-and-efficiency/cost-optimization.md)
- [性能压测](./wiki/ops-and-reliability/performance-testing.md)

### 知识更新后仍检索不到

优先检查：

- [数据收集与清洗](./wiki/data-layer/data-collection-cleaning.md)
- [向量数据库](./wiki/indexing/vector-database.md)
- [自动化运维](./wiki/ops-and-reliability/automated-ops.md)
- [全链路监控](./wiki/ops-and-reliability/full-stack-monitoring.md)

---

## 主题地图

### 基础与架构

| 类别 | 描述 |
|---|---|
| [引言与概述](./wiki/introduction/introduction.md) | 原理、技术边界、业务场景 |
| [系统架构设计](./wiki/architecture/architecture.md) | 数据、索引、检索、生成及端到端设计 |
| [数据处理与准备](./wiki/data-layer/data-layer.md) | 清洗、预处理、增强、标注、安全 |

### 检索与生成

| 类别 | 描述 |
|---|---|
| [索引构建与优化](./wiki/indexing/indexing.md) | Embedding、向量、索引、质量 |
| [检索策略与实现](./wiki/retrieval/retrieval.md) | Query、Sparse/Dense/Hybrid、结果处理 |
| [评估与实验](./wiki/evaluation/evaluation.md) | 指标、实验协议、失败定位 |
| [生成层设计与优化](./wiki/generation/generation.md) | 模型、Prompt、质量、效率 |
| [Evaluation Center](./wiki/evaluation/evaluation.md) | 数据集、指标、端到端评估、回归与线上验证 |

### 生产化

| 类别 | 描述 |
|---|---|
| [业务线落地案例](./wiki/business-cases/business-cases.md) | 案例与场景化实践 |
| [运维与可靠性](./wiki/ops-and-reliability/ops-and-reliability.md) | 监控、响应、压测、复盘 |
| [成本与效率](./wiki/cost-and-efficiency/cost-and-efficiency.md) | 成本模型与优化 |
| [高级专题](./wiki/advanced-topics/advanced-topics.md) | 多模态、Agent、隐私与集成 |

---

## Decision Center

RAG 中很少存在脱离上下文的“唯一最优解”。[Decision Center](./wiki/decisions/decision-center.md) 记录了包括以下问题在内的多组选择：

- 语义检索 vs 关键词检索；
- 大模型 vs 小模型；
- 实时索引 vs 批量构建；
- 固定分块 vs 语义分块；
- 全文上下文 vs 上下文压缩；
- GPU 独占 vs 资源共享。

这些主题已经升级为“约束 → 方案 → 指标 → 风险 → 最小实验 → 复审条件”的 Decision Records；旧 `contradictory.md` 路径继续作为兼容入口。

---

## 来源与证据

历史内容来自《字节跳动 RAG 实践手册》的提取、整理与扩写，但“出现在本仓库”不等价于“已经独立验证”。

涉及精确数字、事故时间、成本、QPS、内部组件名或业务规模的内容，引用前请先检查：

- [来源与证据规范](./SOURCE_POLICY.md)
- [高风险页面核验登记](./sources/source-map.json)

当前历史页面仍处于逐步审计阶段。

---

## 浏览说明

仓库正文大量使用 Obsidian `[[wikilinks]]`。Quartz 构建已加入工程分支，为 Web 端提供 wikilink、backlink、搜索、Explorer 与知识图谱；标准 Markdown 链接仍保留以保证 GitHub 原生浏览兼容。

---

[GitHub 仓库](https://github.com/1998x-stack/rag-tricks) · [贡献指南](./CONTRIBUTING.md) · [来源规范](./SOURCE_POLICY.md)
