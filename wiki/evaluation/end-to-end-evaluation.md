---
title: End-to-End Evaluation
type: playbook
evidence: derived
verified_at: 2026-09-29
---

# End-to-End Evaluation

局部最优不等于系统最优。

例如：

    Top-k ↑
      → Recall ↑
      → context tokens ↑
      → latency / cost ↑
      → noise ↑
      → answer quality 可能下降

因此每次核心改动都需要端到端评估。

## 四个维度

### Quality

- retrieval Recall / Precision / nDCG
- groundedness
- correctness
- completeness
- citation correctness
- task success

### Latency

记录 retrieval latency、reranker latency、time to first token、generation latency、total P50/P95/P99。不要只记录平均值。

### Cost

至少统一到 cost/query：embedding、retrieval infra、reranking、input token、output token、cache/storage 全部纳入口径。

### Reliability

- timeout rate
- dependency error rate
- fallback rate
- empty retrieval rate
- malformed citation rate
- index freshness violations

## 实验记录

每次实验都应固定 baseline、candidate、dataset version、corpus snapshot 和所有组件版本，并记录变更项与结果。

示例：

    experiment_id: exp-2026-09-29-001
    baseline: v12
    candidate: v13
    dataset: golden-v7
    corpus_snapshot: kb-2026-09-28
    changes:
      chunk_size: 512 -> 384
      top_k: 8 -> 12
    quality:
      recall_at_10: ...
      groundedness: ...
    performance:
      p95_ms: ...
      cost_per_query: ...

## Pareto frontier

RAG 优化通常不是寻找唯一最高分，而是在质量、延迟和成本之间寻找 Pareto-optimal 配置。更实用的问题是：在质量不低于门槛时，哪组配置 latency / cost 更低？

## 分层归因

    Answer wrong
     ├─ relevant document absent → retrieval
     ├─ document present but ranked too low → ranking
     ├─ evidence present but omitted → context/generation
     ├─ unsupported claim → grounding
     └─ correct answer but slow → performance

## 来源与证据

- Evidence: Derived
- 本页将检索、生成、成本、延迟和可靠性统一为端到端实验框架。
