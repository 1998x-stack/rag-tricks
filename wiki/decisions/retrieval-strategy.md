---
title: Retrieval Strategy
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Sparse vs Dense vs Hybrid Retrieval

## 决策问题

一个 query 应优先依赖关键词检索、语义检索，还是融合两者？

## 先看约束

- 查询是否包含精确实体、编号、金额、产品参数？
- 用户是否经常使用同义改写、自然语言描述？
- corpus 是否术语密集？
- 是否允许 reranker 的额外延迟？
- 失败更怕漏召回，还是更怕噪声？

## 候选策略

### Sparse / keyword 更适合

- exact match 很重要；
- 专有名词、编号、政策条款多；
- latency 预算很紧；
- 语料词汇稳定。

### Dense / semantic 更适合

- query 常被改写；
- 用户表达与文档措辞差异大；
- 长文本语义匹配重要；
- 召回语义相近内容比精确词匹配更重要。

### Hybrid 更适合

- 同时存在 exact 与 semantic query；
- 业务无法可靠地在查询前判断类型；
- 可以接受融合/重排成本。

## 不要硬编码默认权重

来源材料给出过 0.6:0.4 等示例权重，但这应视为**实验候选值**，而不是跨业务默认值。

## 验证实验

在同一测试集上至少比较 sparse / dense / hybrid 三组：Recall@K、MRR/nDCG、P95 latency、cost/query，并按 exact / semantic / mixed query 分桶。

## 复审条件

embedding 升级、语料领域变化、查询分布变化、reranker 引入后重新评估。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 27–30：ByteBM25、语义检索、混合检索、动态权重及排序评估。
- OCR 页标 28：来源材料给出关键词 fallback、0.6:0.4 等示例。
- 这些数值不是本 Decision Record 的默认推荐。
