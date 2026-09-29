---
title: Retrieval Trigger
type: decision
evidence: derived
verified_at: 2026-09-29
---

# Always Retrieve vs Conditional Retrieval

## 决策问题

每个请求都触发检索，还是先判断是否需要外部知识？

## Always retrieve 更适合

- 事实性回答必须有证据；
- 知识高度时效；
- citation 是产品要求；
- 检索成本相对低且 latency 可接受。

## Conditional retrieval 更适合

- 大量请求是改写、创意或闲聊；
- retrieval 依赖昂贵；
- 无外部知识也能可靠完成任务；
- 有稳定的 router/intent classifier。

## 主要风险

条件路由最大的风险不是多检索一次，而是**错误地不检索**。因此要单独统计 false-negative routing rate。

## 验证实验

建立 need-retrieval / no-retrieval 标注集，比较 always、rule router、LLM router。指标至少包括 route recall、最终正确率、P95、cost/query。

## 来源与证据

- Evidence: Derived
- 原 `contradictory.md` 将该问题描述为无条件与条件触发的权衡；本页将其改写为可测的路由决策。
- 具体节省比例未作为默认结论保留，需后续单独 source audit。
