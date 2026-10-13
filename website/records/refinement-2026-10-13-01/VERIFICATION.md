# Verification — v0.5.4

13 October 2026. Exact refined source tested on local loopback in Chromium.

| Suite | Run | Passed | Failed |
|---|---|---:|---:|
| regression | 20261013T120200Z | 484/484 | 0 |
| corrections | 20261013T120200Z | 81/81 | 0 |
| refinement | 20261013T120912Z | 50/50 | 0 |

Regression includes desktop/tablet/mobile, 200% text stress, keyboard/focus, reduced motion, no-JavaScript/script-failure paths, local-only drafting/copy/download/clear, package selection and request leakage checks. Correction checks include actual required font/glyph usage, blocked-font failure and intentional unsupported-Arabic rejection. No partial Arabic edition was added.

Targeted layout checks cover full 3:2 hero and package frames, uncut portrait artwork, image priority, viewport containment, first-screen compact CTA reach, column separation, no package-card movement on selection, caption/hover contrast and clean local GET traffic at 1440/768/375/320px.

The first targeted run failed eight assertions because the test compared CSS-uppercased innerText with mixed-case source text and viewport-relative coordinates across automatic scrolling. Diagnosis confirmed unchanged document-coordinate card bounds and correct caption source text. The corrected test uses textContent and document coordinates. The failed run is retained locally; final summaries above use corrected checks. No site change was made to satisfy these measurement errors.

## Detector and tool limits

Impeccable ran once and returned 13 warnings (exit 2), retained in impeccable-detector.json. Existing brand typography/status labels and nested-container spacing triggered pattern warnings; this refinement preserves the established tokens, labels and composition rules. Rendered hover checks on 25 visible enabled desktop text controls found minimum contrast 8.23:1, rather than the static detector's two reported 1.2:1 hover combinations. Sticky positioning was disabled only in the supplementary hover collector to stabilize scrolling; colour styles were not changed. Separate regression checks retain real sticky/focus behavior. New hero caption and CTA contrast were also checked at all four widths. This is bounded evidence, not blanket accessibility acceptance.

Expect 0.0.14 produced no report or output beyond its configured 60-second timeout and was stopped (exit 143). It is not counted as passing. No dependency installation was attempted. Existing Playwright suites and targeted checks provided the browser evidence.

Full raw runs, failed exploratory measurements, local source differences, source status extracts and unresolved-image review stay in the local package. Public checks files retain assertion IDs/statuses without private local filesystem paths. Screenshots are unedited captures of existing publicly tracked concept imagery; full-page captures start at the top.

## Preservation

All 360 supplied originals and 86 standalone source/QA files were rehashed without changes. Repository collection validation, index checks, final manifests and ZIP verification are recorded separately in DELIVERY.md. No claim of cross-browser, device, screen-reader, field-performance, linguistic, legal or supplier acceptance is made.

Review HTML initially declared regular font faces with the implicit CSS `normal` weight descriptor. The strict required-face checker rejected the descriptor although Chromium reported custom Jost/Inter glyphs. Both review pages now explicitly declare real weight 400 and normal style; final review-page checks pass 20/20. No font substitution or new font installation occurred.

Expect also created an ignored .expect folder containing an empty log and ignore file. These were moved intact to local evidence before manifest/index validation; they are not part of the public payload. Public CSV line endings were normalized to LF before the final whitespace check.
