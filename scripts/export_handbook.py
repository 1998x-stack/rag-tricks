#!/usr/bin/env python3
"""Build the complete EPUB source and detailed XMind outline from the wiki."""
from __future__ import annotations
import hashlib
import html
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parent))
from quality_check import PARSER, ROOT, local_target, parse_page, markdown_body
from export_manifest import APPENDICES, ARTIFACTS, DEPENDENCIES, EDITION, source_paths

BUILD = ROOT / '.build'
OUT = ROOT / 'downloads'
SITE = 'https://1998x-stack.github.io/rag-tricks/'
GROUPS = [
 ('introduction', '01 基础与技术边界'), ('architecture', '02 系统架构'),
 ('data-layer', '03 数据处理与治理'), ('indexing', '04 索引构建与优化'),
 ('retrieval', '05 检索策略'), ('generation', '06 生成与质量控制'),
 ('evaluation', '07 评估、实验与排障'), ('business-cases', '08 业务案例'),
 ('ops-and-reliability', '09 运维与可靠性'), ('cost-and-efficiency', '10 成本与效率'),
 ('advanced-topics', '11 高级专题'),
]


def key(path):
    return 'p-' + hashlib.sha256(path.relative_to(ROOT).as_posix().encode()).hexdigest()[:12]


def plain(tokens):
    return ''.join(' ' if t.type in {'softbreak', 'hardbreak'} else t.content
                   for t in tokens if t.type in {'text', 'code_inline', 'softbreak', 'hardbreak'})


