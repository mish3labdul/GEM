# Arabic localization — working v0.6.0

Owner instruction, 12 October 2026: implement the approved plan to record PR #14 approval, add Arabic counterparts for all three website pages, reuse shared terminology, and continue private document localization. Decision **WD-22** authorizes this working derivative, not linguistic approval, final font acceptance or publication.

PR #14 approval is recorded in https://github.com/mish3labdul/GEM/pull/14#issuecomment-6114555146 at verified head `9fad24f76c7eeb2d39d20142a46a0f3119719c51`. The authenticated account is the author; the comment is owner authorization, not a separate approving GitHub review. PR #14 remains unmerged.

## Implementation

- Three static Arabic pages under `ar/`, retaining all corresponding page filenames and anchors; reciprocal language navigation and alternate-language links work without JavaScript.
- Arabic root language/direction, zero Arabic tracking, logical CSS layout; Western digits follow OD-G07. Email/number fields and mixed Latin tokens are isolated LTR; arbitrary-length positive room estimates remain exact in both language drafts. User-entered free text uses automatic direction.
- `tools/localization/website-ar.json` contains source-bound proposed translations, retained English signature/programme names, and runtime messages. `build_website_ar.py` regenerates Arabic pages from exact preserved English v0.5.3 templates. No new Arabic legal name is invented.
- Noto Sans Arabic 400 is the existing documented interim face, converted losslessly to WOFF2 without subsetting. The original SIL OFL licence is included. Source/web hashes and embedding permission are in `localization-v0.6.0/font-provenance.json`. Actual browser platform glyph checks must pass; fallback is a failure. Font-family licensing is not brand acceptance.
- English pages gain language links; the compact header uses the permitted 120px logo minimum to fit the added action. Logo/image bytes, tokens, original English copy and existing URLs are preserved. Longer Arabic copy receives script-appropriate line height; brand marks/images are never mirrored.
- Both colourways remain concepts; specifications/availability remain pending. Recipient placement remains draft-only. Privacy/legal/contact placeholders remain explicitly temporary.

## Evidence and limitations

Fresh QA lives under `localization-v0.6.0/qa/`. The first English run identified the obsolete two-font allowlist and the added action overflowing the compact header; both are corrected. The first Arabic stress runner incorrectly compounded parent/child font scaling and exhausted screenshot memory; the runner now snapshots computed sizes before doubling, matching the existing stress method. Failed evidence is retained.

New wording is PROPOSED / PENDING LINGUISTIC APPROVAL. Native speaker, screen reader, other browser engines, legal identity/privacy acceptance and native email-client acceptance remain pending. No backend submission, deployment, merge or release publication. Released V3.0 copies and B01/B02/D8 dispositions remain unchanged.
