---
title: RAG Observability
type: playbook
evidence: external
verified_at: 2026-09-29
---

# RAG Observability

RAG 的 trace 需要跨越多个阶段；只记录 API 总耗时，无法判断问题来自检索、重排还是生成。

## 推荐 trace 结构

    request
      ├─ auth / policy
      ├─ query_understanding
      ├─ retrieval
      │   ├─ sparse
      │   ├─ dense
      │   └─ fusion
      ├─ rerank
      ├─ context_build
      ├─ generation
      ├─ citation_validation
      └─ response

## 每个请求建议关联

- trace_id / request_id
- tenant / permission class（避免直接记录敏感身份）
- corpus/index version
- embedding/reranker/model version
- prompt version
- retrieval Top-k 与返回数量
- token usage
- cache hit/miss
- latency breakdown
- fallback/degradation path

## Metrics

### Retrieval

- retrieval P50/P95/P99
- empty result rate
- candidate count
- rerank latency
- index freshness lag
- index/build failure rate

### Generation

- TTFT
- tokens/sec
- input/output tokens
- model error / timeout
- fallback rate
- cost/query

### Quality signals

- groundedness sample score
- citation validation failure
- no-answer rate
- re-query / regenerate rate
- human escalation

## 日志与隐私

不要默认把完整 prompt、system instruction、retrieved documents 和 model output 全量写入 telemetry。OpenTelemetry 的 GenAI 属性文档明确提示 input/output/retrieval query 等字段可能包含用户或 PII 数据。

建议：

- content telemetry 默认 opt-in；
- redact / hash 敏感字段；
- 为 debug sampling 设置短 TTL；
- 区分 metadata telemetry 与 content telemetry；
- 对日志访问做独立审计。

## Alert 应可行动

例如 `P95 latency high` 还不够。更可行动的告警应能区分 retrieval slow、model TTFT slow、index stale、dependency error、permission rejection spike。

## 来源与证据

- Evidence: External + Derived
- OpenTelemetry Semantic Conventions 1.44.0 提供统一 telemetry 命名思想。
- OpenTelemetry GenAI 属性包含 `gen_ai.operation.name`、retrieval documents/query 等语义，并对潜在敏感内容给出警告。
- trace 分层与 RAG 专用指标集合为本知识库的工程化建议。
