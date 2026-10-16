"""Chromium brand-font acceptance, including actual glyph fallback (not just CSS family names).

Requires a Playwright page. A failed result is a failed brand acceptance, even if fallback
keeps content readable. Future Arabic DOM text enters the same samples automatically.
This is engine-specific font evidence, not native-language or accessibility acceptance.
"""


async def validate_brand_fonts(page, samples=None):
    if samples is None:
        samples = await page.evaluate("""() => {
          const samples = {Jost: '', Inter: ''};
          if (document.documentElement.lang === 'ar' || document.querySelector('[lang=ar]')) samples['Noto Sans Arabic'] = '';
          for (const e of document.querySelectorAll('body *')) {
            if (!e.getClientRects().length) continue;
            const family = getComputedStyle(e).fontFamily.split(',')[0].replaceAll('"', '').trim();
            if (!(family in samples)) continue;
            for (const n of e.childNodes) if (n.nodeType === Node.TEXT_NODE) samples[family] += n.textContent;
            if ('value' in e) samples[family] += e.value || '';
            if (e.hasAttribute('placeholder')) samples[family] += e.getAttribute('placeholder');
          }
          for (const family of Object.keys(samples)) samples[family] = [...new Set(samples[family])].join('');
          return samples;
        }""")
    await page.evaluate("document.fonts.ready")
    faces = await page.evaluate("[...document.fonts].map(f=>({family:f.family.replaceAll('\"',''),weight:f.weight,style:f.style,status:f.status}))")
    cdp = await page.context.new_cdp_session(page)
    rows = []
    try:
        await cdp.send("DOM.enable")
        await cdp.send("CSS.enable")
        for family in samples:
            sample = samples.get(family, "")
            # Render an off-screen probe, never display it or include it in screenshots.
            await page.evaluate("""({family,sample}) => {
              const e = document.createElement('span'); e.id = 'gem-qa-font-probe';
              e.textContent = sample; e.setAttribute('aria-hidden', 'true');
              Object.assign(e.style, {position:'fixed',left:'-100000px',top:'0',whiteSpace:'pre',fontFamily:'"'+family+'"',fontSize:'20px',fontWeight:'400',fontStyle:'normal',fontSynthesis:'none'});
              document.body.append(e);
            }""", {"family": family, "sample": sample})
            try:
                await page.evaluate("({family,sample})=>document.fonts.load('400 20px \"'+family+'\"', sample).catch(()=>[])", {"family": family, "sample": sample})
                # Platform-font evidence is populated after layout/paint, not font-load alone.
                await page.evaluate("new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)))")
                doc = await cdp.send("DOM.getDocument")
                node = await cdp.send("DOM.querySelector", {"nodeId": doc["root"]["nodeId"], "selector": "#gem-qa-font-probe"})
                fonts = (await cdp.send("CSS.getPlatformFontsForNode", {"nodeId": node["nodeId"]}))["fonts"]
                loaded = any(f["family"] == family and f["style"] == "normal" and f["weight"] == "400" and f["status"] == "loaded" for f in faces)
                actual = [f for f in fonts if f["glyphCount"] > 0]
                ok = loaded and bool(sample.strip()) and bool(actual) and all(f["isCustomFont"] and f["familyName"] == family for f in actual)
                rows.append({"family": family, "requested_weight": 400, "sample": sample, "platform_fonts": fonts, "required_face_loaded": loaded, "status": "PASS" if ok else "FAIL"})
            finally:
                await page.evaluate("document.getElementById('gem-qa-font-probe')?.remove()")
    finally:
        await cdp.detach()
    return {"status": "PASS" if all(r["status"] == "PASS" for r in rows) else "FAIL", "faces": faces, "families": rows}
