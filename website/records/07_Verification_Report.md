# 07 · Verification report — homepage v0.1

Environment: local static server (`python3 -m http.server`), headless Chromium 1194 via Playwright 1.56, in the cloud workspace. Scripts: `verify_shots.py`, `verify_func.py` (re-runnable). Raw results: `verify_shots.json`, `verify_func.json`, `perf_lab.json`. Screenshots: `screenshots/`. All results below are from the final build.

## Technical checks performed

| Check | Result | Evidence |
|---|---|---|
| Layout at 1440, 768, 375, 320 px | Renders; no horizontal scroll at any width (scrollWidth = viewport) | `*-full.png`, `*-fold.png` |
| Console errors / page errors | 0 at all four widths | `verify_shots.json` |
| Failed requests | 0 | same |
| Third-party requests | 0 (10 same-origin requests in total) | same |
| Fonts | Jost 400 and Inter 400 loaded from self-hosted files at all widths; h1 computed family Jost. Glyph check: ™ © — – ‘ ’ “ ” & present; → absent (unused) | `verify_shots.json`; fontTools inspection |
| Images | All in-view images load with correct srcset choice (480/800 by width). Threshold study intentionally not displayed and not downloaded below 1024 px | same |
| Anchors | #approach #amenities #clients #partners #enquire #top #main all resolve | `verify_func.json` |
| Headings | One h1; h2 per section; h3/h4 nested correctly; footer column titles h2 | same |
| Landmarks | 1 header, 2 nav (labelled Primary, Footer), 1 main, 1 footer | same |
| Keyboard order | Skip link → logo → 4 nav links → header CTA → hero CTA → hero link → name → organisation → email → role → property → radio group → message → Prepare → Clear → footer links. Matches visual order. Radio group moves with arrow keys | tab sequence output |
| Skip link | Visible on focus; Enter moves focus to `main` | `focus-skiplink.png` |
| Focus ring | 2 px solid, 2 px offset; Ink on light, White on Ink | tab sequence output |
| Mobile menu | aria-expanded false→true on Enter; first link reachable by Tab; Escape closes and returns focus to toggle; closes on link choice | `mobile-375-menu-open.png` |
| Form: empty submit | Error summary (role=alert) with 4 linked messages; inline errors above each control; aria-invalid set; focus to first invalid field | `form-errors-desktop.png` |
| Form: invalid email | Only the email message remains | `verify_func.json` |
| Form: valid submit | "Enquiry prepared. It has not been sent." shown and focused; **no network request made**; composed text in a read-only field | `form-prepared-desktop.png` |
| Clear | Fields, errors, aria-invalid and result all cleared; focus to first field | `verify_func.json` |
| Copy | Uses Clipboard API on secure origins; otherwise selects the text and says so. Not exercised in headless run (no clipboard permission) | code review only |
| Motion | Reveal runs once: ring 0–900 ms, spark ≈900–1100, quarter to 1500, then settles to one unmasked copy | `reveal-300/800/1000/1250/1900ms.png` |
| Reduced motion | No masks, no animation, hover 0 ms; mark shown at rest from first paint | `reduced-motion-t100ms.png` |
| Forced colours (light and dark) | Ink header/hero kept so Beige artwork never sits on white; button borders visible. **Defect found and fixed in this session** | `forced-colors-light-fold.png`, `forced-colors-dark-fold.png` |
| axe-core 4 (WCAG 2.0/2.1/2.2 A/AA + best practice) | 0 violations desktop, 0 mobile; 47 passes; colour-contrast "incomplete" (axe could not resolve backgrounds) → checked by calculation below | `verify_func.json` |
| Contrast (calculated) | White/Ink 18.01:1; Beige/Ink 8.23:1; Ink/Beige 8.23:1. Beige/White 2.19:1 not used for text or logo | WCAG formula |
| Metadata | `lang="en"`, `dir="ltr"`, title, description, theme-color, favicons; `robots: noindex, nofollow` for the preview | `index.html` |
| Public output restrictions | `site/` holds only the page, its CSS/JS, fonts + licences, kit artwork and 3 image sets. No internal records, source images, restricted letterheads, Arabic material or scripts | file listing |
| Performance (lab) | Desktop 1440, 4× CPU throttle, 150 ms latency, 1.6 Mb/s: FCP 0.90 s, LCP 0.90 s, CLS 0.000, 208 KB transferred, 10 requests. Local server, headless; **not field data** | `perf_lab.json` |

## Not verified (gaps)

- Safari, Firefox and real iOS/Android devices — only Chromium was run. The reveal relies on `@property` and CSS masks; browsers without them show the mark at rest after load (graceful, but not observed).
- Screen readers (VoiceOver, NVDA, JAWS) — not run. Automated checks are not manual accessibility acceptance.
- Real 400% browser zoom — approximated by the 320 px reflow test.
- Clipboard copy in a real browser session.
- The built-in browser on your computer cannot open this workspace's local server, so the site was not viewed there.
- No delivery path exists, so no delivery test was possible (by design).

## Editorial judgments (not defects)
- H1 is the fixed secondary line; owner may prefer a more literal headline.
- "Who we work with" uses a Beige surface across a full section; Part A allows Beige for selected surfaces — owner to confirm.
- The hero mark includes the kit's ™; whether ™ appears in artwork and running text is [REQUIRES OWNER · Legal/IP].