def short(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text if len(text) <= 52 else text[:51] + '…'


def page_node(path, registry):
    """Headings form the hierarchy; all paragraphs, list items and table rows retain notes."""
    page = parse_page(path)
    state = registry.get(str(path.relative_to(ROOT)), {}).get('status', 'reference')
    label = {'needs_verification': 'Unverified · 待核验', 'derived': 'Derived · 工程建议',
             'external': 'External · 外部依据'}.get(state, '来源与维护')
    root = {'title': page.headings[0][1], 'labels': [label], 'note': page.text,
            'href': SITE + path.relative_to(ROOT).with_suffix('.html').as_posix(), 'children': []}
    tokens = PARSER.parse(markdown_body(page.text))
    stack = [(1, root)]
    row = None
    items = []
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            level = int(token.tag[1])
            if level == 1:
                continue
            while len(stack) > 1 and stack[-1][0] >= level:
                stack.pop()
            child = {'title': plain(tokens[i+1].children or []), 'children': []}
            stack[-1][1]['children'].append(child)
            stack.append((level, child))
        elif token.type == 'list_item_open':
            child = {'title': '列表项', 'children': []}
            (items[-1] if items else stack[-1][1])['children'].append(child)
            items.append(child)
        elif token.type == 'list_item_close':
            items.pop()
        elif token.type == 'tr_open':
            row = []
        elif token.type == 'tr_close' and row:
            content = ' | '.join(row)
            (items[-1] if items else stack[-1][1])['children'].append({'title': short(content), 'note': content})
            row = None
        elif token.type == 'inline' and (i == 0 or tokens[i-1].type != 'heading_open'):
            text = plain(token.children or []).strip()
            if not text:
                continue
            if row is not None:
                row.append(text)
            elif items and items[-1]['title'] == '列表项':
                items[-1].update(title=short(text), note=text)
            else:
                (items[-1] if items else stack[-1][1])['children'].append({'title': short(text), 'note': text})
        elif token.type in {'fence', 'code_block'}:
            (items[-1] if items else stack[-1][1])['children'].append({'title': '代码 / 配置示例', 'note': token.content})
    return root


def render_page(path, selected):
    page = parse_page(path)
    text = markdown_body(page.text)
    # GitHub admonition labels are rendered as prose by CommonMark; use readable print labels.
    text = re.sub(r'^> \[!WARNING\]\s*$', '> **证据提示**', text, flags=re.M)
    tokens = PARSER.parse(text)
    used = set()
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            title = plain(tokens[i+1].children or [])
            slug = re.sub(r'[^\w\-\s]', '', title.lower()).replace(' ', '-')
            anchor, suffix = slug, 0
            while anchor in used:
                suffix += 1
                anchor = f'{slug}-{suffix}'
            used.add(anchor)
            token.attrSet('id', key(path) if token.tag == 'h1' else key(path) + '--' + anchor)
            token.tag = f'h{min(int(token.tag[1])+1,6)}'
        elif token.type == 'heading_close':
            token.tag = f'h{min(int(token.tag[1])+1,6)}'
        for child in token.children or []:
            if child.type != 'link_open':
                continue
            raw = child.attrGet('href') or ''
            target = local_target(ROOT, path, raw)
            if target is None:
                continue
            dest, frag = target
            if dest in selected:
                first_title = parse_page(dest).headings[0][1]
                first_slug = re.sub(r'[^\w\-\s]', '', first_title.lower()).replace(' ', '-')
                href = '#' + key(dest) + ('--' + frag if frag and frag != first_slug else '')
            else:
                relative = dest.relative_to(ROOT).as_posix()
                if relative.endswith('.md'):
                    relative = relative[:-3] + '.html'
                href = SITE + quote(relative) + ('#' + quote(frag) if frag else '')
            child.attrSet('href', href)
    source = html.escape(path.relative_to(ROOT).as_posix())
    return (PARSER.renderer.render(tokens, PARSER.options, {})
            + f'<p class="source-line">仓库章节：{source}</p>')


def finish_xmind(outlines):
    path = OUT/'rag-tricks-detailed.xmind'
    with zipfile.ZipFile(path) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    sheets = json.loads(members['content.json'])
    palette = ['#276678', '#477A69', '#826645', '#5F6588', '#347C87', '#966B59']
    def decorate(topic, source, depth, color):
        if source.get('href'):
            topic['href'] = source['href']
        props = {'fo:font-family': 'sans-serif', 'fo:font-size': '13pt',
                 'fo:color': '#20303B', 'line-color': color}
        if depth == 0:
            props.update({'svg:fill': '#102B3B', 'fo:color': '#FFFFFF', 'fo:font-size': '24pt'})
            topic['structureClass'] = 'org.xmind.ui.logic.right'
        elif depth == 1:
            props.update({'svg:fill': color, 'fo:color': '#FFFFFF', 'fo:font-size': '16pt'})
        elif depth == 2:
            props.update({'svg:fill': '#EDF3F2', 'fo:font-size': '13pt'})
            if topic.get('children'):
                topic['branch'] = 'folded'
        topic['style'] = {'properties': props}
        children = topic.get('children', {}).get('attached', [])
        for idx, (child, data) in enumerate(zip(children, source.get('children', []))):
            decorate(child, data, depth+1, palette[idx % len(palette)] if depth == 0 else color)
    for sheet, outline in zip(sheets, outlines):
        decorate(sheet['rootTopic'], outline, 0, palette[0])
    # Overview branches jump directly to the corresponding detailed sheet root.
    for branch, sheet in zip(sheets[0]['rootTopic']['children']['attached'], sheets[1:]):
        branch['href'] = 'xmind:#' + sheet['rootTopic']['id']
    members['content.json'] = json.dumps(sheets, ensure_ascii=False).encode()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    def size(topic):
        return 1 + sum(size(c) for c in topic.get('children', {}).get('attached', []))
    return {'sheets': len(sheets), 'topics': sum(size(s['rootTopic']) for s in sheets)}


def main():
    BUILD.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    registry = json.loads((ROOT/'sources/source-map.json').read_text())['pages']
    groups = []
    for folder, title in GROUPS:
        files = sorted((ROOT/'wiki'/folder).glob('*.md'))
        main_path = ROOT/'wiki'/folder/(folder+'.md')
        if main_path in files:
            files.remove(main_path)
            files.insert(0, main_path)
        groups.append((title, files))
    groups.append(('12 设计权衡与证据附录', [ROOT/p for p in APPENDICES]))
    selected = {p for _, files in groups for p in files}
    expected = {ROOT/p for p in source_paths(ROOT)}
    if selected != expected:
        raise ValueError(f'Export section configuration omits pages: {expected - selected}')
    overview = {'title': 'RAG TRICKS｜工程知识地图', 'note':
        f'{EDITION} 详细版。先读证据标记，再进入主题工作表。历史指标未逐条验证；完整正文保留在主题备注与 EPUB 中。',
        'children': []}
    sheets = [overview]
    for title, files in groups:
        nodes = [page_node(p, registry) for p in files]
        overview['children'].append({'title': title, 'children': [
            {'title': n['title'], 'labels': n['labels'], 'href': n['href'],
             'note': '详细内容见对应主题工作表；点击链接可访问在线章节。'} for n in nodes]})
        sheets.append({'title': title, 'children': nodes, 'note':
            '标题为导航摘要；长段落的全文在备注中。Unverified 表示尚未逐条核验，不能将历史数值当作统一门槛。'})
    (BUILD/'outline.json').write_text(json.dumps(sheets, ensure_ascii=False, indent=2))
    body = ['<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"/>'
            '<title>RAG Tricks：RAG 工程知识手册</title></head><body>',
            '<h1 id="reading-guide">阅读指南</h1><p>2026 年 10 月 · 详细工程版</p>',
            '<p>本书收录完整知识库正文，按基础、架构、数据、索引、检索、生成、评估、案例、运维、成本和高级专题编排。'
            '技术段落与来源说明均保留；不附第三方原始 PDF。</p>',
            '<blockquote><p>历史 63 篇知识页仍为 Unverified。名称、事故、成本和性能数字尚未逐条独立核验。'
            '新增工程流程标记 Derived，外部指标依据标记 External。结构检查通过不等于事实认证。</p></blockquote>',
            '<p>首次阅读按目录学习；设计系统时先建立评估基线；排障时先保存失败样本。'
            '书内章节引用可点击跳转，外部资料需要联网。导图长节点保留完整备注。</p>',
            '<p>编辑整理：RAG Tricks 项目维护者。原始材料权利归原权利人；本书不宣称获得原始材料的再分发许可。</p>']
    for title, files in groups:
        body.append('<h1>'+html.escape(title)+'</h1>')
        body.extend(render_page(p, selected) for p in files)
    body.append('</body></html>')
    (BUILD/'handbook.html').write_text('\n'.join(body))
    subprocess.run(['pandoc', str(BUILD/'handbook.html'), '-f', 'html', '-t', 'epub3',
        '-o', str(OUT/'rag-tricks-handbook.epub'), '--toc', '--toc-depth=3', '--split-level=2',
        '--css', str(ROOT/'assets/exports/epub.css'), '--epub-cover-image', str(ROOT/'assets/exports/cover.png'),
        '-M', 'title=RAG Tricks：RAG 工程知识手册', '-M', 'subtitle=可追溯 · 可验证 · 面向生产实践',
        '-M', 'toc-title=目录', '-M', 'abstract-title=摘要',
        '-M', 'author=RAG Tricks 项目维护者', '-M', 'lang=zh-CN', '-M', f'date={EDITION}',
        '-M', 'rights=原始材料权利归各自权利人；历史内容仍待逐条核验。'], check=True)
    subprocess.run(['node', str(ROOT/'tools/export/xmind.cjs')], check=True)
    xmind_counts = finish_xmind(sheets)
    manifest = {'schema_version': 2, 'edition': EDITION, 'pages': len(selected), 'sections': len(groups),
                'chapters': [{'path': str(p.relative_to(ROOT)), 'id': key(p), 'title': parse_page(p).headings[0][1]} for _, files in groups for p in files],
                'dependencies': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in DEPENDENCIES},
                'xmind': xmind_counts, 'inputs': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(selected)},
                'files': {p.name: {'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in (OUT/name for name in ARTIFACTS)}}
    (OUT/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(f'Exported {len(selected)} pages across {len(groups)} sections; {len(sheets)} XMind sheets.')


if __name__ == '__main__':
    main()
