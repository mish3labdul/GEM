// D5 rehearsal: 400% browser zoom on a 1280 px window is a 320 CSS px wide viewport at device scale 4.
// Usage: PW=<path to playwright module> BASE=<site origin> node zoom-400.mjs   (prints a JSON summary; not a substitute for a manual pass)
import {createRequire} from 'module'; const require=createRequire(import.meta.url);
const {chromium}=require(process.env.PW); const base=process.env.BASE;
const b=await chromium.launch(); const res=[]; const rec=(n,ok,d='')=>{res.push({n,ok,d});};
const ctx=await b.newContext({viewport:{width:320,height:256},deviceScaleFactor:4});
for (const lang of ['en','ar']) {
  const p=await ctx.newPage();
  for (const slug of ['','about/','amenities-packaging/','contact/','privacy/']) {
    const route=`${lang}/${slug}`; await p.goto(`${base}/${route}`); await p.waitForTimeout(900);
    const notice=p.locator('.cookie-notice');
    if (await notice.isVisible()) {
    const nh=await notice.evaluate(e=>({h:e.getBoundingClientRect().height,vh:innerHeight})).catch(()=>null);
    rec(`${route} cookie notice leaves room (<=50% of viewport)`, !!nh && nh.h<=nh.vh*0.5+1, nh?`${Math.round(nh.h)}/${nh.vh}`:'missing');
    const closeBox=await notice.locator('.cookie-close').boundingBox();
    rec(`${route} cookie close button inside viewport`, !!closeBox && closeBox.y>=0 && closeBox.y+closeBox.height<=256+1 && closeBox.x>=0 && closeBox.x+closeBox.width<=321, JSON.stringify(closeBox));
    await notice.locator('.cookie-close').click(); 
    }
    const m=await p.evaluate(()=>{const w=innerWidth;const off=[];for(const e of document.querySelectorAll('body *')){const r=e.getBoundingClientRect();if(r.width===0||r.height===0)continue;if(r.right>w+1||r.left<-1){let a=e,clip=false;while(a&&a!==document.body){const o=getComputedStyle(a).overflowX;if(o==='auto'||o==='scroll'||o==='hidden'){clip=true;break;}a=a.parentElement;}if(!clip&&getComputedStyle(e).position!=='fixed')off.push(e.tagName.toLowerCase()+'.'+(e.className||'').toString().slice(0,30));}}return {sw:document.documentElement.scrollWidth,w,off:off.slice(0,4),count:off.length,h1:!!document.querySelector('h1')&&document.querySelector('h1').getBoundingClientRect().width>0};});
    rec(`${route} no horizontal scroll`, m.sw<=m.w+1, `scrollWidth ${m.sw} / ${m.w}`);
    rec(`${route} no content pushed outside the viewport`, m.count===0, m.off.join(', '));
    rec(`${route} heading present`, m.h1);
    const tg=p.locator('.menu-toggle');
    if (await tg.isVisible()) { await tg.click(); const ex=await tg.getAttribute('aria-expanded'); const nav=await p.locator('#navigation a').first().boundingBox(); rec(`${route} menu opens with links in view`, ex==='true' && !!nav && nav.x>=-1 && nav.x+nav.width<=321, JSON.stringify(nav)); await tg.click(); } else rec(`${route} menu toggle visible`, false);
  }
  // journeys
  await p.goto(`${base}/${lang}/contact/`); await p.waitForTimeout(700); if (await p.locator('.cookie-close').isVisible()) await p.locator('.cookie-close').click();
  await p.fill('#name','Test Person'); await p.fill('#company','Test Hotel'); await p.fill('#email','test@example.com'); await p.fill('#market','Riyadh');
  const opts=await p.locator('#interest option').count(); await p.selectOption('#interest',{index:Math.min(1,opts-1)}); await p.fill('#message','Guest-room amenities for a new property.');
  await p.waitForTimeout(500); const sub=p.locator('form button[type=submit]'); rec(`${lang} enquiry: submit enabled`, await sub.isEnabled());
  await sub.scrollIntoViewIfNeeded(); await sub.click(); await p.waitForTimeout(600);
  const out=p.locator('#brief-text'); rec(`${lang} enquiry: brief prepared and visible`, await out.isVisible() && (await out.inputValue()).length>20);
  const sw=await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1); rec(`${lang} enquiry: no horizontal scroll after submit`, sw);
  rec(`${lang} enquiry: copy and download reachable`, await p.locator('#copy-brief').isVisible() && await p.locator('#download-brief').isVisible());
  await p.goto(`${base}/${lang}/amenities-packaging/`); await p.waitForTimeout(700); if (await p.locator('.cookie-close').isVisible()) await p.locator('.cookie-close').click();
  const btns=p.locator('.product-list button'); await btns.nth(2).click(); const nm=await p.locator('#product-name').innerText(); rec(`${lang} product viewer: selecting item 3 updates name`, nm.length>0, nm);
  const vis=p.locator('button.product-visual'); await vis.focus(); await p.keyboard.press('Space'); const dlg=p.locator('.gem-lightbox'); rec(`${lang} lightbox opens by keyboard`, await dlg.isVisible()); await p.keyboard.press('Escape'); rec(`${lang} lightbox closes with Escape`, !(await dlg.isVisible()));
  await p.close();
}
await b.close();
const fail=res.filter(r=>!r.ok); console.log(JSON.stringify({total:res.length,failed:fail.length,failures:fail,passed:res.filter(r=>r.ok).length},null,1));
