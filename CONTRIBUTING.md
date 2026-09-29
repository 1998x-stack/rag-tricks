# Contributing

感谢参与 RAG Tricks。这个项目优先追求**可追溯、可验证、可维护、可执行**，而不是单纯增加文章数量。

## 内容类型

新增页面前，先判断它属于哪一类：Concept、Pattern、Decision、Playbook、Case、Benchmark、Failure、Tradeoff、Checklist 或 Glossary。

不要强制所有页面套用同一个“是什么/为什么/如何使用/常见误区”模板。

## 提交前检查

### 1. 先分类证据

关键事实必须能回答：Source / Synthesis / Derived / External / Unverified？是否有来源？是否可以定位页码/章节？是否增加了原材料里没有的新事实？

详见 [SOURCE_POLICY.md](./SOURCE_POLICY.md)。

### 2. 数字必须有上下文

不要只写“Recall 提升 9%”。至少说明数据集、corpus、query 数、embedding、chunking、retrieval 配置、metric、测量环境与来源。

若上下文缺失，明确标记为来源材料中的局部结果，不要推广为通用 benchmark。

### 3. 决策内容要写边界

技术选型页面应尽量包含：问题、约束、备选方案、评价维度、风险、适用场景、不适用场景与验证实验。

### 4. 案例不能伪装成历史事实

组合案例、教学案例、作者推演必须标记。如果不能证明一个精确日期、地点、事故、成本或内部系统名称来自可核验来源，就不要把它写成确定性历史记录。

### 5. 链接兼容

重要导航使用标准 Markdown 链接，例如 `[混合检索](./wiki/retrieval/hybrid-retrieval.md)`。

正文知识网络可以继续使用 Obsidian `[[hybrid-retrieval]]`，但不要假设 GitHub Pages 的 Jekyll Cayman 会自动渲染 wikilink。

## 推荐页面 frontmatter

新页面推荐包含 title、type、evidence、verified_at、source_refs 与 tags。历史页面采用渐进迁移，不要求一次性全部补齐。

## 本地质量检查

使用 Python 3：

    python3 scripts/quality_check.py

检查器会：

- 阻止失效的标准 Markdown 相对文件链接；
- 校验 `sources/source-map.json`；
- 提示未解析 wikilink；
- 提示重复 H1；
- 提示含大量精确数字但没有“来源与证据”章节的页面。

现有历史债务以 warning 为主；新增内容不应继续扩大 warning 数量。

## PR 建议

一个 PR 尽量只解决一类问题，例如 source audit、navigation、evaluation content、retrieval decision matrix 或 site infrastructure。

PR 描述建议包含 Why、What changed、Evidence impact、Validation 与 Known limitations。

## 内容演进原则

优先把知识变成：

    来源
      ↓
    Claim
      ↓
    Pattern / Tradeoff
      ↓
    Playbook / Decision
      ↓
    Evaluation

最终目标不是“更多 Markdown”，而是更快回答：我该怎么设计？为什么出问题？两种方案怎么选？如何验证改动有效？这个结论来自哪里？
