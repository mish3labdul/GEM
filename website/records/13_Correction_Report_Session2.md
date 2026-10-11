# 13 · Correction report — session 2 (2026-10-10)

**Starting state:** the owner's Mac copy matched the audit's `FILE_MANIFEST_SHA256.txt` (70/70; `final-integrity.json` PASS). The workspace copy matched byte for byte except `records/_update.tar.gz`, which exists only on the Mac. Before write-back the Mac copy was re-verified (70/70 unchanged). A new, separate folder `website-assets-2026-10-10-01/` from another agent was found; no path overlaps, not integrated (see record 15).
**Records 01–08** are unchanged and kept as session-1 history. Supplements: 09–15.
**Final QA run:** `records/qa-runs/20261010T124726Z` — 348 checks, 348 PASS. Two earlier runs from this session are kept and marked `SUPERSEDED.txt`.

## Per task

| Task | Changed paths | Correction | Fresh evidence (run 20261010T124726Z) | Residual limitation |
|---|---|---|---|---|
| **GEM-01** fail closed | `site/index.html` (form), `site/assets/js/site.js` | The only submit button is `disabled` in the markup and has no `action`; with a disabled default button, Enter cannot submit implicitly. A `preventDefault` submit handler is installed first, unconditionally. The button is enabled only after every form handler is installed. Any initialization error leaves it disabled with a visible "needs JavaScript" notice. No destination added. | `fail-closed-no-data-request` and `prepare-disabled-and-notice-shown` PASS for no-JS, blocked-script and forced init-exception at 375 and 1440 (Enter in two fields plus a forced click; no data-bearing request; URL unchanged; no query). `form-valid-prepared-not-sent` PASS (zero requests). | Chromium only. Implicit-submission rules are standard HTML but not observed in WebKit/Gecko. |
| **GEM-02** progressive enhancement | `index.html`, `reference.html`, `privacy.html` (header), `site.css` (nav, hero), `site.js` | Navigation renders as a visible list by default. The Menu button is `hidden` until `site.js` installs its handlers, then the header gets `.nav-ready` and collapses. The hero shows one unchanged static kit symbol, with no masks and no `.js` gating. | `primary-nav-visible-or-disclosable` and `static-mark-complete` PASS ×6. `primary-nav-keyboard-reachable` PASS with JS off (375, 1440). Screenshots: `no-js-*`, `blocked-script-*`, `init-exception-*`. | — |
| **GEM-04** stale draft | `site.js` | Any `input`/`change` after preparing hides the result and empties the draft. A polite status reads "Your details changed. Prepare the enquiry again…". Copy does nothing without a current draft. Clear removes all state. | `stale-draft-invalidated-every-field` PASS for name, organisation, email, role, property, interest and message. `re-prepare-uses-current-values` and `clear-resets-all-state` PASS. | — |
| **GEM-05** footer hit areas | `site.css` | Negative block margins removed. Each footer link is a 44px-high `inline-flex` box in an unpadded list item. | `footer-targets-44px` and `footer-targets-no-overlap` PASS ×15. `footer-edge-taps` PASS ×3 pages: `elementFromPoint` 2px inside the top and bottom edges hits the intended link. | Pointer emulation only, not a physical touch device. |
| **GEM-03** text enlargement | `site.css` | Hero no longer `overflow: hidden`. Grid items `min-inline-size: 0`. Headings `overflow-wrap: anywhere`. The partners section clips only its decorative ring, and its text wraps. | `text200-stress-no-loss` PASS at 1440/768/375/320: the audit's doubling simulation, plus a check that no text box is cut by a clipping ancestor. `zoom200-of-1280` and `zoom400-of-1280` reflow PASS on all 3 pages (CSS viewport 640@2x and 320@4x). Screenshots: `text200-stress-*`, `zoom*`. | At 200% stress and 320px, the hero word breaks as "compose / d." (legible, nothing lost). Not native text-only zoom: font sizes are px tokens, so Chrome's font-size setting has no effect, while page zoom works. Real-browser 200%/400% zoom still needs a manual check. |
| **GEM-14** motion geometry | `index.html`, `site.css`, `site.js` | The masked reveal is removed. The unchanged kit symbol is shown at rest in every mode. The artwork was not redrawn or separated. Motion is withheld until a corrected sequence can be reviewed against motion masters (VAL-14). | `mark-identical-in-every-frame` PASS: frames at 50/400/900/1600ms are byte-identical for standard motion, reduced motion and forced colours light/dark. `no-autoplay-animations` PASS. | The signature reveal from Part A slide 51 is not implemented. A proposal is in record 15. |
| **GEM-06** reproducible QA | `qa/run_qa.py`, `qa/vendor/axe.min.js` (axe-core 4.14.0, MPL-2.0), `README.md` | Parameterized `--root`, `--out-base` and `--axe` (default: the vendored copy). It serves the site itself on 127.0.0.1 with an ephemeral port, refuses to reuse a run folder, writes `environment.json` (versions plus SHA-256 of every served file), `checks.json`, `observations.json` and `summary.json`, and exits non-zero on any FAIL. Synthetic data only; asserts zero data requests. | Three runs in `records/qa-runs/`; the last is authoritative. | `verify_*.py` (session 1) are kept as history and are not runnable as-is (hard-coded paths). The zero-byte `records/_update.tar.gz` (SHA-256 `e3b0c442…b855`, the empty-file hash) is a leftover from session-1 delivery. It holds nothing and can be deleted by the owner; it was not deleted here because the Mac shell has no delete permission. |
| **GEM-09** source reconciliation | `records/09_Source_Register_Supplement_2026-10-10.md` | Adopted workbook (S1, hash re-verified on the Mac), adoption record (S2), FA01/OD01/FD01 overlays, HR01 scope. Corrects record 01's "not supplied". B01 and B02 are carried forward. Record 01 itself is preserved. | Hash re-check: `ccce4613…7ab3`. | Remaining packages (AR01, AX01, D3, D7, NP01, ODI01) are not read in full; the audit's summary-level review is relied on. |

