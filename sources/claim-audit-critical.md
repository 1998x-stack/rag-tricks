# Critical Claim Audit · 2026-09-29

本文件记录第一轮高风险 Claim 审计。页码指 `raw/full-text.txt` 中的 `@@@PAGE<n>@@@` OCR 页标；它用于定位原始抽取内容，不代表仓库已经对外部真实性或版权来源做了独立认证。

## 审计原则

- 能在原始抽取文本中定位：记为 `partial` 或 `verified`，并记录页段；
- 页面中新增的总结、推导和泛化建议仍按 `Synthesis` / `Derived` 处理；
- 原始材料中的局部 benchmark 不自动升级为通用工程基准；
- 本轮不编造 PDF 页码，也不把 OCR 页标伪装成正式出版页码。

## 已审计页面

| 页面 | 状态 | OCR 页标 | 已定位的高风险 Claim |
|---|---|---:|---|
| `wiki/ops-and-reliability/failure-postmortem.md` | Partial | 112-116 | 两起故障的时间、影响、恢复时长、根因、改进措施与后续效果 |
| `wiki/cost-and-efficiency/cost-optimization.md` | Partial | 81-86 | ByteCost、成本拆解、飞书 120 万→45 万/62.5%、缓存/冷热分离等案例数据 |
| `wiki/introduction/bytedance-rag-applications.md` | Partial | 21-23, 44-56 | ByteVectorDB/ByteLB、NRT 更新、抖音/飞书/金融/剪映业务案例 |
| `wiki/advanced-topics/future-outlook.md` | Partial | 68-69 | 10 亿用户、500 万企业、QPS≥20000、成本下降 70%、四大发展方向 |

## 尚未完成

- `contradictory.md` 的 12 组设计权衡仍需逐条建立来源映射；
- `wiki/architecture/overview.md` 中默认参数和“标准部署方案”仍需审计；
- 技术组件名称（如 ByteRetrieval、ByteGen 等）需要逐项核验，不应由相邻段落自动推断；
- 外部公开来源与原始 PDF 再分发授权仍是独立问题。

## 下一步

下一轮优先审计 `contradictory.md`，并把每个权衡改造成 `约束 → 备选方案 → 指标 → 风险 → 验证实验 → 来源` 的决策记录。
