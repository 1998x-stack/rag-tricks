---
title: 业务落地案例
type: hub
evidence: synthesis
verified_at: 2026-09-29
source_refs:
  - source-manual
---

# 业务落地案例

## 概述

RAG 技术在字节跳动各业务线已实现规模化落地，覆盖智能客服、知识库问答、金融研报分析、视频创意辅助等核心场景。本章选取抖音电商、飞书、金融科技、剪映四个典型业务线，详细阐述 RAG 的落地流程、关键优化点与量化业务效果，为其他业务线提供可复用的实践参考。

## 案例使用规则

本目录中的数字属于来源材料的 **Source-reported** 案例结果，除非另有明确复现实验记录，否则不应作为跨业务通用 benchmark。

- 统一案例目录：[[../cases/case-catalog]]
- Benchmark 规范：[[../benchmarks/benchmark-standard]]
- 评估方法：[[../evaluation/evaluation]]

## 详细知识

- [[douyin-ecommerce]] — 抖音电商智能客服与商品问答：500万日均咨询量，响应时间从5分钟降至300ms
- [[feishu-knowledge]] — 飞书知识库问答与文档助手：100万+企业客户，5亿文档，召回率从60%提升至92%
- [[fintech-research]] — 金融科技研报解读与投资问答：日均1万份研报，分析师效率提升6倍
- [[jianying-script]] — 剪映视频脚本生成与创意辅助：3亿用户，创作效率从3小时降至30分钟

## 核心实践

### 智能客服场景
- **场景**：抖音电商每日500万+用户咨询，涵盖商品咨询、订单问题、售后政策
- **要点**：意图分类 → 实体识别 → 混合检索 → 轻量模型生成 → 质量控制
- **参见**：[[douyin-ecommerce]]、[[../ops-and-reliability/full-stack-monitoring]]

### 知识库问答场景
- **场景**：飞书百万企业客户的文档检索、信息总结、跨文档问答需求
- **要点**：文档解析 → 多粒度索引 → 表格语义索引 → 权限适配 → 多轮记忆
- **参见**：[[feishu-knowledge]]、[[../ops-and-reliability/tech-reuse-platform]]

### 金融研报分析场景
- **场景**：机构客户研报分析、投资问答、风险提示
- **要点**：研报解析 → 金融领域微调 → 实时数据关联 → 观点冲突分析
- **参见**：[[fintech-research]]、[[../architecture/architecture]]

### 创意辅助场景
- **场景**：剪映3亿用户的视频脚本生成、素材匹配、创意迁移
- **要点**：脚本结构化 → 跨模态检索 → 行业规则适配 → 爆款创意迁移
- **参见**：[[jianying-script]]、[[../advanced-topics/multimodal-rag]]
