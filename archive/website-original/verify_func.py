import asyncio, json
from playwright.async_api import async_playwright
URL="http://localhost:8765/"; OUT="/home/claude/gem-website/records/screenshots/"
AXE=open("/home/claude/fontpkg/node_modules/axe-core/axe.min.js").read()
async def main():
    R={}
    async with async_playwright() as p:
        b=await p.chromium.launch()
        # --- Keyboard order desktop
        pg=await b.new_page(viewport={"width":1440,"height":900})
        await pg.goto(URL); await pg.wait_for_timeout(500)
        order=[]
        for i in range(14):
            await pg.keyboard.press("Tab")
            order.append(await pg.evaluate("(()=>{const e=document.activeElement;const cs=getComputedStyle(e);return (e.textContent.trim()||e.name||e.alt||e.id).slice(0,30)+' | outline '+cs.outlineStyle+' '+cs.outlineWidth+' '+cs.outlineColor})()"))
        R["tab_order_desktop"]=order
        # skip link activates
        await pg.goto(URL); await pg.keyboard.press("Tab"); await pg.screenshot(path=OUT+"focus-skiplink.png", clip={"x":0,"y":0,"width":600,"height":120})
        await pg.keyboard.press("Enter"); R["skip_link_target"]=await pg.evaluate("document.activeElement.id")
        # anchors
        R["anchors"]={}
        for a in ["#approach","#amenities","#clients","#partners","#enquire","#top","#main"]:
            R["anchors"][a]=await pg.evaluate(f"!!document.querySelector('{a}')")
        # headings & landmarks
        R["headings"]=await pg.evaluate("[...document.querySelectorAll('h1,h2,h3,h4')].map(h=>h.tagName+': '+h.textContent.trim())")
        R["landmarks"]=await pg.evaluate("['header','nav','main','footer'].map(t=>t+':'+document.querySelectorAll(t).length)")
        # axe
        await pg.add_script_tag(content=AXE)
        ax=await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}}).then(r=>({violations:r.violations.map(v=>({id:v.id,impact:v.impact,n:v.nodes.length,t:v.nodes.slice(0,3).map(n=>n.target.join(' '))})),passes:r.passes.length,incomplete:r.incomplete.map(v=>v.id)}))")
        R["axe_desktop"]=ax
        # --- Form: empty submit
        await pg.goto(URL+"#enquire"); await pg.wait_for_timeout(300)
        await pg.click("button[type=submit]"); await pg.wait_for_timeout(200)
        R["form_empty"]={"summary_visible":await pg.is_visible("#error-summary"),"errors":await pg.evaluate("[...document.querySelectorAll('#error-list li')].map(l=>l.textContent)"),"focused":await pg.evaluate("document.activeElement.id"),"invalid":await pg.evaluate("[...document.querySelectorAll('[aria-invalid=true]')].map(e=>e.id||e.name)")}
        await pg.locator("#enquiry-form").screenshot(path=OUT+"form-errors-desktop.png")
        # invalid email
        await pg.fill("#f-name","Test Person"); await pg.fill("#f-email","not-an-email"); await pg.check("#f-interest"); await pg.fill("#f-message","Test message for a preview check.")
        await pg.click("button[type=submit]"); await pg.wait_for_timeout(200)
        R["form_bad_email"]=await pg.evaluate("[...document.querySelectorAll('#error-list li')].map(l=>l.textContent)")
        await pg.fill("#f-email","test@example.com"); await pg.select_option("#f-role","Procurement")
        reqs=[]; pg.on("request", lambda r: reqs.append(r.url))
        await pg.click("button[type=submit]"); await pg.wait_for_timeout(300)
        R["form_valid"]={"result_visible":await pg.is_visible("#form-result"),"focused":await pg.evaluate("document.activeElement.id"),"output":await pg.input_value("#f-output"),"network_requests_on_submit":reqs,"summary_hidden":not await pg.is_visible("#error-summary")}
        await pg.locator("#enquiry-form").screenshot(path=OUT+"form-prepared-desktop.png")
        await pg.click("button[type=reset]"); await pg.wait_for_timeout(200)
        R["form_clear"]={"result_hidden":not await pg.is_visible("#form-result"),"name":await pg.input_value("#f-name"),"focused":await pg.evaluate("document.activeElement.id"),"invalid_left":await pg.evaluate("document.querySelectorAll('[aria-invalid]').length")}
        await pg.close()
        # --- Mobile menu
        ctx=await b.new_context(viewport={"width":375,"height":812})
        pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_timeout(1700)
        R["menu_initial"]=await pg.get_attribute(".nav-toggle","aria-expanded")
        await pg.focus(".nav-toggle"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(300)
        R["menu_open"]={"expanded":await pg.get_attribute(".nav-toggle","aria-expanded"),"nav_visible":await pg.is_visible("#primary-nav a[href='#approach']")}
        await pg.screenshot(path=OUT+"mobile-375-menu-open.png")
        await pg.keyboard.press("Tab"); R["menu_next_focus"]=await pg.evaluate("document.activeElement.textContent.trim()")
        await pg.keyboard.press("Escape"); await pg.wait_for_timeout(100)
        R["menu_escape"]={"expanded":await pg.get_attribute(".nav-toggle","aria-expanded"),"focus":await pg.evaluate("document.activeElement.className")}
        await pg.add_script_tag(content=AXE)
        R["axe_mobile"]=await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}}).then(r=>r.violations.map(v=>v.id+':'+v.nodes.length))")
        await ctx.close()
        # --- Reduced motion & reveal
        ctx=await b.new_context(viewport={"width":1440,"height":900}, reduced_motion="reduce")
        pg=await ctx.new_page(); await pg.goto(URL); await pg.wait_for_timeout(100)
        R["reduced_motion"]=await pg.evaluate("(()=>{const m=document.querySelector('.mark--ring');const cs=getComputedStyle(m);return {mask:cs.maskImage,core:getComputedStyle(document.querySelector('.mark--core')).display,stage:document.querySelector('.mark-stage').className,hover:getComputedStyle(document.documentElement).getPropertyValue('--gem-motion-duration-hover')}})()")
        await pg.screenshot(path=OUT+"reduced-motion-t100ms.png")
        await ctx.close()
        ctx=await b.new_context(viewport={"width":1440,"height":900})
        pg=await ctx.new_page(); await pg.goto(URL)
        frames=[]
        for t in (1700,):
            await pg.wait_for_timeout(t- (frames[-1] if frames else 0)); frames.append(t)
            await pg.screenshot(path=OUT+f"reveal-check-{t}ms.png", clip={"x":760,"y":120,"width":680,"height":560})
        R['reveal_final']=await pg.evaluate("document.querySelector('.mark-stage').className")
        await ctx.close()
        # --- 400% zoom approximation: 320 CSS px reflow already measured; check 1280/4=320
        await b.close()
    print(json.dumps(R,indent=1))
asyncio.run(main())
