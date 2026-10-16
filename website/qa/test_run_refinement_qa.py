"""Evidence retention regressions; browser boundaries are mocked, runner is real."""
import asyncio
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import run_refinement_qa as qa


class RefinementEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'site'
        self.root.mkdir()
        (self.root / 'index.html').write_text('fixture')
        self.out = Path(self.temp.name) / 'evidence'
        self.args = SimpleNamespace(root=self.root, out_base=self.out)
        self.server = MagicMock(server_port=12345)
        self.browser = MagicMock(version='mock Chromium')
        self.browser.close = AsyncMock()
        self.browser.new_page = AsyncMock()
        self.playwright = MagicMock()
        self.playwright.__aenter__ = AsyncMock(return_value=SimpleNamespace(
            chromium=SimpleNamespace(launch=AsyncMock(return_value=self.browser))))
        self.playwright.__aexit__ = AsyncMock(return_value=False)

    def invoke(self, serve_error=None):
        with patch.object(qa, 'serve', side_effect=serve_error, return_value=self.server), \
                patch.object(qa, 'free_port', return_value=12345), \
                patch.object(qa, 'async_playwright', return_value=self.playwright), \
                contextlib.redirect_stdout(io.StringIO()):
            return asyncio.run(qa.run(self.args))

    def evidence(self):
        folders = list(self.out.iterdir())
        self.assertEqual(len(folders), 1)
        values = {}
        for name in ('summary', 'checks', 'environment'):
            path = folders[0] / (name + '.json')
            self.assertTrue(path.is_file(), f'missing {name} evidence')
            values[name] = json.loads(path.read_text())
        self.assertEqual(values['environment']['site_sha256'], {
            'index.html': hashlib.sha256(b'fixture').hexdigest()})
        return values

    def test_runtime_error_preserves_partial_checks_and_original_exception(self):
        error = RuntimeError('controlled browser failure')
        async def fail_after_check(*args, **kwargs):
            # Record a real check before the browser boundary fails.
            self.results.add('completed before error', True)
            raise error
        self.results = qa.Results()
        self.browser.new_page.side_effect = fail_after_check
        with patch.object(qa, 'Results', return_value=self.results):
            with self.assertRaises(RuntimeError) as caught:
                self.invoke()
        self.assertIs(caught.exception, error)
        self.server.shutdown.assert_called_once()
        self.server.server_close.assert_called_once()
        evidence = self.evidence()
        self.assertEqual(evidence['checks'][0]['id'], 'completed before error')
        self.assertGreater(evidence['summary']['failed'], 0)
        self.assertEqual(evidence['environment']['exception']['type'], 'RuntimeError')
        self.assertEqual(evidence['environment']['exception']['message'], str(error))

    def test_server_startup_failure_saves_failed_evidence(self):
        error = OSError('controlled startup failure')
        with self.assertRaises(OSError) as caught:
            self.invoke(serve_error=error)
        self.assertIs(caught.exception, error)
        evidence = self.evidence()
        self.assertGreater(evidence['summary']['failed'], 0)
        self.server.shutdown.assert_not_called()

    def configure_pages(self, overflow=False):
        async def new_page(viewport):
            width = viewport['width']
            image = dict(x=0, y=200, right=width, width=300, height=200,
                         naturalWidth=600, naturalHeight=400, complete=True,
                         priority='high', loading='eager')
            geometry = dict(pageWidth=width + int(overflow), ctaBottom=100,
                            image=image, caption='Generated GEM concept; final product colour is not confirmed; Not production photography')
            page = MagicMock()
            for method in ('goto', 'check', 'close', 'screenshot', 'wait_for_timeout'):
                setattr(page, method, AsyncMock())
            async def evaluate(script):
                if 'pageWidth:' in script:
                    return geometry
                if 'window.gemQAContrast=ratio' in script:
                    return 7
                return True
            page.evaluate = AsyncMock(side_effect=evaluate)
            locator = MagicMock()
            locator.hover = AsyncMock()
            locator.scroll_into_view_if_needed = AsyncMock()
            locator.evaluate = AsyncMock(return_value={'ratio': 7})
            async def evaluate_all(script):
                if 'objectFit' in script:
                    return [dict(width=300, height=200, fit='contain')] * 2
                return [[0, 0, 300, 200]]
            locator.evaluate_all = AsyncMock(side_effect=evaluate_all)
            page.locator.return_value = locator
            return page
        self.browser.new_page.side_effect = new_page

    def test_success_retains_fifty_checks_and_zero_exit(self):
        self.configure_pages()
        with patch.object(qa, 'watch', new=AsyncMock(return_value={
                'failed': [], 'console_errors': [], 'page_errors': [], 'requests': []})):
            self.assertFalse(self.invoke())
        evidence = self.evidence()
        self.assertEqual(evidence['summary']['total'], 50)
        self.assertEqual(evidence['summary']['failed'], 0)
        self.assertNotIn('exception', evidence['environment'])
        self.browser.close.assert_awaited_once()
        self.server.shutdown.assert_called_once()
        self.server.server_close.assert_called_once()

    def test_assertion_failure_retains_checks_and_nonzero_exit(self):
        self.configure_pages(overflow=True)
        with patch.object(qa, 'watch', new=AsyncMock(return_value={
                'failed': [], 'console_errors': [], 'page_errors': [], 'requests': []})):
            self.assertTrue(self.invoke())
        evidence = self.evidence()
        self.assertEqual(evidence['summary']['total'], 50)
        self.assertEqual(evidence['summary']['failed'], 4)
        self.assertNotIn('exception', evidence['environment'])
        self.server.shutdown.assert_called_once()
        self.server.server_close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
