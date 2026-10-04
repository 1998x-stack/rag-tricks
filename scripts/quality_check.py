#!/usr/bin/env python3
"""Check repository links and evidence registration; never certify claim truth."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {'verified', 'partial', 'needs_verification', 'derived', 'external'}
EXCLUDED = {'.git', '.venv', 'venv', 'node_modules', '_site', 'vendor', '.bundle', 'raw'}
PARSER = MarkdownIt('commonmark').enable(['table', 'strikethrough'])
WIKILINK_RE = re.compile(r'\[\[([^\]]+)\]\]')
NUMERIC_CLAIM_RE = re.compile(
    r'\d+(?:\.\d+)?\s*%|\bQPS\b|\bP(?:50|95|99)\b|'
    r'\d+(?:\.\d+)?\s*(?:ms|毫秒|秒|分钟|小时|万|亿|GB|MB|TB)', re.I)


@dataclass
class Page:
    path: Path
    text: str
    links: list[str]
    wikilinks: list[str]
    headings: list[tuple[str, str]]
    anchors: set[str]
    prose: str


def parse_page(path: Path) -> Page:
    text = path.read_text(encoding='utf-8')
    body = re.sub(r'\A---\s*\n.*?\n---\s*(?:\n|$)', '', text, count=1, flags=re.S)
    tokens = PARSER.parse(body)
    links, wikilinks, headings, prose = [], [], [], []
    anchors: set[str] = set()
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            children = tokens[i + 1].children or []
            title = ''.join(t.content for t in children if t.type in {'text', 'code_inline'})
            headings.append((token.tag, title))
            slug = re.sub(r'[^\w\-\s]', '', title.lower()).replace(' ', '-')
            anchor, suffix = slug, 0
            while anchor in anchors:
                suffix += 1
                anchor = f'{slug}-{suffix}'
            anchors.add(anchor)
        if token.type == 'inline':
            for child in token.children or []:
                if child.type == 'link_open':
                    links.append(child.attrGet('href') or '')
                elif child.type == 'image':
                    links.append(child.attrGet('src') or '')
                elif child.type == 'text':
                    prose.append(child.content)
                    wikilinks.extend(WIKILINK_RE.findall(child.content))
                elif child.type == 'html_inline':
                    anchors.update(re.findall(r'\b(?:id|name)=[\"\']([^\"\']+)', child.content))
        elif token.type == 'html_block':
            anchors.update(re.findall(r'\b(?:id|name)=[\"\']([^\"\']+)', token.content))
    return Page(path, text, links, wikilinks, headings, anchors, '\n'.join(prose))


def inside(root: Path, path: Path) -> bool:
    return path.is_relative_to(root)


def local_target(root: Path, source: Path, raw: str) -> tuple[Path, str] | None:
    url = urlsplit(raw)
    if url.scheme or url.netloc:
        return None
    decoded = unquote(url.path)
    if not decoded:
        target = source
    elif decoded.startswith('/'):
        target = root / decoded.lstrip('/')
    else:
        target = source.parent / decoded
    return target.resolve(), unquote(url.fragment)


def resolve_wikilink(root: Path, source: Path, raw: str, pages: dict[Path, Page]) -> Path | None:
    name = raw.split('|', 1)[0].split('#', 1)[0].strip()
    if not name:
        return source
    if not name.endswith('.md'):
        name += '.md'
    for candidate in ((source.parent / name).resolve(), (root / name).resolve()):
        if candidate in pages:
            return candidate
    if '/' not in name:
        matches = [p for p in pages if p.name == name]
        if len(matches) == 1:
            return matches[0]
    return None


def check_source_map(root: Path, pages: dict[Path, Page], errors: list[str], warnings: list[str]) -> dict:
    try:
        data = json.loads((root / 'sources/source-map.json').read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        errors.append(f'cannot read source-map: {exc}')
        return {}
    if not isinstance(data, dict):
        errors.append('source-map must be an object')
        return {}
    if type(data.get('schema_version')) is not int or data['schema_version'] != 1:
        errors.append('source-map schema_version must be 1')
    statuses = data.get('statuses')
    if not isinstance(statuses, list) or any(not isinstance(s, str) for s in statuses):
        errors.append('source-map statuses must be a list of strings')
    elif set(statuses) != STATUSES or len(statuses) != len(STATUSES):
        errors.append('source-map statuses must contain each supported status exactly once')
    sources, entries = data.get('sources'), data.get('pages')
    if not isinstance(sources, dict) or not isinstance(entries, dict):
        errors.append('source-map sources and pages must be objects')
        return {}
    for name, source in sources.items():
        if not isinstance(source, dict) or not isinstance(source.get('title'), str) or not source['title'].strip():
            errors.append(f'source-map source {name}: nonempty title required')
    for name, entry in entries.items():
        target = (root / name).resolve()
        if not inside(root, target) or Path(name).is_absolute() or '..' in Path(name).parts:
            errors.append(f'source-map invalid page path: {name}')
        elif target not in pages:
            errors.append(f'source-map references missing Markdown page: {name}')
        if not isinstance(entry, dict):
            errors.append(f'source-map entry must be an object: {name}')
            continue
        status = entry.get('status')
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f'source-map invalid status for {name}: {status!r}')
            status = ''
        refs = entry.get('source_refs')
        if not isinstance(refs, list) or any(not isinstance(r, str) for r in refs):
            errors.append(f'source-map source_refs must be a list of strings: {name}')
        else:
            for ref in refs:
                if ref not in sources:
                    errors.append(f'source-map unknown source ref for {name}: {ref}')
            if status in {'verified', 'partial', 'external'} and not refs:
                errors.append(f'source-map {status} page requires source_refs: {name}')
        if status in {'verified', 'partial'} and not entry.get('evidence'):
            errors.append(f'source-map {status} page requires evidence locators: {name}')
        if target in pages:
            expected = {'needs_verification': 'Unverified', 'derived': 'Derived', 'external': 'External'}.get(status)
            if expected and f'Evidence: {expected}' not in pages[target].text:
                errors.append(f'source-map/page evidence mismatch: {name} requires Evidence: {expected}')
    for path, page in pages.items():
        name = path.relative_to(root).as_posix()
        if name.startswith('wiki/') or name == 'contradictory.md':
            if name not in entries:
                errors.append(f'knowledge page missing source-map registration: {name}')
            if ('h2', '来源与证据') not in page.headings:
                warnings.append(f'missing 来源与证据: {name} ({len(NUMERIC_CLAIM_RE.findall(page.prose))} numeric markers)')
    return entries


def check(root: Path) -> dict:
    root = root.resolve()
    pages = {p.resolve(): parse_page(p.resolve()) for p in sorted(root.rglob('*.md'))
             if p.relative_to(root).parts[:2] != ('docs', 'superpowers')
             and not any(part in EXCLUDED or part.startswith('.') for part in p.relative_to(root).parts)}
    errors: list[str] = []
    warnings: list[str] = []
    titles: dict[str, list[str]] = defaultdict(list)
    link_count = 0
    graph: dict[Path, set[Path]] = defaultdict(set)
    for path, page in pages.items():
        name = path.relative_to(root).as_posix()
        h1s = [t for tag, t in page.headings if tag == 'h1']
        if len(h1s) != 1:
            warnings.append(f'expected one H1: {name} (found {len(h1s)})')
        for title in h1s:
            titles[title].append(name)
        for raw in page.links:
            link_count += 1
            try:
                result = local_target(root, path, raw)
            except ValueError:
                errors.append(f'invalid link URL: {name} -> {raw}')
                continue
            if result is None:
                continue
            target, fragment = result
            if not inside(root, target):
                errors.append(f'link escapes repository: {name} -> {raw}')
            elif not target.exists():
                errors.append(f'broken markdown link: {name} -> {raw}')
            elif target.is_dir():
                errors.append(f'link must point to a file: {name} -> {raw}')
            elif target in pages:
                graph[path].add(target)
                if fragment and fragment not in pages[target].anchors:
                    errors.append(f'broken heading anchor: {name} -> {raw}')
        for raw in page.wikilinks:
            target = resolve_wikilink(root, path, raw, pages)
            if target is None:
                errors.append(f'unresolved or ambiguous wikilink: {name} -> [[{raw}]]')
            else:
                graph[path].add(target)
                # A valid Obsidian link still needs web-compatible navigation.
                warnings.append(f'wikilink is not web navigation: {name} -> [[{raw}]]')
    for title, names in sorted(titles.items()):
        if len(names) > 1:
            warnings.append(f'duplicate H1 {title!r}: {", ".join(names)}')
    visited, pending = set(), [root / 'index.md', root / 'README.md']
    while pending:
        current = pending.pop()
        if current not in visited:
            visited.add(current)
            pending.extend(graph[current] - visited)
    for path in pages:
        if path.relative_to(root).parts[0] == 'wiki' and path not in visited:
            warnings.append(f'unreachable knowledge page: {path.relative_to(root)}')
    entries = check_source_map(root, pages, errors, warnings)
    counts = Counter(e.get('status') for e in entries.values()
                     if isinstance(e, dict) and isinstance(e.get('status'), str))
    return {'files': len(pages), 'links': link_count, 'evidence_statuses': dict(sorted(counts.items())),
            'errors': errors, 'warnings': warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--strict', action='store_true', help='fail on warnings as well as errors')
    parser.add_argument('--json', action='store_true', help='emit machine-readable report')
    args = parser.parse_args()
    report = check(args.root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Checked {report['files']} Markdown files and {report['links']} links.")
        print('Evidence inventory (not factual verification): ' + json.dumps(report['evidence_statuses']))
        for kind in ('warnings', 'errors'):
            print(f"\n{kind.upper()} ({len(report[kind])})")
            for item in report[kind]:
                print(f'- {item}')
    return int(bool(report['errors'] or (args.strict and report['warnings'])))


if __name__ == '__main__':
    sys.exit(main())
