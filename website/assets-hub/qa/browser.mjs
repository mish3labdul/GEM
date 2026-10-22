import {chromium,firefox} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const origin=process.env.HUB_URL||'http://localhost:4318';
const results=[];
fs.mkdirSync(path.join(root,'qa/screenshots'),{recursive:true});
const docs=[['part-a',80],['part-d',24],['part-e',24],['part-b',35],['part-c',78]];
for(const type of [chromium,firefox]){
 let browser;
 try{browser=await type.launch(type===chromium?{channel:'chrome',headless:true}:{headless:true,executablePath:process.env.FIREFOX_PATH});}
 catch(e){results.push({browser:type.name(),error:e.message});continue;}
 const context=await browser.newContext({viewport:{width:1440,height:1000}}),page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 try{
  for(const lang of ['ar','en']){
   const pdfRequests=[];const record=r=>{if(/\.pdf(?:\?|$)/.test(r.url()))pdfRequests.push(r.url());};page.on('request',record);
   await page.goto(`${origin}/${lang}/`);await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('html').getAttribute('dir'),lang==='ar'?'rtl':'ltr');
   assert.equal(await page.locator('#font-failure').isVisible(),false);
   assert.equal(pdfRequests.length,0,'landing must not load PDFs');page.off('request',record);
   for(const width of [320,375,1440]){
    await page.setViewportSize({width,height:900});
    assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${lang} overflow ${width}`);
    await page.screenshot({path:path.join(root,`qa/screenshots/${type.name()}-${lang}-${width}.png`),fullPage:true});
   }
   await page.setViewportSize({width:1440,height:1000});
   await page.keyboard.press('Tab');
   assert.equal(await page.locator(':focus').getAttribute('href'),'#main');
   for(const [id,count] of docs){
    await page.goto(`${origin}/${lang}/documents/${id}/`);
    const frame=await (await page.locator('iframe').elementHandle()).contentFrame();
    await frame.waitForFunction(()=>window.PDFViewerApplication?.pdfDocument,{timeout:45000});
    assert.equal(await frame.evaluate(()=>window.PDFViewerApplication.pdfDocument.numPages),count);
    await frame.waitForFunction(()=>window.PDFViewerApplication.pdfViewer.pagesCount>0);
    await frame.waitForFunction(()=>window.PDFViewerApplication.isInitialViewSet&&window.PDFViewerApplication.pdfViewer.pageViewsReady);
    await frame.evaluate(()=>new Promise(r=>setTimeout(r,50)));
    assert.equal(await frame.evaluate(()=>document.documentElement.dir),lang==='ar'?'rtl':'ltr');
    if(id==='part-a')for(const width of [320,375]){
      await page.setViewportSize({width,height:852});
      await frame.waitForFunction(()=>{const p=document.querySelector('.page')?.getBoundingClientRect();return p&&p.left>=-1&&p.right<=innerWidth+1;});
      assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
      assert.match(await frame.locator('#toolbarContainer').evaluate(e=>getComputedStyle(e).fontFamily),/HubInter/);
    }
    await page.setViewportSize({width:1440,height:1000});
    if(id==='part-a')await frame.waitForFunction(()=>{
      const p=document.querySelector('.page').getBoundingClientRect();
      const c=document.querySelector('#viewerContainer');
      return Math.abs(p.width-(c.clientWidth-22))<4;
    });
    await frame.locator('#pageNumber').fill(String(count));await frame.locator('#pageNumber').press('Enter');
    await frame.waitForFunction(n=>window.PDFViewerApplication.page===n,count);
    await frame.locator('#pageNumber').fill('0');await frame.locator('#pageNumber').press('Enter');
    assert.ok(await frame.evaluate(()=>window.PDFViewerApplication.page>=1));
    const toggle=frame.locator('#viewsManagerToggleButton');
    const initial=await toggle.getAttribute('aria-expanded');
    await toggle.click();
    assert.notEqual(await toggle.getAttribute('aria-expanded'),initial);
    if(initial==='true')await toggle.click();
    const zoom=await frame.evaluate(()=>window.PDFViewerApplication.pdfViewer.currentScale);
    await frame.locator('#zoomInButton').click();
    assert.ok(await frame.evaluate(n=>window.PDFViewerApplication.pdfViewer.currentScale>n,zoom));
    await frame.locator('#pageNumber').fill('1');await frame.locator('#pageNumber').press('Enter');
    await frame.locator('#viewFindButton').click();await frame.locator('#findInput').fill('GEM');
    await frame.waitForFunction(()=>window.PDFViewerApplication.findController.pageMatches.some(a=>a.length>0),{timeout:15000});
    await frame.locator('#findInput').press('Escape');
    await frame.waitForFunction(()=>document.querySelectorAll('.textLayer span').length>0);
    if(id==='part-a'||id==='part-b'){
      const arPage=id==='part-a'?37:9;
      const text=await frame.evaluate(async n=>(await(await window.PDFViewerApplication.pdfDocument.getPage(n)).getTextContent()).items.map(x=>x.str).join(' '),arPage);
      assert.match(text,/[\u0600-\u06ff]/);
      if(id==='part-a')assert.ok(!text.includes('ٮ('),'corrupt Quartz Arabic mapping');
      await frame.locator('#viewFindButton').click();
      await frame.locator('#findInput').fill(id==='part-a'?'بكم':'أب');
      await frame.waitForFunction(()=>window.PDFViewerApplication.findController.pageMatches.some(a=>a.length>0),{timeout:15000});
      await frame.locator('#findInput').press('Escape');
    }
    if(id==='part-d'){
      const download=page.waitForEvent('download');await page.locator('.reader-downloads a[download]').first().click();
      const file=await download;assert.match(file.suggestedFilename(),/\.pdf$/);
      await frame.locator('#secondaryToolbarToggleButton').click();
      await frame.locator('#presentationMode').click();
      await frame.waitForFunction(()=>document.fullscreenElement!==null&&window.PDFViewerApplication.pdfViewer.scrollMode===3);
      await frame.evaluate(()=>document.exitFullscreen());
      await frame.waitForFunction(()=>!window.PDFViewerApplication.isInPresentationMode);
    }
    await page.locator('.language').click();assert.match(page.url(),new RegExp(`/${lang==='ar'?'en':'ar'}/documents/${id}/$`));
    await page.waitForLoadState('networkidle');
    results.push({browser:type.name(),lang,document:id,pages:count,status:'passed'});
   }
  }
  // Failed document loads keep actionable direct links; no broken blank-only page.
  await page.route('**/pdf/*.pdf',route=>route.abort());
  await page.goto(`${origin}/en/documents/part-a/`);
  await page.locator('.fallback').waitFor();
  assert.ok(await page.locator('.reader-downloads a[download]').count()>=2);
  await page.unroute('**/pdf/*.pdf');
  await page.route('**/*.woff2',route=>route.abort());
  await page.goto(`${origin}/ar/`);await page.locator('#font-failure').waitFor({state:'visible',timeout:15000});
  results.push({browser:type.name(),status:'passed',checks:['mobile overflow','keyboard skip','no PDF preloads','PDF failure fallback','font failure alert']});
  assert.deepEqual(errors,[]);
 }catch(e){results.push({browser:type.name(),error:e.stack,consoleErrors:errors});}
 await browser.close();
}
fs.writeFileSync(path.join(root,'qa/browser-results.json'),JSON.stringify({origin,results},null,2)+'\n');
console.log(JSON.stringify({origin,readerChecks:results.filter(x=>x.document&&x.status==='passed').length,browserChecks:results.filter(x=>x.checks),failures:results.filter(x=>x.error)},null,2));
if(results.some(x=>x.error))process.exitCode=1;
