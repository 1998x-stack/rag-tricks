---
title: Model vs Corpus Investment
type: decision
evidence: derived
verified_at: 2026-09-29
---

# Invest in the Model or the Retrieval Corpus?

## 决策问题

下一笔工程预算应该投入模型能力，还是投入知识库、检索和数据质量？

## 先做错误归因

### 更像 corpus / retrieval 问题

- 正确事实根本不在知识库；
- 文档过期；
- relevant document 没召回；
- 权限过滤错；
- chunk 丢失关键上下文。

### 更像 model / generation 问题

- 正确证据已经在 context，但模型没使用；
- 多证据综合失败；
- 格式/推理/指令遵循失败；
- 同样 context 下更强模型显著改善。

## 决策方法

不要用模型升级掩盖数据问题，也不要假设更大 corpus 能解决生成推理缺陷。先在 [[../evaluation/evaluation]] 中做 failure attribution。

## 最小实验

构造四象限：baseline model + baseline retrieval、strong model + baseline retrieval、baseline model + improved retrieval、strong model + improved retrieval。比较边际收益和成本。

## 来源与证据

- Evidence: Derived
- 原始材料分别包含小模型客服、大模型金融、超大向量库等案例，但“模型 vs 语料库”本质是本知识库基于这些案例抽象出的投资决策框架。
- 因此本页不宣称存在统一的公司级二选一规则。
