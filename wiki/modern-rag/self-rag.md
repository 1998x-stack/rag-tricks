---
title: Self-RAG
type: concept
evidence: external
verified_at: 2026-09-29
---

# Self-RAG

## 核心思想

Self-RAG 研究的是：模型不应对每个请求无条件检索固定数量文档，而应能**按需检索，并对检索内容和自身生成进行反思/批评**。

原论文通过训练模型生成特殊 reflection tokens，让模型在推理过程中控制是否检索、评价证据以及评价自己的输出。

## 与普通 conditional retrieval 的区别

普通 production router 可以是规则、分类器或 LLM；Self-RAG 则是一个训练范式，把 retrieval 与 self-reflection 行为融入模型。

因此不要把“用了 LLM 判断要不要检索”直接称为 Self-RAG。

## 适合研究的问题

- 有些 query 根本不需要外部知识；
- 检索到的 passage 可能不相关；
- 生成过程中需要对 evidence/usefulness 做显式控制。

## 工程风险

- 训练与推理协议更复杂；
- reflection token 行为依赖具体训练数据和模型；
- 与普通 router + reranker + judge 的系统方案相比，需要单独证明收益。

## 最小实验

至少比较 always-retrieve、conditional router、Self-RAG-style candidate，并统一测 correctness、groundedness、retrieval rate、latency 与 cost/query。

## 来源与证据

- Evidence: External
- Asai et al., “Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection”, 2023。
- 原论文描述按需检索和 reflection tokens 驱动的自我反思机制。
