# XMind 与 EPUB 导出维护

## 交付设计

电子书按端到端学习路径编排，覆盖 66 篇 wiki 文档与 5 篇设计权衡/证据/维护附录，共 71 篇。12 个主题部分之外另有阅读指南。使用 EPUB 3 流式排版，章节有分级目录和稳定 ID；内部 Markdown 链接在打包时转换为书内锚点。

XMind 使用官方 [xmind-generator](https://github.com/xmindltd/xmind-generator) 1.0.1 创建原生档案，补充原生主题样式、折叠状态和链接。13 张工作表包括总览与 12 个详细主题；详细节点覆盖标题、段落、列表项、表格行和代码示例。节点标题控制长度，备注保留全文。它是详尽阅读导图，不是经过额外事实认证的摘要。

## 重建

需要 Python 3.10+、Node.js、Pandoc。Python 依赖使用根目录的 `requirements-dev.txt`，Node 依赖及锁文件位于 `tools/export/`。

```bash
.venv/bin/python -m pip install -r requirements-dev.txt
npm ci --prefix tools/export
.venv/bin/python scripts/export_handbook.py
.venv/bin/python scripts/check_exports.py
```

生成结果位于 `downloads/`。`.build/` 中的 HTML 与 JSON 是中间产物，不提交。封面和 CSS 位于 `assets/exports/`；封面视觉方案见[设计说明](../assets/exports/design-philosophy.md)。本次使用 Pandoc 3.10。

## 内容覆盖与版本

`downloads/manifest.json` 记录参与导出的每篇文档、封面、CSS、生成脚本、依赖锁文件及来源登记的 SHA-256，以及交付文件大小和哈希。清单还记录每篇文章的稳定锚点和标题；具体节点数以清单为准。导出校验检查完整页面清单与生成依赖，防止正文、样式或生成器修改后仍发布旧文件。更新本页或下载介绍不改变书内内容；修改纳入书内的文档后必须重新导出。

电子书的结构生成采用 Markdown 解析器，非正则拼接正文。XMind 备注保留源 Markdown，嵌套列表保留父子关系，外部链接标记为在线跳转。原始 PDF 和全文抽取文件没有嵌入交付物。

## 验证

- 使用 [EPUBCheck](https://github.com/w3c/epubcheck) 5.4.0 验证 EPUB 标准；运行方式为 `java -jar epubcheck.jar downloads/rag-tricks-handbook.epub`。
- `check_exports.py` 检查两类 ZIP 容器、必需成员、EPUB XHTML/锚点/资源引用、XMind 唯一节点 ID、工作表跳转、文件哈希与源文档与生成依赖新鲜度。文章入口必须指向正确标题或以该标题开头的 section，不能只验证锚点存在。
- 发布工作流下载固定版本 EPUBCheck 并校验 SHA-256；任何标准校验警告或错误都会阻止发布。
- `--root` 支持检查独立副本，`--json` 输出完整诊断。损坏档案或清单会报告错误并返回非零状态。
- 封面与电子书代表性章节进行视觉抽查。EPUB 阅读器之间字体、分页和表格排版可能不同。
- 当前环境没有 XMind 桌面应用；已用官方 SDK 生成并做结构验证，未声称在桌面应用内完成视觉验收。

[下载入口](../downloads/index.md) · [在线发布说明](github-pages.md)。
