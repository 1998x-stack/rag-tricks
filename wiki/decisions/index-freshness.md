---
title: Index Freshness
type: decision
evidence: synthesis
verified_at: 2026-09-29
---

# Near-real-time vs Batch Indexing

## 决策问题

知识更新应该近实时进入索引，还是周期性批量构建？

## 关键约束

- freshness SLO；
- 更新率；
- corpus 规模；
- 是否允许短暂版本不一致；
- 重建成本；
- 回滚需求。

## Near-real-time 更适合

库存、权限、政策、用户文档等变化后很快就必须可检索的内容。

## Batch 更适合

稳定历史语料、大规模离线重建、需要统一质量校验或原子版本切换的场景。

## 常见生产方案

热更新层 + 稳定主索引并存，通过后台 compaction / merge 将增量逐步合并，避免把“实时 vs 批量”当成只能选一个。

## 验证实验

测 freshness lag、query consistency、write amplification、build duration、rollback time 和在线 P95。

## 来源与证据

- Evidence: Synthesis + Derived
- OCR 页标 21–23：来源材料描述内存增量索引、异步磁盘同步、读写分离及大规模批量构建。
- 飞书“修改后 2 秒内可检索”等属于来源材料案例。
