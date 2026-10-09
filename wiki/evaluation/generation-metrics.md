---
title: Generation Metrics
type: concept
evidence: external
verified_at: 2026-09-29
---

# Generation Metrics

生成层不能只问“答案像不像参考答案”。RAG 更重要的是：是否基于检索证据、是否回答了问题、是否遗漏关键内容、引用是否真的支持对应陈述。

## Faithfulness / Groundedness

检查回答中的事实陈述是否得到上下文支持。它主要解决模型有没有超出证据自行补充的问题。高 groundedness 不代表回答一定完整，也不代表检索到的上下文本身正确。

## Answer Relevance

检查回答是否直接解决用户 query。常见失败包括事实正确但没有回答问题、输出大量无关背景、把相关主题当成目标问题。

## Completeness

检查应该回答的重要信息是否遗漏。Groundedness 更接近“不要多说无依据内容”，Completeness 更接近“不要漏掉应该说的内容”。两者应分开测。

## Correctness

当有可信 reference answer 时，可以评估关键事实、数值、结论是否与 reference 一致。不要只依赖字符串相似度，同一正确答案可以有很多表达方式。

## Citation Correctness

建议拆成三个维度：

- **Citation precision**：被引用的 source 是否真的支持对应 claim。
- **Citation coverage**：重要 claim 是否都有 source。
- **Citation validity**：链接/文档 ID 是否真实存在、权限是否合法、版本是否对应。

## LLM-as-a-Judge

LLM judge 适合规模化评估主观维度，但必须记录 judge model/version、judge prompt version、temperature、rubric、是否提供 reference、是否提供完整 context，并用人工标注样本做校准。

不要把“模型打分”当成客观真值。

## No-answer / Abstention

至少分开统计 answerable query 的错误拒答率，以及 unanswerable query 的错误回答率。

## 来源与证据

- Evidence: External + Derived
- Microsoft Foundry 的 RAG evaluator 文档将 groundedness、relevance、response completeness 分成不同评估维度。
- Citation precision / coverage / validity 的拆分属于本知识库的工程化评价模型。
