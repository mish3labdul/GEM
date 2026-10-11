#!/usr/bin/env python3
"""Identical baseline/current settings; fail on any changed pixel."""
import argparse, asyncio, json, sys
from pathlib import Path
from PIL import Image, ImageChops
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'website/qa'))
from run_qa import serve, free_port, settle_lazy

async def run(args):
    out = Path(args.out).resolve();out.mkdir(parents=True, exist_ok=False)
    servers = [serve(Path(args.baseline).resolve(), free_port()), serve(ROOT/'website/site', free_port())]
    rows=[]
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            for page_name in ['index','reference','privacy']:
                for width,height in [(1440,900),(375,812)]:
                    paths=[]
                    for label,server in zip(['before','after'],servers):
                        context=await browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce',device_scale_factor=1)
                        page=await context.new_page()
                        await page.goto(f'http://127.0.0.1:{server.server_port}/{page_name}.html',wait_until='networkidle')
                        await page.evaluate('document.fonts.ready');await settle_lazy(page)
                        path=out/f'{page_name}-{width}-{label}.png'
                        await page.screenshot(path=str(path),full_page=True,animations='disabled',caret='hide')
                        paths.append(path);await context.close()
                    a,b=(Image.open(path).convert('RGB') for path in paths)
                    equal=a.size==b.size and ImageChops.difference(a,b).getbbox() is None
                    rows.append({'page':page_name,'width':width,'before_size':a.size,'after_size':b.size,'pixel_identical':equal,'before':paths[0].name,'after':paths[1].name})
            await browser.close()
        report={'engine':'Chromium','browser_version':browser.version,'reduced_motion':'reduce','comparisons':rows,'passed':all(r['pixel_identical'] for r in rows)}
        (out/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2))
        return 0 if report['passed'] else 1
    finally:
        for server in servers:server.shutdown()

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',required=True);ap.add_argument('--out',required=True)
    raise SystemExit(asyncio.run(run(ap.parse_args())))
