import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from scripts.check_site import validate


class SiteCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, content=''):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def check(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            failed = validate(self.root, '/rag-tricks')
        return failed, output.getvalue()

    def test_baseurl_directory_and_unicode_anchor(self):
        self.write('index.html', '<a href="/rag-tricks/deep/#%E4%B8%AD%E6%96%87">Go</a>')
        self.write('deep/index.html', '<h2 id="中文">标题</h2>')
        self.assertFalse(self.check()[0])

    def test_missing_baseurl_and_resource(self):
        self.write('index.html', '<a href="/deep/">Go</a><script src="missing.js"></script>')
        failed, output = self.check()
        self.assertTrue(failed)
        self.assertIn('omits baseurl', output)
        self.assertIn('missing destination', output)

    def test_missing_and_duplicate_anchors(self):
        self.write('index.html', '<h2 id="a">A</h2><h2 id="a">B</h2><a href="#b">B</a>')
        failed, output = self.check()
        self.assertTrue(failed)
        self.assertIn('duplicate id', output)
        self.assertIn('missing anchor', output)

    def test_malformed_url_is_diagnostic(self):
        self.write('index.html', '<a href="http://[broken">Bad</a>')
        self.assertIn('malformed URL', self.check()[1])

    def test_no_html_and_accidental_raw_publication_rejected(self):
        self.write('raw/private.txt', 'source')
        failed, output = self.check()
        self.assertTrue(failed)
        self.assertIn('No HTML', output)
        self.assertIn('Raw source files', output)

    def test_relative_escape_rejected(self):
        self.write('index.html', '<a href="../outside.html">Outside</a>')
        self.assertIn('escapes site', self.check()[1])
