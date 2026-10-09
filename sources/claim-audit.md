# 原文抽样审计记录

审计日期：2026-10-04。核验对象是仓库中的文本抽取文件，不是材料发布方身份或业务事实真实性。

## 定位约定

`raw/full-text.txt` 使用 `@@@PAGE<n>@@@` 标记抽取页。以下定位指该标记到下一标记之间的内容，**不等同于手册目录的印刷页码**。抽取存在双栏交错和重复字问题，本次未用 PDF 图像复核版式。没有找到匹配也不能据此断言原文不存在。

文本 SHA-256：`aef5b56e2e597557102952e83560902f8a2ecddefead7bbecbd89e28747e094d`。

## 本次抽样

| Claim | 抽取定位 | 发现与处理 |
|---|---|---|
| Recall@k 的分母 | `@@@PAGE24@@@`，检索 `Recall@k`，与 `总相关文档` 的上下文对应 | 原文分母为总相关文档；索引评估笔记误写为返回结果中的比例。已修正笔记，并引入外部指标定义 |
| ByteRetrievalEval 名称 | `@@@PAGE30@@@`，检索 `ByteRetrievalEval` | 名称出现在本地材料中；不能因此证实该内部工具存在或已公开可用 |
| 以语义相似度计算事实准确率 | `@@@PAGE43@@@`，检索 `ByteGenEval` 后的说明 | 原材料确实包含此表述，但来源可定位不代表方法有效。笔记已区分相似度信号与事实核验 |
| 默认 768 维 | `@@@PAGE20@@@`，检索 `768` 与 `维维度度选选择择依依据据` | 仅定位到材料表述，未获得实验配置、发布方证明或适用范围；维持待核验 |

本表是局部 Claim 审计，不将整页升级为 `verified`。相关历史页仍登记为 `needs_verification`。

## 复现定位

在仓库根目录执行：

```python
from pathlib import Path
import re

text = Path("raw/full-text.txt").read_text(encoding="utf-8")
for page in (20, 24, 30, 43):
    match = re.search(rf"@@@PAGE{page}@@@(.*?)(?=@@@PAGE|\Z)", text, re.S)
    print(f"抽取页 {page}\n{match.group(1) if match else '未找到'}")
```

## 后续核验优先级

1. 发布者、原始发布渠道、版本和再分发许可。
2. 故障日期、业务影响、成本和规模数字的逐条定位与外部交叉验证。
3. 将来源描述与工程建议拆开，明确实验数据集、测量环境和适用边界。

关联：[来源规范](../SOURCE_POLICY.md) · [核验登记](source-map.json) · [指标定义](../wiki/evaluation/metrics.md)。
