---
title: RAG Learning Path
type: guide
evidence: derived
verified_at: 2026-09-29
---

# RAG Learning Path

这条路线面向公开仓库读者，不依赖任何内部产品或工具。目标是从“会解释 RAG”逐步走到“能设计、评估并上线一个 RAG 系统”。

## Stage 0 · 建立系统模型

先理解 RAG 为什么存在，以及数据如何沿链路流动：

1. [[../introduction/rag-basics]]
2. [[../architecture/overview]]
3. [[../introduction/rag-vs-finetuning]]
4. [[../introduction/rag-vs-ir]]

**完成标准**：能够画出 ingestion 与 online query 两条数据流，并解释每层最常见的失败模式。

## Stage 1 · 数据与索引

1. [[../data-layer/data-layer]]
2. [[../data-layer/text-preprocessing]]
3. [[../indexing/embedding-model-selection]]
4. [[../indexing/vector-generation-strategy]]
5. [[../indexing/vector-database]]
6. [[../decisions/chunking-strategy]]
7. [[../decisions/embedding-dimension]]

**实践**：选一小批文档，比较两种 chunking 策略，并记录 index size、Recall@K 与失败样本。

## Stage 2 · 检索与排序

1. [[../retrieval/query-understanding]]
2. [[../retrieval/keyword-retrieval]]
3. [[../retrieval/semantic-retrieval]]
4. [[../retrieval/hybrid-retrieval]]
5. [[../retrieval/result-processing]]
6. [[../decisions/retrieval-strategy]]
7. [[../evaluation/retrieval-metrics]]

**实践**：在同一 query set 上对 sparse / dense / hybrid 做 per-query diff，而不是只看平均分。

## Stage 3 · 生成与证据使用

1. [[../generation/prompt-engineering]]
2. [[../generation/generation-quality]]
3. [[../generation/model-selection]]
4. [[../decisions/context-compression]]
5. [[../evaluation/generation-metrics]]

**实践**：构造 answerable / no-answer 样本，分别测 groundedness、completeness 与错误回答率。

## Stage 4 · Evaluation-first Engineering

1. [[../evaluation/evaluation]]
2. [[../evaluation/evaluation-dataset]]
3. [[../evaluation/end-to-end-evaluation]]
4. [[../evaluation/regression-testing]]
5. [[../benchmarks/benchmark-standard]]

**完成标准**：任何“优化”都能给出 baseline、candidate、dataset version、quality / latency / cost 三维结果。

## Stage 5 · Production

1. [[../production/production-readiness]]
2. [[../production/observability]]
3. [[../production/security]]
4. [[../production/recoverability]]
5. [[../production/capacity-performance]]
6. [[../production/release-readiness-checklist]]

**实践**：为一个候选版本写 release checklist，并模拟 model timeout 或 stale index 的降级/回滚。

## Stage 6 · 设计与高级主题

1. [[../decisions/decision-center]]
2. [[../advanced-topics/multimodal-rag]]
3. [[../advanced-topics/rag-agent]]
4. [[../advanced-topics/system-integration]]
5. [[../cases/case-catalog]]
6. [[../modern-rag/modern-rag]] — 学习原手册之外的方法，但保持来源边界

**完成标准**：面对新业务时，不是复制某个案例配置，而是能明确约束、设计实验并写 Decision Record。

## 学习闭环

    Read
      ↓
    Build a small experiment
      ↓
    Evaluate per-query failures
      ↓
    Write a Decision Record
      ↓
    Add a regression case
      ↓
    Revisit assumptions

术语不清楚时先查 [[../glossary/glossary]]。不同角色的重点路线见 [[role-based-paths]]。

## 来源与证据

- Evidence: Derived
- 本路径基于仓库现有知识结构重新组织，不等同于来源手册中的内部培训计划。
