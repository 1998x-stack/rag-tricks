---
title: Recoverability
type: playbook
evidence: synthesis
verified_at: 2026-09-29
---

# Recoverability

可靠性不仅是“尽量不挂”，还包括出现故障后能否快速恢复，并知道恢复到了哪个数据/索引/模型版本。

## 先定义 RTO / RPO

- **RTO**：业务允许多长时间恢复？
- **RPO**：允许丢失多少最新数据/索引更新？

不同业务等级应该有不同目标，不要复制统一数字。

## 需要独立恢复的资产

- source documents
- normalized/chunked dataset
- embedding artifacts
- vector/index snapshot
- metadata + ACL
- prompts/config
- model/reranker version
- evaluation dataset
- deployment configuration

## 索引版本化

推荐将 index 作为可替换 artifact，而不是不可解释的数据库当前状态：

    corpus snapshot
       + embedding version
       + chunking version
       + index config
       = index version

切换使用 immutable version + alias/pointer，便于原子切换和回滚。

## 降级策略

故障时可考虑：

- dense unavailable → sparse fallback；
- reranker unavailable → baseline ranking；
- primary model unavailable → fallback model；
- fresh index unavailable → last-known-good snapshot，并明确 freshness；
- non-critical features disabled to preserve core Q&A。

降级必须在上线前测试，不能只写在 runbook。

## Game Day

定期演练：vector DB 节点故障、模型 provider timeout、stale index、region loss、权限服务不可用、cache corruption。记录实际 RTO/RPO 和用户影响。

## 来源与证据

- Evidence: Synthesis + Derived
- 原始手册的运维、灾备、故障复盘与跨地域章节包含 RTO/RPO、备份和故障切换案例。
- immutable index version、alias rollback 与 game-day 门禁为本知识库工程化建议。
