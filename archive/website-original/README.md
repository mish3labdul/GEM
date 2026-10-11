# GEM™ website — working build v0.5.1 (PROPOSED, not for publication)

v0.3 aligns the site to the GEM™ Digital Design System V3.0 (Part B) and adds the Part B website concept scenes B01–B04 and a Part D label study. See records 16–18. v0.4 applies the 2026-10-11 UI/UX audit (record 19).

```
site/              Deployable static site. Serve this folder only.
  index.html       Homepage (clients and partners)
  reference.html   Brand and design reference (secondary audience)
  privacy.html     Temporary privacy and legal notice
  assets/css/      gem-tokens.v3.0.css (release package, unchanged) + site.css (site layer)
  assets/js/       site.js (progressive enhancement; makes no network requests)
  assets/fonts/    Jost 400, Inter 400 (SIL OFL 1.1, licences included)
  assets/brand/    Logo kit SVGs, unchanged
  assets/img/      WebP + JPEG derivatives (provenance: records/06, 12 and 17)
qa/run_qa.py       Assertion suite (Playwright + Chromium). Serves site/ on 127.0.0.1 itself and writes a NEW run folder.
qa/vendor/         axe-core 4.x (MPL-2.0) used by the suite
records/           Project records. Read 23_Merge_Uploaded_v2_v0.5.1.md, 22, 21, 20 and 19 first, then 18.
records/qa-runs/   One folder per QA run; never overwritten
source-images/     Original images (not public)
verify_*.py        Session-1 helpers, kept as history only (hard-coded paths; superseded by qa/run_qa.py)
```

Preview: `python3 -m http.server 8000 --bind 127.0.0.1 --directory site`, then open http://127.0.0.1:8000/.
QA: `pip install playwright && python3 -m playwright install chromium`, then `python3 qa/run_qa.py --root site --out-base records/qa-runs`.

Edit copy in the HTML files and styling in `site/assets/css/site.css`, using `--gem-*` tokens only. The header and footer are repeated in each page (static site, no build step), so change all three together. Temporary contact details are marked `data-contact-status="temporary"`.
Do not replace `gem-tokens.v3.0.css` or the brand SVGs by hand.
