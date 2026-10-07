#!/usr/bin/env python3
"""Check export freshness, complete page coverage and internal references."""
from __future__ import annotations
import argparse
import hashlib
import json
import posixpath
import sys
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_manifest import ARTIFACTS, DEPENDENCIES, source_paths

ROOT = Path(__file__).resolve().parents[1]


def read_local(root, name):
    if not isinstance(name, str):
        raise ValueError('File path must be a string')
    path = (root/name).resolve()
    if Path(name).is_absolute() or not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes repository: {name}')
    return path.read_bytes()


def verify_xmind(archive, root, manifest, errors):
    content = json.loads(archive.read('content.json'))
    json.loads(archive.read('metadata.json'))
    file_entries = json.loads(archive.read('manifest.json'))['file-entries']
    for name in file_entries:
        if name not in archive.namelist():
            errors.append(f'XMind manifest missing member: {name}')
    ids, jumps, notes = set(), [], set()
    count = 0
    def walk(topic):
        nonlocal count
        count += 1
        if topic['id'] in ids:
            errors.append('Duplicate XMind topic ID')
        ids.add(topic['id'])
        if not topic.get('title'):
            errors.append('Empty XMind topic title')
        href = topic.get('href', '')
        if href.startswith('xmind:#'):
            jumps.append(href[7:])
        note = topic.get('notes', {}).get('plain', {}).get('content', '')
        notes.add(note.rstrip('\n'))
        for child in topic.get('children', {}).get('attached', []):
            walk(child)
    for sheet in content:
        walk(sheet['rootTopic'])
    for target in jumps:
        if target not in ids:
            errors.append(f'Broken XMind sheet link: {target}')
    if {'sheets': len(content), 'topics': count} != manifest['xmind']:
        errors.append('XMind count mismatch')
    for name in manifest['inputs']:
        if read_local(root, name).decode('utf-8').rstrip('\n') not in notes:
            errors.append(f'XMind missing full source notes: {name}')
    return {'sheets': len(content), 'topics': count, 'sheet_links': len(jumps)}


def verify_epub(archive, chapters, errors):
    members = set(archive.namelist())
    if (archive.namelist()[0] != 'mimetype'
            or archive.getinfo('mimetype').compress_type != zipfile.ZIP_STORED
            or archive.read('mimetype') != b'application/epub+zip'):
        errors.append('EPUB mimetype must be the first, uncompressed entry with the correct value')
    docs = {name: ET.fromstring(archive.read(name)) for name in members
            if name.endswith(('.xhtml', '.opf', '.ncx', '.xml'))}
    ids = {}
    destinations = {}
    for name, doc in docs.items():
        ids[name] = set()
        for node in doc.iter():
            identifier = node.get('id')
            if identifier:
                if identifier in ids[name]:
                    errors.append(f'EPUB duplicate ID: {name}#{identifier}')
                ids[name].add(identifier)
                destinations.setdefault(identifier, []).append((name, node))
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
    # An existing empty div in the previous chapter is NOT a valid page destination.
    for chapter in chapters:
        matches = [(name, node) for name, node in destinations.get(chapter['id'], []) if name.endswith('.xhtml')]
        if len(matches) != 1:
            errors.append(f'EPUB chapter destination missing or ambiguous: {chapter["path"]}')
        else:
            _, node = matches[0]
            # Pandoc transfers heading IDs to a section whose first child is that heading.
            if node.tag.rsplit('}', 1)[-1] == 'section' and len(node):
                node = node[0]
            title = ''.join(node.itertext()).strip()
            if node.tag.rsplit('}', 1)[-1] != 'h2' or title != chapter['title']:
                errors.append(f'EPUB chapter destination is not its article heading: {chapter["path"]}')
    return {'xml_documents': len(docs), 'chapters': len(chapters)}


def inspect(root=ROOT):
    root = root.resolve()
    report = {'errors': [], 'xmind': {}, 'epub': {}}
    errors = report['errors']
    try:
        manifest = json.loads(read_local(root, 'downloads/manifest.json'))
        if not isinstance(manifest, dict) or manifest.get('schema_version') != 2:
            raise ValueError('Export manifest schema_version must be 2; regenerate exports')
        for key in ('inputs', 'dependencies', 'files', 'xmind'):
            if not isinstance(manifest.get(key), dict):
                raise ValueError(f'Export manifest {key} must be an object')
        chapters = manifest.get('chapters')
        if not isinstance(chapters, list) or any(not isinstance(c, dict) or not all(
                isinstance(c.get(k), str) for k in ('path', 'id', 'title')) for c in chapters):
            raise ValueError('Export chapters must list path, id and title')
        expected = source_paths(root)
        if set(manifest['inputs']) != expected:
            errors.append('Export source inventory differs from all wiki pages and required appendices')
        if (set(c['path'] for c in chapters) != expected or len(chapters) != len(expected)
                or manifest.get('pages') != len(expected)):
            errors.append('Export chapter inventory/count mismatch')
        if len({c['id'] for c in chapters}) != len(chapters):
            errors.append('Export chapter IDs must be unique')
        if set(manifest['dependencies']) != set(DEPENDENCIES):
            errors.append('Export dependency inventory incomplete; regenerate exports')
        for category in ('inputs', 'dependencies'):
            for name, checksum in manifest[category].items():
                try:
                    if hashlib.sha256(read_local(root, name)).hexdigest() != checksum:
                        errors.append(f'Stale export {category}: {name}; rerun export_handbook.py')
                except (OSError, ValueError) as exc:
                    errors.append(f'Cannot read export {category}: {exc}')
        if set(manifest['files']) != set(ARTIFACTS):
            errors.append('Export manifest must declare exactly the EPUB and XMind artifacts')
        for name in ARTIFACTS:
            info = manifest['files'].get(name)
            try:
                data = read_local(root, 'downloads/' + name)
                if not isinstance(info, dict) or len(data) != info.get('bytes') or hashlib.sha256(data).hexdigest() != info.get('sha256'):
                    errors.append(f'Export checksum mismatch: {name}')
                with zipfile.ZipFile(root/'downloads'/name) as archive:
                    if len(archive.namelist()) != len(set(archive.namelist())):
                        errors.append(f'Duplicate archive members: {name}')
                    if archive.testzip() is not None:
                        errors.append(f'Corrupt archive member: {name}')
                    if name.endswith('.xmind'):
                        report['xmind'] = verify_xmind(archive, root, manifest, errors)
                    else:
                        report['epub'] = verify_epub(archive, chapters, errors)
            except (OSError, ValueError, KeyError, TypeError, AttributeError, zipfile.BadZipFile,
                    ET.ParseError, RecursionError, IndexError) as exc:
                errors.append(f'Invalid export {name}: {exc}')
    except (OSError, ValueError, TypeError) as exc:
        errors.append(f'Cannot validate export manifest: {exc}')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    report = inspect(args.root)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f'XMind: {report["xmind"]}; EPUB: {report["epub"]}')
        for error in report['errors']:
            print(error)
        print(f'Export verification: {len(report["errors"])} errors')
    return int(bool(report['errors']))


if __name__ == '__main__':
    raise SystemExit(main())
