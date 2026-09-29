---
title: RAG Decision Center
type: hub
evidence: derived
verified_at: 2026-09-29
---

# RAG Decision Center

这里不提供脱离上下文的“最佳方案”。每个 Decision Record 都把技术选择拆成：**约束 → 备选方案 → 评价指标 → 风险 → 最小实验 → 决策记录**。

## 决策原则

1. 先定义 SLO 和失败成本，再选技术。
2. 不把来源材料中的局部 benchmark 当作默认参数。
3. 可以组合的方案，不强行写成二选一。
4. 每个重大决策必须能被实验推翻。
5. 决策必须记录适用范围和复审条件。

## 决策地图

| 决策 | 核心变量 |
|---|---|
| [[retrieval-strategy]] | sparse / dense / hybrid |
| [[model-size]] | 质量、延迟、成本 |
| [[embedding-dimension]] | 表达能力、存储、延迟 |
| [[index-freshness]] | freshness、一致性、构建成本 |
| [[retrieval-trigger]] | always-retrieve / conditional |
| [[vector-precision]] | FP32 / FP16 / INT8 |
| [[chunking-strategy]] | fixed / structural / semantic |
| [[context-compression]] | 完整上下文 / 压缩 |
| [[platform-vs-custom]] | 平台复用 / 业务定制 |
| [[multi-region]] | 单地域 / 多地域 |
| [[gpu-scheduling]] | 专属 / 共享 / 混合调度 |
| [[model-vs-corpus]] | 模型能力 / 外部知识能力 |

## 标准决策流程

    业务目标 / SLO
          ↓
    确定不可违反的约束
          ↓
    建立 baseline
          ↓
    选择 2–3 个候选方案
          ↓
    在固定 Evaluation Dataset 上评估
          ↓
    比较 quality / latency / cost / reliability
          ↓
    灰度验证
          ↓
    记录决定与复审触发条件

统一评估方法见 [[../evaluation/evaluation]]。

## 来源与证据

- Evidence: Derived
- 本模块将原 `contradictory.md` 的观点汇总重构为工程 Decision Records。
- 原始材料中的数字只作为案例证据，不能自动成为推荐默认值。
