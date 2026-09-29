---
title: Multi-region Deployment
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Single-region vs Multi-region

## 决策问题

RAG 服务是否值得承担多地域复制和故障切换复杂度？

## 先定义

- Availability SLO；
- RTO / RPO；
- 数据驻留与合规；
- 用户地域分布；
- 跨地域同步量；
- failover 是否需要自动化。

## 单地域适合

非核心、批处理、内部实验、可接受较长恢复时间的系统。

## 多地域适合

核心在线业务、全球用户、严格 RTO/RPO、地域灾难需要自动切换的系统。

## 隐藏成本

多地域不只是“多部署一份”：还包括索引版本一致性、向量/文档复制、缓存冷启动、权限数据同步、模型版本一致性和故障演练。

## 验证实验

定期做 region evacuation game day，实际测 RTO、RPO、错误率、数据一致性和回切时间，而不是只验证配置存在。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 63–64：来源材料描述北京/上海/广州多区域、RTO/RPO 与备份策略。
- OCR 页标 96–97：跨地域部署与双地域热备案例。
- 具体 SLA 属于来源场景，不自动成为本项目推荐门槛。
