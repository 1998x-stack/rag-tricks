---
title: Contextual Retrieval
type: concept
evidence: external
verified_at: 2026-09-29
---

# Contextual Retrieval

## 核心问题

传统 chunking 会让一个片段离开原文后失去章节、实体或时间背景，导致 embedding/BM25 难以把它和 query 对齐。

Anthropic 在 2024 年提出的 Contextual Retrieval 用两类方法缓解这个问题：**Contextual Embeddings** 与 **Contextual BM25**。核心思想是在索引前为 chunk 补充一小段与整篇文档相关的上下文，再做 embedding 与 lexical indexing。

## 适合什么时候

- chunk 本身语义不完整；
- 文档内有大量代词、局部实体、章节继承上下文；
- BM25 与 dense retrieval 都经常因为背景缺失而漏召回。

## 成本与风险

- 每个 chunk 增加额外预处理；
- contextualization prompt/model 变化会改变 index artifact；
- 上下文生成错误会把噪声永久写入索引；
- corpus 更新后需要明确哪些 chunk 重新 contextualize。

## 最小实验

用同一 corpus/query set 比较：

1. 原始 chunk + dense；
2. 原始 chunk + BM25；
3. contextualized chunk + dense；
4. contextualized chunk + BM25；
5. 两路融合。

指标至少记录 Recall@K、MRR/nDCG、index build cost、index size、query latency 与 end-to-end groundedness。

## 重要边界

Contextual Retrieval 是**检索预处理方法**，不是“让模型自动知道全文”。生成层仍然只看到最终构造的 context。

## 来源与证据

- Evidence: External
- Anthropic Engineering, “Introducing Contextual Retrieval”, 2024-09-19。
- 来源明确提出 Contextual Embeddings 与 Contextual BM25，用于减少 chunk 脱离上下文造成的检索失败。
