#!/usr/bin/env python3
"""Validate local destinations and fragments in the rendered Pages artifact."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import argparse


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.links = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ('id', 'name'):
            if key in attrs:
                self.ids.add(attrs[key])
        if tag in {'a', 'img', 'link', 'script'}:
            value = attrs.get('href', attrs.get('src'))
            if value:
                self.links.append(value)


def validate(root, baseurl):
    root = root.resolve()
    pages = {p: Document(p.read_text(encoding='utf-8')) for p in root.rglob('*.html')}
    errors = []
    for page, doc in pages.items():
        for raw in doc.links:
            url = urlsplit(raw)
            if url.scheme or url.netloc:
                continue
            name = unquote(url.path)
            if name.startswith('/'):
                if baseurl and not (name == baseurl or name.startswith(baseurl + '/')):
                    errors.append(f'{page.relative_to(root)}: link omits baseurl: {raw}')
                    continue
                name = name[len(baseurl):].lstrip('/')
                target = (root / name).resolve()
            else:
                target = (page.parent / name).resolve() if name else page
            if not target.is_relative_to(root):
                errors.append(f'{page.relative_to(root)}: link escapes site: {raw}')
                continue
            if target.is_dir():
                target /= 'index.html'
            if not target.is_file():
                errors.append(f'{page.relative_to(root)}: missing destination: {raw}')
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                errors.append(f'{page.relative_to(root)}: missing anchor: {raw}')
    if not pages:
        errors.append('No HTML pages found')
    if (root/'raw').exists():
        errors.append('Raw source files must not be in the Pages artifact')
    print(f'Checked {len(pages)} rendered HTML pages; {len(errors)} errors.')
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--baseurl', default='/rag-tricks')
    args = parser.parse_args()
    raise SystemExit(validate(args.directory, args.baseurl.rstrip('/')))
