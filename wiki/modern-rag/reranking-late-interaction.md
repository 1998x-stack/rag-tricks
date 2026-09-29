---
title: Reranking and Late Interaction
type: concept
evidence: external
verified_at: 2026-09-29
---

# Reranking and Late Interaction

初始 retriever 的任务是高效地产生候选集；最终排序可以使用更昂贵、更细粒度的模型。

## Cross-Encoder Reranking

Cross-Encoder 同时输入 query-document pair，并直接输出相关性分数。SentenceTransformers 文档指出，这类模型通常比 bi-encoder 匹配效果更强，但因为要对每个 pair 计算，因此更慢，常用于 rerank Top-k 候选。

适合：候选集已经能覆盖正确文档，但排序不稳定。

## Late Interaction / ColBERT-style

Late Interaction 为 query 和 document 保留 token-level 多向量表示，再通过 MaxSim 等操作进行细粒度匹配。ColBERT 的核心优势是文档表示可以预计算，同时比 single-vector 表示保留更多 token 级匹配信息。

SentenceTransformers v6 已加入 `MultiVectorEncoder`，直接支持 ColBERT-style / late-interaction 模型及训练、评估。

## 如何选择

### Cross-Encoder

- 最终候选数较小；
- 追求高精度排序；
- 可以接受逐 pair 计算。

### Late Interaction

- 希望比 single-vector retrieval 保留更细粒度匹配；
- 可以承担更大的 index footprint 与更复杂检索执行；
- 需要从大 corpus 直接进行 multi-vector retrieval。

## 最小实验

统一候选集与 query set，比 baseline retriever、retriever+cross-encoder、late-interaction：nDCG/MRR/Recall、P95 latency、index size、GPU/CPU cost。

## 来源与证据

- Evidence: External
- SentenceTransformers CrossEncoder usage / Retrieve & Re-Rank 文档。
- SentenceTransformers v6 MultiVectorEncoder 文档。
- Khattab & Zaharia, “ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT”, 2020。
