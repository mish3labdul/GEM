# GEM™ Arabic Part D — R4 recovery QA

11 October 2026. Overall: WORKING DRAFT / INTERNAL REVIEW ONLY / PENDING LOCALIZATION APPROVAL.

## Source and exact targets

Authoritative branch `claude/gem-worktree-safety-30b559`, commit `4e8c7f18f73d9f4b368fcd735c1cd5e3725a879d`, rechecked live before editing. Promoted source: `GEM_V3.0_RP01_Release_Artifact_Promotion/17_release_artifacts/04_amenities_concept/GEM_BRAND_AmenitiesPackagingConcept_PartD_v3.0_20261009.pptx`. Highest authority remains the Final Brand Approval Register plus subsequent documented FA01/HR01/OD01/RP01 decisions; historical RC2 gates are not silently reset. Excluded External Partners Brief.

Editable target `01_editable/internal_review/GEM_BRAND_AmenitiesPackagingConcept_PartD_AR_L10N01_R4.pptx`; PDF target `02_pdf/internal_review/GEM_BRAND_AmenitiesPackagingConcept_PartD_AR_L10N01_R4.pdf`. Exact hashes in SHA256SUMS.txt and finalizer/PDF verification records.

## Finding and acceptance register

| ID | File/page | Finding or test | Governing source / correction | Severity | Result |
|---|---|---|---|---|---|
| R4-01 | PPTX all 24 slides | Footer/page metadata interrupted meaningful content in R3 native pane. | Part B accessibility / AX01: explicit title, associated imagery/content, notes, status, footer sequence. Reordered only where overlap stacking is unchanged. Reading_Order_Register.json records every shape. | P1 HIGH | PASS static; PENDING native/AT |
| R4-02 | PPTX/PDF 5,6,8,11,12,14–17,20,23 | Latin-language punctuation caused incorrect RTL bracket mirroring in R3. | Part B mixed-direction / M05: restored Arabic language context on 256 neutral runs; keep Inter punctuation glyphs and exact logical bracket text. Arabic letters remain Noto Sans Arabic, tracking 0. | P1 HIGH | PASS local visual; PENDING native |
| R4-03 | PDF all pages | Prior local export corrupted Arabic extraction; online export substituted Calibri. | Part B typography/accessibility: reject prior exports. Local R4 fonts all prescribed and embedded. Repair 17 missing Unicode mappings only from exporter cluster evidence; 393 paragraph ActualText values derived exactly from the editable source. | P0 BLOCKER | PASS bounded local extraction/font test; native viewer copy/search PENDING |
| R4-04 | PDF all pages | Generic heading tags and root language needed correction. | Part B document accessibility: H1 cover, H2 subsequent titles; ar-SA root and per-paragraph language; original 24 bookmarks retained without duplicates. | P1 HIGH | PASS structure; PENDING per-Latin-span/AT |
| R4-05 | PDF 23 | Register semantics/editability. | Source native table preserved. PDF retains one Table, five TR, three TH and twelve TD. | P1 HIGH | PASS structure; PENDING native navigation |
| R4-06 | PPTX all media | Native R3 save removed compatibility fallback PNGs. | Supplied Asset Kit / preservation requirement: canonical R4 retains all 21 media members exactly; unchanged SVGs plus all four fallbacks. Two SVG hashes matched exact kit paths. | P1 HIGH | PASS source package |
| R4-07 | Private embedding trial | No embedded fonts in R2; online conversion lacked required families. | Supplied OFL/fonts: all three fsType=0. Created isolated full-font uncompressed EOT trial; headers and sfnt payload hashes checked. Trial is not promoted into canonical R4. | P1 HIGH | PASS structural trial; native embedding/online conversion PENDING |
| R4-08 | PPTX native reopen/edit/save | Computer bridge unavailable. | User acceptance test: reconnect/reset/select app retried; exact error `Sky Computer Use native pipe closed before response`. Do not reuse R3 result as an R4 pass. | P1 HIGH | PENDING |
| R4-09 | Cover, catalogue, 5,23 / AT | Screen-reader speech, meaningful order and table interaction unavailable. | Part B / QA evidence discipline: tag presence cannot establish accessible experience. | P1 HIGH | PENDING |
| R4-10 | PPTX technical notes / remaining batches | Source English technical notes retained; A/B/C and company-wide localization unfinished. | Translation scope: translate meaningful notes in subsequent controlled batch while preserving paths, IDs and citations. | P2 MEDIUM | PENDING |
| R4-11 | Arabic wording, descriptor, product terminology | Newly localized text is proposed. English signature lines deliberately unchanged. | HR01/OD01 / Approval Register: professional Arabic editor and owner acceptance; no Arabic legal name invented. | Governance | REQUIRES OWNER |
| R4-12 | Physical output/product specifications | No new stock, CMYK, Pantone, tolerance or supplier fact introduced. | Part C / supplier evidence gates retained. | Governance | REQUIRES SUPPLIER |

## Independent technical evidence

R4_Verification.json checks exact final PDF: 24 pages, 1200 × 675 pt presentation canvas, 393 exact source-bound paragraphs, 31 meaningful image alternatives, 24 bookmarks, H1/H2 and table structure. Poppler emits visual-order RTL segments with explicit RLE/PDF controls; the audit reverses only those explicit segments and applies NFC. It does not strip marks, normalize whitespace, remove punctuation or sort words. No mismatches. This is an extraction test, not a native viewer search/clipboard or screen-reader pass.

17 ToUnicode additions derive from explicit exporter ActualText clusters. Whole-paragraph logical alternatives use `/Span` marked content because Poppler did not honor the same replacement on `/P` wrappers. Redundant nested cluster replacement wrappers were removed after the evidenced mappings were repaired. Existing vector/text painting operators are identical before and after semantic repair on every page: no hidden overlay, text-to-image or glyph repainting. qpdf syntax/stream check passed. All font resources are embedded Inter, Jost or Noto Sans Arabic with ToUnicode maps; no substituted family.

Presentation finalizer and first-party Artifact Tool import passed for exact R4; native table 23 present, 24 slides, declared font families only. Three cover out-of-bounds warnings are retained source cropping (ring/artwork), not newly introduced content clipping. Source shape positions/sizes and overlap pairs are unchanged. All 24 final PDF pages inspected individually at 1600 px. Slides 3 headline and dark statuses retain R2 fixes; brackets visible and correctly oriented locally. Production printing, alternative renderers and native re-export may behave differently and remain unvalidated.

## Governance and publication

FA01 AC20 remains authorized with formal deferrals and release-scope exclusions. Arabic L10N01/R4 remains internal review; no production/localization/external-PDF authority is conferred. Supplier, rights, master/font acceptance and D8 restrictions retained. The public draft PR receives QA/control records and hashes, not the internal PPTX/PDF or page render set. No merge performed.

## Baseline regression and next batch

Compared R2 and R4 at identical 1600 px output size, masking only text-shape bounds with 4 px padding. Twenty-three pages were pixel-identical outside those bounds. Cover had two antialiased ring-edge pixels differing by at most 14 RGB levels; both full pages reviewed, with source geometry/media unchanged. No visual-content correction required. Baseline_Visual_Regression.json records this bounded result.

Part B translation resumed: 103 nonempty paragraphs across source slides 1–5 have proposed Arabic or explicit English/technical retention. Remaining 30 slides and full Part B editable/PDF production are pending. Two source-governance wording issues are held for owner review, not silently corrected. Parts A/C source inventories refreshed; their translations remain pending.

Final PDF header explicitly set to PDF 1.7 to support retained tagging/language features; qpdf rechecked after the change.
