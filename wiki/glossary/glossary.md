---
title: RAG Glossary
type: glossary
evidence: derived
verified_at: 2026-09-29
---

# RAG Glossary

本页给出仓库内常用术语的短定义。详细方法仍以对应专题页为准。

## A–D

**ANN (Approximate Nearest Neighbor)** 近似最近邻检索。在大规模向量集合中以可接受误差换取速度与资源效率。

**BM25** 基于词频、逆文档频率和长度归一化的经典稀疏检索排序方法。

**Chunk** 文档被切分后的最小检索单元。Chunk 边界直接影响召回、上下文完整性与索引规模。见 [[../decisions/chunking-strategy]]。

**Context** 最终提供给生成模型的证据与指令集合。检索结果不等同于最终 context。

**Dense Retrieval** 使用 embedding 向量进行语义相似检索。

## E–H

**Embedding** 将文本/对象映射到向量空间的表示。

**Faithfulness / Groundedness** 回答中的事实陈述是否得到提供上下文支持。见 [[../evaluation/generation-metrics]]。

**Hard Negative** 与 query 很相似、但实际上不应被判为相关的样本。对检索和 reranker 评估非常重要。

**Hit Rate@K** Top-K 中至少包含一个相关结果的查询比例。

**Hybrid Retrieval** 组合 sparse 与 dense 等多路召回，并通过融合或重排得到结果。见 [[../decisions/retrieval-strategy]]。

## I–M

**Index Freshness** 源数据变化到新内容可被检索之间的延迟。见 [[../decisions/index-freshness]]。

**MRR (Mean Reciprocal Rank)** 第一个相关结果排名倒数的平均值，强调首个正确结果出现的位置。

**nDCG** 支持分级相关性的排序指标，对高位错误排序给予更大惩罚。

## P–R

**Precision@K** Top-K 结果中相关结果所占比例。

**RAG (Retrieval-Augmented Generation)** 在生成前从外部知识源获取证据，并将证据用于回答生成的系统模式。

**Recall@K** Top-K 覆盖全部已标注相关文档的比例。

**Reranker** 对初始候选集进行二次排序的模型/算法。

**RPO** Recovery Point Objective，可接受的数据丢失范围。

**RTO** Recovery Time Objective，故障后恢复服务的目标时间。

## S–Z

**Sparse Retrieval** 基于词项/稀疏向量的检索，典型方法包括 BM25。

**Source-reported** 来源材料明确报告，但当前仓库没有完整复现实验的结果。见 [[../benchmarks/benchmark-standard]]。

**TTFT (Time to First Token)** 从请求开始到模型输出首个 token 的时间。

**Vector Database** 面向向量存储、过滤和近似最近邻检索的数据系统。

## 证据状态术语

**Source** 可直接定位到原始来源。

**Synthesis** 重新组织来源，不新增关键事实。

**Derived** 工程推导或建议。

**External** 来自原手册之外的明确来源。

**Unverified** 历史内容尚未完成来源核验。

完整规范见 [来源与证据规范](../../SOURCE_POLICY.md)。

## 来源与证据

- Evidence: Derived
- 指标定义与详细限制以 [[../evaluation/retrieval-metrics]]、[[../evaluation/generation-metrics]] 等专题为准。
