# 18 · Verification and handoff — v0.3 (session 3, 2026-10-10)

## Verification
Run `records/qa-runs/20261010T132217Z`. Environment: Playwright, Chromium (headless), axe-core 4.14.0, served from `site/` on 127.0.0.1. **438 assertions, 438 PASS.** This is evidence for one engine with synthetic data. It is not acceptance.

- **Carried over from v0.2 (348):** 3 pages × 5 widths for errors, requests, overflow, fonts, weights, images, landmarks, anchors, footer targets and axe (zero violations); cross-page links; no-JS, blocked-script and init-exception fail-closed modes; the form journey (validation, stale draft, clipboard, Clear); keyboard; static mark across motion and forced-colour modes; 200% text stress and 200/400% zoom reflow; public-root probes.
- **New in v0.3 (90):** Part B conformance at every page and width: type sizes on the token scale; concept frames are 3:2 in both box and source; every image is in a figure whose caption has a status label; fields ≤420px; radios 24×24; square labels and images.
- **Visual review:** full-page screenshots were viewed at 1440, 768 and 375 (homepage) and 1440 (reference page). The layout was corrected once: the #clients intro and scene now share a row on desktop.
- **Lab performance** (one cold sample; same conditions as v0.2): FCP and LCP 1.00s, CLS 0, 275,955 bytes, 10 requests. That is lighter than v0.2's 307,725 because the first image below the fold is now a 3:2 study instead of the 16:9 room set.
- **First screen at 320×640:** the primary action's bottom edge is at 705px (v0.2: 729px). It is still below the fold, as recorded before.
- **axe "incomplete":** colour contrast on 1–2 nodes at 1440/1024 (text over the Ink field). The pairings are approved by calculation (18.0:1 and 8.2:1).

**Not verified:** Safari/Firefox, physical devices, screen readers (including how the new help-plus-error descriptions are announced), native text-only zoom, and real touch.

## State
- Three pages; static HTML/CSS/JS; no third-party requests. All copy and imagery are PROPOSED. Contact details are temporary. No destination is connected.
- Nothing was published, deployed, pushed or merged. The private preview artifact was updated in place.

## Read first next session
This file, records 16 and 17, then record 15 for older open items. Before editing, compare the files with `qa-runs/20261010T132217Z/environment.json`.

## Owner decisions now needed
1. **Accept the concept scenes B01–B04 for public use** and the placements (the design system lists them as PROPOSED, with public use pending). Also accept the new label study and the moves in record 17.
2. **Colourway per product** (hand wash amber or ivory?) and **tier naming** ("Amenities Collection" on B02 is not approved; "Core Collection" is still [REQUIRES OWNER]).
3. **The four deviations in record 16** (fail-closed `disabled`, a single alert, visitor wording for status labels, "Being defined" shown as Conditional): accept them, or decide otherwise.
4. Still open from record 15: real contact details and legal text; a form destination with separate authorization; motion masters; the Arabic edition; testing beyond Chromium.

## Housekeeping
- `records/retired-site-assets/` holds the 12 image files removed from `site/`.
- `records/_transfer/concept-r02-in.tar.gz` on the Mac is a transfer copy (it carried the concept package into the workspace). The owner may delete it along with the other `_transfer` files.
