---
title: Embedding Dimension
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Embedding Dimension

## 决策问题

向量维度应该多大？

## 不要从“768 vs 1024”开始

先确认模型本身支持哪些输出维度、是否支持 Matryoshka/降维，以及维度变化是否会改变模型训练分布。维度不是独立于 embedding model 的自由旋钮。

## 评价维度

- Recall@K / nDCG；
- index memory；
- disk footprint；
- network bandwidth；
- build time；
- P95 retrieval latency。

## 决策方法

以最低能满足质量门槛的维度为候选，逐步提高维度并绘制 quality-cost 曲线。若质量收益趋于平坦，应优先选择资源开销更低的点。

## 验证实验

同一 embedding checkpoint、同一 corpus snapshot、同一 ANN 配置，只改变输出维度；至少测试 head queries、long-tail、hard negatives。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 20–21：来源材料讨论 768/1024 维与存储、语义区分度之间的权衡。
- 这些具体比例属于来源案例，不是通用维度规律。
