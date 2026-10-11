#!/usr/bin/env python3
"""GEM website QA suite (session 2, addresses audit GEM-06).

Assertion suite, not an observation collector: every check records PASS or FAIL with detail,
and the process exits non-zero if any check fails. A green exit is still not acceptance:
it covers one Chromium engine on loopback with synthetic data only.

Usage (all paths are arguments; nothing is hard-coded to one machine):
  python3 qa/run_qa.py --root site --out-base records/qa-runs --axe /path/to/axe.min.js

- Serves --root itself on 127.0.0.1 with an ephemeral port (never 0.0.0.0).
- Writes only to a NEW directory <out-base>/<UTC timestamp>; refuses to reuse one.
- Never sends data anywhere: form tests use synthetic values and assert zero requests.
"""
import argparse, asyncio, contextlib, datetime, functools, hashlib, http.server, json, os, platform, socket, sys, threading
from pathlib import Path

PAGES = ["index.html", "reference.html", "privacy.html"]
VIEWPORTS = [("desktop-1440", 1440, 900), ("breakpoint-1024", 1024, 768), ("tablet-768", 768, 1024), ("mobile-375", 375, 812), ("narrow-320", 320, 640)]
PROBES = [".DS_Store", "assets/.DS_Store", "records/", "source-images/", "qa/run_qa.py", "verify_func.py", "verify_shots.py", ".git/config", "audit-2026-10-10-independent-01/", "README.md"]
SYNTH = {"name": "Synthetic Tester", "organisation": "Example Org", "email": "qa@example.invalid", "message": "Synthetic QA enquiry. Do not send."}


class Results:
    def __init__(self):
        self.checks = []

    def add(self, cid, ok, detail=None):
        self.checks.append({"id": cid, "status": "PASS" if ok else "FAIL", "detail": detail})
        return ok

    @property
    def failed(self):
        return [c for c in self.checks if c["status"] == "FAIL"]


def free_port():
    with contextlib.closing(socket.socket()) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def serve(root, port):
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a, **k):
            pass
    handler = functools.partial(Quiet, directory=str(root))
    class QuietServer(http.server.ThreadingHTTPServer):
        def handle_error(self, request, client_address):
            pass  # aborted requests (e.g. the blocked-script test) are expected
    httpd = QuietServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


async def watch(page):
    log = {"console_errors": [], "page_errors": [], "requests": [], "failed": []}
    page.on("console", lambda m: log["console_errors"].append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: log["page_errors"].append(str(e)))
    page.on("request", lambda r: log["requests"].append({"url": r.url, "method": r.method, "post": r.post_data}))
    page.on("requestfailed", lambda r: log["failed"].append(r.url))
    return log


async def ax_description(page, selector):
    """Accessible name and description as Chromium computes them (aria-describedby includes hidden targets)."""
    cdp = await page.context.new_cdp_session(page)
    doc = await cdp.send("DOM.getDocument")
    nid = (await cdp.send("DOM.querySelector", {"nodeId": doc["root"]["nodeId"], "selector": selector}))["nodeId"]
    node = (await cdp.send("Accessibility.getPartialAXTree", {"nodeId": nid, "fetchRelatives": False}))["nodes"][0]
    await cdp.detach()
    return (node.get("description") or {}).get("value", "")


TITLES = {"index.html": "GEM™ — Hospitality supplier and partner", "reference.html": "GEM™ brand and design reference", "privacy.html": "GEM™ privacy and legal notice"}


async def settle_lazy(page):
    await page.add_style_tag(content="html{scroll-behavior:auto!important}")
    n = await page.evaluate("document.images.length")
    for i in range(n):
        await page.evaluate("(i)=>document.images[i].scrollIntoView({block:'center'})", i)
        await page.wait_for_timeout(60)
    await page.wait_for_function("[...document.images].filter(i=>i.offsetParent!==null).every(i=>i.complete)", timeout=15000)
    await page.evaluate("scrollTo(0,0)")
    await page.wait_for_timeout(150)


