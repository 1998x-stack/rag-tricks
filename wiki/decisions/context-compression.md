---
title: Context Compression
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Full Context vs Context Compression

## 决策问题

检索结果直接全部进入 LLM，还是先过滤/压缩？

## 保留更多原文更适合

- 精确数据/法律条款不能丢；
- context 尚未接近窗口与成本上限；
- 引用需要原文证据；
- 压缩模型本身可能引入失真。

## 压缩更适合

- Top-k 文本高度冗余；
- 文档很长；
- token 成本或 TTFT 是主要瓶颈；
- 能对信息损失做自动回归。

## 优先级

通常先做去重、rerank、句段级抽取，再考虑生成式摘要压缩。越靠后的方法越可能改变事实表达。

## 验证实验

测 evidence retention、groundedness、citation coverage、input tokens、TTFT、total latency、cost/query。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 37：来源材料描述长文本压缩案例，并报告提示长度/推理效率的局部效果。
- 本页不把来源案例的百分比作为通用收益。
