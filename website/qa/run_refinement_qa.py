#!/usr/bin/env python3
"""Loopback-only layout checks for v0.5.4; preserves raw evidence in a new run folder."""
import argparse
import asyncio
import datetime
import json
from pathlib import Path

from playwright.async_api import async_playwright
from run_qa import Results, free_port, serve, sha, watch


async def run(args):
    root = Path(args.root).resolve()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = Path(args.out_base) / stamp
    out.mkdir(parents=True, exist_ok=False)
    results = Results()
    server = serve(root, free_port())
    base = f'http://127.0.0.1:{server.server_port}/'
    environment = {'site_sha256': {str(p.relative_to(root)): sha(p) for p in root.rglob('*') if p.is_file()}}
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            environment['chromium'] = browser.version
            for width, height in ((1440, 900), (768, 1024), (375, 812), (320, 640)):
                page = await browser.new_page(viewport={'width': width, 'height': height})
                log = await watch(page)
                await page.goto(base, wait_until='networkidle')
                await page.evaluate('document.fonts.ready')
                geometry = await page.evaluate('''() => {
                  const image = document.querySelector('.hero-figure img');
                  const rect = image.getBoundingClientRect();
                  const cta = document.querySelector('.hero .button').getBoundingClientRect();
                  const caption = document.querySelector('.hero-figure figcaption');
                  return {pageWidth: document.documentElement.scrollWidth, ctaBottom: cta.bottom,
                    image: {x: rect.x, y: rect.y, right: rect.right, width: rect.width, height: rect.height,
                      naturalWidth: image.naturalWidth, naturalHeight: image.naturalHeight,
                      complete: image.complete, priority: image.fetchPriority, loading: image.loading},
                    caption: caption.textContent, captionColor: getComputedStyle(caption).color};
                }''')
                image = geometry['image']
                results.add(f'no horizontal overflow at {width}', geometry['pageWidth'] <= width, geometry)
                results.add(f'full 3:2 hero frame at {width}', image['complete'] and image['naturalWidth'] > 0 and abs(image['width'] / image['height'] - 1.5) < .01 and abs(image['naturalWidth'] / image['naturalHeight'] - 1.5) < .01, image)
                results.add(f'hero image within viewport at {width}', image['x'] >= 0 and image['right'] <= width, image)
                results.add(f'hero is eager high-priority at {width}', image['priority'] == 'high' and image['loading'] != 'lazy')
                results.add(f'concept and colour qualifications at {width}', all(s in geometry['caption'] for s in ('Generated GEM concept', 'final product colour is not confirmed', 'Not production photography')))
                results.add(f'hero action precedes image on compact/tablet at {width}' if width < 1024 else 'hero columns do not overlap', geometry['ctaBottom'] <= image['y'] if width < 1024 else await page.evaluate("document.querySelector('.hero-copy').getBoundingClientRect().right < document.querySelector('.hero-figure').getBoundingClientRect().left"))
                if width < 720:
                    results.add(f'primary action in first viewport at {width}', geometry['ctaBottom'] <= height, geometry['ctaBottom'])
                contrast = await page.evaluate(r"""() => {
                  const rgb = s => s.match(/[\d.]+/g).slice(0,3).map(Number);
                  const luminance = s => rgb(s).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((a,x,i)=>a+x*[.2126,.7152,.0722][i],0);
                  const ratio = (a,b) => (Math.max(luminance(a),luminance(b))+.05)/(Math.min(luminance(a),luminance(b))+.05);
                  const caption=getComputedStyle(document.querySelector('.hero-figure figcaption'));
                  const hero=getComputedStyle(document.querySelector('.hero'));
                  window.gemQAContrast=ratio;
                  return ratio(caption.color,hero.backgroundColor);
                }""")
                results.add(f'hero qualification contrast at {width}', contrast >= 4.5, contrast)
                await page.locator('.hero .button').hover()
                hover = await page.locator('.hero .button').evaluate('(e)=>{const c=getComputedStyle(e);return {foreground:c.color,background:c.backgroundColor,ratio:window.gemQAContrast(c.color,c.backgroundColor)}}')
                results.add(f'hero action hover contrast at {width}', hover['ratio'] >= 4.5, hover)
                await page.screenshot(path=str(out / f'home-{width}.png'))
                bounds_before = await page.locator('.package-card').evaluate_all('(es)=>es.map(e=>{const r=e.getBoundingClientRect();return [r.x+scrollX,r.y+scrollY,r.width,r.height]})')
                await page.check('#pkg-room')
                bounds_after = await page.locator('.package-card').evaluate_all('(es)=>es.map(e=>{const r=e.getBoundingClientRect();return [r.x+scrollX,r.y+scrollY,r.width,r.height]})')
                results.add(f'selection does not move package cards at {width}', bounds_before == bounds_after)
                await page.locator('#packages').scroll_into_view_if_needed()
                await page.wait_for_timeout(300)
                sizes = await page.locator('.package-card img').evaluate_all('(es)=>es.map(e=>{const r=e.getBoundingClientRect();return {width:r.width,height:r.height,fit:getComputedStyle(e).objectFit}})')
                results.add(f'consistent 3:2 package frames at {width}', all(abs(r['width'] / r['height'] - 1.5) < .01 for r in sizes), sizes)
                results.add(f'portrait artwork not cropped at {width}', sizes[1]['fit'] == 'contain', sizes[1])
                results.add(f'local GET traffic and clean runtime at {width}', not log['failed'] and not log['console_errors'] and not log['page_errors'] and all(r['method'] == 'GET' and r['url'].startswith(base) for r in log['requests']))
                await page.close()
            await browser.close()
    finally:
        server.shutdown()
        server.server_close()
    summary = {'total': len(results.checks), 'passed': len(results.checks) - len(results.failed), 'failed': len(results.failed), 'failures': results.failed, 'scope': 'Chromium on loopback; layout evidence only, not publication or accessibility certification.'}
    for name, value in [('summary', summary), ('checks', results.checks), ('environment', environment)]:
        (out / (name + '.json')).write_text(json.dumps(value, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    return bool(results.failed)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='website/site')
    parser.add_argument('--out-base', required=True)
    raise SystemExit(asyncio.run(run(parser.parse_args())))
