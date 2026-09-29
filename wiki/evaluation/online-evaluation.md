---
title: Online Evaluation
type: playbook
evidence: derived
verified_at: 2026-09-29
---

# Online Evaluation

离线评估用于快速、可重复地筛选方案；线上评估用于验证用户真实收益。两者不能互相替代。

## 上线顺序

    offline gate
      ↓
    shadow traffic
      ↓
    canary
      ↓
    small A/B
      ↓
    progressive rollout
      ↓
    full rollout

每一步都应支持快速回滚。

## Online metrics

### 用户结果

- task success
- resolution rate
- CSAT
- re-query rate
- escalation rate
- abandonment rate

### 系统指标

- P95/P99 latency
- timeout/error rate
- fallback rate
- cache hit
- index freshness
- cost/query

### 质量 proxy

- citation click / evidence open rate
- regenerate rate
- thumbs up/down
- human override
- complaint rate

Proxy 只能辅助判断，不能自动等价为“答案正确”。

## A/B 实验注意事项

- 用户稳定分桶；
- 两组访问同一知识版本，除非知识版本就是实验变量；
- 控制模型、prompt、索引等非目标变量；
- 预先定义 primary metric 与 guardrail metrics；
- 实验运行覆盖典型业务周期。

## Segment analysis

总平均值可能隐藏严重退化。至少按 query category、locale、tenant / permission class、region、corpus type、query difficulty、answerable / no-answer 切分。

## Feedback loop

    online failure
      ↓
    sample + trace
      ↓
    root cause
      ↓
    offline challenge set
      ↓
    fix
      ↓
    regression gate

生产反馈最终应该回到离线测试集。

## 来源与证据

- Evidence: Derived
- 本页侧重生产实验设计与反馈闭环。
