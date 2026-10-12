# Bilingual website v0.6.0 — verification, 12 October 2026

WORKING LOCALIZATION / PENDING LINGUISTIC APPROVAL. The English concept baseline and owner decisions WD-18–WD-21 are preserved. WD-22 authorizes the new working Arabic derivative.

| Fresh Chromium suite | Result | Evidence |
|---|---:|---|
| English regression | 487/487 | `localization-v0.6.0/qa/english-regression/20261011T223328Z/` |
| English correction/font | 81/81 | `localization-v0.6.0/qa/english-corrections/20261011T223245Z/` |
| Arabic/bilingual | 196/196 | `localization-v0.6.0/qa/arabic/20261011T224208Z/` |

The Arabic suite covers all six page routes, matching anchors, reciprocal language links, 1440/1024/768/375/320 layouts, responsive images, actual platform glyph fonts, keyboard menu/Escape, 200% text enlargement, mixed-direction tokens, both draft flows, validation/errors, exact very long positive room estimates, no-JavaScript and script-failure behavior, no backend submission, and blocked-font failure. Negative-test passes mean failure was correctly detected; fallback is never accepted. The final Arabic-only version-token isolation refinement does not change the English files tested by the English suites.

Representative mobile top sections were inspected for all three Arabic pages and the desktop reference layout. Full-page browser captures are retained in the suite directories. Original image bytes remain unchanged and are not mirrored. English header/footer language controls and Arabic text flow are intentional visual changes; no pixel-identical pre/post claim is made for localization. Historical cleanup pixel-equality evidence applies only to its original baseline.

## Preview

`website/previews/GEM_Website_Preview_v0.6.0_2026-10-12.zip` contains exactly the 87 files under `website/site/`, with matching entry bytes. It includes the six pages, runtime assets and font licence; it excludes source records, QA, caches and operating-system metadata.

SHA-256: `344951cff81202b14eecdde636a6a673b43df7329c3024c3f3ae4105dc073531`.

## Approval and remaining gates

Owner authorization for PR #14 is recorded in [its approval comment](https://github.com/mish3labdul/GEM/pull/14#issuecomment-6114555146), at head `9fad24f76c7eeb2d39d20142a46a0f3119719c51`. The author account cannot submit its own approving review. No merge was performed.

Website linguistic approval, other browser engines, native screen readers, actual email-client handling and legal/privacy acceptance remain pending. The separate private document continuation has incomplete native acceptance and no new matching PDFs; see [its control record](../../documents/working/arabic-localization-l10n01/05_continuation-20261012/README.md). No WCAG certification, deployment, release publication, production/font-master approval or document sign-off is claimed.
