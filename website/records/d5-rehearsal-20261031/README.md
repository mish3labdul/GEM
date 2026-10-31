# D5 400% zoom rehearsal — 31 October 2026

**This is an engineering rehearsal, not the D5 review.** D5 must be run on the final launch candidate (after the privacy notice is merged); this pass used the preview of `main` at `097ec32` (deployment `faac360d-f1a0-435c-aa34-232c83954e2f`). Chromium only.

Method: `website/remake/qa/zoom-400.mjs`, a 320 × 256 CSS px viewport at device scale 4 (what 400% zoom gives on a 1280 px window), English and Arabic, all five pages each, plus journeys. 58 checks: no horizontal scroll; no content pushed outside the viewport; heading present; cookie notice leaves at least half the viewport and its Close button is reachable; the menu opens with its links in view; the enquiry journey (fill, submit, brief visible, copy and download reachable, no horizontal scroll after); the product viewer; the image lightbox by keyboard and Escape.

Result against the preview: **56 of 58 passed. Two failed, in English and Arabic: the cookie notice's Close button sat below the visible part of the notice (about 400 px down in a 256 px viewport), so a visitor had to scroll inside the notice to find it.** Fixed in this change by placing Close at the top of the notice on small widths (DOM order unchanged), with a regression test. Rerun locally after the fix: **58 of 58 passed.**

Not covered: other browsers, real screen readers, a human judgement of readability at 400%. The fix is not deployed until this change is merged and a preview is deployed.