## Owner decisions and content (records 10, 11, 12)
- WD-01…WD-11 applied. CONTENT_REVIEW wording adopted for GEM-10 and GEM-11, and for GEM-12 except the Arabic line, which the owner kept (WD-08). GEM-13 (compact hero) addressed with a 96px compact mark and tighter padding.
- New pages: `reference.html` (principles, label order and production sequence moved off the homepage, per GEM-11) and `privacy.html` (temporary).
- New images: four Part D mockups (record 12).

## Before/after hashes (SHA-256, first 12 characters; full values in `qa-runs/20261010T124726Z/environment.json` and the audit manifest)
| Path | Before | After |
|---|---|---|
| README.md | b45aa9a0b299 | 04e9a1181d7c |
| site/index.html | bcc044ac5be0 | ae1ac48c5f6f |
| site/assets/css/site.css | ad83d0bda6d5 | 89987a5e1ff8 |
| site/assets/js/site.js | 1bb1898a07a9 | ed4bd5dfafcf |
| site/reference.html | — | 2a393d9ad8a3 |
| site/privacy.html | — | 6662e4668011 |
| qa/run_qa.py | — | 5393c63e26c2 |
| 24 image derivatives, 4 source images, 4 records, 2 vendor files | — | listed in `environment.json` and this folder |
Unchanged: all 8 kit/icon files, `gem-tokens.v3.0.css`, both fonts, the 22 session-1 image derivatives, records 01–08, `verify_*.py`.

## Delivery to the owner's Mac (write-back integrity)
- First write-back committed files individually. The file-transfer channel inserted a C2PA "Content Credentials" manifest into image files created in this workspace (the 24 JPEG/WebP derivatives and the QA screenshots), which changed their bytes. HTML, CSS, JS, JSON and Markdown were unaffected. The original Part D PNGs already carry their own C2PA manifests, so they arrived unchanged.
- Fix: the affected files were re-sent inside `.tar.gz` archives and extracted in place by a byte-for-byte write. Final check on the Mac: **247/247 delivered files match the workspace SHA-256** (`records/_transfer/EXPECTED_SHA256.txt`), and **56/56 site files match the tested run** `20261010T124726Z`.
- `records/_transfer/` (13 archives plus the expected-hash list) is left in place because the Mac shell has no delete permission. It holds transfer copies only, outside `site/`, and the owner may delete it.
