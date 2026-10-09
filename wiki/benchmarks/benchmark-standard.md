---
title: Benchmark Standard
type: guide
evidence: derived
verified_at: 2026-09-29
---

# Benchmark Standard

一个数字只有在测量上下文可解释时才是 benchmark。否则它最多是**某个来源里的案例结果**。

## Benchmark 最小上下文

### Dataset

- dataset / query set version
- query count
- query taxonomy
- ground-truth 标注方式
- corpus snapshot / size

### Retrieval / Generation configuration

- chunking strategy/version
- embedding model/version
- vector/index type + parameters
- Top-k / reranker
- generator model/version
- prompt version

### Runtime

- hardware / provider（若相关）
- concurrency / QPS
- cache state
- region
- measurement window

### Metrics

- metric definition
- aggregation method
- confidence interval / sample count（可得时）
- P50/P95/P99 而不仅是平均 latency
- cost 口径和币种/计费周期

## Benchmark Record 模板

    Benchmark:
    Scope:
    Dataset:
    Corpus snapshot:
    Candidate:
    Baseline:
    Metric:
    Result:
    Runtime:
    Cost basis:
    Source:
    Limitations:
    Reproduction status:

## 三种数字状态

### Reproduced

仓库拥有足够配置和数据，可复现结果。

### Source-reported

来源材料明确报告，但仓库没有完整复现实验。

### Illustrative

用于解释概念的示例，不应作为效果声明。

历史页面中的绝大多数精确业务数字当前属于 **Source-reported**，不是 Reproduced。

## 禁止外推

以下情况不能直接比较：不同 corpus、不同 query distribution、不同模型、不同 Top-k、不同硬件、不同缓存状态、不同 latency 统计口径。

## 与 Evaluation Center 的关系

新的仓库实验应使用 [[../evaluation/evaluation-dataset]] 与 [[../evaluation/end-to-end-evaluation]] 建立可重现记录。

## 来源与证据

- Evidence: Derived
- 本规范是为了阻止来源案例数字被误写为跨系统通用 benchmark。
