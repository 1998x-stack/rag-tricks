---
title: GPU Scheduling
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Dedicated vs Shared GPU Capacity

## 决策问题

生成服务应使用业务独占 GPU，还是共享资源池？

## 专属容量

适合严格 latency/availability、流量可预测、故障隔离要求高的核心业务。

## 共享池

适合多业务峰谷互补、预算敏感、允许排队/抢占或弹性调度的工作负载。

## 常见更优方案：分层混合

保留核心业务的 guaranteed capacity，把 burst / batch / 中低优任务放进共享池，通过优先级、限流和抢占实现弹性。

## 验证指标

GPU utilization、queue time、TTFT、P95/P99、preemption count、cost/query、capacity headroom、failover capacity。

## 验证实验

使用真实峰谷流量回放，并注入高优业务突发流量，验证共享资源是否会侵蚀核心 SLO。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 41–42：来源材料明确按业务优先级描述专属 GPU、共享 GPU 与夜间空闲资源，并包含动态扩缩容案例。
- 本页将其归纳为 guaranteed capacity + shared burst 的容量模型。
