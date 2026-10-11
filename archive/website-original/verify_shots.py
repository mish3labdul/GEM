import asyncio, json, sys
from playwright.async_api import async_playwright
URL="http://localhost:8765/"
OUT="/home/claude/gem-website/records/screenshots/"
sizes={"desktop-1440":(1440,900),"tablet-768":(768,1024),"mobile-375":(375,812),"compact-320":(320,640)}
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        report={}
        for name,(w,h) in sizes.items():
            ctx=await b.new_context(viewport={"width":w,"height":h})
            pg=await ctx.new_page()
            logs=[]; reqs=[]; fails=[]
            pg.on("console", lambda m: logs.append(f"{m.type}: {m.text}"))
            pg.on("pageerror", lambda e: logs.append(f"pageerror: {e}"))
            pg.on("request", lambda r: reqs.append(r.url))
            pg.on("requestfailed", lambda r: fails.append(r.url))
            await pg.goto(URL, wait_until="networkidle"); await pg.add_style_tag(content="html{scroll-behavior:auto !important}")
            await pg.wait_for_timeout(1800)
            # load lazy images
            H=await pg.evaluate("document.body.scrollHeight")
            for y in range(0,H,600):
                await pg.evaluate(f"window.scrollTo(0,{y})"); await pg.wait_for_timeout(250)
            await pg.evaluate("window.scrollTo(0,0)"); await pg.wait_for_timeout(400)
            await pg.screenshot(path=OUT+f"{name}-full.png", full_page=True)
            await pg.screenshot(path=OUT+f"{name}-fold.png")
            info=await pg.evaluate("""()=>({
              hscroll: document.documentElement.scrollWidth > window.innerWidth,
              sw: document.documentElement.scrollWidth,
              fonts: [...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight),
              h1: document.querySelector('h1').textContent,
              h1font: getComputedStyle(document.querySelector('h1')).fontFamily,
              imgs: [...document.images].map(i=>({src:i.currentSrc.split('/').pop(), ok:i.complete&&i.naturalWidth>0, alt:i.alt}))
            })""")
            report[name]={"console":logs,"failed":fails,"external":[r for r in reqs if not r.startswith("http://localhost")],"requests":len(reqs),**info}
            await ctx.close()
        await b.close()
        print(json.dumps(report,indent=1))
asyncio.run(main())
