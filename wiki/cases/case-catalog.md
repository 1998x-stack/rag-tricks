---
title: Case Catalog
type: hub
evidence: synthesis
verified_at: 2026-09-29
---

# Case Catalog

案例的价值不是提供“可复制数字”，而是提供**问题背景、约束、架构选择、测量方式、结果和适用边界**。

## 当前案例

| 案例 | 来源状态 | 主要场景 | OCR 页标 |
|---|---|---|---:|
| [[../business-cases/douyin-ecommerce]] | Partial | 电商客服 / 商品问答 | 44–47 |
| [[../business-cases/feishu-knowledge]] | Partial | 企业知识库 / 文档助手 | 47–50 |
| [[../business-cases/fintech-research]] | Partial | 研报 / 投资问答 | 50–53 |
| [[../business-cases/jianying-script]] | Partial | 脚本生成 / 创意辅助 | 53–56 |

## Case Card 必备字段

每个正式案例至少说明：

- **Source scope**：来源页段/外部来源；
- **Workload**：query 类型、数据规模、并发/时效特征；
- **System boundary**：案例涉及哪些层；
- **Intervention**：具体改了什么；
- **Reported metrics**：来源材料报告了什么；
- **Measurement context**：测试集、时间窗口、硬件/模型/配置（若来源可得）；
- **Portability**：哪些结论可以迁移，哪些只是场景局部数据；
- **Evidence status**：Source / Partial / Synthesis / Derived。

## 如何引用案例数字

不要写：

> 动态分块能让 Recall 提升 9%。

更好的写法：

> 来源材料在其飞书案例中报告了 Recall@10 的局部提升；当前仓库没有完整实验配置，因此该数值不能直接外推到其他 corpus。

Benchmark 引用规范见 [[../benchmarks/benchmark-standard]]。

## 来源与证据

- Evidence: Synthesis
- 四个业务案例均可在《字节跳动 RAG 实践手册》抽取文本的对应 OCR 页段定位。
- 本目录对案例表达方式进行标准化，不改变原材料的事实层级。
