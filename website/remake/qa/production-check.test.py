"""Exercise real preview/production builds in disposable directories."""
from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]
ORIGIN = 'https://example.test'


class BuildChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='gem-build-test-')
        self.root = Path(self.temp.name) / 'site'
        shutil.copytree(SOURCE, self.root, ignore=shutil.ignore_patterns('qa', '__pycache__'))

    def tearDown(self):
        self.temp.cleanup()

    def build(self, origin=''):
        env = dict(os.environ, SITE_ORIGIN=origin)
        subprocess.run(['node', 'build.mjs'], cwd=self.root, env=env,
                       check=True, capture_output=True, text=True)

    def check(self, origin=''):
        return subprocess.run(['python3', 'check.py', *(['--origin', origin] if origin else [])],
                              cwd=self.root, capture_output=True, text=True)

    def test_preview(self):
        self.build()
        result = self.check()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_clean_build_preserves_assets_and_removes_stale_output(self):
        shutil.rmtree(self.root / 'dist')
        self.build()
        for name in ['logo-ink.svg', 'arabic.woff2', 'social.png',
                     'conditioner-source.webp', 'format-room-960.webp']:
            self.assertTrue((self.root / 'dist/assets' / name).is_file(), name)
        stale = self.root / 'dist/stale.html'
        stale.write_text('obsolete generated page')
        self.build()
        self.assertFalse(stale.exists())
        self.assertEqual(self.check().returncode, 0)

    def test_production(self):
        self.build(ORIGIN)
        result = self.check(ORIGIN)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_clean_build_retains_pages_preview_policy_and_redirects(self):
        shutil.rmtree(self.root / 'dist')
        self.build()
        headers = self.root / 'dist/_headers'
        redirects = self.root / 'dist/_redirects'
        self.assertTrue(headers.is_file(), 'Clean build lost Pages noindex/form protection')
        self.assertTrue(redirects.is_file(), 'Clean build lost Arabic default/legacy redirects')
        text = headers.read_text()
        self.assertIn('X-Robots-Tag: noindex, nofollow', text)
        self.assertIn("Content-Security-Policy: form-action 'none'", text)
        self.assertIn('X-Content-Type-Options: nosniff', text)
        self.assertIn('Cache-Control: no-cache', text)
        self.assertIn('/ /ar/ 302', redirects.read_text())
        self.assertIn('/privacy.html /en/privacy/ 301', redirects.read_text())
        self.assertIn('/ar/privacy.html /ar/privacy/ 301', redirects.read_text())

    def test_production_metadata_corruption_is_rejected(self):
        changes = [
            ('canonical', 'rel="canonical" href="https://example.test/en/"',
             'rel="canonical" href="https://wrong.test/en/"'),
            ('alternate', 'hreflang="ar" href="https://example.test/ar/"',
             'hreflang="ar" href="https://example.test/en/"'),
            ('robots', 'name="robots" content="index,follow"',
             'name="robots" content="noindex,nofollow"'),
        ]
        for label, old, new in changes:
            with self.subTest(label=label):
                self.build(ORIGIN)
                page = self.root / 'dist/en/index.html'
                text = page.read_text()
                self.assertIn(old, text)
                page.write_text(text.replace(old, new))
                self.assertNotEqual(self.check(ORIGIN).returncode, 0)


if __name__ == '__main__':
    unittest.main()
