"""Integration guards for the current English-to-Arabic build; no network/browser."""
import hashlib
import importlib.util
from pathlib import Path
import shutil
import tempfile
import unittest

HERE=Path(__file__).parent
ROOT=HERE.parents[1]

class ArabicBuildTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory()
  self.addCleanup(self.tmp.cleanup)
  self.root=Path(self.tmp.name)
  self.site=self.root/'website/site'
  (self.site/'assets/js').mkdir(parents=True)
  (self.root/'tools/localization').mkdir(parents=True)
  shutil.copyfile(HERE/'website-ar.json',self.root/'tools/localization/website-ar.json')
  for name in ('index','reference','privacy'):
   shutil.copyfile(ROOT/f'website/site/{name}.html',self.site/f'{name}.html')
  spec=importlib.util.spec_from_file_location('build_ar',HERE/'build_website_ar.py')
  self.builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(self.builder)
  self.builder.ROOT=self.root;self.builder.SITE=self.site
 def snapshot(self):
  return {str(p.relative_to(self.site)):hashlib.sha256(p.read_bytes()).hexdigest() for p in self.site.rglob('*') if p.is_file()}
 def test_current_refinement_and_idempotence(self):
  self.builder.build();before=self.snapshot();self.builder.build()
  self.assertEqual(before,self.snapshot())
  self.assertIn('hero-figure',(self.site/'ar/index.html').read_text())
  self.assertIn('GEM-WEB-B01',(self.site/'ar/index.html').read_text())
 def test_unregistered_text_fails_without_partial_outputs(self):
  p=self.site/'privacy.html';p.write_text(p.read_text().replace('</main>','<p>UNREGISTERED OWNER COPY</p></main>'))
  before=self.snapshot()
  with self.assertRaisesRegex(ValueError,'Unregistered string'):self.builder.build()
  self.assertEqual(before,self.snapshot())
 def test_unregistered_accessible_label_fails_without_partial_outputs(self):
  p=self.site/'privacy.html';p.write_text(p.read_text().replace('</main>','<img alt="UNREGISTERED OWNER LABEL" src="assets/test.svg"></main>'))
  before=self.snapshot()
  with self.assertRaisesRegex(ValueError,'Unregistered attribute'):self.builder.build()
  self.assertEqual(before,self.snapshot())

if __name__=='__main__':unittest.main()
