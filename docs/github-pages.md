# GitHub Pages 配置与发布手册

## 站点与发布架构

- 仓库：`1998x-stack/rag-tricks`，默认分支 `main`。
- 站点：[RAG Tricks](https://1998x-stack.github.io/rag-tricks/)。
- 发布方式：GitHub Actions，工作流文件 `.github/workflows/pages.yml`。
- 构建：Jekyll Cayman；项目路径 `/rag-tricks`；HTTPS 开启，无自定义域名。
- 下载：站内 `downloads/` 提供 EPUB、XMind 和哈希清单。

```text
main 更新 / 手动运行
    → Python 回归测试
    → Markdown 严格检查
    → 导出新鲜度与包结构验证
    → EPUBCheck 标准校验（固定版本与 SHA-256）
    → Jekyll 构建
    → 最终 HTML 链接与下载验证
    → Pages artifact
    → github-pages 环境部署
```

Pull Request 执行构建和校验，不部署。只有 main 的 push 或手动运行可以进入部署阶段。构建失败时不会替换线上站点。

## 用 gh 配置

以下命令用于该仓库的维护；首次使用先执行 `gh auth status` 确认账号。不要把认证 token 写入配置或日志。

```bash
# 读取当前设置
gh repo view 1998x-stack/rag-tricks --json defaultBranchRef,visibility,url
gh api repos/1998x-stack/rag-tricks/pages

# 已有站点：切换为 Actions 发布
gh api --method PUT repos/1998x-stack/rag-tricks/pages -f build_type=workflow

# 强制 HTTPS
gh api --method PUT repos/1998x-stack/rag-tricks/pages -F https_enforced=true
```

如果 GET 返回 404 且确认尚未创建 Pages，使用 `POST` 创建站点并设置 `build_type=workflow`。现有站点不要重复创建。

GitHub 的 [Pages REST API](https://docs.github.com/en/rest/pages) 和[自定义工作流文档](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)是维护依据，查阅日期为 2026-10-04。

## 配置文件的作用

| 配置 | 作用 |
|---|---|
| `url` | 固定公开域名 `https://1998x-stack.github.io` |
| `baseurl` | 项目站点前缀 `/rag-tricks`，避免子页面引用错误地落到域名根目录 |
| `jekyll-relative-links` | 将 `.md` 相对链接改为构建后的 HTML 路径 |
| `jekyll-optional-front-matter` | 将未带 YAML frontmatter 的历史 Markdown 处理为页面 |
| `include` | 明确包含 README 与 CONTRIBUTING，避免被视为无需渲染的元文件 |
| `defaults.layout` | 使用 handbook 阅读布局，继承 Cayman 并增加主导航、阅读底栏及渐进增强目录 |
| `exclude` | 不将 raw、脚本、测试、工具和本地草稿复制进站点 |

排除 raw 只影响 Pages 构建产物，不移除仓库中的原始文件，也不改变版权状态。

## 工作流权限与发布条件

构建阶段仅需要仓库读取。部署阶段单独授予 `pages: write` 与 `id-token: write`，目标环境为 `github-pages`。工作流使用 `needs: build`，保证部署依赖已成功构建的产物。

同一分支的发布使用并发组串行处理，不取消正在进行的发布。未设置自动提交、自动修改仓库权限或自定义域名。当前规则存在于工作流中；是否要求合并前强制通过检查由仓库分支保护另行决定。

## 检查发布结果

```bash
gh run list --repo 1998x-stack/rag-tricks --workflow pages.yml --limit 5
gh run view <RUN_ID> --repo 1998x-stack/rag-tricks
gh run view <RUN_ID> --repo 1998x-stack/rag-tricks --log-failed
gh api repos/1998x-stack/rag-tricks/pages
```

先确认运行对应的 commit，再确认 build/deploy 均成功。然后检查首页、一个深层知识页、中文锚点和两种下载文件。CDN 更新可能稍有延迟；不要把旧缓存页面的 HTTP 200 当成新版本已发布。

`check_site.py` 校验生成后的本地 HTML、锚点、资源路径以及 baseurl。它不检查外部网站可用性，也不替代浏览器视觉检查。

## 手动重建与恢复

```bash
gh workflow run pages.yml --repo 1998x-stack/rag-tricks --ref main
```

如内容变更引起问题，恢复已知正确的源文件，通过 PR 或常规提交重新运行工作流。不要为了恢复站点而强制重写 main 历史。若导出校验提示 stale source，先按[导出维护说明](exports.md)重新生成离线文件。

## 常见问题

| 现象 | 检查方向 |
|---|---|
| 首页可访问，深层页面 404 | optional-front-matter、相对链接转换、baseurl 与具体构建日志 |
| 链接文件存在但锚点失败 | 标题标点、Unicode、重复标题编号；优先检查构建出的 id |
| deploy 找不到 artifact | upload 是否执行成功、deploy 是否依赖 build、artifact 名称是否一致 |
| 403 / 权限不足 | Pages 设置、Actions 启用状态、部署 job 权限和环境限制 |
| 下载到旧 EPUB | manifest 源哈希是否更新、当前部署 commit 和 CDN 缓存 |
| PR 触发部署 | 检查 deploy 的事件与分支条件，不依赖页面设置猜测行为 |

返回[首页](../index.md) · [下载](../downloads/index.md) · [质量维护](maintenance.md)。
