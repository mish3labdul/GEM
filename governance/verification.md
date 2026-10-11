# Cleanup verification

Fresh collection validation passed with no failures before staging: all 6,416 source records have explicit dispositions; imported/archive bytes, catalogue, paths, anchors, release-copy digests, filename collision checks and exact ZIP membership passed. All four frozen source branches, V3.0 tag/ref, published notes and 14 attachment identities/digests/download URLs remained unchanged.

The generated `SHA256SUMS.txt` covers every deliverable file except itself; ignored OS/runtime caches are outside membership. Run `python3 tools/validate_collection.py` for fresh full verification, including remote state. A successful stored report is bounded to its captured state.

Negative utility checks: altered README bytes were correctly rejected by checksum validation, then restored; overwriting the existing ZIP was refused and its SHA-256 remained unchanged. See `tool-negative-checks.json`.

Website baseline and migrated regression: 484/484 each. Migrated correction/font suite: 76/76. Six full-page before/after pairs were pixel-identical at desktop/mobile sizes. Their contact sheet was manually inspected. See `../website/records/cleanup-qa/` for original JSON, environment and screenshots. Chromium-only coverage; native Office/RTL, human screen-reader, other-engine, mail-client, legal and production acceptance remain outside this cleanup.

No document, artwork, site code or source font bytes were edited. Existing historical checksum manifests are preserved byte-identically, not rewritten or represented as newly validated source-era claims. Migration identity is established independently through the inventory and current collection manifest.

## Authorized merge validation

The owner subsequently instructed proceeding with the merge. The remote validator now accepts main advancing only when its history contains both the frozen main commit and the validated checkout HEAD. Other frozen source branches and all release checks remain exact. This prevents the intended merge from becoming a false preservation failure while rejecting a divergent main history or a main that lacks the tested cleanup.

## Subsequent website revisions

Working website revisions use `website/records/site-revisions.json`: each changed public file must identify its previous digest, preserved original, new digest and owner decision record. Historical preview ZIPs are verified against their own version rather than the current site. Main must retain the frozen main history and the original cleanup commit that introduced `source-freeze.json`; an unmerged follow-up PR need not already be present in main. Checkout integrity remains checked independently against the inventory, final checksum manifest and optional Git-index validation.
