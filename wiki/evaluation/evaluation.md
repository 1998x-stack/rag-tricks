---
title: RAG Evaluation Center
type: hub
evidence: external
verified_at: 2026-09-29
---

# RAG Evaluation Center

RAG 评估的核心不是得到一个“总分”，而是回答三个问题：

1. **哪里坏了？** 数据、检索、重排、上下文还是生成？
2. **改动真的更好吗？** 是否在同一测试集、同一约束和同一成本口径下改善？
3. **离线提升能否转化为线上收益？** 是否改善真实任务成功率，而不是只优化代理指标？

## 分层评估模型

    Evaluation Dataset
          ↓
    Retrieval Evaluation
          ↓
    Context / Reranking Evaluation
          ↓
    Generation Evaluation
          ↓
    End-to-End Evaluation
          ↓
    Regression Gate
          ↓
    Online Evaluation

### 检索层

关注“正确证据有没有被找到、排在什么位置”。核心指标包括 Recall@K、Precision@K、Hit Rate@K、MRR、nDCG@K。

见 [[retrieval-metrics]]。

### 生成层

关注“回答是否基于证据、是否回答了问题、是否遗漏关键信息”。核心维度包括 Faithfulness / Groundedness、Answer relevance、Completeness、Correctness、Citation correctness。

见 [[generation-metrics]]。

### 系统层

关注生产属性：P50/P95/P99 latency、error rate、throughput、tokens/query、cost/query、cache hit rate、index freshness。

见 [[end-to-end-evaluation]]。

### 业务层

最终需要回到业务结果，例如 Task Success Rate、Resolution Rate、Escalation Rate、CSAT、human override rate。

## 推荐工作流

    建立测试集
      ↓
    冻结 baseline
      ↓
    运行分层评估
      ↓
    定位瓶颈
      ↓
    单变量改动
      ↓
    回归测试
      ↓
    小流量线上验证
      ↓
    推广 / 回滚

## 不要只看一个指标

例如 Recall@10 提升并不意味着最终回答一定更好：Top-k 增大可能提高召回，同时引入更多噪声；reranker 可能提升排序，却增加延迟；更长上下文可能提高覆盖率，却降低生成注意力质量；更强模型可能提高答案质量，却显著增加成本。

因此评估结果至少应同时包含 **quality / latency / cost** 三个维度。

## 详细页面

- [[evaluation-dataset]] — 如何构建可复用评测集
- [[retrieval-metrics]] — 检索指标与适用条件
- [[generation-metrics]] — 生成质量与引用质量
- [[end-to-end-evaluation]] — 端到端质量、延迟、成本
- [[regression-testing]] — 每次改动的质量门禁
- [[online-evaluation]] — A/B、灰度与真实业务指标

已有专题：[[../retrieval/retrieval-evaluation]]、[[../generation/generation-evaluation]]。

## 来源与证据

- Evidence: External + Derived
- Microsoft Learn 的 RAG evaluator 文档将检索过程评估与系统级 groundedness / relevance / completeness 分开。
- Microsoft Azure Architecture Center 的 RAG 检索指南列出 Precision@K、Recall@K 与 MRR 等经典 IR 指标。
- 本页的分层框架与上线门禁结构属于仓库的工程化整理，不代表原始《字节跳动 RAG 实践手册》的原文结构。
