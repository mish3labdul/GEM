# 23 · Merge of the uploaded "gem-site-v2" — v0.5.1 (2026-10-11)

**Input:** `gem-site-v2.zip`, uploaded by the owner at 18:16 (SHA-256 `bd47524a75bb3999b223a18e88f45366cea81ddf4983e75ce0a8ec6192f1fca7`; 80 site files plus macOS `__MACOSX` metadata). Compared with the tested v0.5 run `20261011T103930Z`, three files differed: `index.html`, `assets/css/site.css` and `assets/js/site.js`. The other 77 were identical.
**Owner instruction (18:43):** "proceed as recommended". Keep the script fix and the CSS clean-up, restore the homepage head, and add checks.

## Merged (taken byte for byte from the upload)
| File | v0.5 → v0.5.1 | Change | Why it is kept |
|---|---|---|---|
| `assets/js/site.js` | `b786f195c271 → ba116c3de324` | After init, each working submit button is described only by its intro line (`aria-describedby` reset to `form-intro` / `quote-intro`). | **Real accessibility defect in v0.5.** Accessible descriptions include hidden elements, so with the page working, screen readers announced "…needs JavaScript…" on "Draft enquiry" and "Request a quotation". Measured in Chromium's accessibility tree, before and after. The no-JS behaviour is unchanged: the disabled button still explains why. |
| `assets/css/site.css` | `b1dca59c94a8 → bcbce545f495` | Removed unused rules: `.principles-layout`, `.principles`, `.principles-figure`, `.amenities-intro`, `.sequence`, `.caption--inverse`. | No page uses these classes (`principles` appears only as an id on the reference page). |

## Not merged (`index.html` head)
- `<title>` changed to "GEM Website Preview", the private preview's label. The original "GEM™ — Hospitality supplier and partner" is kept.
- `viewport-fit=cover` plus an inline `<style>` padding only the top and bottom with `env(safe-area-inset-*)`. On notched iPhones, edge-to-edge mode without left and right insets puts content under the notch in landscape: logo and headline sit at 32px at 844px wide. It would also leave white bands above the Ink header and below the Ink footer. The inline style also hard-codes `#fff`, `#000` and a 14px system font, outside the tokens. This is inferred from Safari's documented safe-area behaviour; it was not tested on a device.
- These edits match the preview page wrapper, so they were most likely carried in by exporting the preview rather than made deliberately.
- Edge-to-edge, if wanted, needs safe-area padding on all four sides in `site.css` with tokens, then a test on a real iPhone.

## New checks (qa/run_qa.py `78e124c33316 → e811fcf75dc4`)
- **a11y:** working submit buttons are not described by the hidden needs-JavaScript notices; their descriptions contain "This page sends nothing." Read from Chromium's accessibility tree.
- **a11y:** with JavaScript off, the disabled "Draft enquiry" button still explains why (description contains "needs JavaScript").
- **Head integrity** (3 pages): expected title, standard viewport (no `viewport-fit`), and no inline `<style>` in the served `<head>`.

## Verification
- Merged site: run `records/qa-runs/20261011T154529Z`, **482/482 PASS**.
- Control: the same suite against the unmodified upload gives 481/482. Only the homepage head-integrity check fails, as intended, and the new accessibility checks pass there because the upload carries the fix.
- One development run (`…154336Z`) is marked SUPERSEDED: its head check counted a style tag the test itself injects.

Only the merged script and stylesheet changed; `index.html`, images, fonts, brand files and tokens are unchanged.
