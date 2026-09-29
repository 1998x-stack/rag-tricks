---
title: Production Readiness
type: hub
evidence: external
verified_at: 2026-09-29
---

# RAG Production Readiness

生产化不是“模型能回答”之后再补监控，而是上线前就明确 **SLO、风险、回滚、容量、数据安全与可观测性**。

## 五个上线门禁

| Gate | 必须回答的问题 |
|---|---|
| [[observability]] | 出问题时能否定位到 query → retrieval → rerank → generation？ |
| [[security]] | 非可信输入、检索文档和模型输出是否被当作潜在攻击面？ |
| [[recoverability]] | 模型、索引、数据或区域故障时能否在目标 RTO/RPO 内恢复？ |
| [[capacity-performance]] | 峰值、冷启动、依赖变慢时是否仍满足 SLO？ |
| [[release-readiness-checklist]] | 候选版本是否通过质量、安全、性能和回滚门禁？ |

## Production SLO 不只是一条 latency

建议至少包含：

- Availability / success rate
- P50 / P95 / P99 latency
- Time to first token
- Retrieval empty-result rate
- Index freshness lag
- Groundedness / critical factual error rate
- Citation validity
- Permission-denied correctness
- cost/query
- fallback / degradation rate

具体阈值由业务决定，不从来源材料的局部案例直接复制。

## 生产变更路径

    offline evaluation
          ↓
    security / permission tests
          ↓
    load & failure tests
          ↓
    shadow / canary
          ↓
    progressive rollout
          ↓
    SLO + quality observation
          ↓
    full rollout / rollback

评估体系见 [[../evaluation/evaluation]]，架构权衡见 [[../decisions/decision-center]]。

## 来源与证据

- Evidence: External + Derived
- OpenTelemetry 提供跨 traces/metrics/logs 的语义约定；GenAI 属性包含 retrieval/query/model 等语义，并明确提示内容字段可能含敏感数据。
- OWASP GenAI Security Project 2025 Top 10 明确包含 Prompt Injection、Sensitive Information Disclosure、Vector and Embedding Weaknesses、Unbounded Consumption 等风险。
- NIST AI RMF Generative AI Profile 提供跨 AI 生命周期的风险管理框架。
- 本页的五门禁模型属于仓库工程化整合。
