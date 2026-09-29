---
title: Evaluation Dataset
type: playbook
evidence: derived
verified_at: 2026-09-29
---

# Evaluation Dataset

评估体系的上限由测试集决定。没有稳定测试集，任何“提升 5%”都很难复现。

## 一个样本至少需要什么

建议记录 query、expected answer、相关文档、相关性标签、是否可回答、类别、难度、时效性和权限上下文。

示例：

    id: query-001
    query: 如何申请差旅费报销？
    expected_answer: ...
    relevant_documents:
      - doc-policy-travel
    relevance_labels:
      doc-policy-travel: 3
      doc-policy-finance: 1
    answerable: true
    category: policy
    difficulty: medium
    freshness_sensitive: true
    permissions:
      role: employee

其中 expected answer 不是所有指标都必需，但 query 与 ground-truth relevance 对严谨检索评估非常重要。

## Query taxonomy

| 类型 | 目的 |
|---|---|
| Exact fact | 基础事实检索 |
| Paraphrase | 测试语义泛化 |
| Multi-hop | 测试多文档整合 |
| Ambiguous | 测试澄清与路由 |
| No-answer | 测试拒答 |
| Temporal | 测试 freshness |
| Long-tail | 测试低频知识 |
| Hard negative | 测试近似但错误内容 |
| Permission-sensitive | 测试 ACL |
| Multilingual | 测试语言能力 |

## Golden / Challenge / Shadow

- **Golden set**：稳定、人工高质量标注，用于每次回归。
- **Challenge set**：专门收集线上失败、边界情况和高难样本。
- **Shadow set**：暂不用于调参，只用于检测过拟合。

不要长期对同一组公开结果反复调参，否则评估集会逐渐变成训练集。

## 标注原则

文档相关性可以使用二分类，也可以使用 0–3 分级标签。使用 nDCG 等 graded metric 时，分级标签比简单 relevant / irrelevant 更有表达力。

答案标注建议同时记录：必须包含的事实、不允许出现的事实、可接受表达差异、必须引用的证据，以及是否允许拒答。

## 从线上失败补充数据

    线上失败
      ↓
    归因
      ↓
    最小复现样本
      ↓
    加入 challenge set
      ↓
    修复
      ↓
    回归门禁

## 数据集版本

每次正式评估记录 dataset version、corpus snapshot、embedding version、index version、reranker version、generator version、prompt version。否则跨时间比较没有意义。

## 常见误区

- 测试集全是简单 FAQ；
- 只标 expected answer，不标 relevant documents；
- 混合不同知识库版本；
- 修改测试集后继续与旧分数直接比较；
- 没有 no-answer / permission / stale-data 样本；
- 只保留平均分，不保存 per-query 结果。

## 来源与证据

- Evidence: Derived
- 本页是面向可复现工程评估的数据契约设计。
- 经典检索指标依赖 ground-truth relevance，因此测试集必须明确 query 与相关文档的关系。