LAYOUT_JS = r"""() => {
  const vis = e => e.offsetParent !== null || getComputedStyle(e).position === 'fixed';
  const imgs = [...document.images].map(i => ({src: i.currentSrc.split('/').pop(), alt: i.getAttribute('alt'), visible: vis(i), ok: i.complete && i.naturalWidth > 0, w: i.naturalWidth}));
  const footerLinks = [...document.querySelectorAll('.site-footer a')].map(a => { const r = a.getBoundingClientRect(); return {text: a.textContent.trim(), top: r.top + scrollY, bottom: r.bottom + scrollY, left: r.left, right: r.right, h: r.height}; });
  return {
    width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
    fonts: [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/"/g, '') + ' ' + f.weight),
    weights: [...new Set([...document.querySelectorAll('body *')].filter(vis).map(e => getComputedStyle(e).fontWeight))],
    families: [...new Set([...document.querySelectorAll('body *')].filter(e => vis(e) && e.childNodes.length && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())).map(e => getComputedStyle(e).fontFamily.split(',')[0].replace(/"/g, '')))],
    imgs, h1: document.querySelectorAll('h1').length,
    landmarks: {header: document.querySelectorAll('header').length, main: document.querySelectorAll('main').length, footer: document.querySelectorAll('footer').length, nav: document.querySelectorAll('nav').length},
    anchors: [...document.querySelectorAll('a[href^="#"]')].map(a => ({href: a.getAttribute('href'), ok: a.getAttribute('href') === '#' ? false : !!document.getElementById(a.getAttribute('href').slice(1))})),
    links: [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(h => !h.startsWith('#')),
    footerLinks,
    ds: (() => {
      const textEls = [...document.querySelectorAll('body *')].filter(e => vis(e) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
      const figs = [...document.querySelectorAll('main figure')].filter(vis);
      return {
        tokenSizes: (() => { const out = new Set(); for (const sh of document.styleSheets) { let rules; try { rules = sh.cssRules; } catch (e) { continue; }
          for (const r of rules) { const st = r.style; if (!st) continue; for (let i = 0; i < st.length; i++) { const n = st[i]; if ((/^--gem-type-size-/.test(n) && !/arabic/.test(n)) || /^--site-type-.*-size$/.test(n)) { const v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue(n)); if (v) out.add(v); } } } }
          return [...out].sort((a, b) => a - b); })(),
        sizes: [...new Set(textEls.map(e => parseFloat(getComputedStyle(e).fontSize)))].sort((a, b) => a - b),
        frames: [...document.querySelectorAll('.figure--frame-3x2 img')].filter(vis).map(i => { const r = i.getBoundingClientRect(); return {src: i.currentSrc.split('/').pop(), box: +(r.width / r.height).toFixed(3), nat: +(i.naturalWidth / i.naturalHeight).toFixed(3)}; }),
        uncaptioned: figs.filter(f => !(f.querySelector('figcaption .status-label') && f.querySelector('figcaption').textContent.trim().length > 20)).map(f => (f.querySelector('img') || {}).currentSrc),
        fieldWidths: [...document.querySelectorAll('.enquiry-form input:not([type=radio]), .enquiry-form select, .enquiry-form textarea')].filter(e => vis(e) && e.id !== 'f-output' && e.id !== 'f-website').map(e => ({id: e.id, w: e.getBoundingClientRect().width})),
        radios: [...document.querySelectorAll('.choice input')].filter(vis).map(e => { const r = e.getBoundingClientRect(); return [r.width, r.height]; }),
        labelRadius: [...document.querySelectorAll('.status-label')].filter(vis).map(e => getComputedStyle(e).borderTopLeftRadius).filter(v => v !== '0px'),
        imgRadius: [...document.querySelectorAll('main img')].filter(vis).map(e => getComputedStyle(e).borderTopLeftRadius).filter(v => v !== '0px')
      };
    })(),
    textOutside: [...document.querySelectorAll('body *')].filter(e => vis(e) && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())).filter(e => { const r = e.getBoundingClientRect(); return r.width && (r.right > innerWidth + 1 || r.left < -1); }).map(e => e.tagName + '.' + e.className + ': ' + e.textContent.trim().slice(0, 50)).slice(0, 10)
  };
}"""


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="site")
    ap.add_argument("--out-base", default="records/qa-runs")
    ap.add_argument("--axe", default=str(Path(__file__).parent / "vendor" / "axe.min.js"))
    args = ap.parse_args()
    root = Path(args.root).resolve()
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = Path(args.out_base).resolve() / stamp
    if out.exists():
        sys.exit(f"refusing to overwrite existing run directory {out}")
    (out / "screenshots").mkdir(parents=True)
    axe = Path(args.axe).read_text()
    port = free_port()
    httpd = serve(root, port)
    base = f"http://127.0.0.1:{port}/"
    R = Results()
    raw = {}

    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        env = {"run": stamp, "url": base, "root": str(root), "python": sys.version.split()[0], "platform": platform.platform(),
               "chromium": browser.version, "axe": axe.split("axe v")[1].split(" ")[0] if "axe v" in axe else "unknown",
               "site_files": {str(f.relative_to(root)): sha(f) for f in sorted(root.rglob("*")) if f.is_file()}}
        (out / "environment.json").write_text(json.dumps(env, indent=2))

        # ---------- 1. Pages x viewports ----------
        for page_name in PAGES:
            for vname, w, h in VIEWPORTS:
                ctx = await browser.new_context(viewport={"width": w, "height": h})
                pg = await ctx.new_page()
                log = await watch(pg)
                resp = await pg.goto(base + page_name, wait_until="networkidle")
                await pg.screenshot(path=str(out / "screenshots" / f"{page_name[:-5]}-{vname}-fold.png"))
                await settle_lazy(pg)
                L = await pg.evaluate(LAYOUT_JS)
                await pg.screenshot(path=str(out / "screenshots" / f"{page_name[:-5]}-{vname}-full.png"), full_page=True)
                tag = f"{page_name}@{vname}"
                R.add(f"http-200 {tag}", resp.status == 200, resp.status)
                R.add(f"no-console-or-page-errors {tag}", not log["console_errors"] and not log["page_errors"], log["console_errors"] + log["page_errors"])
                R.add(f"no-failed-requests {tag}", not log["failed"], log["failed"])
                ext = [r["url"] for r in log["requests"] if not r["url"].startswith(base)]
                R.add(f"no-third-party-requests {tag}", not ext, ext)
                R.add(f"no-horizontal-scroll {tag}", L["scrollWidth"] <= L["width"], [L["scrollWidth"], L["width"]])
                R.add(f"no-text-outside-viewport {tag}", not L["textOutside"], L["textOutside"])
                R.add(f"fonts-jost-inter-400 {tag}", any(f.startswith("Jost 400") for f in L["fonts"]) and any(f.startswith("Inter 400") for f in L["fonts"]), L["fonts"])
                R.add(f"weights-400-only {tag}", L["weights"] == ["400"], L["weights"])
                R.add(f"families-prescribed-latin-and-arabic-only {tag}", set(L["families"]) <= {"Jost", "Inter", "Noto Sans Arabic"}, L["families"])
                bad_img = [i for i in L["imgs"] if i["visible"] and not i["ok"]]
                R.add(f"visible-images-load {tag}", not bad_img, bad_img)
                R.add(f"images-have-alt-attr {tag}", all(i["alt"] is not None for i in L["imgs"]), [i["src"] for i in L["imgs"] if i["alt"] is None])
                R.add(f"one-h1 {tag}", L["h1"] == 1, L["h1"])
                R.add(f"landmarks {tag}", L["landmarks"]["header"] == 1 and L["landmarks"]["main"] == 1 and L["landmarks"]["footer"] == 1, L["landmarks"])
                R.add(f"in-page-anchors-resolve {tag}", all(a["ok"] for a in L["anchors"]), [a for a in L["anchors"] if not a["ok"]])
                fl = L["footerLinks"]
                overlaps = [(a["text"], b["text"]) for i, a in enumerate(fl) for b in fl[i + 1:] if a["left"] < b["right"] and b["left"] < a["right"] and a["top"] < b["bottom"] - 0.5 and b["top"] < a["bottom"] - 0.5]
                R.add(f"footer-targets-44px {tag}", all(x["h"] >= 44 for x in fl), [x for x in fl if x["h"] < 44])
                R.add(f"footer-targets-no-overlap {tag}", not overlaps, overlaps)
                await pg.add_script_tag(content=axe)
                ax = await pg.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}}).then(r=>({violations:r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target.join(' '))})),incomplete:r.incomplete.map(v=>({id:v.id,nodes:v.nodes.length}))}))")
                R.add(f"axe-zero-violations {tag}", not ax["violations"], ax["violations"])
                # ---- Part B design-system conformance (v0.3) ----
                D = L["ds"]
                ALLOWED = set(D["tokenSizes"])  # every --gem-type-size-* and --site-type-*-size value (Latin styles)
                R.add(f"ds-type-scale {tag}", set(D["sizes"]) <= ALLOWED, D["sizes"])
                R.add(f"ds-concept-full-3x2 {tag}", all(abs(f["box"] - 1.5) < 0.01 and abs(f["nat"] - 1.5) < 0.01 for f in D["frames"]), D["frames"])
                R.add(f"ds-images-captioned-with-status {tag}", not D["uncaptioned"], D["uncaptioned"])
                R.add(f"ds-field-max-420 {tag}", all(x["w"] <= 420.5 for x in D["fieldWidths"]), D["fieldWidths"])
                R.add(f"ds-radio-24 {tag}", all(abs(w - 24) < 0.5 and abs(h - 24) < 0.5 for w, h in D["radios"]), D["radios"])
                R.add(f"ds-square-labels-and-images {tag}", not D["labelRadius"] and not D["imgRadius"], [D["labelRadius"], D["imgRadius"]])
                raw[tag] = {"layout": L, "axe_incomplete": ax["incomplete"], "requests": len(log["requests"])}
                # cross-page links (files) resolve
                if vname == "desktop-1440":
                    src = await (await ctx.request.get(base + page_name)).text()
                    head_src = src[:src.find("</head>")]
                    head = await pg.evaluate("({title:document.title,vp:document.querySelector('meta[name=viewport]').content})")
                    head["styles"] = head_src.count("<style")  # as served, before any test injection
                    R.add(f"head-integrity {page_name}: title, standard viewport, no inline styles", head["title"] == TITLES[page_name] and "viewport-fit" not in head["vp"] and head["styles"] == 0, head)
                    for href in sorted(set(L["links"])):
                        target, _, frag = href.partition("#")
                        r2 = await ctx.request.get(base + target)
                        ok = r2.status == 200
                        if ok and frag:
                            chk = await ctx.new_page(); await chk.goto(base + target)
                            ok = await chk.evaluate("(f)=>!!document.getElementById(f)", frag); await chk.close()
                        R.add(f"link-resolves {page_name} -> {href}", ok, r2.status)
                    # footer edge taps hit the intended link
                    taps = []
                    for a in fl:
                        for y in (a["top"] + 2, a["bottom"] - 2):
                            await pg.evaluate("(y)=>scrollTo(0, y - 200)", y)
                            sy = await pg.evaluate("scrollY")
                            got = await pg.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);const l=e&&e.closest('a');return l?l.textContent.trim():null}", [a["left"] + 4, y - sy])
                            taps.append((a["text"], got))
                    R.add(f"footer-edge-taps {page_name}", all(t == g for t, g in taps), [t for t in taps if t[0] != t[1]])
                await ctx.close()

        # ---------- 2. Failure modes: no JS, blocked script, init exception ----------
        for mode in ["no-js", "blocked-script", "init-exception"]:
            for vname, w, h in [("mobile-375", 375, 812), ("desktop-1440", 1440, 900)]:
                ctx = await browser.new_context(viewport={"width": w, "height": h}, java_script_enabled=(mode != "no-js"))
                pg = await ctx.new_page()
                log = await watch(pg)
                if mode == "blocked-script":
                    await pg.route("**/assets/js/site.js", lambda r: r.abort())
                if mode == "init-exception":
                    src = (root / "assets/js/site.js").read_text().replace('var DELIVERY = { endpoint: "" };', 'throw new Error("QA forced init failure");')
                    await pg.route("**/assets/js/site.js", lambda r: r.fulfill(status=200, content_type="text/javascript", body=src))
                await pg.goto(base + "index.html")
                await pg.wait_for_timeout(600)
                tag = f"{mode}@{vname}"
                nav = await pg.evaluate("[...document.querySelectorAll('#primary-nav a')].map(a=>({t:a.textContent.trim(),v:a.offsetParent!==null&&a.getBoundingClientRect().height>0}))")
                if mode == "init-exception" and w < 1024:
                    # navigation installed fine; the failure is in the form block, so the Menu must still work
                    await pg.click(".nav-toggle"); await pg.wait_for_timeout(250)
                    nav = await pg.evaluate("[...document.querySelectorAll('#primary-nav a')].map(a=>({t:a.textContent.trim(),v:a.offsetParent!==null&&a.getBoundingClientRect().height>0}))")
                    await pg.click(".nav-toggle")
                R.add(f"primary-nav-visible-or-disclosable {tag}", all(x["v"] for x in nav) and len(nav) == 6, nav)
                mark = await pg.evaluate("(()=>{const m=document.querySelector('.mark');const cs=getComputedStyle(m);return {ok:m.complete&&m.naturalWidth>0,mask:cs.maskImage||cs.webkitMaskImage||'none',clip:cs.clipPath,opacity:cs.opacity,w:m.getBoundingClientRect().width}})()")
                R.add(f"static-mark-complete {tag}", mark["ok"] and mark["mask"] == "none" and mark["clip"] == "none" and mark["opacity"] == "1" and mark["w"] >= 32, mark)
                await pg.screenshot(path=str(out / "screenshots" / f"{mode}-{vname}-fold.png"))
                if mode != "init-exception" or vname == "mobile-375":
                    # keyboard reach of every primary destination without the disclosure
                    if mode == "no-js":
                        reached = []
                        await pg.keyboard.press("Tab")
                        for _ in range(9):
                            await pg.keyboard.press("Tab")
                            reached.append(await pg.evaluate("document.activeElement.textContent.trim()"))
                        R.add(f"primary-nav-keyboard-reachable {tag}", all(t in reached for t in ["Approach", "Amenities & Packaging", "Packages", "Who it serves", "Partners", "Draft an enquiry"]), reached)
                state = await pg.evaluate("({disabled:document.getElementById('prepare-button').disabled,notice:document.getElementById('form-unavailable').offsetParent!==null})")
                R.add(f"prepare-disabled-and-notice-shown {tag}", state["disabled"] and state["notice"], state)
                if mode == "no-js":
                    dn = await ax_description(pg, "#prepare-button")
                    R.add(f"a11y: disabled submit explains why {tag}", "needs JavaScript" in dn, dn)
                if mode != "init-exception":
                    qs = await pg.evaluate("({disabled:document.getElementById('quote-button').disabled,notice:document.getElementById('quote-unavailable').offsetParent!==null})")
                    R.add(f"quote-disabled-and-notice-shown {tag}", qs["disabled"] and qs["notice"], qs)
                    await pg.fill("#q-rooms", "120"); await pg.focus("#q-rooms"); await pg.keyboard.press("Enter")
                    await pg.click("#quote-button", force=True, timeout=2000); await pg.wait_for_timeout(300)
                url_before = pg.url
                n_before = len(log["requests"])
                for k, v in SYNTH.items():
                    sel = {"name": "#f-name", "organisation": "#f-org", "email": "#f-email", "message": "#f-message"}[k]
                    await pg.fill(sel, v)
                await pg.focus("#f-name"); await pg.keyboard.press("Enter")
                await pg.focus("#f-email"); await pg.keyboard.press("Enter")
                await pg.click("#prepare-button", force=True, timeout=2000)
                await pg.wait_for_timeout(800)
                leaked = [r for r in log["requests"] if any(x in (r["url"] + str(r["post"] or "")) for x in ["Synthetic", "example.invalid", "qa%40", "Synthetic+Tester", "rooms=", "package="])]
                R.add(f"fail-closed-no-data-request {tag}", not leaked and pg.url == url_before and "?" not in pg.url, {"url": pg.url, "leaked": leaked})
                await ctx.close()

        # ---------- 3. Normal form journey (JS on) ----------
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        await ctx.grant_permissions(["clipboard-read", "clipboard-write"])
        pg = await ctx.new_page()
        log = await watch(pg)
        await pg.goto(base + "index.html#enquire")
        await pg.wait_for_timeout(300)
        init = await pg.evaluate("({disabled:document.getElementById('prepare-button').disabled,notice:document.getElementById('form-unavailable').hidden})")
        R.add("form-initial-enabled-notice-hidden", (not init["disabled"]) and init["notice"], init)
        await pg.click("#prepare-button")
        errs = await pg.locator("#error-list li").all_inner_texts()
        R.add("form-empty-four-linked-errors", len(errs) == 4 and await pg.evaluate("document.activeElement.id") == "f-name", errs)
        await pg.locator("#error-list a").nth(2).click()
        R.add("form-error-link-focuses-radio", await pg.evaluate("document.activeElement.name") == "interest")
        await pg.locator("#enquiry-form").screenshot(path=str(out / "screenshots" / "form-errors.png"))
        await pg.fill("#f-name", SYNTH["name"]); await pg.fill("#f-email", "invalid"); await pg.check("#f-interest"); await pg.fill("#f-message", SYNTH["message"])
        await pg.click("#prepare-button")
        errs = await pg.locator("#error-list li").all_inner_texts()
        R.add("form-invalid-email-only", errs == ["Enter an email address in the format name@example.com."], errs)
        await pg.fill("#f-email", SYNTH["email"]); await pg.fill("#f-org", SYNTH["organisation"])
        n0 = len(log["requests"])
        await pg.click("#prepare-button"); await pg.wait_for_timeout(200)
        outp = await pg.input_value("#f-output")
        R.add("form-valid-prepared-not-sent", await pg.locator("#form-result").is_visible() and await pg.evaluate("document.activeElement.id") == "form-result" and len(log["requests"]) == n0 and "Name: Synthetic Tester" in outp, {"requests": log["requests"][n0:], "output": outp})
        await pg.locator("#enquiry-form").screenshot(path=str(out / "screenshots" / "form-prepared.png"))
        await pg.click("#copy-output"); await pg.wait_for_timeout(200)
        R.add("clipboard-granted-copies-draft", await pg.evaluate("navigator.clipboard.readText()") == outp and "Copied" in await pg.inner_text("#copy-status"))
        await pg.evaluate("Object.defineProperty(navigator,'clipboard',{value:{writeText:()=>Promise.reject(new Error('denied'))},configurable:true})")
        await pg.click("#copy-output"); await pg.wait_for_timeout(200)
        sel = await pg.evaluate("(()=>{const o=document.getElementById('f-output');return [o.selectionStart,o.selectionEnd,o.value.length]})()")
        R.add("clipboard-denied-selects-text", sel[0] == 0 and sel[1] == sel[2] and "not available" in await pg.inner_text("#copy-status"), sel)
        # stale draft: every field type invalidates
        edits = [("name", "fill", "#f-name", "Changed Name"), ("organisation", "fill", "#f-org", "Other Org"), ("email", "fill", "#f-email", "other@example.invalid"),
                 ("interest", "check", "#f-interest-partner", None), ("message", "fill", "#f-message", "Changed message.")]
        stale = {}
        for field, how, sel_, val in edits:
            await pg.click("#prepare-button"); await pg.wait_for_timeout(100)
            ready = await pg.locator("#form-result").is_visible()
            if how == "fill": await pg.fill(sel_, val)
            elif how == "select": await pg.select_option(sel_, val)
            else: await pg.check(sel_)
            await pg.wait_for_timeout(80)
            vis = await pg.locator("#form-result").is_visible()
            stale[field] = {"was_ready": ready, "result_visible_after_edit": vis, "output_after_edit": await pg.input_value("#f-output"), "status": await pg.inner_text("#draft-status")}
        R.add("stale-draft-invalidated-every-field", all(v["was_ready"] and not v["result_visible_after_edit"] and v["output_after_edit"] == "" and "changed" in v["status"] for v in stale.values()), stale)
        await pg.click("#prepare-button"); await pg.wait_for_timeout(100)
        R.add("re-prepare-uses-current-values", "Changed Name" in await pg.input_value("#f-output") and "Becoming a partner" in await pg.input_value("#f-output"))
        await pg.click("button[type=reset]"); await pg.wait_for_timeout(80)
        clr = await pg.evaluate("({name:document.getElementById('f-name').value,result:document.getElementById('form-result').hidden,invalid:document.querySelectorAll('[aria-invalid]').length,focus:document.activeElement.id,status:document.getElementById('draft-status').textContent,out:document.getElementById('f-output').value})")
        R.add("clear-resets-all-state", clr["name"] == "" and clr["result"] and clr["invalid"] == 0 and clr["focus"] == "f-name" and clr["status"] == "" and clr["out"] == "", clr)
        R.add("normal-journey-no-requests-after-load", len([r for r in log["requests"] if r["method"] != "GET" or "?" in r["url"]]) == 0)
        # keyboard sequence + skip link
        await pg.goto(base + "index.html"); seq = []
        for _ in range(20):
            await pg.keyboard.press("Tab")
            seq.append(await pg.evaluate("(()=>{const e=document.activeElement;const host=e.closest('.package-card')||e;const cs=getComputedStyle(host);return {t:(e.getAttribute('aria-label')||e.textContent||e.id).trim().slice(0,30),outline:cs.outlineStyle+' '+cs.outlineWidth}})()"))
        raw["keyboard_desktop"] = seq
        R.add("focus-visible-ring-2px (on the control, or on the whole package card for its radio)", all(s["outline"] == "solid 2px" for s in seq), [s for s in seq if s["outline"] != "solid 2px"])
        await pg.goto(base + "index.html"); await pg.keyboard.press("Tab"); await pg.keyboard.press("Enter")
        R.add("skip-link-moves-focus-to-main", await pg.evaluate("document.activeElement.id") == "main")
        await ctx.close()

        # mobile disclosure
        ctx = await browser.new_context(viewport={"width": 375, "height": 812}); pg = await ctx.new_page()
        await pg.goto(base + "index.html"); await pg.wait_for_timeout(200)
        hidden_before = await pg.evaluate("document.querySelector('#primary-nav a').offsetParent===null")
        await pg.focus(".nav-toggle"); await pg.keyboard.press("Enter"); await pg.wait_for_timeout(250)
        opened = await pg.get_attribute(".nav-toggle", "aria-expanded")
        await pg.screenshot(path=str(out / "screenshots" / "mobile-menu-open.png"))
        await pg.keyboard.press("Tab"); nxt = await pg.evaluate("document.activeElement.textContent.trim()")
        await pg.keyboard.press("Escape")
        R.add("mobile-disclosure-enter-tab-escape", hidden_before and opened == "true" and nxt == "Approach" and await pg.get_attribute(".nav-toggle", "aria-expanded") == "false" and await pg.evaluate("document.activeElement.className") == "nav-toggle", {"hidden_before": hidden_before, "opened": opened, "next": nxt})
        cta = await pg.evaluate("(()=>{const r=document.querySelector('.hero .button').getBoundingClientRect();return r.bottom})()")
        R.add("compact-first-screen-shows-primary-action-375x812", cta <= 812, cta)
        await ctx.close()
        ctx = await browser.new_context(viewport={"width": 320, "height": 640}); pg = await ctx.new_page(); await pg.goto(base + "index.html")
        cta = await pg.evaluate("document.querySelector('.hero .button').getBoundingClientRect().bottom")
        raw["cta_bottom_320x640"] = cta
        R.add("compact-first-screen-shows-primary-action-320x640", cta <= 640, cta)
        await ctx.close()

        # ---------- 3b. Audit fixes (v0.4, 2026-10-11) ----------
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}); pg = await ctx.new_page(); log = await watch(pg)
        await pg.goto(base + "index.html", wait_until="networkidle")
        n_cta = await pg.evaluate("document.querySelectorAll('main a[href=\"#enquire\"]').length")
        R.add("audit-C2 enquiry reachable from hero, offer and partner sections", n_cta >= 3, n_cta)
        hdr = await pg.evaluate("getComputedStyle(document.querySelector('.site-header')).position")
        await pg.mouse.wheel(0, 1600); await pg.wait_for_timeout(500)
        tucked = await pg.evaluate("document.querySelector('.site-header').classList.contains('is-tucked')")
        await pg.mouse.wheel(0, -300); await pg.wait_for_timeout(500)
        back = await pg.evaluate("(()=>{const h=document.querySelector('.site-header');const r=h.getBoundingClientRect();return !h.classList.contains('is-tucked')&&r.top===0&&getComputedStyle(h).visibility==='visible'})()")
        R.add("audit-C2 header sticky, tucks reading down, returns on scroll up", hdr == "sticky" and tucked and back, {"position": hdr, "tucked": tucked, "back": back})
        # focus never hidden under the sticky header (WCAG 2.4.11)
        await pg.goto(base + "index.html", wait_until="networkidle"); await pg.add_style_tag(content="html{scroll-behavior:auto!important}"); hidden_focus = []
        for i in range(45):
            await pg.keyboard.press("Tab"); await pg.wait_for_timeout(40)
            o = await pg.evaluate("(()=>{const a=document.activeElement;const h=document.querySelector('.site-header');if(h.contains(a)||a===document.body)return null;const r=a.getBoundingClientRect();const pts=[[r.left+r.width/2,r.top+r.height/2],[r.left+2,r.top+2],[r.right-2,r.bottom-2]];const hidden=pts.every(([x,y])=>{const e=document.elementFromPoint(x,y);return !e||h.contains(e)});return hidden?(a.textContent||a.id).trim().slice(0,30):null})()")
            if o: hidden_focus.append(o)
        R.add("audit-C2 focus not obscured by sticky header (45 tab stops)", not hidden_focus, hidden_focus)
        # section CTA preselects the topic and withdraws a stale draft
        await pg.goto(base + "index.html", wait_until="networkidle")
        await pg.fill("#f-name", SYNTH["name"]); await pg.fill("#f-email", SYNTH["email"]); await pg.check("#f-interest"); await pg.fill("#f-message", SYNTH["message"])
        await pg.click("#prepare-button"); await pg.wait_for_timeout(100)
        had = await pg.locator("#form-result").is_visible()
        await pg.locator('a[data-interest="f-interest-partner"]').click(); await pg.wait_for_timeout(600)
        st = await pg.evaluate("({checked:document.getElementById('f-interest-partner').checked,result:!document.getElementById('form-result').hidden,status:document.getElementById('draft-status').textContent,hash:location.hash})")
        R.add("audit-C2 partner CTA selects topic and withdraws stale draft", had and st["checked"] and not st["result"] and "changed" in st["status"] and st["hash"] == "#enquire", st)
        before = await pg.evaluate("(()=>{const e=document.getElementById('email-output');return {hidden:e.hidden,href:e.getAttribute('href')}})()")
        await pg.click("#prepare-button"); await pg.wait_for_timeout(100)
        after = await pg.evaluate("(()=>{const e=document.getElementById('email-output');return {hidden:e.hidden,href:e.getAttribute('href')||''}})()")
        href = after["href"]
        from urllib.parse import urlparse, parse_qs, unquote
        u = urlparse(href); q = parse_qs(u.query)
        body_ok = q.get("body", [""])[0] == await pg.input_value("#f-output")
        await pg.fill("#f-message", "Edited after drafting.")
        stale_mail = await pg.evaluate("(()=>{const e=document.getElementById('email-output');return {hidden:e.hidden,href:e.getAttribute('href')}})()")
        R.add("audit-C1 email hand-off: hidden until drafted, addressed to the owner address, body equals the draft, withdrawn on edit (link not followed)",
              before["hidden"] and before["href"] is None and not after["hidden"] and u.scheme == "mailto" and unquote(u.path) == "mish3labdul@gmail.com" and q.get("subject") == ["Enquiry for GEM"] and body_ok and stale_mail["hidden"] and stale_mail["href"] is None,
              {"before": before, "href_prefix": href[:60], "body_ok": body_ok, "after_edit": stale_mail})
        dp = await ax_description(pg, "#prepare-button"); dq = await ax_description(pg, "#quote-button")
        R.add("a11y: working submit buttons are not described by the hidden needs-JavaScript notices",
              "needs JavaScript" not in dp and "needs JavaScript" not in dq and "This page sends nothing." in dp and "This page sends nothing." in dq, {"prepare": dp, "quote": dq})
        R.add("audit-C1 no requests from the drafting journey", len([r for r in log["requests"] if r["method"] != "GET"]) == 0)
        # you-are-here marking
        await pg.evaluate("document.getElementById('partners').scrollIntoView()"); await pg.mouse.wheel(0, -10); await pg.wait_for_timeout(600)
        cur = await pg.evaluate("[...document.querySelectorAll('#primary-nav a[aria-current]')].map(a=>a.textContent.trim())")
        R.add("audit-I5 nav marks the current section", cur == ["Partners"], cur)
        # C5 form is shorter; reset is not beside the primary action
        nf = await pg.evaluate("document.querySelectorAll('#enquiry-form input:not([type=radio]):not([type=hidden]):not(#f-website), #enquiry-form select, #enquiry-form textarea:not(#f-output)').length")
        pair = await pg.evaluate("(()=>{const p=document.getElementById('prepare-button').getBoundingClientRect();const r=document.querySelector('button[type=reset]').getBoundingClientRect();return Math.round(r.top-p.bottom)})()")
        R.add("audit-C5 four text inputs, reset separated from primary action", nf == 4 and pair >= 24, {"inputs": nf, "gap": pair})
        await ctx.close()
        # I2 menu: outside tap and tabbing out close it; scrim present
        ctx = await browser.new_context(viewport={"width": 375, "height": 812}); pg = await ctx.new_page()
        await pg.goto(base + "index.html", wait_until="networkidle")
        await pg.click(".nav-toggle"); await pg.wait_for_timeout(250)
        scrim = await pg.evaluate("getComputedStyle(document.querySelector('.site-header'),'::before').backgroundColor")
        await pg.mouse.click(180, 700); await pg.wait_for_timeout(200)
        out1 = await pg.get_attribute(".nav-toggle", "aria-expanded")
        await pg.click(".nav-toggle"); await pg.wait_for_timeout(200)
        for _ in range(7): await pg.keyboard.press("Tab")
        await pg.wait_for_timeout(150)
        out2 = await pg.get_attribute(".nav-toggle", "aria-expanded")
        R.add("audit-I2 menu has scrim, closes on outside tap and on tabbing out", "0.64" in scrim and out1 == "false" and out2 == "false", {"scrim": scrim, "outside": out1, "tabout": out2})
        await ctx.close()

        # ---------- 3c. Concept packages: discussion request (2026-10-11) ----------
        for vw, vh in [(1440, 900), (375, 812)]:
            ctx = await browser.new_context(viewport={"width": vw, "height": vh}); await ctx.grant_permissions(["clipboard-read", "clipboard-write"])
            pg = await ctx.new_page(); log = await watch(pg); qt = f"@{vw}"
            await pg.goto(base + "index.html", wait_until="networkidle"); await pg.add_style_tag(content="html{scroll-behavior:auto!important}")
            init = await pg.evaluate("({disabled:document.getElementById('quote-button').disabled,notice:document.getElementById('quote-unavailable').hidden})")
            R.add(f"quote-initial-enabled-notice-hidden {qt}", not init["disabled"] and init["notice"], init)
            await pg.click("#quote-button"); await pg.wait_for_timeout(100)
            errs = await pg.locator("#quote-error-list li").all_inner_texts()
            R.add(f"quote-empty-two-linked-errors-focus-first {qt}", errs == ["Choose a package.", "Enter a positive whole number of rooms."] and await pg.evaluate("document.activeElement.id") == "pkg-room", errs)
            # whole card is the target: click the middle of the Wall-mounted card's table
            await pg.evaluate("document.querySelectorAll('.package-card')[1].querySelector('.spec-table').scrollIntoView({block:'center'})"); await pg.wait_for_timeout(100)
            box = await pg.locator(".package-card").nth(1).locator(".spec-table").bounding_box()
            await pg.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            R.add(f"quote-whole-card-selects {qt}", await pg.is_checked("#pkg-wall"))
            # arrow keys move within the group
            await pg.focus("#pkg-wall"); await pg.keyboard.press("ArrowRight"); await pg.wait_for_timeout(50)
            R.add(f"quote-arrow-keys-move-selection {qt}", await pg.is_checked("#pkg-travel") and await pg.evaluate("document.activeElement.id") == "pkg-travel")
            ring = await pg.evaluate("getComputedStyle(document.querySelectorAll('.package-card')[2]).outlineStyle")
            R.add(f"quote-selected-card-shows-focus-ring {qt}", ring == "solid", ring)
            await pg.fill("#q-rooms", "abc"); await pg.click("#quote-button"); await pg.wait_for_timeout(100)
            errs = await pg.locator("#quote-error-list li").all_inner_texts()
            inv = await pg.get_attribute("#q-rooms", "aria-invalid"); desc = await pg.get_attribute("#q-rooms", "aria-describedby")
            R.add(f"quote-invalid-rooms-only {qt}", errs == ["Enter a positive whole number of rooms."] and inv == "true" and "q-rooms-hint" in desc and "q-rooms-error" in desc, [errs, inv, desc])
            await pg.fill("#q-rooms", "120"); await pg.check("#q-stationery")
            await pg.click("#q-sampling")
            tg = await pg.evaluate("({p:document.getElementById('q-sampling').getAttribute('aria-pressed'),t:document.getElementById('q-sampling').textContent,s:document.getElementById('q-sampling-status').textContent})")
            R.add(f"quote-sampling-toggle-label-state-status {qt}", tg == {"p": "true", "t": "Remove sampling from brief", "s": "Sampling selected."}, tg)
            n0 = len(log["requests"])
            await pg.click("#quote-button"); await pg.wait_for_timeout(150)
            out_ = await pg.input_value("#q-output"); href = await pg.get_attribute("#quote-email", "href") or ""
            from urllib.parse import urlparse, parse_qs, unquote
            u = urlparse(href); qq = parse_qs(u.query)
            expect = "Concept discussion for GEM\nConcept package: Travel set\nEstimated rooms: 120\nArrival stationery interest: Yes\nSampling interest: Yes\nAvailability and specifications are pending."
            R.add(f"quote-drafted-not-sent-email-handoff {qt}", out_ == expect and await pg.evaluate("document.activeElement.id") == "quote-result" and unquote(u.path) == "mish3labdul@gmail.com" and qq.get("subject") == ["Concept discussion for GEM: Travel set"] and qq.get("body") == [expect] and len(log["requests"]) == n0,
                  {"out": out_, "href": href[:80], "requests": log["requests"][n0:]})
            await pg.click("#quote-copy"); await pg.wait_for_timeout(150)
            R.add(f"quote-copy {qt}", await pg.evaluate("navigator.clipboard.readText()") == expect)
            stale = {}
            for name, act in [("package", lambda: pg.check("#pkg-room")), ("rooms", lambda: pg.fill("#q-rooms", "80")), ("stationery", lambda: pg.uncheck("#q-stationery")), ("sampling", lambda: pg.click("#q-sampling"))]:
                await pg.click("#quote-button"); await pg.wait_for_timeout(80)
                ready = await pg.locator("#quote-result").is_visible()
                await act(); await pg.wait_for_timeout(80)
                stale[name] = {"ready": ready, "after": await pg.locator("#quote-result").is_visible(), "href": await pg.get_attribute("#quote-email", "href"), "status": await pg.inner_text("#quote-status")}
            R.add(f"quote-stale-request-withdrawn-every-control {qt}", all(v["ready"] and not v["after"] and v["href"] is None and "changed" in v["status"] for v in stale.values()), stale)
            await pg.locator("#packages").screenshot(path=str(out / "screenshots" / f"packages-{vw}.png"))
            R.add(f"quote-no-data-requests {qt}", len([r for r in log["requests"] if r["method"] != "GET" or "?" in r["url"]]) == 0)
            await ctx.close()

        # ---------- 4. Motion, reduced motion, forced colours ----------
        for mode, opts in [("standard-motion", {}), ("reduced-motion", {"reduced_motion": "reduce"}), ("forced-colors-light", {"forced_colors": "active", "color_scheme": "light"}), ("forced-colors-dark", {"forced_colors": "active", "color_scheme": "dark"})]:
            ctx = await browser.new_context(viewport={"width": 1440, "height": 900}, **opts); pg = await ctx.new_page()
            await pg.goto(base + "index.html")
            frames = []
            for t in (50, 400, 900, 1600):
                await pg.wait_for_timeout(t - (frames[-1][0] if frames else 0))
                path = out / "screenshots" / f"{mode}-mark-{t}ms.png"
                await pg.locator(".hero-mark").screenshot(path=str(path))
                frames.append((t, sha(path)))
            same = len({h for _, h in frames}) == 1
            R.add(f"mark-identical-in-every-frame {mode}", same, frames)
            anim = await pg.evaluate("document.getAnimations().map(a=>a.animationName||a.constructor.name)")
            R.add(f"no-autoplay-animations {mode}", anim == [], anim)
            if mode.startswith("forced"):
                await pg.screenshot(path=str(out / "screenshots" / f"{mode}-fold.png"))
                hb = await pg.evaluate("getComputedStyle(document.querySelector('.site-header')).backgroundColor")
                R.add(f"beige-artwork-keeps-ink-field {mode}", hb == "rgb(18, 23, 29)", hb)
            await ctx.close()

        # ---------- 5. Text enlargement and zoom ----------
        for w in (1440, 768, 375, 320):
            ctx = await browser.new_context(viewport={"width": w, "height": 900}); pg = await ctx.new_page()
            await pg.goto(base + "index.html"); await pg.wait_for_timeout(200)
            await pg.evaluate("""()=>{const es=[...document.querySelectorAll('body *')];const v=es.map(e=>[e,getComputedStyle(e).fontSize,getComputedStyle(e).lineHeight]);for(const [e,s,l] of v){e.style.fontSize=parseFloat(s)*2+'px';if(l!=='normal')e.style.lineHeight=parseFloat(l)*2+'px'}}""")
            await pg.wait_for_timeout(150)
            L = await pg.evaluate(LAYOUT_JS)
            clipped = await pg.evaluate("""()=>{const out=[];for(const e of document.querySelectorAll('h1,h2,h3,h4,p,li,a,label,legend,button,figcaption,span')){if(e.offsetParent===null||e.closest('.trap,.visually-hidden'))continue;let a=e.parentElement;const r=e.getBoundingClientRect();while(a&&a!==document.body){const cs=getComputedStyle(a);if(/hidden|clip/.test(cs.overflowX+cs.overflowY)&&!a.classList.contains('table-wrap')){const ar=a.getBoundingClientRect();if(r.right>ar.right+1||r.left<ar.left-1||r.bottom>ar.bottom+1){out.push(e.tagName+': '+e.textContent.trim().slice(0,40));break}}a=a.parentElement}}return out.slice(0,10)}""")
            await pg.screenshot(path=str(out / "screenshots" / f"text200-stress-{w}.png"), full_page=True)
            R.add(f"text200-stress-no-loss {w}", L["scrollWidth"] <= L["width"] and not L["textOutside"] and not clipped, {"scroll": [L["scrollWidth"], L["width"]], "outside": L["textOutside"], "clipped": clipped})
            await ctx.close()
        for label, cssw, dpr in [("zoom200-of-1280", 640, 2), ("zoom400-of-1280", 320, 4)]:
            for page_name in PAGES:
                ctx = await browser.new_context(viewport={"width": cssw, "height": 400}, device_scale_factor=dpr); pg = await ctx.new_page()
                await pg.goto(base + page_name); await pg.wait_for_timeout(200)
                L = await pg.evaluate(LAYOUT_JS)
                R.add(f"{label} reflow {page_name}", L["scrollWidth"] <= L["width"] and not L["textOutside"], [L["scrollWidth"], L["textOutside"]])
                if page_name == "index.html":
                    await pg.screenshot(path=str(out / "screenshots" / f"{label}-index-fold.png"))
                await ctx.close()

        # ---------- 6. Public-root restrictions ----------
        ctx = await browser.new_context()
        for probe in PROBES:
            r = await ctx.request.get(base + probe)
            R.add(f"public-root-excludes {probe}", r.status == 404, r.status)
        await ctx.close()

        # ---------- 7. Lab performance (bounded, one cold sample) ----------
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900}); pg = await ctx.new_page(); cdp = await ctx.new_cdp_session(pg)
        await cdp.send("Network.enable"); await cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
        await cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": 150, "downloadThroughput": 200000, "uploadThroughput": 93750})
        await cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
        await pg.add_init_script("window.__m={lcp:0,cls:0};new PerformanceObserver(l=>{for(const e of l.getEntries())__m.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)__m.cls+=e.value}).observe({type:'layout-shift',buffered:true});")
        await pg.goto(base + "index.html", wait_until="load"); await pg.wait_for_timeout(3000)
        perf = await pg.evaluate("({lcp:Math.round(__m.lcp),cls:__m.cls,fcp:Math.round(performance.getEntriesByName('first-contentful-paint')[0].startTime),bytes:performance.getEntriesByType('resource').reduce((a,e)=>a+e.transferSize,0)+performance.getEntriesByType('navigation')[0].transferSize,requests:performance.getEntriesByType('resource').length+1})")
        perf["conditions"] = "Chromium headless, 1440x900, DPR1, 4x CPU throttle, 150ms latency, 200000 B/s down, cache disabled, loopback server; viewport only, no scroll"
        raw["perf"] = perf
        await ctx.close()
        await browser.close()
    httpd.shutdown()

    summary = {"run": stamp, "total": len(R.checks), "passed": len(R.checks) - len(R.failed), "failed": len(R.failed), "failures": R.failed}
    (out / "checks.json").write_text(json.dumps(R.checks, indent=1))
    (out / "observations.json").write_text(json.dumps(raw, indent=1))
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "failures"}))
    for f in R.failed:
        print("FAIL", f["id"], json.dumps(f["detail"])[:400])
    print("output:", out)
    sys.exit(1 if R.failed else 0)


if __name__ == "__main__":
    asyncio.run(main())
