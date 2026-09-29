---
title: Platform vs Business Customization
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Shared RAG Platform vs Business-specific Stack

## 决策问题

能力应该沉淀到统一平台，还是由业务线独立开发？

## 平台化适合

- 接口稳定、跨业务复用率高；
- 安全、观测、评估、权限等横切能力；
- 重复建设成本高；
- 需要统一治理。

## 业务定制适合

- schema/术语/工作流强领域化；
- 业务迭代速度远快于平台；
- 差异化能力本身就是产品价值；
- 平台抽象会造成大量 escape hatch。

## 推荐边界

平台负责 contract 与横切能力，业务负责 domain policy：数据接口、检索/生成插件协议、评估契约统一，但 chunking、词典、prompt、模型路由允许配置/扩展。

## 验证指标

接入 lead time、平台复用率、业务 override 比例、breaking-change 次数、独立故障域、单位维护成本。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 73–76：来源材料描述 RAG 技术中台、ByteDocParser、ByteRetrievalKit 与业务配置接口。
- “平台 contract + domain policy”是本知识库的工程抽象。
