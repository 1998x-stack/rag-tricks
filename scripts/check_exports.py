#!/usr/bin/env python3
"""Check export freshness, package structure and internal references."""
import hashlib
import json
import posixpath
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def check():
    errors = []
    manifest = json.loads((ROOT/'downloads/manifest.json').read_text())
    for name, checksum in manifest['inputs'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != checksum:
            errors.append(f'Stale export source: {name}; rerun export_handbook.py')
    expected = {str(p.relative_to(ROOT)) for p in (ROOT/'wiki').rglob('*.md')}
    if not expected.issubset(manifest['inputs']):
        errors.append('Not all wiki pages are covered by exports')
    for name, info in manifest['files'].items():
        data = (ROOT/'downloads'/name).read_bytes()
        if len(data) != info['bytes'] or hashlib.sha256(data).hexdigest() != info['sha256']:
            errors.append(f'Export checksum mismatch: {name}')
    with zipfile.ZipFile(ROOT/'downloads/rag-tricks-detailed.xmind') as archive:
        assert archive.testzip() is None
        content = json.loads(archive.read('content.json'))
        json.loads(archive.read('metadata.json'))
        file_entries = json.loads(archive.read('manifest.json'))['file-entries']
        for name in file_entries:
            if name not in archive.namelist():
                errors.append(f'XMind manifest missing member: {name}')
        ids, jumps = set(), []
        count = 0
        def walk(topic):
            nonlocal count
            count += 1
            if topic['id'] in ids:
                errors.append('Duplicate XMind topic ID')
            ids.add(topic['id'])
            if not topic.get('title'):
                errors.append('Empty XMind topic title')
            if topic.get('href', '').startswith('xmind:#'):
                jumps.append(topic['href'][7:])
            for child in topic.get('children', {}).get('attached', []):
                walk(child)
        for sheet in content:
            walk(sheet['rootTopic'])
        for target in jumps:
            if target not in ids:
                errors.append(f'Broken XMind sheet link: {target}')
        if {'sheets': len(content), 'topics': count} != manifest['xmind']:
            errors.append('XMind count mismatch')
        print(f'XMind: {len(content)} sheets, {count} topics, {len(jumps)} sheet links')
    with zipfile.ZipFile(ROOT/'downloads/rag-tricks-handbook.epub') as archive:
        assert archive.testzip() is None
        assert archive.namelist()[0] == 'mimetype'
        assert archive.getinfo('mimetype').compress_type == zipfile.ZIP_STORED
        assert archive.read('mimetype') == b'application/epub+zip'
        members = set(archive.namelist())
        docs = {name: ET.fromstring(archive.read(name)) for name in members
                if name.endswith(('.xhtml', '.opf', '.ncx', '.xml'))}
        ids = {name: {node.get('id') for node in doc.iter() if node.get('id')}
               for name, doc in docs.items()}
        for name, doc in docs.items():
            for node in doc.iter():
                for attr in ('href', 'src'):
                    raw = node.get(attr)
                    if not raw:
                        continue
                    url = urlsplit(raw)
                    if url.scheme or url.netloc:
                        continue
                    target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path))) if url.path else name
                    if target not in members:
                        errors.append(f'EPUB missing resource: {name} -> {raw}')
                    elif url.fragment and target in ids and unquote(url.fragment) not in ids[target]:
                        errors.append(f'EPUB missing anchor: {name} -> {raw}')
        print(f'EPUB: {len(docs)} XML/XHTML documents checked')
    for error in errors:
        print(error)
    print(f'Export verification: {len(errors)} errors')
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(check())
