---
layout: default
title: 字节跳动 RAG 实践手册 Wiki
description: 从《字节跳动 RAG 实践手册》(118页) 中提取、分类、深化的结构化知识库
---

# 字节跳动 RAG 实践手册 Wiki

> 覆盖从数据处理、索引构建、检索策略到生成优化的全链路 RAG 方法论 — 62 个页面，10 大类别

## 快速入口

### 核心架构

| 类别 | 描述 |
|------|------|
| [引言与概述](./wiki/introduction/introduction.md) | RAG基本原理, RAG vs Fine-tuning vs IR, 字节业务应用现状 |
| [系统架构设计](./wiki/architecture/architecture.md) | 四层架构: 数据层+索引层+检索层+生成层 |
| [数据处理与准备](./wiki/data-layer/data-layer.md) | 数据收集清洗, 文本预处理, 数据增强, 标注分类, 安全隐私 |
| [索引构建与优化](./wiki/indexing/indexing.md) | 嵌入模型选型, 向量生成策略, 向量数据库, 性能优化, 质量评估 |
| [检索策略与实现](./wiki/retrieval/retrieval.md) | 检索触发, 查询理解, 语义/关键词/混合检索, 结果处理, 效果评估 |
| [生成层设计与优化](./wiki/generation/generation.md) | 模型选型, Prompt Engineering, 质量控制, 效率与成本优化 |

### 实践落地

| 类别 | 描述 |
|------|------|
| [业务线落地案例](./wiki/business-cases/business-cases.md) | 抖音电商, 飞书知识库, 金融科技, 剪映脚本生成 |
| [运维与可靠性](./wiki/ops-and-reliability/ops-and-reliability.md) | 全链路监控, 自动化运维, 应急响应, 性能压测, 技术复用, 跨地域部署, 故障复盘 |
| [成本与效率](./wiki/cost-and-efficiency/cost-and-efficiency.md) | 成本构成拆解, 优化策略, 监控归因, 效率极致优化 |

### 高级专题

| 类别 | 描述 |
|------|------|
| [高级专题](./wiki/advanced-topics/advanced-topics.md) | 多模态RAG, RAG-Agent集成, 隐私安全, 系统集成, 新手入门, 总结展望 |

### 专题

| 页面 | 描述 |
|------|------|
| [矛盾观点汇总](./contradictory.md) | 多组设计权衡、业务分歧及分析 |

---

## 关于本项目

本知识库使用 [Obsidian](https://obsidian.md) 风格的双向链接（`[[wikilinks]]`）构建，推荐在 Obsidian 中作为 Vault 打开以获得最佳浏览体验。

- **62 个 Markdown 文件** — 10 个主页面 + 52 个知识点深度页面
- **200+ 交叉引用** — 连接相关知识，构建知识网络
- **全中文内容** — 保留原始技术术语和行业表达
- **来源可追溯** — 内容来源于《字节跳动 RAG 实践手册》(118页 PDF)

[GitHub 仓库](https://github.com/1998x-stack/rag-tricks) · [矛盾观点](./contradictory.md) · [原始素材](./raw/字节跳动%20RAG%20实践手册.pdf)
