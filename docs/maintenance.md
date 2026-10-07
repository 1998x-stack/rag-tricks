# 知识库维护说明

## 本地检查

使用 Python 3.10+。依赖固定在 `requirements-dev.txt`；不需要运行模型或访问外部 API。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/quality_check.py --strict
.venv/bin/python scripts/quality_check.py --json
```

`--root <目录>` 可检查独立副本。默认命令返回码 1 表示有错误；`--strict` 同时将 warning 视为失败。JSON 输出含 files、links、evidence_statuses、errors、warnings；即使返回非零也会输出完整报告。

## 检查范围

| 项目 | 行为 |
|---|---|
| Markdown 解析 | 使用 markdown-it-py 的 CommonMark 解析器，开启表格和删除线 |
| 本地链接 | 检查正文、图片、引用式链接；处理 URL 编码、标题、带括号路径、同页片段 |
| 锚点 | 检查 Markdown 标题与显式 HTML id/name；中文和重复标题编号有回归测试 |
| 仓库边界 | 拒绝相对路径逃逸；目录链接必须改为具体文件 |
| Wikilink | 当前目录、根目录、唯一 basename 依次查找；失效/歧义报错，有效链接仍提示网页兼容 warning |
| 来源登记 | 校验固定状态集合、字段类型、文件路径、source_refs 与正文状态标记 |
| 知识覆盖 | wiki 全部页面及 contradictory 必须登记、包含来源章节，并从 README/index 可达 |
| 文档结构 | 缺少/多个 H1、跨页面重复 H1 提示 warning |

代码块、行内代码和 HTML 注释不作为正文链接检查。跳过隐藏目录、虚拟环境、node_modules、vendor、_site、raw，以及仓库原有忽略目录 docs/superpowers。解析每页一次并复用结果。

## 明确的边界

- 不联网检查外部 URL，不证明外部页面可访问或支持相关 Claim。
- 不对 Markdown 以外的 HTML/Liquid 模板做完整链接检查；HTML 的 id/name 仅作为锚点补充。
- 标题自动锚点按本仓库常用的 GitHub 风格生成；复杂 Unicode、图片标题或 Jekyll 特殊属性应使用简单显式锚点并检查最终构建产物。
- 证据章节和登记状态属于结构验证，不是事实认证；`needs_verification` 数量应持续可见。
- 图片/引用式链接会检查；未定义引用在 CommonMark 中是普通文本，解析器不会把它视为有效链接。

## 新增页面流程

1. 新建明确类型的文章，使用标准相对链接，避免把未证实指标写成默认门槛。
2. 增加「来源与证据」，明确 Source / Synthesis / Derived / External / Unverified。
3. 在 `sources/source-map.json` 登记页面；公司实践和历史数字未逐条核验时保留 `needs_verification`。
4. 在主题目录或首页添加入口，执行回归测试和严格检查。
5. 新增 verified/partial 状态时提供 evidence 定位，并人工审核测量条件与结论范围。

## Pages 渲染

保留 Cayman 主题，通过 [jekyll-relative-links](https://github.com/benbalter/jekyll-relative-links) 转换 Markdown 相对链接；通过 [jekyll-optional-front-matter](https://github.com/benbalter/jekyll-optional-front-matter) 处理没有 frontmatter 的历史文档。README 和 CONTRIBUTING 显式 include，避免被插件作为元文件跳过。插件均在 [GitHub Pages 支持列表](https://pages.github.com/versions/)中，查阅日期为 2026-10-04。

站点排除 raw、测试、脚本和本地设计草稿。源文件仍保留在仓库；站点排除不改变其仓库可见性。该配置不引入搜索、反向链接或知识图谱。

## 阅读体验

`handbook` 布局继承 Cayman：主导航与返回链接由静态 HTML 提供，关闭 JavaScript 仍可使用。JavaScript 仅生成本页二级标题目录；窄屏默认折叠、宽屏默认展开。站点语言设为 `zh-CN`，键盘焦点可见，打印时隐藏导航控件。

## 证据审计

[抽样 Claim 审计](../sources/claim-audit.md)记录抽取页标记、文件哈希和核验边界。全文抽取有交错文本，不能把抽取标记自动换算为目录中的印刷页码。`verified` 必须有人工可审查的来源与 Claim 范围；不能因 CI 通过而升级。
