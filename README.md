# RAG Tricks：RAG 工程知识库

> 基于《字节跳动 RAG 实践手册》等材料整理的 RAG 工程知识库。目标不是简单复刻 PDF，而是把概念、工程模式、设计权衡、案例与可执行检查项组织成可持续演进的知识网络。

[![Pages](https://img.shields.io/badge/GitHub_Pages-在线浏览-blue)](https://1998x-stack.github.io/rag-tricks/)
[![Obsidian](https://img.shields.io/badge/Obsidian-兼容-7C3AED)](https://obsidian.md)
[![Content Quality](https://github.com/1998x-stack/rag-tricks/actions/workflows/content-quality.yml/badge.svg)](https://github.com/1998x-stack/rag-tricks/actions/workflows/content-quality.yml)

## 从这里开始

这个仓库同时服务三种使用方式：

| 目标 | 推荐入口 |
|---|---|
| 系统学习 RAG | [学习路径](./index.md#学习路径) |
| 设计一个生产 RAG 系统 | [系统架构](./wiki/architecture/architecture.md) |
| 做上线与生产就绪检查 | [Production Readiness](./wiki/production/production-readiness.md) |
| 排查检索/生成问题 | [问题排查入口](./index.md#问题排查入口) |
| 建立评估与回归体系 | [Evaluation Center](./wiki/evaluation/evaluation.md) |
| 做技术选型与权衡 | [Decision Center](./wiki/decisions/decision-center.md) |
| 查原始材料与证据状态 | [来源与证据规范](./SOURCE_POLICY.md) |

## 知识地图

| 领域 | 内容 |
|---|---|
| [引言与概述](./wiki/introduction/introduction.md) | RAG 基本原理、RAG vs Fine-tuning、RAG vs IR、业务应用 |
| [系统架构设计](./wiki/architecture/architecture.md) | 数据层、索引层、检索层、生成层及端到端架构 |
| [数据处理与准备](./wiki/data-layer/data-layer.md) | 数据收集、清洗、预处理、增强、标注、安全 |
| [索引构建与优化](./wiki/indexing/indexing.md) | 嵌入模型、向量生成、向量数据库、索引质量 |
| [检索策略与实现](./wiki/retrieval/retrieval.md) | 查询理解、语义/关键词/混合检索、结果处理、评估 |
| [生成层设计与优化](./wiki/generation/generation.md) | 模型选型、Prompt、质量控制、效率与成本 |
| [Evaluation Center](./wiki/evaluation/evaluation.md) | 数据集、检索/生成指标、端到端评估、回归门禁、线上实验 |
| [Decision Center](./wiki/decisions/decision-center.md) | 检索、模型、索引、分块、部署与资源的结构化技术决策 |
| [Production Readiness](./wiki/production/production-readiness.md) | Observability、安全、恢复、容量与发布门禁 |
| [Benchmark Standard](./wiki/benchmarks/benchmark-standard.md) | 规范案例数字、实验上下文与复现状态 |
| [业务线落地案例](./wiki/business-cases/business-cases.md) | 业务案例与场景化实践；统一目录见 [Case Catalog](./wiki/cases/case-catalog.md) |
| [运维与可靠性](./wiki/ops-and-reliability/ops-and-reliability.md) | 监控、自动化运维、应急响应、压测、故障复盘 |
| [成本与效率](./wiki/cost-and-efficiency/cost-and-efficiency.md) | 成本拆解、优化与监控 |
| [高级专题](./wiki/advanced-topics/advanced-topics.md) | 多模态、RAG Agent、隐私安全、系统集成 |

## 内容可信度：先区分“来源”与“推导”

仓库包含大量工程数字、案例、产品/组件名称和经验性结论。为避免把二次整理误读成已独立验证的事实，本项目从现在开始使用统一证据等级：

- **Source**：原始材料中可直接定位的内容。
- **Synthesis**：对一个或多个来源进行结构化整理，不新增关键事实。
- **Derived**：基于来源与工程常识得到的推导、建议或设计方案。
- **External**：来自原始手册之外、且明确给出来源的内容。
- **Unverified**：暂未完成逐条来源核验的历史内容。

详细规则见 [SOURCE_POLICY.md](./SOURCE_POLICY.md)。高风险页面的核验状态登记在 [sources/source-map.json](./sources/source-map.json)。

> **重要说明**：历史页面中出现的精确 QPS、成本、延迟、百分比、事故时间、内部组件名称等，不应仅因为出现在本仓库就被视为已经独立验证。引用这些信息前，请检查页面的来源状态及原始材料。

## 两种浏览方式

### Obsidian

仓库保留 Obsidian 风格的 `[[wikilinks]]`，适合作为本地知识库使用：

```bash
git clone https://github.com/1998x-stack/rag-tricks.git
```

然后在 Obsidian 中将仓库目录作为 Vault 打开。

### GitHub / GitHub Pages

README 与主要导航使用标准 Markdown 链接，保证 GitHub 可点击。Quartz 构建已经加入工程分支，Web 端支持 wikilink、backlink、全文搜索、Explorer 与知识图谱；部署仅在相关改动按顺序合并到 `main` 后生效。

## 项目结构

```text
rag-tricks/
├── README.md
├── index.md
├── SOURCE_POLICY.md              # 来源、证据与事实表达规范
├── CONTRIBUTING.md               # 内容贡献与审核规则
├── contradictory.md              # 设计权衡
├── wiki/                         # 主知识库
├── sources/
│   └── source-map.json           # 高风险内容来源核验登记
├── scripts/
│   └── quality_check.py          # 内容质量静态检查
├── .github/workflows/
│   └── content-quality.yml       # CI 质量门禁
└── raw/                          # 原始材料（再分发权限需单独确认）
```

## 质量保障

每次 PR 会自动执行内容检查：

- 标准 Markdown 相对链接是否指向存在的文件；
- 来源登记文件是否合法、是否引用存在的页面；
- 重复一级标题提示；
- 未解析的 Obsidian wikilink提示；
- 含大量数字指标但缺少“来源与证据”章节的页面提示。

当前 CI 对历史遗留的 wikilink 与数字证据问题先采用 **warning**，避免一次性阻断全部内容；新增/修改内容应主动遵循证据规范。

## 贡献原则

新增内容优先回答四个问题：

1. 这是原始材料明确表达的，还是整理者的工程推导？
2. 精确数字是否可以定位到来源、页码或外部链接？
3. 这个建议的适用条件、约束和失败模式是什么？
4. 它是否能转化为可验证的实验、指标或检查项？

具体见 [CONTRIBUTING.md](./CONTRIBUTING.md)。

## 路线图

近期重点：

1. 完成高风险精确事实的 Claim Audit；
2. 为核心页面补齐来源页码/证据类型；
3. 持续扩展 Evaluation Center，并把评估门禁接入后续实验资产；
4. 将“目录式 Wiki”升级为 Learn / Build / Debug / Decide 四类入口；
5. 持续优化 Quartz 站点的信息架构、搜索与知识图谱体验。

## 版权与来源说明

本仓库包含对第三方材料的整理。原始材料的版权归各自权利人所有。仓库中的结构化笔记、工程推导与维护代码不意味着获得原材料的再分发授权。

在确认公开再分发授权前，不应把“用于学习”视为充分的版权依据。对 `raw/` 下原始 PDF 的长期公开托管建议单独完成授权/来源核验。

---

目标：把一次性的资料整理，逐步建设成**可追溯、可验证、可维护、可演进的 RAG Engineering Handbook**。
