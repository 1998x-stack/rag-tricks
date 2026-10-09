---
title: Role-based Learning Paths
type: guide
evidence: derived
verified_at: 2026-09-29
---

# Role-based Learning Paths

不同角色不需要以同样深度学习所有模块。以下路线用于确定“先学什么、做到什么程度”。

## Application / Product Engineer

重点：把 RAG 能力可靠接进产品。

- [[../architecture/overview]]
- [[../retrieval/retrieval]]
- [[../generation/prompt-engineering]]
- [[../evaluation/end-to-end-evaluation]]
- [[../production/release-readiness-checklist]]
- [[../production/security]]

目标：能定义 API contract、fallback、citation、权限和上线指标。

## Retrieval / Search Engineer

重点：数据、索引、query、召回、排序。

- [[../data-layer/text-preprocessing]]
- [[../indexing/indexing]]
- [[../retrieval/query-understanding]]
- [[../retrieval/hybrid-retrieval]]
- [[../evaluation/retrieval-metrics]]
- [[../decisions/retrieval-strategy]]
- [[../decisions/vector-precision]]

目标：能用 per-query evidence 解释为什么检索变好或变差。

## LLM / Generation Engineer

重点：上下文使用、生成质量、模型选择。

- [[../generation/generation]]
- [[../generation/prompt-engineering]]
- [[../generation/generation-quality]]
- [[../evaluation/generation-metrics]]
- [[../decisions/model-size]]
- [[../decisions/context-compression]]

目标：能区分 retrieval failure 与 generation failure。

## Platform / SRE

重点：SLO、容量、可观测性、恢复与成本。

- [[../production/production-readiness]]
- [[../production/observability]]
- [[../production/capacity-performance]]
- [[../production/recoverability]]
- [[../cost-and-efficiency/cost-and-efficiency]]
- [[../ops-and-reliability/incident-response]]

目标：任何请求都可 trace，任何关键依赖都有 timeout/fallback，任何重要版本都可回滚。

## Security / Governance

重点：数据来源、权限、注入、泄露、日志与风险治理。

- [[../data-layer/data-security]]
- [[../production/security]]
- [[../advanced-topics/privacy-security]]
- [[../production/observability]]
- [[../production/release-readiness-checklist]]

目标：把权限与数据边界落实到 ingestion、retrieval、cache、telemetry 和 output，而不是只写 prompt。

## Tech Lead / Architect

重点：跨层 tradeoff、评估契约、平台边界与长期演进。

- [[../decisions/decision-center]]
- [[../evaluation/evaluation]]
- [[../production/production-readiness]]
- [[../benchmarks/benchmark-standard]]
- [[../cases/case-catalog]]
- [[../decisions/platform-vs-custom]]

目标：把“技术偏好”转成带约束、指标和复审条件的工程决策。

## 来源与证据

- Evidence: Derived
- 角色划分用于学习导航，不代表组织岗位定义。
