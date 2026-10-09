---
title: RAG Security
type: checklist
evidence: external
verified_at: 2026-09-29
---

# RAG Security

RAG 增加了一类传统 LLM 应用没有的攻击面：**外部知识会进入模型上下文**。因此用户输入、文档内容、metadata、向量索引和模型输出都应该视为不同信任级别的数据。

## 主要风险面

### Prompt Injection

检索到的文档可能包含恶意或冲突指令。系统不能因为文本来自“知识库”就自动把它视为可信指令。

### Sensitive Information Disclosure

权限过滤必须发生在检索链路中，而不是仅依赖模型“不要透露”。

### Data / Model Poisoning

数据摄取流程需要来源、审核、版本和撤回能力；高影响知识源应支持 provenance。

### Improper Output Handling

模型输出如果进入 HTML、SQL、工具参数或下游 API，必须按对应上下文做验证/转义。

### Excessive Agency

如果 RAG 与 Agent/工具调用结合，应最小化权限、限制工具集合、对高影响动作要求明确授权。

### Vector / Embedding Weaknesses

需要防止跨租户向量泄露、metadata filter 绕过、错误 ACL、恶意文档污染和未经授权的相似性检索。

### Unbounded Consumption

限制 query 长度、Top-k、rerank candidate、上下文 token、生成 token、并发和重试，防止单请求资源无限扩张。

## RAG 专用安全检查

- ingestion source 是否可信且可追溯？
- 文档 ACL 是否与 chunk/vector 一起传播？
- delete/revoke 后向量和缓存是否同步失效？
- retrieval filter 是否在服务端强制？
- system instruction 是否与检索内容隔离？
- retrieved text 是否被明确视为 data 而非 privileged instruction？
- citation 是否会暴露无权限 source metadata？
- telemetry 是否会泄露 prompt/document？
- cache key 是否包含 tenant/permission boundary？

## 安全测试进入回归

把已发现的问题转成固定测试：越权检索、跨租户缓存、注入文档、恶意 metadata、超长输入、无权限 citation 等都应成为 regression case。

## 来源与证据

- Evidence: External + Derived
- OWASP Top 10 for LLM Applications 2025 包含 Prompt Injection、Sensitive Information Disclosure、Supply Chain、Data and Model Poisoning、Improper Output Handling、Excessive Agency、System Prompt Leakage、Vector and Embedding Weaknesses、Misinformation、Unbounded Consumption。
- NIST AI RMF Generative AI Profile 用于补充生命周期风险治理视角。
- RAG 专用检查项是本仓库基于这些风险类别的工程化映射。
