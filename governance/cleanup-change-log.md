# Cleanup implementation — 11 October 2026

## Source and migration

Implementation branch: `codex/gem-repository-cleanup-20261011`, based on published V3.0 commit `4e8c7f18f73d9f4b368fcd735c1cd5e3725a879d`. Intended PR target: `main`; the released baseline commits are intentionally included because main predates V3.0. Neither main nor the release branch is changed by preparing this PR.

- Froze all four existing branches, tags, annotated V3.0 ref, full release metadata and 14 attachment digests/URLs. ZIP source SHA-256: `fc5e4213c9139a916caaff2dacd9cac524f8f8570597db9c262287cb6f294555`.
- Inventoried 6,416 source records, including all frozen branch files and relevant local material. Source scope/ref disambiguates repeated paths. SHA-256 establishes exact identity, not approval.
- Preserved all 994 released-baseline files under `archive/baseline-v3.0/`, plus two older branch variants. The baseline README, internal manifests and two tracked build caches remain unchanged evidence.
- Copied RP01 released files into current document folders without editing their bytes. All 14 attachment copies match frozen published digests. Original PDFs remain historical; no new export is created.
- Catalogued 170 working brand assets. Supplied filenames and bytes remain unchanged; existing controlled X12 proposals are mapped, not issued as fictional versioned artwork. Production-master and taxonomy acceptance remain pending.
- Imported 38 newer localization files from `d8921f13aa485a5afeefb42dd6cbee105eee0149` into a separately labelled working area. No release promotion or native-language acceptance is inferred.
- Imported the named ZIP's 80 files unchanged into `website/site/`. Imported associated source imagery, records, historical QA, transport archives and later correction evidence. Retired assets remain outside the public root.
- Independent local audit folders, unrelated previews/exports and experimental creative packages are catalogued as outside this import, with originals retained locally. The selected concept masters/provenance required by the site are included. New machine caches are excluded. Three removed Finder-metadata files intentionally preserved by earlier correction evidence are retained byte-identically with `.evidence.bin` suffixes and mapped in the register.

## Active reference changes

Added current navigation, naming/exception rules, source/disposition registers, duplicate report, collection checksums, packaging and validation tools. Repaired the active QA README's link to the relocated correction evidence; preserved its original bytes under `archive/website-original/qa/README.md`. Maintained QA scripts remain byte-identical. Archived source-era build scripts and original document descriptions retain historical paths; resolve those paths using the migration register.

No site HTML/CSS/JavaScript, image, logo, font, DOCX or PPTX content was changed. Public page names and anchors remain unchanged. No link redirect service is introduced; original commit/tag URLs remain accessible.

## Verification

- Frozen ZIP baseline: **484/484** Chromium regression checks passed; output preserved under `website/records/cleanup-qa/baseline-regression/`.
- Migrated site: **484/484** regression checks passed; output under `website/records/cleanup-qa/regression/20261011T185626Z/`.
- Migrated site correction/font suite: **76/76** checks passed; output under `website/records/cleanup-qa/corrections/`. Includes fail-closed initialization, blocked-font and unsupported-Arabic negative cases, clipboard/draft preservation and no submission.
- Visual comparison: **6/6 pixel-identical** full-page pairs, all three pages at 1440 and 375 widths in Chromium 143.0.7499.4 with identical reduced-motion settings. Paired renders, comparison JSON and manually inspected contact sheet under `website/records/cleanup-qa/visual-comparison/`.
- Preview: `GEM_Website_Preview_v0.5.1_2026-10-11.zip`, exactly 80 site files; entry bytes match the frozen source ZIP. Archive compression/metadata differ; source payload does not. SHA-256: `eb073e84933149128f66c34a3479b6a9ba7c91bbfc92e07934852a626cf95fcf`.
- Collection validation checks every recorded imported/archive destination, frozen-branch inventory completeness, catalogue, published-copy digests, active navigation/HTML/CSS paths and anchors, Unicode/case collisions, ZIP contents and fresh remote release/branch preservation. Final checksum verification is recorded separately in `verification.md`.

## Retained limitations

B01/B02, D8 external-issue restrictions, working logo-master acceptance, Part C production validation, Part D concept status, Legal/IP deferral and native/browser/human acceptance limitations remain unchanged. No WCAG certification, release, deployment, merge, font substitution or document remediation is claimed.

## Follow-up — owner website decisions WD-18/WD-19

Website working v0.5.2 keeps the recipient only in draft handoff and presents all packages as concepts for discussion. Availability/specifications remain pending. Three public source files changed; previous source and QA versions were archived with exact path/digest lineage, and the inventory now has 6,421 records. Active specification labels wrap under 200% text enlargement after a captured initial failure. Final regression is 484/484 and correction/font checks 76/76. See `website/records/24_Owner_Concept_Discussion_and_Contact.md` and `25_Concept_Discussion_Verification_v0.5.2.md`. The version-aware validator preserves both historical and current preview packages, and permits unmerged follow-up checkouts while checking main retains original cleanup history. Unanswered owner questions remain open.

## Follow-up — owner decisions WD-20/WD-21, 12 October 2026

Working website v0.5.3 retains amber and ivory hand-wash concept variations with explicit scene captions and an unchanged-image hash register. Supporting records distinguish this concept choice from final product colour and naming approval. Room estimates accept positive whole decimal numbers without the previous 100,000 ceiling or numeric rounding. Regression passes 484/484; correction/font checks pass 81/81. Exact previous sources are archived and mapped; the source inventory now has 6,425 records. See website records 26/27 for scope and evidence.

## Arabic working localization — 12 October 2026

PR #14 owner approval was recorded at unchanged head as a comment because the authenticated account is also the author; merging remains separate. Website v0.6.0 adds three Arabic counterparts, reciprocal language links, proposed translation register, interim licensed Noto Sans Arabic 400, isolated LTR draft values and maintained bilingual QA. Fresh suites pass 487/487, 81/81 and 196/196. The site-only preview contains 87 files. Exact v0.5.3 originals and failed QA iterations are preserved; the source inventory has 6,438 rows. See website records 28/29.

Private Part D R4 was recovered exactly; new private A/B/C editable proposals cover 193 slides and six correspondence variants are available for internal review. Only permitted control/QA records are published. Structural and encoded glyph checks do not establish native acceptance; remaining layout, mixed-direction, reading-order and linguistic gates are explicit. No new document PDF was exported. Released documents/tag/attachments and B01/B02/D8 remain unchanged.

## Native Office continuation — 12 October 2026

Current private proposals are A R14, B R16 and C R12. Native PowerPoint exports cover all 193 current slides; bounded retests repair mixed-script spacing, Western-number units, trademark order, A31 placeholder direction, B10 technical reference and C62 disposition-line fit. Source letters/digits and original media bytes are preserved. Failed isolate/embedding and mislabeled export tests are excluded and retained privately.

All six R3 correspondence variants passed Word edit/save/reopen/restoration, full-page visual inspection and native Accessibility Assistant checks (zero issues each). A task-scoped font configuration removed an auxiliary renderer fallback; actual temporary font resources use only Inter/Jost/Noto Sans Arabic Regular. Native Word is layout authority; the auxiliary bilingual-continuation margin difference is retained as a limitation. Canonical document bytes are unchanged by native QA. Presentation all-slide visual/font/body-editing/reading-order and assistive-technology acceptance, linguistic approval and D8 external issue remain open. Part D retains its 23 reading-order review items. New matching document PDFs remain withheld. See the permitted native Office QA report in the document continuation folder.
