---
title: Chunking Strategy
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Fixed vs Structural vs Semantic Chunking

## 决策问题

文档应该固定 token 切块，按结构切块，还是按语义边界切块？

## Fixed

实现简单、吞吐稳定，适合格式统一、短段落文档和 baseline。

## Structural

利用标题、段落、表格、列表、章节边界，通常比纯 token 截断更容易保留信息结构。

## Semantic

适合结构弱、长段落、主题切换明显的文档，但构建成本与复杂度更高。

## 真正要优化的不是 chunk size

目标是最大化“单个可检索单元包含完整回答证据的概率”，同时控制噪声与上下文重复。

## 验证实验

对每种策略记录 Recall@K、answer evidence coverage、平均 chunk token、index size、duplicate context ratio、end-to-end groundedness。

## 来源与证据

- Evidence: Synthesis + Derived
- 原始材料包含固定分块与动态/语义分块的案例，并报告过飞书 Recall@10 的局部变化。
- 该案例不能证明语义分块在所有 corpus 上都更优。
