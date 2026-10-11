# 14 · Verification report — v0.2

Run `records/qa-runs/20261010T124726Z`. Environment: Playwright with Chromium 141.0.7390.37 (headless), Python 3.13, axe-core 4.14.0, Linux workspace, served from `site/` on 127.0.0.1 with an ephemeral port. **348 assertions, 348 PASS.** This is evidence for one engine on loopback with synthetic data. It is not acceptance.

## Coverage
| Area | What was asserted | Result |
|---|---|---|
| Pages × widths | 3 pages × 1440, 1024, 768, 375, 320: HTTP 200; no console/page errors; no failed requests; no third-party requests; no horizontal scroll; no text outside the viewport; Jost 400 + Inter 400 loaded; only weight 400 and only Jost/Inter used; every visible image loads; every image has an alt attribute; one h1; header/main/footer landmarks; in-page anchors resolve; footer targets ≥44px and non-overlapping; axe (WCAG 2.0–2.2 A/AA + best practice) zero violations | PASS 255/255 |
| Links | Every cross-page link returns 200 and its fragment exists (21 links) | PASS |
| Failure modes | No-JS, blocked script, forced init exception at 375 and 1440: nav visible or disclosable; complete static mark; Prepare disabled with notice; no data-bearing request on Enter or click | PASS 26/26 |
| Form (JS) | Initial state; empty (4 linked errors, focus); error link to radio group; invalid email; valid (focused result, zero requests); clipboard granted (read-back matches) and denied (text selected); stale draft for 7 fields; re-prepare; Clear | PASS |
| Keyboard | 20-step tab sequence all with 2px solid focus; skip link to `main`; mobile disclosure Enter → Tab → Escape | PASS |
| First screen | Primary action fully visible at 375×812 | PASS (at 320×640 its bottom edge is at 729px, below the fold: recorded, not asserted) |
| Motion | Mark byte-identical across 4 frames in standard, reduced, forced-light and forced-dark modes; no running animations | PASS |
| Forced colours | Header keeps the Ink field behind Beige artwork (light and dark) | PASS |
| Text and zoom | 200% stress simulation at 4 widths with no clipped text; reflow at 640@2x and 320@4x on 3 pages | PASS |
| Public root | 404 for records/, source-images/, qa/run_qa.py, verify_*.py, .git/config, audit folder, README.md | PASS 8/8 |

**Contrast:** axe reports "color-contrast incomplete" on 8 nodes across the runs, where backgrounds could not be resolved (text over Ink and Beige fields). These were checked by calculation: White/Ink 18.01:1, Beige/Ink 8.23:1, Ink/Beige 8.23:1. Beige on White is not used for any text; the one occurrence found this session (the reference page's contents label) was fixed before the final run.

**Lab performance** (one cold sample; not field data): Chromium 1440×900, DPR 1, 4× CPU throttle, 150ms latency, 200,000 B/s down, cache disabled, loopback, viewport only. FCP 0.96s, LCP 0.96s, CLS 0, 307,725 bytes transferred, 10 requests. The extra bytes against v0.1 (208 KB) come from the room-set image in the second viewport section.

## Defects found and fixed during this session
- Reference page overflowed at 375px (scrollWidth 624). Grid children now shrink.
- Partners ring bled into the section above after a clipping change. That section's clipping was restored; its text wraps.
- Reference "On this page" label was Beige on White. It now uses Ink.
- 200% stress: "composed." widened the page at 375/320. Headings now wrap with `overflow-wrap: anywhere`.
- Six unused image derivatives: four removed, two added to the room-set srcset.

## Not verified
- Safari/WebKit, Firefox, physical iOS/Android devices.
- Native browser 200% text-only zoom.
- VoiceOver, NVDA or JAWS announcements, including the live regions for draft status and copy status.
- Real touch input.
- Arabic text inside images is pixels, not live text, so it was not checked for shaping or reading order.
- No delivery path exists, so delivery is untestable by design.
