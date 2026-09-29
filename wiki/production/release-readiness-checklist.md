---
title: Release Readiness Checklist
type: checklist
evidence: derived
verified_at: 2026-09-29
---

# Release Readiness Checklist

候选 RAG 版本上线前应有一份可以明确回答 **pass / fail / accepted risk** 的清单。

## Quality

- [ ] 固定 evaluation dataset 上无关键回归
- [ ] retrieval 与 generation 指标均评估
- [ ] no-answer / hard-negative 样本通过
- [ ] citation validity / coverage 达到业务门槛
- [ ] 线上历史高影响失败已进入 regression set

## Data / Index

- [ ] corpus snapshot 可识别
- [ ] chunking / embedding / index version 可追溯
- [ ] freshness SLO 已验证
- [ ] delete / revoke / ACL propagation 已验证
- [ ] index rollback 可执行

## Security

- [ ] prompt injection 测试
- [ ] 跨租户/权限边界测试
- [ ] sensitive telemetry 审查
- [ ] cache isolation 测试
- [ ] output handling / tool permission 测试（若适用）
- [ ] consumption limits 已设置

## Reliability

- [ ] dependency timeout / retry 有界
- [ ] fallback 路径测试
- [ ] last-known-good model/index 可回滚
- [ ] RTO/RPO 演练
- [ ] runbook 与 owner 明确

## Performance / Cost

- [ ] P50/P95/P99 符合 SLO
- [ ] burst / cold-cache / long-context 压测
- [ ] quota/headroom 足够
- [ ] cost/query 在预算内
- [ ] autoscaling 在目标时间内生效

## Observability

- [ ] end-to-end trace 可关联
- [ ] model/index/prompt 版本进入 telemetry
- [ ] retrieval / rerank / generation latency 可拆分
- [ ] freshness、empty retrieval、fallback 有指标
- [ ] alert 对应 owner 与 runbook

## Rollout

- [ ] canary / progressive rollout 配置
- [ ] rollback trigger 明确
- [ ] primary + guardrail metrics 明确
- [ ] 变更窗口与观察窗口明确
- [ ] 发布后验证负责人明确

## 结论

清单不是为了全部打勾，而是让未满足项变成**显式风险接受**，有 owner、有期限、有回滚条件。

## 来源与证据

- Evidence: Derived
- 由 [[production-readiness]]、[[security]]、[[observability]]、[[recoverability]]、[[capacity-performance]] 和 [[../evaluation/regression-testing]] 汇总。
