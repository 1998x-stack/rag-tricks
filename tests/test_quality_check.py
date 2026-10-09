"""Regression tests for false positives and integrity gaps in the content gate."""
import json
import tempfile
import unittest
from pathlib import Path

from scripts.quality_check import STATUSES, check, parse_page


class QualityCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.write('README.md', '# Home\n')
        self.write('index.md', '# Index\n')
        self.registry = {'schema_version': 1, 'statuses': sorted(STATUSES), 'sources': {}, 'pages': {}}
        self.save_registry()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def save_registry(self):
        self.write('sources/source-map.json', json.dumps(self.registry))

    def report(self):
        return check(self.root)

    def assertClean(self):
        report = self.report()
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['warnings'], [])

    def test_code_and_comments_do_not_create_links_or_headings(self):
        self.write('README.md', '# Home\n`[bad](absent)` and `[[sample]]`\n\n'
                   '```md\n# Home\n[x](bad.md)\n```\n\n'
                   '~~~md\n[[missing]]\n~~~\n\n    [x](no.md)\n\n<!-- [x](none) -->\n')
        self.assertClean()

    def test_inline_reference_image_and_nested_badge_links(self):
        self.write('README.md', '# Home\n[inline](absent.md)\n[ref][r]\n'
                   '![image](missing.png)\n[![badge](badge.svg)](target.md)\n\n[r]: reference.md\n')
        self.assertEqual(len(self.report()['errors']), 5)

    def test_balanced_parentheses_encoded_paths_and_titles(self):
        self.write('a(b).md', '# Parentheses\n')
        self.write('空 格.md', '# 中文\n')
        self.write('README.md', '# Home\n[x](a(b).md "title")\n'
                   '[y](%E7%A9%BA%20%E6%A0%BC.md#%E4%B8%AD%E6%96%87)\n'
                   "[z](<空 格.md> 'another title')\n")
        self.assertClean()

    def test_schemes_are_not_local_files(self):
        self.write('README.md', '# Home\n[web](https://example.org) [mail](mailto:a@b.org) '
                   '[ftp](ftp://example.org) [network](//example.org/path)\n')
        self.assertClean()

    def test_same_page_and_duplicate_heading_anchors(self):
        self.write('README.md', '# Home\n[one](#中文标题) [two](#中文标题-1)\n'
                   '[code](#use-code)\n\n## 中文标题\n## 中文标题\n## Use `code`\n')
        self.assertClean()

    def test_missing_anchor_is_error(self):
        self.write('README.md', '# Home\n[x](index.md#absent) [y](#missing)\n')
        self.assertEqual(len(self.report()['errors']), 2)

    def test_html_explicit_anchor(self):
        self.write('README.md', '# Home\n<a id="custom"></a>\n\n[x](#custom)\n')
        self.assertClean()

    def test_frontmatter_not_treated_as_heading(self):
        path = self.write('README.md', '---\ntitle: demo\n---\n# Home\n')
        self.assertEqual(parse_page(path).headings, [('h1', 'Home')])
        self.assertClean()

    def test_repository_escape_and_directory_link(self):
        self.write('README.md', '# Home\n[x](../outside) [y](sources/)\n')
        self.assertEqual(len(self.report()['errors']), 2)

    def test_ignored_generated_files(self):
        for folder in ('.venv', '_site', 'vendor', 'node_modules', 'raw', 'docs/superpowers'):
            self.write(f'{folder}/bad.md', '# Home\n[x](missing)\n')
        self.assertEqual(self.report()['files'], 2)
        self.assertClean()

    def test_valid_basename_wikilink_warns_about_web(self):
        self.write('notes/unique.md', '# Unique\n')
        self.write('README.md', '# Home\n[[unique]]\n')
        self.assertEqual(self.report()['errors'], [])
        self.assertEqual(len(self.report()['warnings']), 1)

    def test_ambiguous_wikilink_is_error(self):
        self.write('a/name.md', '# A\n')
        self.write('b/name.md', '# B\n')
        self.write('README.md', '# Home\n[[name]]\n')
        self.assertIn('ambiguous', self.report()['errors'][0])

    def test_malformed_top_level_never_crashes(self):
        for data in ([], None, 3, 'invalid', {'statuses': [None], 'sources': [], 'pages': []}):
            with self.subTest(data=data):
                self.write('sources/source-map.json', json.dumps(data))
                self.assertTrue(self.report()['errors'])

    def test_malformed_entries_never_crash(self):
        for entry in ([], None, 4, {'status': [], 'source_refs': [{}]}):
            with self.subTest(entry=entry):
                self.registry['pages'] = {'README.md': entry}
                self.save_registry()
                self.assertTrue(self.report()['errors'])

    def test_unknown_status_cannot_be_authorized_by_registry(self):
        self.registry['statuses'].append('invented')
        self.registry['pages']['README.md'] = {'status': 'invented', 'source_refs': []}
        self.save_registry()
        self.assertEqual(len(self.report()['errors']), 2)

    def test_registry_paths_and_refs(self):
        self.registry['pages'] = {'../out.md': {'status': 'derived', 'source_refs': ['unknown']}}
        self.save_registry()
        self.assertEqual(len(self.report()['errors']), 2)

    def test_verified_requires_evidence_and_sources(self):
        self.registry['pages']['README.md'] = {'status': 'verified', 'source_refs': []}
        self.save_registry()
        self.assertEqual(len(self.report()['errors']), 2)

    def test_inventory_must_match_page_marker(self):
        self.registry['pages']['README.md'] = {'status': 'derived', 'source_refs': []}
        self.save_registry()
        self.assertIn('evidence mismatch', self.report()['errors'][0])

    def test_unregistered_and_orphan_page_are_reported(self):
        self.write('wiki/new.md', '# New\n')
        report = self.report()
        self.assertTrue(any('registration' in e for e in report['errors']))
        self.assertTrue(any('unreachable' in w for w in report['warnings']))
        self.assertTrue(any('来源与证据' in w for w in report['warnings']))

    def test_reachable_registered_page_passes(self):
        self.write('wiki/new.md', '# New\n\n## 来源与证据\n\n- Evidence: Derived\n')
        self.write('index.md', '# Index\n[new](wiki/new.md)\n')
        self.registry['pages']['wiki/new.md'] = {'status': 'derived', 'source_refs': []}
        self.save_registry()
        self.assertClean()

    def test_invalid_json_is_reported(self):
        self.write('sources/source-map.json', '{bad')
        self.assertTrue(self.report()['errors'])

    def test_duplicate_h1_is_warning(self):
        self.write('other.md', '# Home\n')
        self.assertTrue(any('duplicate H1' in w for w in self.report()['warnings']))


if __name__ == '__main__':
    unittest.main()
