---
title: RAG Regression Testing
type: playbook
evidence: derived
verified_at: 2026-09-29
---

# RAG Regression Testing

RAG 系统任何一个组件升级都可能产生非局部影响：embedding 模型变化需要重建索引；chunking 改动会改变召回分布；reranker 升级会改变 context 顺序；prompt 改动会影响引用与拒答；LLM 升级会改变格式、事实性和 token 使用量。

因此评估必须进入 CI/CD。

## Baseline vs Candidate

每次变更都运行同一测试集，输出 aggregate score 之外，还要保留 improved queries、regressed queries、unchanged queries、largest regressions 与 category-level deltas。

## 建议门禁

不要把门禁写死成通用数字，而应该根据业务建立 SLO。

### Blocking

- critical safety / permission test regression
- answerable query catastrophic regression
- citation validity failure

### Budgeted

- P95 latency increase
- cost/query increase

### Review-required

- quality improves but cost rises
- retrieval improves but groundedness falls

## Regression budget

允许小幅波动时，显式配置 quality / latency / cost regression tolerance。但对权限泄露、错误引用、关键业务事实错误等类别，应采用零容忍门禁。

## Golden failures

每一次生产事故或高影响错误都应该新增最小复现测试：

    bug
     ↓
    repro query
     ↓
    expected behavior
     ↓
    regression case
     ↓
    永久进入 CI

## 模型版本变化

使用外部模型 API 时，至少记录 provider、model ID、dated model version（若存在）、prompt hash/version 与 evaluation date。否则“同样代码”并不保证“同样行为”。

## 来源与证据

- Evidence: Derived
- 本页把传统软件回归思想应用于 RAG 的数据、检索、模型和 prompt 多版本系统。
