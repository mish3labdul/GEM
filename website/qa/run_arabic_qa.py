#!/usr/bin/env python3
"""Arabic/RTL working-site QA. Local synthetic data; no mailto navigation or submission."""
import argparse,asyncio,datetime,json,re
from pathlib import Path
from playwright.async_api import async_playwright
from run_qa import Results,serve,free_port,watch,sha,settle_lazy
from font_validation import validate_brand_fonts
async def run(args):
 root=Path(args.root).resolve();out=Path(args.out_base)/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ');out.mkdir(parents=True,exist_ok=False);(out/'screenshots').mkdir();r=Results();raw={};server=serve(root,free_port());base=f'http://127.0.0.1:{server.server_port}/'
 try:
  async with async_playwright() as p:
   browser=await p.chromium.launch();raw['browser']=browser.version;raw['site_files']={str(f.relative_to(root)):sha(f) for f in root.rglob('*') if f.is_file()};axe=(Path(__file__).parent/'vendor/axe.min.js').read_text()
   for route in ('index','reference','privacy'):
    for width,height in ((1440,900),(1024,768),(768,1024),(375,812),(320,700)):
     context=await browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce');page=await context.new_page();log=await watch(page);await page.goto(base+'ar/'+route+'.html',wait_until='networkidle');await settle_lazy(page);tag=f'{route}-{width}'
     r.add('Arabic root '+tag,await page.evaluate('document.documentElement.lang==="ar" && document.documentElement.dir==="rtl"'))
     r.add('RTL reflow '+tag,await page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
     fonts=await validate_brand_fonts(page);r.add('actual required glyph faces '+tag,fonts['status']=='PASS',fonts);raw[tag]={'fonts':fonts}
     r.add('loaded responsive images '+tag,await page.locator('img').evaluate_all('(es)=>es.every(e=>e.complete && e.naturalWidth>0 && getComputedStyle(e).transform==="none")'))
     r.add('runtime and local GET only '+tag,not log['page_errors'] and not log['failed'] and not log['console_errors'] and all(x['url'].startswith(base) and x['method']=='GET' for x in log['requests']),log)
     if route=='reference':r.add('complete isolated version '+tag,await page.locator('bdi').filter(has_text='GEM™ V3.0').count()>0)
     r.add('English counterpart link '+tag,await page.locator('.language-switch').get_attribute('href')=='../'+route+'.html')
     # Verify a real return journey, not only link text.
     await page.locator('.language-switch').click();await page.wait_for_load_state('networkidle');r.add('English language destination '+tag,await page.evaluate('document.documentElement.lang==="en"'));await page.locator('.language-switch').click();await page.wait_for_load_state('networkidle');r.add('Arabic return destination '+tag,page.url.endswith('/ar/'+route+'.html'))
     await page.add_script_tag(content=axe);violations=await page.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}}).then(r=>r.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})))");r.add('axe violations '+tag,not violations,violations)
     if width<1024:
      await page.locator('.nav-toggle').click();r.add('Arabic menu and disclosure '+tag,await page.locator('.nav-toggle').inner_text()=='إغلاق' and await page.locator('.nav-toggle').get_attribute('aria-expanded')=='true');await page.keyboard.press('Escape');r.add('Escape closes and focuses menu '+tag,await page.locator('.nav-toggle').get_attribute('aria-expanded')=='false' and await page.evaluate('document.activeElement.classList.contains("nav-toggle")'))
     await settle_lazy(page);await page.screenshot(path=str(out/'screenshots'/f'{tag}.png'),full_page=True)
     if width in (1440,320):
      await page.add_style_tag(content='html {scroll-behavior:auto!important}');await page.evaluate("()=>{const sizes=[...document.querySelectorAll('body *')].map(e=>[e,parseFloat(getComputedStyle(e).fontSize)]);for(const [e,size] of sizes)e.style.fontSize=size*2+'px'}");r.add('200 percent RTL text reflow '+tag,await page.evaluate('document.documentElement.scrollWidth<=innerWidth'));await page.screenshot(path=str(out/'screenshots'/f'{tag}-text200.png'),full_page=True)
     await context.close()
   context=await browser.new_context(permissions=['clipboard-read','clipboard-write'],viewport={'width':375,'height':812});page=await context.new_page();log=await watch(page);await page.goto(base+'ar/index.html',wait_until='networkidle');await page.locator('#quote-button').click();r.add('Arabic errors focus first package',await page.evaluate('document.activeElement.id')=='pkg-room' and await page.locator('#q-rooms-error').inner_text()=='أدخل عددًا صحيحًا موجبًا للغرف.')
   await page.check('#pkg-room')
   for val in ('0','-1','1.2','1e3','١٢'):
    await page.fill('#q-rooms',val);await page.locator('#quote-button').click();r.add('reject invalid or nonpolicy digits '+val,await page.locator('#q-rooms-error').is_visible() and not await page.locator('#quote-result').is_visible())
   for val in ('1','100001','9007199254740993','9'*400):
    await page.fill('#q-rooms',val);await page.locator('#quote-button').click();draft=await page.input_value('#q-output');r.add('Arabic draft retains exact positive estimate '+val[:20],await page.locator('#quote-result').is_visible() and '\u2068'+val+'\u2069' in draft and 'المجموعة التصورية: مجموعة الغرفة' in draft);href=await page.get_attribute('#quote-email','href');r.add('Arabic subject and exact body '+val[:20],href.startswith('mailto:mish3labdul@gmail.com?') and 'subject=' in href)
   await page.fill('#q-rooms','120');await page.click('#q-sampling');await page.check('#q-stationery');await page.click('#quote-button');draft=await page.input_value('#q-output');r.add('Arabic sampling stationery and pending status',all(x in draft for x in ('الاهتمام بالعينات: نعم','الاهتمام بمطبوعات الوصول: نعم','التوافر والمواصفات بانتظار التأكيد.')));await page.click('#quote-copy');await page.wait_for_function('document.querySelector("#quote-copy-status").textContent.length>0');r.add('Arabic request clipboard',await page.evaluate('navigator.clipboard.readText()')==draft)
   await page.fill('#q-rooms','121');r.add('Arabic stale request withdrawn',not await page.locator('#quote-result').is_visible() and 'تغيرت' in await page.locator('#quote-status').inner_text())
   for sel,val in (('#f-name','اختبار تجريبي'),('#f-email','qa@example.invalid'),('#f-org','منشأة اختبار'),('#f-message','رسالة اختبار عربية. لا تُرسل.')):await page.fill(sel,val)
   await page.check('#f-interest-partner');await page.click('#prepare-button');draft=await page.input_value('#f-output');r.add('Arabic enquiry draft and isolated email',all(x in draft for x in ('استفسار إلى GEM','اختبار تجريبي','الشراكة','\u2068qa@example.invalid\u2069')));await page.click('#copy-output');await page.wait_for_function('document.querySelector("#copy-status").textContent.length>0');r.add('Arabic enquiry clipboard exact',await page.evaluate('navigator.clipboard.readText()')==draft);await page.locator('#form-result').screenshot(path=str(out/'screenshots'/'arabic-enquiry-draft.png'))
   await page.fill('#f-message','تعديل');r.add('Arabic stale enquiry withdrawn',not await page.locator('#form-result').is_visible());r.add('LTR email and estimate, auto-direction free text',await page.locator('#f-email').get_attribute('dir')=='ltr' and await page.locator('#q-rooms').get_attribute('dir')=='ltr' and await page.locator('#f-message').get_attribute('dir')=='auto');r.add('no draft submission',all(x['url'].startswith(base) and x['method']=='GET' and x['post'] is None for x in log['requests']),log);await context.close()
   for mode in ('no-js','blocked-messages','incomplete-messages','invalid-message','blocked-script','blocked-font'):
    context=await browser.new_context(java_script_enabled=mode!='no-js');page=await context.new_page()
    if mode=='blocked-messages':await page.route('**/messages-ar.js',lambda x:x.abort())
    if mode in ('incomplete-messages','invalid-message'):
     async def damaged_messages(route):
      response=await route.fetch();body=await response.text()
      damage='delete window.GEM_AR_MESSAGES["Enter your name."];' if mode=='incomplete-messages' else 'window.GEM_AR_MESSAGES["Enter your name."] = "   ";'
      await route.fulfill(response=response,body=body+'\n'+damage)
     await page.route('**/messages-ar.js',damaged_messages)
    if mode=='blocked-script':await page.route('**/site.js',lambda x:x.abort())
    if mode=='blocked-font':await page.route('**/noto-sans-arabic-400.woff2',lambda x:x.abort())
    await page.goto(base+'ar/index.html',wait_until='networkidle')
    if mode=='blocked-font':
     fonts=await validate_brand_fonts(page);r.add('missing Arabic font FAILS acceptance',fonts['status']=='FAIL',fonts)
    else:
     before=page.url;log=await watch(page);await page.fill('#q-rooms','120');await page.focus('#q-rooms');await page.keyboard.press('Enter');await page.fill('#f-name','اختبار');await page.focus('#f-name');await page.keyboard.press('Enter');await page.wait_for_timeout(150);r.add('no implicit submission '+mode,page.url==before and all(x['method']=='GET' for x in log['requests']),log)
     r.add('fail closed '+mode,await page.locator('#quote-button').is_disabled() and await page.locator('#prepare-button').is_disabled() and await page.locator('#quote-unavailable').is_visible() and await page.locator('#form-unavailable').is_visible());r.add('language link works without scripts '+mode,await page.locator('.language-switch').get_attribute('href')=='../index.html')
     if mode in ('incomplete-messages','invalid-message'):
      r.add('static navigation retained '+mode,await page.locator('.nav-toggle').is_hidden() and not await page.locator('.site-header').evaluate('(el) => el.classList.contains("nav-ready")') and await page.locator('#primary-nav').is_visible())
    await context.close()
   await browser.close()
 finally:
  server.shutdown();server.server_close();(out/'checks.json').write_text(json.dumps(r.checks,ensure_ascii=False,indent=2));(out/'observations.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2))
 summary={'total':len(r.checks),'passed':len(r.checks)-len(r.failed),'failed':len(r.failed),'failures':r.failed};(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2));return bool(r.failed)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',default='website/site');ap.add_argument('--out-base',required=True);raise SystemExit(asyncio.run(run(ap.parse_args())))
