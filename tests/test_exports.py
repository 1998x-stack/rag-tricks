"""Verify destinations, outline structure and corrupt/stale export diagnostics."""
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from xml.etree import ElementTree as ET

from scripts import export_handbook as exporter
from scripts.check_exports import inspect, read_local, verify_epub, verify_xmind


class ExportRenderingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.patcher = patch.object(exporter, 'ROOT', self.root)
        self.patcher.start()
        self.addCleanup(self.patcher.stop)
        self.page = self.root/'one.md'

    def test_page_destination_is_heading_not_preceding_empty_div(self):
        self.page.write_text('# 文章标题\n\n## 细节\n\n正文\n')
        rendered = exporter.render_page(self.page, {self.page})
        dom = ET.fromstring('<body>'+rendered+'</body>')
        self.assertEqual(dom[0].tag, 'h2')
        self.assertEqual(dom[0].get('id'), exporter.key(self.page))
        self.assertEqual(dom[0].text, '文章标题')

    def test_page_and_h1_links_share_correct_destination(self):
        self.page.write_text('# 文章\n\n[整篇](one.md) [标题](#文章) [章节](#细节)\n\n## 细节\n')
        rendered = exporter.render_page(self.page, {self.page})
        dom = ET.fromstring('<body>'+rendered+'</body>')
        hrefs = [e.get('href') for e in dom.iter('a')]
        key = exporter.key(self.page)
        self.assertEqual(hrefs, ['#'+key, '#'+key, '#'+key+'--细节'])

    def test_frontmatter_excluded_from_outline_and_epub(self):
        self.page.write_text('---\ntitle: hidden-metadata\n---\n# Visible\n\nText\n')
        node = exporter.page_node(self.page, {})
        self.assertNotIn('hidden-metadata', json.dumps(node['children']))
        self.assertNotIn('hidden-metadata', exporter.render_page(self.page, {self.page}))
        self.assertIn('hidden-metadata', node['note'])  # Full source remains intact.

    def test_nested_lists_preserve_parent_child_relationship(self):
        self.page.write_text('# Outline\n\n## Steps\n\n- Parent\n  - Child\n    - Grandchild\n- Sibling\n')
        section = exporter.page_node(self.page, {})['children'][0]
        self.assertEqual([n['title'] for n in section['children']], ['Parent', 'Sibling'])
        self.assertEqual(section['children'][0]['children'][0]['title'], 'Child')
        self.assertEqual(section['children'][0]['children'][0]['children'][0]['title'], 'Grandchild')

    def test_soft_line_break_does_not_join_words(self):
        tokens = exporter.PARSER.parseInline('first\nsecond')[0].children
        self.assertEqual(exporter.plain(tokens), 'first second')

    def test_metric_formula_survives_table_rendering(self):
        self.page.write_text('# Metrics\n\n| Metric | Definition |\n|---|---|\n| Recall | `count(S ∩ R) / count(R)` |\n')
        dom = ET.fromstring('<body>'+exporter.render_page(self.page, {self.page})+'</body>')
        self.assertIn('count(S ∩ R) / count(R)', ''.join(dom.itertext()))


class ExportValidationTests(unittest.TestCase):
    def archive(self, xhtml, extra=None):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as z:
            z.writestr('mimetype', b'application/epub+zip')
            z.writestr('EPUB/page.xhtml', xhtml)
            for name, content in (extra or {}).items():
                z.writestr(name, content)
        data.seek(0)
        archive = zipfile.ZipFile(data)
        self.addCleanup(archive.close)
        return archive

    def test_existing_but_wrong_chapter_anchor_is_rejected(self):
        errors = []
        verify_epub(self.archive('<html><body><h2>Previous</h2><div id="article"/></body></html>'),
                    [{'id': 'article', 'title': 'Correct', 'path': 'article.md'}], errors)
        self.assertTrue(any('not its article heading' in e for e in errors))

    def test_correct_chapter_heading_and_link_pass(self):
        errors = []
        verify_epub(self.archive('<html><body><h2 id="article">Correct</h2><a href="#article">Go</a></body></html>'),
                    [{'id': 'article', 'title': 'Correct', 'path': 'article.md'}], errors)
        self.assertEqual(errors, [])

    def test_pandoc_section_destination_starts_with_its_heading(self):
        errors = []
        verify_epub(self.archive('<html><section id="article"><h2>Correct</h2><p>Body</p></section></html>'),
                    [{'id': 'article', 'title': 'Correct', 'path': 'article.md'}], errors)
        self.assertEqual(errors, [])

    def test_duplicate_id_and_missing_resource_reported(self):
        errors = []
        verify_epub(self.archive('<html><h2 id="a"/><p id="a"/><img src="absent.png"/></html>'), [], errors)
        self.assertTrue(any('duplicate ID' in e for e in errors))
        self.assertTrue(any('missing resource' in e for e in errors))

    def test_missing_chapter_rejected(self):
        errors = []
        verify_epub(self.archive('<html/>'), [{'id':'missing','title':'Missing','path':'missing.md'}], errors)
        self.assertTrue(any('destination missing' in e for e in errors))

    def test_mimetype_check_is_explicit_not_assert(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as z:
            z.writestr('mimetype', b'wrong')
        data.seek(0)
        with zipfile.ZipFile(data) as z:
            errors = []
            verify_epub(z, [], errors)
        self.assertTrue(any('mimetype' in e for e in errors))

    def test_malformed_manifest_returns_diagnostic(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'downloads').mkdir()
            for value in ('{invalid', '[]', '{}', '{"schema_version":2,"inputs":[]}'):
                (root/'downloads/manifest.json').write_text(value)
                self.assertTrue(inspect(root)['errors'])

    def test_missing_manifest_returns_diagnostic(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertTrue(inspect(Path(directory))['errors'])

    def test_manifest_paths_cannot_escape_root(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                read_local(Path(directory), '../outside.txt')

    def test_stale_dependency_and_corrupt_archives_return_diagnostics(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'downloads').mkdir()
            (root/'style.css').write_text('changed')
            for name in ('rag-tricks-handbook.epub', 'rag-tricks-detailed.xmind'):
                (root/'downloads'/name).write_bytes(b'not a zip')
            data = {'schema_version':2,'inputs':{},'dependencies':{'style.css':'old'},
                    'files':{},'xmind':{},'chapters':[],'pages':0}
            (root/'downloads/manifest.json').write_text(json.dumps(data))
            report = inspect(root)
            self.assertTrue(any('Stale export dependencies' in e for e in report['errors']))
            self.assertEqual(sum('Invalid export' in e for e in report['errors']), 2)
