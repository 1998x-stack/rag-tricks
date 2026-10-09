---
title: Retrieval Metrics
type: concept
evidence: external
verified_at: 2026-09-29
---

# Retrieval Metrics

检索评估回答的是：对一个 query，系统是否找到了应该找到的文档，并把它们排在足够靠前的位置？

## Precision@K

Top-K 中有多少是相关结果：

    Precision@K = relevant_in_top_k / K

适合关注“噪声有多少”的场景。

## Recall@K

Top-K 覆盖了多少已知相关文档：

    Recall@K = relevant_in_top_k / all_relevant_documents

适合关注“有没有漏掉关键证据”。如果无法标出所有相关文档，Recall 的解释会变弱。

## Hit Rate@K

只问 Top-K 中是否至少出现一个相关结果。对于单事实 FAQ 很直观，但无法区分“只找到一个”与“覆盖全部关键证据”。

## MRR

Mean Reciprocal Rank 关注第一个相关结果出现得有多早：

    RR = 1 / rank_of_first_relevant_result
    MRR = mean(RR)

适合“第一条正确结果非常重要”的场景。

## nDCG@K

nDCG 适合 graded relevance：强相关应比弱相关排得更前，且高位排序错误受到更明显惩罚，最后与理想排序归一化比较。

## 指标怎么选

| 场景 | 优先指标 |
|---|---|
| 单一 FAQ | Hit Rate@K, MRR |
| 多证据回答 | Recall@K |
| 噪声敏感 | Precision@K |
| 有分级相关性 | nDCG@K |
| Reranker | MRR, nDCG@K |

不要用一个指标覆盖全部问题。

## Per-query 分析

平均 Recall 从 0.82 到 0.85，可能是所有 query 都略微变好，也可能是一批 query 巨幅提升而另一批退化。因此回归结果必须保留 per-query diff。

## 与生成层的关系

检索好并不保证答案好；检索差则通常意味着生成层没有足够证据。检索评估与答案评估不能相互替代。

## 来源与证据

- Evidence: External
- Microsoft Azure Architecture Center 将 Precision@K、Recall@K、MRR 作为 RAG 检索阶段的标准评估方法。
- Microsoft Research 的信息检索资料给出了 Precision、Recall、MRR、MAP 与 nDCG 的经典定义。
