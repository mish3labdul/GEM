# Fresh verification

Environment: macOS 26.3.1 arm64, Python 3.14.4, Playwright 1.57.0, Chromium 143.0.7499.4, axe-core 4.14.0. Local static site; no application build step. Existing QA server and targeted runner bind only 127.0.0.1 and stop their own ephemeral servers after testing. No real enquiry, mailto navigation, backend connection or deployment.

## Commands actually run

```sh
python3 qa/run_qa.py --root site --out-base remediation-2026-10-11-01/raw-results/regression
python3 qa/run_corrections_qa.py --root site --out-base remediation-2026-10-11-01/raw-results/corrections
```

Shell output was redirected to raw-results/regression.log and corrections.log. Source and records inspected with `rg`, Python reads/hash/diffs and local image viewer. No dependencies installed. Local review skill used to inspect corrections/diffs and surrounding source. The selected Code Review connector exposes remote PR CI checks; there is no local Git repository/PR, so no remote-review claim is made. Review is recorded in CODE_REVIEW.md.

## Results tied to source

- **Regression:** `raw-results/regression/20261011T170638Z/summary.json`: 484 total, 484 passed, zero failed. Preserves earlier 482 assertions with expected room error updated; adds two Finder metadata probes. Covers three pages × 1440/1024/768/375/320 widths, axe, forms, keyboard/focus, safe script failures, no data submission/URL leakage, stale draft, copy/reset, motion, responsive assets, text stress, public-root restrictions and bounded performance.
- **Targeted corrections:** `raw-results/corrections/20261011T171103Z/summary.json`: 76 total, 76 passed, zero failed. Three pages × 1440/768/375/320, actual required loaded regular faces and rendered-glyph fonts, normal network/runtime/reflow, regular emphasis, blocked required-font negative case, unsupported Arabic negative case, room validation and boundaries, copy preservation/guidance, editing/reset, privacy scope, metadata denial and both isolated initialization failures.
- Every tested normal page/font sample passes. Blocking both WOFF2 files returns **FAIL brand acceptance** for both families; the negative assertion passes because the failure was correctly detected. Arabic probes also return FAIL, correctly detecting that current Latin fonts do not support that script. This is not a completed Arabic edition or native-language acceptance.
- Room cases rejected with actionable error and preserved input: empty, 0, -1, 1.5, abc, 100001. Summary links focus the field. 1, 100000 and whitespace-trimmed 120 pass. Ceiling itself unchanged.
- Long-draft full clipboard checks: 164, 35,129 and 105,129 draft characters; encoded mailto lengths 282, 47,235 and 141,235. Clipboard equals complete output in each case. Nothing truncated; no mailto followed; client support remains unverified.
- Both removed metadata URLs return 404. Both forms have truthful unavailable notices in disabled/blocked and affected initialization-failure states. Normal script/keyboard/copy/reset and no-submission checks remain green.

The final site hashes match those captured in both successful runs. INTEGRITY.md and raw-results/final-comparison.json record attribution and final QA/source hashes.

## Initial test-harness failures retained

The first targeted run (`20261011T170837Z`) stopped because Chromium's CSS inspection domain was not enabled. Log retained as corrections-initial-harness-failure.log. The second (`20261011T170924Z`) completed 65/76, with 11 empty platform-font observations caused by reading before layout/paint populated them. Log retained as corrections-unsettled-probe-failure.log. Corrected the helper to enable DOM/CSS and wait two animation frames after loading; final run passes 76/76. No website code was changed to hide those failures. Initial failed outputs are historical harness evidence, not final product results.

## Visual and accessibility scope

Successful runs include full-page captures of all three pages and requested widths, plus failure, room error and long-draft states. Manual image review checked the revised privacy page, error presentation and new copy guidance against existing typography/layout. Font probe nodes are removed before screenshots. Locator screenshots on tall pages may include sticky header position; do not infer a persistent layout defect solely from capture placement.

Regression axe checks report zero violations in tested states; incomplete/manual contrast evidence remains in observations. DOM and keyboard automation are not actual screen-reader testing or certification. Text enlargement/viewport-DPR proxies are not native zoom acceptance. Only Chromium was tested. No new fonts, RTL route, production artwork, legal/IP clearance, supplier/print proof, Safari/Firefox coverage or native email-client acceptance was established.

## Lab sample

One fresh cold loopback sample, Chromium headless, 1440×900 DPR1, CPU 4×, 150ms latency, 200000 B/s down, cache disabled, viewport only: FCP 1024ms, LCP 1868ms, CLS 0, 305168 bytes, 10 requests. This is one lab observation, not field performance/INP or a Core Web Vitals acceptance claim.

## Retest requirements

Run both QA commands after future edits into another new directory. Preserve owner-dependent items in PENDING_DECISIONS.md. Complete WD-15 human/other-engine release checks when authorized/equipped. A regenerated asset, changed typography, connected backend, revised privacy practice or public hosting needs corresponding fresh acceptance evidence; this local correction package does not approve those actions.
