---
title: Vector Precision
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# FP32 vs FP16 vs INT8 Vectors

## 决策问题

向量存储/计算精度应该保留 FP32，还是压缩到 FP16/INT8？

## 关键约束

- ANN backend 是否原生支持对应精度；
- corpus 规模与内存预算；
- hard-negative 区分难度；
- Recall@K 容忍度；
- 重建/量化校准成本。

## 决策方法

不要从存储节省比例直接做决定。先以 FP32/模型原始精度建立质量 baseline，再测试压缩方案对 Recall@K、nDCG 和 tail queries 的影响。

## 风险

- 平均 Recall 几乎不变，但 hard negatives 退化；
- 不同 ANN 实现的量化方式不可互换；
- embedding 模型升级后旧校准数据失效。

## 验证实验

固定 embedding、index topology、query set，只改变 vector precision/quantization，记录 memory、build time、P95 与 per-query regression。

## 来源与证据

- Evidence: Synthesis + Derived
- 原始材料在向量精度和成本章节讨论 FP16/INT8 压缩及质量损失案例。
- 具体损失百分比依赖材料中的实验条件，不作为跨系统保证。
