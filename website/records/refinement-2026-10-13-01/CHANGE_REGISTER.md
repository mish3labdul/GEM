# GEM website v0.5.4 — asset-led refinement

**Status: PROPOSED WORKING PREVIEW / DRAFT REVIEW.** Decision ID: OWNER-REFINEMENT-20261013. The owner requested review of GEMV2 and Gem Mockups New, then refinement of the existing site using installed tools, delivered as a separate draft PR. No new source-document instructions were adopted as user authorization.

## Baseline and reconciliation

Repository: mish3labdul/GEM. Parent branch: `codex/gem-concept-discussion-20261011` at `9fad24f76c7eeb2d39d20142a46a0f3119719c51` (PR #14). New branch: `codex/gem-assets-website-refinement-20261013`. Draft PR targets that parent branch, not main. Arabic PRs #12/#15 remain separate and unchanged.

The supplied collection has 360 files: 349 in GEMV2, 11 in Gem Mockups New; 106 match existing repository bytes. All 11 new mockups remain local, with per-image findings and pending public-use/artwork status. No full supplied catalogue, reference PDFs or unresolved mockup pixels are uploaded by this change. Exact matching bytes are identity evidence, not approval.

The standalone website/QA comparison has 80 identical files and six differences: homepage, site CSS, site JavaScript, QA README, regression suite, and correction suite. Repository v0.5.3 remains the baseline. Standalone bytes and readable differences remain preserved locally; no standalone-only change was silently imported. See source-comparison.csv.

## Changes

- Homepage: use the existing GEM-WEB-B01 responsive family image beside the hero message; preserve the full 3:2 frame, descriptive alt text, amber colourway qualifier and concept/non-production caption. Image is eager and high priority. Compact/tablet views retain message/actions before the image.
- CSS: keep the supplied static symbol at 48px, use the existing 12-column grid for the split hero, give package bodies the shared spacing step, align specification columns, and place the complete mounted portrait on the existing Beige surface.
- No image bytes changed and no redundant derivatives were created: existing 480/800/1200 exports suffice. No new imagery was generated. Previously tracked imagery remains concept artwork, not production photography or confirmed SKUs.
- JavaScript, fonts, tokens, SVG marks, factual copy, existing concept captions, form behavior and page destinations remain unchanged. No API or backend change.

Exact pre-refinement homepage and CSS are preserved under `archive/website-v0.5.3-before-asset-refinement/site/`. Before/after SHA-256 values are in site-revisions.json; v0.5.4 extends the existing lineage. To recover, restore those two files from the archive in a new corrective commit; do not reset history or overwrite a release.

## Retained limitations

New mockups introduce generated mark interpretations, numeric/repeated product identifiers, unapproved collection naming, incomplete function labels, unresolved mounted compatibility and/or raster Arabic. These are reference candidates, not approved replacements. Native Arabic font/shaping, linguistic, visual and reading-order acceptance is not established. Missing required fonts or unsupported glyph fallback fails brand acceptance.

B01/B02, D8 restrictions, logo production-master acceptance, legal/IP deferrals, supplier validation, final product colour/naming/specifications and native accessibility gates stay as recorded. No merge, deployment, release, production-artwork approval, email or enquiry was performed.

The migration inventory redirects the two superseded active-file entries to exact archived bytes and adds two owner-authorized v0.5.4 entries. Source hashes, prior decisions and all frozen branch inventories are retained; no validator exception is introduced.
