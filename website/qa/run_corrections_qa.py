#!/usr/bin/env python3
"""Targeted G26 correction checks. Loopback only, synthetic data, new output only; no mailto.

python3 qa/run_corrections_qa.py --root site --out-base <new-evidence-dir>
"""
import argparse, asyncio, datetime, json
from pathlib import Path
from playwright.async_api import async_playwright
from run_qa import Results, free_port, serve, watch, sha, settle_lazy
from font_validation import validate_brand_fonts


async def run(args):
    root = Path(args.root).resolve()
    out = Path(args.out_base) / datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out.mkdir(parents=True, exist_ok=False)
    (out / 'screenshots').mkdir()
    server = serve(root, free_port()); base = f'http://127.0.0.1:{server.server_port}/'
    R = Results(); raw = {}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            environment = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'browser':browser.version, 'url':base, 'site_files':{str(f.relative_to(root)):sha(f) for f in root.rglob('*') if f.is_file()}}
            for route in ('index','reference','privacy'):
                for width,height in ((1440,900),(768,1024),(375,812),(320,700)):
                    context = await browser.new_context(viewport={'width':width,'height':height})
                    page = await context.new_page(); log = await watch(page)
                    await page.goto(base+route+'.html',wait_until='networkidle')
                    await settle_lazy(page)
                    fonts = await validate_brand_fonts(page)
                    tag = f'{route}-{width}'; raw[tag] = {'font_acceptance':fonts}
                    R.add('brand faces and current glyphs '+tag,fonts['status']=='PASS',fonts)
                    R.add('responsive reflow '+tag,await page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
                    R.add('normal network and runtime '+tag,not log['console_errors'] and not log['page_errors'] and not log['failed'] and all(r['url'].startswith(base) and r['method']=='GET' for r in log['requests']),log)
                    await page.screenshot(path=str(out/'screenshots'/f'{tag}-full.png'),full_page=True)
                    if route=='reference':
                        emph = await page.locator('em').evaluate_all('(es)=>es.map(e=>({style:getComputedStyle(e).fontStyle,synthesis:getComputedStyle(e).fontSynthesis}))')
                        R.add('semantic emphasis uses real regular face '+tag,bool(emph) and all(e['style']=='normal' and e['synthesis']=='none' for e in emph),emph)
                    await context.close()
            context = await browser.new_context(); page = await context.new_page()
            await page.route('**/*.woff2',lambda r:r.abort())
            await page.goto(base,wait_until='networkidle')
            raw['blocked_fonts'] = await validate_brand_fonts(page)
            R.add('blocked required fonts FAIL brand acceptance',raw['blocked_fonts']['status']=='FAIL' and all(r['status']=='FAIL' for r in raw['blocked_fonts']['families']),raw['blocked_fonts'])
            R.add('font failure preserves readable content',await page.locator('h1').is_visible())
            await page.screenshot(path=str(out/'screenshots'/'blocked-fonts-failed-brand-acceptance.png'))
            await context.close()
            context = await browser.new_context(permissions=['clipboard-read','clipboard-write']); page = await context.new_page(); log = await watch(page)
            await page.goto(base,wait_until='networkidle')
            raw['unsupported_arabic_probe'] = await validate_brand_fonts(page,{'Jost':'العربية','Inter':'العربية'})
            R.add('unsupported Arabic fallback FAILS brand acceptance',raw['unsupported_arabic_probe']['status']=='FAIL' and all(r['status']=='FAIL' for r in raw['unsupported_arabic_probe']['families']),raw['unsupported_arabic_probe'])
            await page.check('#pkg-room')
            for val in ('','0','-1','1.5','abc','100001'):
                await page.fill('#q-rooms',val); await page.click('#quote-button')
                error = await page.locator('#q-rooms-error').inner_text()
                R.add('room error explains range '+repr(val),error=='Enter a whole number of rooms from 1 to 100,000.' and await page.input_value('#q-rooms')==val and await page.evaluate('document.activeElement.id')=='q-rooms',error)
                await page.locator('#quote-error-list a').click()
                R.add('room summary focuses input '+repr(val),await page.evaluate('document.activeElement.id')=='q-rooms')
            for val in ('1','100000',' 120 '):
                await page.fill('#q-rooms',val); await page.click('#quote-button')
                R.add('room boundary valid '+repr(val),await page.locator('#quote-result').is_visible() and ('Rooms to supply: '+val.strip()) in await page.input_value('#q-output'))
            await page.fill('#q-rooms','100001');await page.click('#quote-button');await page.wait_for_timeout(400)
            await page.locator('#quote-form').screenshot(path=str(out/'screenshots'/'room-range-error.png'))
            for sel,val in (('#f-name','Synthetic Tester'),('#f-email','qa@example.invalid'),('#f-org','Example Org')): await page.fill(sel,val)
            await page.check('#f-interest-partner')
            for repeats in (1,1000,3000):
                msg='Synthetic QA enquiry. Do not send. '*repeats
                await page.fill('#f-message',msg);await page.click('#prepare-button')
                draft=await page.input_value('#f-output');href=await page.get_attribute('#email-output','href')
                await page.click('#copy-output');await page.wait_for_function('document.getElementById("copy-status").textContent.includes("Copied")')
                copied=await page.evaluate('navigator.clipboard.readText()')
                R.add(f'full copy preserved at {repeats} repeats',draft.endswith(msg.strip()) and copied==draft)
                R.add(f'email copy guidance at {repeats} repeats',await page.locator('#email-copy-guidance').is_visible() and await page.get_attribute('#email-output','aria-describedby')=='email-copy-guidance')
                raw[f'draft-{repeats}']={'draft_characters':len(draft),'mailto_characters':len(href),'copy_matches':copied==draft}
            await page.wait_for_timeout(400)
            await page.locator('#enquiry-form').screenshot(path=str(out/'screenshots'/'long-draft-copy.png'))
            await page.fill('#f-message','Changed synthetic text')
            R.add('editing long draft withdraws handoff',not await page.locator('#form-result').is_visible() and await page.get_attribute('#email-output','href') is None)
            await page.click('button[type=reset]');await page.wait_for_timeout(50)
            R.add('clear removes long draft',await page.input_value('#f-output')=='' and await page.input_value('#f-message')=='')
            R.add('drafting and copying make no submission',all(r['url'].startswith(base) and r['method']=='GET' and r['post'] is None for r in log['requests']),log)
            await page.goto(base+'privacy.html');text=await page.locator('main').inner_text()
            R.add('privacy covers both drafts and external app',all(s in text for s in ('room count','sampling choices','privacy and synchronization settings','does not confirm that GEM has received it','remain to be approved')) and 'Nothing leaves your device' not in text and 'used only to reply' not in text)
            for path in ('.DS_Store','assets/.DS_Store'):
                resp=await context.request.get(base+path);R.add('Finder metadata not served '+path,resp.status in (403,404),resp.status)
            await context.close()
            for mode in ('disabled','blocked','enquiry-init-failure','quote-init-failure'):
                context=await browser.new_context(java_script_enabled=mode!='disabled');page=await context.new_page()
                if mode=='blocked': await page.route('**/assets/js/site.js',lambda r:r.abort())
                if mode.endswith('init-failure'):
                    src=(root/'assets/js/site.js').read_text()
                    token='var qDraft = false;' if mode.startswith('quote') else 'var hasDraft = false;'
                    assert token in src
                    src=src.replace(token,'throw new Error("Synthetic initialization failure"); '+token)
                    await page.route('**/assets/js/site.js',lambda r:r.fulfill(status=200,content_type='text/javascript',body=src))
                await page.goto(base,wait_until='networkidle')
                affected=['quote','enquiry'] if mode in ('disabled','blocked') else [mode.split('-')[0]]
                for form in affected:
                    notice='#quote-unavailable' if form=='quote' else '#form-unavailable';button='#quote-button' if form=='quote' else '#prepare-button'
                    text=await page.locator(notice).inner_text()
                    R.add('safe truthful unavailable notice '+mode+' '+form,await page.locator(button).is_disabled() and await page.locator(notice).is_visible() and 'could not start' in text and 'placeholders' in text and 'use the contact details' not in text,text)
                await context.close()
            await browser.close()
    finally:
        server.shutdown();server.server_close()
        (out/'checks.json').write_text(json.dumps(R.checks,indent=2,ensure_ascii=False))
        (out/'observations.json').write_text(json.dumps(raw,indent=2,ensure_ascii=False))
        if 'environment' in locals(): (out/'environment.json').write_text(json.dumps(environment,indent=2))
    summary={'total':len(R.checks),'passed':len(R.checks)-len(R.failed),'failed':len(R.failed),'failures':R.failed}
    (out/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False));print(json.dumps(summary,indent=2,ensure_ascii=False))
    return bool(R.failed)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--root',default='site');parser.add_argument('--out-base',required=True)
    raise SystemExit(asyncio.run(run(parser.parse_args())))
