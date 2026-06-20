# 索引构建与优化

## 概述

索引层是 RAG 系统的核心枢纽，负责将处理后的数据转化为可高效检索的向量索引结构。字节跳动围绕"业务适配性"和"效率平衡"两大原则，建立了一套涵盖嵌入模型选型、向量生成策略、向量数据库构建、索引性能优化和质量评估迭代的完整体系。自研的 ByteEmbedding 多语言嵌入模型、ByteVectorDB 分布式向量数据库和 ByteLB 负载均衡组件构成了索引层的基础设施，支撑抖音、飞书、金融科技等业务线的大规模检索需求。

## 详细知识

- [[embedding-model-selection]] — 嵌入模型选型与定制：ByteEmbedding 系列、领域微调（金融、医疗）、模型轻量化蒸馏
- [[vector-generation-strategy]] — 向量生成策略：动态分块、多粒度向量（文档级+段落级+句子级）、维度选择（768/1024）与精度压缩（FP16/INT8）
- [[vector-database]] — 向量数据库构建与管理：ByteVectorDB 分布式架构、Milvus 改造实践、离线索引构建与实时索引更新（NRT）
- [[index-performance-optimization]] — 索引性能优化：三级过滤（Bloom+ANN+余弦）、ByteLB 负载均衡、向量去重与 LZ4 压缩
- [[index-quality-evaluation]] — 索引质量评估与迭代：三维指标体系（效果+性能+成本）、每周评估流程、A/B 验证机制

## 核心实践

| 实践 | 场景 | 要点 | 参见 |
|------|------|------|------|
| 模型蒸馏 | 边缘端、低延迟场景（抖音客服实时问答） | 百亿→百万参数蒸馏，硬蒸馏+软蒸馏结合，保证 90% 以上效果对齐，推理速度提升 15 倍 | [[embedding-model-selection]] |
| 多粒度向量 | 飞书知识库检索 | 文档级(粗筛)+段落级(中筛)+句子级(精筛)三级向量，召回率提升 22%，输入文本减少 60% | [[vector-generation-strategy]] |
| 三级过滤 | 抖音客服高并发检索 | Bloom Filter(粗筛)→ANN HNSW(中筛)→余弦(精筛)，召回率 95%，检索速度提升 40% | [[index-performance-optimization]] |
| NRT 近实时更新 | 飞书文档实时场景 | 内存索引(1秒可检索)→异步磁盘合并，文档修改后 2 秒内可检索 | [[vector-database]] |
| A/B 验证 | 索引优化后的效果验证 | 10% 流量导入优化服务，稳定运行 72 小时后全量切换 | [[index-quality-evaluation]] |
