import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync, existsSync, statSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const dist = path.join(root, 'dist');
test('all five readers retain 241 pages and exact hosted bytes', () => {
  const manifest = JSON.parse(readFileSync(path.join(dist, 'manifest.json')));
  assert.equal(manifest.documents.length, 5);
  assert.equal(manifest.documents.reduce((n,d) => n+d.pages,0),241);
  for (const d of manifest.documents) {
    const pdf = path.join(dist,d.pdf);
    assert.ok(statSync(pdf).size < 25*1024*1024);
    assert.equal(createHash('sha256').update(readFileSync(pdf)).digest('hex'),d.pdfSha256);
    assert.match(d.originalUrl,/4bcaaf48b55d27084186e3e1c0ef7f2e69362b8a/);
    for (const lang of ['ar','en']) assert.ok(existsSync(path.join(dist,lang,'documents',d.id,'index.html')));
  }
  assert.equal(manifest.documents.find(d=>d.id==='part-e').pdfSha256,'29b79ebd4693af7c3e584a5cfce2f06180d0cb4514931f8fbe433708a676b12d');
  assert.deepEqual(manifest.documents.find(d=>d.id==='part-a').arabicSlides,[37,38,39,65,66,68]);
  assert.deepEqual(manifest.documents.find(d=>d.id==='part-b').arabicSlides,[9]);
});
test('noindex, Arabic default, on-demand readers and restricted-asset exclusion',()=>{
  assert.match(readFileSync(path.join(dist,'_headers'),'utf8'),/X-Robots-Tag: noindex/);
  assert.match(readFileSync(path.join(dist,'robots.txt'),'utf8'),/Disallow: \/$/m);
  assert.match(readFileSync(path.join(dist,'_redirects'),'utf8'),/^\/ \/ar\/ 302/m);
  for(const lang of ['ar','en']){
    const html=readFileSync(path.join(dist,lang,'index.html'),'utf8');
    assert.ok(!html.includes('<iframe'));
    assert.ok(!/rel="(?:preload|prefetch)"/.test(html));
    assert.match(html,new RegExp(`lang="${lang}" dir="${lang==='ar'?'rtl':'ltr'}"`));
    assert.match(html,/property="og:image" content="https:\/\/gemassets\.mish3l\.com\/assets\/social\.png"/);
    assert.match(html,/name="twitter:card" content="summary_large_image"/);
    assert.ok(!/restricted-internal|ArabicFirstPage|BilingualFirstPage/.test(html));
  }
  assert.ok(existsSync(path.join(dist,'pdfjs/build/pdf.worker.mjs')));
  assert.ok(existsSync(path.join(dist,'pdfjs/web/locale/ar/viewer.ftl')));
});
