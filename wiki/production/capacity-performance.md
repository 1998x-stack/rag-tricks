---
title: Capacity and Performance
type: playbook
evidence: derived
verified_at: 2026-09-29
---

# Capacity and Performance

平均 latency 无法描述生产容量。RAG 链路包含检索、重排和 token 生成，尾延迟会随着并发和上下文长度快速放大。

## 容量模型至少包含

- steady QPS
- burst QPS
- concurrent requests
- query/input token distribution
- retrieved context token distribution
- output token distribution
- cache hit rate
- vector DB candidate count
- reranker batch size
- model batch/concurrency
- dependency quotas

## 压测场景

### Baseline

正常流量与正常依赖。

### Burst

短时间放大流量，观察 queue、TTFT、fallback 和 autoscaling。

### Cache cold

模拟部署/故障后的缓存冷启动。

### Long-context

使用高分位上下文长度，避免只测短 query。

### Dependency degradation

向量库、reranker、模型 API 人为增加延迟/错误率。

### Index rebuild

在索引更新/compaction 同时压测查询，观察资源争用。

## 指标

至少保存 P50/P95/P99，而不是只保存平均值；同时记录 queue time、retrieval、rerank、TTFT、generation、total latency 和 cost/query。

## Capacity headroom

生产容量不能把稳态跑到理论极限。headroom 应根据 autoscaling 启动时间、故障时剩余副本、provider quota 和峰值不可预测性确定。

## 与 Evaluation 的连接

性能优化必须通过 [[../evaluation/end-to-end-evaluation]] 验证质量没有同时退化。

## 来源与证据

- Evidence: Derived
- 本页整合传统容量工程与仓库现有性能压测内容。
- 具体 QPS/latency 门槛必须由业务 SLO 与真实 workload 确定。
