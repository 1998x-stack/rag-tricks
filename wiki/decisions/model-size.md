---
title: Model Size Decision
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Larger vs Smaller Generation Model

## 决策问题

生成层应该使用更大模型，还是更小、更便宜的模型？

## 关键约束

- 最低可接受 groundedness / correctness；
- P95 latency SLO；
- 峰值 QPS；
- cost/query 预算；
- 上下文长度与任务复杂度；
- 是否允许模型路由。

## 候选方案

### 更小模型

适合高并发、短答案、结构稳定、检索证据强、成本敏感的请求。

### 更大模型

适合复杂推理、多文档综合、长上下文、领域语言复杂且错误成本高的请求。

### 路由而不是一刀切

常见更优架构是按任务难度/风险做 model routing：简单请求走小模型，复杂或低置信度请求升级到更强模型。

## 验证实验

固定 retrieval/context，只替换 generator，比较 groundedness、correctness、task success、P95、tokens/query、cost/query，并单独分析复杂 query。

## 风险

- 大模型未必能弥补错误检索；
- 小模型可能在长上下文中漏证据；
- 量化收益必须与任务质量一起测。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 32–34：来源材料按业务需求、模型能力、资源成本进行模型选型，并列出 1.8B/7B/13B 场景示例。
- OCR 页标 41–42：推理并行、动态批处理与资源调度。
- OCR 页标 52：金融案例使用领域模型的材料描述。
