# GEM visual and interaction candidate — 27 October 2026

Status: **draft review candidate**. This record does not change L08, L09, L12, or production deployment status.

## Source and changes

- Base: `main` at `9038de070688f351b688c54aa3e79a3bfd1d73f9` (PR 31). The verified local visual candidate `b9bae6e` was applied to an isolated worktree.
- The tablet hero stack and approved shampoo re-export from `b9bae6e` address V01, V04, V05, V08, and V12. The phone product hint now occupies a strip below the image (V07), and the packaging card focal point is adjusted (partial V11).
- Image zoom targets are buttons with accessible names and Space/Enter activation. The modal traps focus on its close control, closes on Escape, and restores focus. Its image is created when opened. With JavaScript blocked, the product zoom button stays disabled.
- Reduced-motion mode disables cross-page view-transition animation and keeps the header visible during scrolling.

## Verification on this candidate

- Preview build and `check.py`: 10 localized pages, PASS; production-check: 6/6.
- Browser regression: Chromium 33/33 and Firefox 33/33. A 60-load Chromium sweep (10 routes at 320, 360, 390, 768, 1024, and 1440 CSS px) found no horizontal overflow, broken image, or font-error screen.
- Six adversarial product-switch sequences across Arabic/English at 320, 390, and 768 px ended on the requested image, with focus restored after closing the modal.
- Arabic font coverage: all 43 Arabic-script code points present in the built Arabic pages are covered by the bundled `arabic.woff2` cmap (`fc-query`).
- Local Lighthouse mobile lab, English Amenities, three equivalent runs: median score 94, LCP 2,928 ms, CLS 0, TBT 0. The same local setup on `main` measured score 94, LCP 2,928 ms, CLS 0, TBT 0. These are loopback lab results, not field data.

## Open work and release limits

- V02, V03, V06, and V09 need owner-reviewed outpaint assets with source and output provenance. V10 and V13–V16 need master-file re-exports or an explicit visual acceptance decision. The tablet stack hides the home loop at 761–1100 px and starts the still lower on a 1024×768 screen.
- Native Arabic, screen-reader, physical-device, WebKit font-retry, and true 400% browser-zoom reviews remain separate release checks. This candidate is neither merged nor deployed.
- The M8 record calls `social-photo-original.png` an “original photograph.” The owner's 26 October statement classifies the share source as Nano Banana Pro generated, with no third-party inputs (owner-reported). Preserve the historical record and use this correction for future provenance; rights review under L08 remains pending.
