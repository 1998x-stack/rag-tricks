---
title: HyDE
type: concept
evidence: external
verified_at: 2026-09-29
---

# HyDE · Hypothetical Document Embeddings

## 核心思想

HyDE 不直接把 query 编成检索向量，而是先让语言模型根据 query 生成一个**假想文档**，再把该假想文档编码成向量，用它去真实语料库中寻找邻近文档。

原论文关注的是**没有 relevance labels 的 zero-shot dense retrieval**。

## 为什么可能有效

短 query 往往只有需求表达，没有目标文档常见的叙述方式。假想文档把 query 扩成更接近目标文档分布的文本，然后 dense encoder 再做匹配。

## 最大风险

假想文档可以包含错误细节。它的用途是**构造检索表示**，不是作为回答事实来源。

因此：

- 不要把 hypothetical document 直接当 evidence；
- 最终答案必须回到真实检索文档；
- 记录生成模型与 prompt 版本；
- 对事实敏感 query 单独分析失败样本。

## 最小实验

比较 direct dense retrieval 与 HyDE：Recall@K、nDCG、hard-negative 错误、额外生成 latency/cost。

如果已有高质量 supervised retriever，HyDE 不一定值得增加额外生成步骤。

## 来源与证据

- Evidence: External
- Gao et al., “Precise Zero-Shot Dense Retrieval without Relevance Labels”, 2022。
- 原论文将 HyDE 定义为：先生成 hypothetical document，再用无监督 dense encoder 编码并检索真实 corpus。
