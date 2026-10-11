# Change record

Authorization: user requested implementation of confirmed corrections in the 11 October CLAUDE_HANDOFF, with owner-dependent proposals pending and fresh QA in a new directory. Starting audited files matched the earlier audit baseline. Snapshot: BASELINE_SHA256.txt and raw-results/baseline.json; files about to change were copied to before/.

## Existing files changed

- `site/privacy.html`: G26-02; replace privacy paragraphs/headings to cover enquiry and package drafts, external email-app handling and pending final policy. Temporary identity and source-authority qualifications remain.
- `site/index.html`: G26-03 failure notice titles/bodies, G26-06 range hint, G26-09 adjacent copy guidance and accessible email-link description. No package heading, price/quotation framing, recipient, temporary identity, image, working name or concept qualification changed.
- `site/assets/css/site.css`: G26-05; regular semantic emphasis and `font-synthesis:none`. No palette, spacing scale, font asset or weight changed.
- `site/assets/js/site.js`: G26-06 error message; correct stale delivery comment. Validation expression, bounds, draft composition, recipient, guarded initialization, copy/reset and submission interception remain unchanged.
- `qa/run_qa.py`: retain assertions, update expected room-count error text, add `.DS_Store` and `assets/.DS_Store` denial probes. Original 482 assertions plus two probes = 484.

## Removed from public root

`site/.DS_Store` and `site/assets/.DS_Store` (10,244 bytes each). Exact copies retained in before/site/. They are Finder metadata, not original artwork. No source scene or font was removed. Test server returns 404 for both URLs.

## New QA files

`qa/font_validation.py`: actual glyph/font validation using Chromium CDP and required FontFace status/style/weight. Samples use visible current text/values/placeholders. Probes are off-screen, removed after use, and never persisted into website source. Paint is awaited before platform-font inspection. Returned failed brand states are explicit even when fallback remains legible.

`qa/run_corrections_qa.py`: loopback-only targeted tests with new timestamped output, synthetic fields and no email-app navigation. Covers current glyph usage/normal loads, blocked required fonts, unsupported Arabic fallback, regular emphasis, responsive/no-network-error states, room boundaries, very long full-copy preservation, stale/reset state, privacy scope, metadata denial and script/initialization failures. Expected negative font cases are clearly separated from acceptance.

`qa/README.md`: requires both QA commands and states engine/native/production limits. No project dependency installation or new third-party runtime resource.

## Evidence

All new reports, before copies, diffs, screenshots, logs and machine-readable results are in this remediation directory. Earlier records and packages were not overwritten. Final comparison and hashes are in INTEGRITY.md and FINAL_SHA256.txt. Formal owner approval/publication and any later remediation of pending proposals require separate scope.
