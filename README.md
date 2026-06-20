# 字节跳动 RAG 实践手册 Wiki

> 从《字节跳动 RAG 实践手册》(118页 PDF) 中提取、分类、深化的结构化知识库 —— 覆盖从数据处理、索引构建、检索策略到生成优化的全链路 RAG 方法论。

[![Pages](https://img.shields.io/badge/GitHub_Pages-在线浏览-blue)](https://1998x-stack.github.io/rag-tricks/)
[![Obsidian](https://img.shields.io/badge/Obsidian-兼容-7C3AED)](https://obsidian.md)
[![Files](https://img.shields.io/badge/Wiki页面-62个-orange)](./wiki/)

---

## 是什么

这是一个**字节跳动 RAG 实践的结构化知识库**，原始素材来自《字节跳动 RAG 实践手册》(118 页 PDF)。我们从手册中：

1. **提取** 200+ 条可操作的实践要点
2. **分类** 为 10 个主题领域
3. **深化** 为 52 个知识点的详细解释
4. **发现** 12 组设计权衡与矛盾观点

结果是一个适合日常查阅、系统学习和团队共享的**知识网络**。

## 快速导航

| 类别 | 核心知识点 |
|------|-----------|
| [引言与概述](./wiki/introduction/introduction.md) | RAG基本原理, RAG vs Fine-tuning, RAG vs IR, 字节业务应用 |
| [系统架构设计](./wiki/architecture/architecture.md) | 四层架构, 数据层, 索引层, 检索层, 生成层 |
| [数据处理与准备](./wiki/data-layer/data-layer.md) | 数据收集清洗, 文本预处理, 数据增强, 数据标注, 数据安全 |
| [索引构建与优化](./wiki/indexing/indexing.md) | 嵌入模型, 向量生成, 向量数据库, 性能优化, 质量评估 |
| [检索策略与实现](./wiki/retrieval/retrieval.md) | 检索触发, 查询理解, 语义/关键词/混合检索, 结果处理, 评估调优 |
| [生成层设计与优化](./wiki/generation/generation.md) | 模型选型, Prompt Engineering, 质量控制, 效率成本 |
| [业务线落地案例](./wiki/business-cases/business-cases.md) | 抖音电商, 飞书知识库, 金融科技, 剪映脚本生成 |
| [运维与可靠性](./wiki/ops-and-reliability/ops-and-reliability.md) | 全链路监控, 自动化运维, 应急响应, 性能压测, 技术复用 |
| [成本与效率](./wiki/cost-and-efficiency/cost-and-efficiency.md) | 成本拆解, 优化策略, 监控归因, 效率极致优化 |
| [高级专题](./wiki/advanced-topics/advanced-topics.md) | 多模态RAG, RAG-Agent, 隐私安全, 系统集成, 新手入门 |

另见：[矛盾观点汇总](./contradictory.md) — 12 组设计权衡及分析

## 特点

- **实战导向** — 每条实践来自字节跳动真实业务场景，非教科书复述
- **深度解释** — 52 个知识页面覆盖「是什么、为什么重要、如何使用、常见误区」
- **可交叉引用** — 200+ Obsidian 风格 [[双向链接]] 连接相关知识
- **矛盾追踪** — `contradictory.md` 记录了 12 组设计权衡并附分析
- **全中文内容** — 保留原始中文技术术语和行业表达
- **持续可扩展** — 目录结构支持添加新的类别和知识点

## 如何使用

### 在 Obsidian 中打开（推荐）
```bash
git clone https://github.com/1998x-stack/rag-tricks.git
# 在 Obsidian 中作为 Vault 打开
# File → Open Vault → 选择 rag-tricks 目录
```

### 在 GitHub 上浏览
直接通过 GitHub 的 Markdown 渲染浏览所有页面，链接可直接点击跳转。

### 在任意 Markdown 编辑器中查看
所有文件均为标准 Markdown，兼容 VS Code、Typora、Notion 等工具。

## 项目结构

```
rag-tricks/
├── README.md                     # 项目主页
├── contradictory.md              # 12 组设计权衡及分析
├── index.md                      # 导航入口
├── _config.yml                   # Jekyll 配置
├── wiki/                         # 10 个类别 × 知识页面
│   ├── introduction/             # 引言与概述 (4 文件)
│   ├── architecture/             # 系统架构设计 (5 文件)
│   ├── data-layer/               # 数据处理与准备 (6 文件)
│   ├── indexing/                 # 索引构建与优化 (5 文件)
│   ├── retrieval/                # 检索策略与实现 (8 文件)
│   ├── generation/               # 生成层设计与优化 (6 文件)
│   ├── business-cases/           # 业务线落地案例 (5 文件)
│   ├── ops-and-reliability/      # 运维与可靠性 (8 文件)
│   ├── cost-and-efficiency/      # 成本与效率 (5 文件)
│   └── advanced-topics/          # 高级专题 (7 文件)
└── raw/
    └── 字节跳动 RAG 实践手册.pdf  # 原始 PDF
```

## 统计

| 指标 | 数值 |
|------|------|
| 主题类别 | 10 |
| 知识点页面 | 52 |
| 总文件数 | 62 |
| 双向链接 | 200+ |
| 实践条目 | 200+ |
| 设计权衡 | 12 组 |

## 声明

本知识库内容来源于《字节跳动 RAG 实践手册》，原始版权归字节跳动所有。本项目仅做提取、分类和系统化整理，供学习参考使用。如有版权问题，请联系处理。

---

<p align="center">
  <sub>用 <a href="https://claude.ai/code">Claude Code</a> 构建 · 2026</sub>
</p>
