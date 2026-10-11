# GEM™ Part D Arabic — native validation follow-up R3

11 October 2026. **WORKING DRAFT / PENDING LOCALIZATION APPROVAL / INTERNAL REVIEW ONLY. NO VALIDATED PDF RELEASE.**

This is a QA iteration, not a new approved document revision. Canonical editable source remains L10N01 R2. Native R3 test copies and rejected PDF exports remain private. Repository source branch `claude/gem-worktree-safety-30b559`, commit `4e8c7f18f73d9f4b368fcd735c1cd5e3725a879d`, reverified through GitHub API this turn. No source release, original R2 package or unrelated work overwritten.

## Native application evidence

Microsoft PowerPoint for Mac 16.113.3 (26092714). Computer access succeeded. Opened the exact R2 output from Recents; Save As to isolated native_r3 folder; selected Arabic title on slide5; deleted its text and undid the deletion; saved, closed and reopened the copy. Restored title appeared, no repair/missing-font prompt observed. Package comparison confirms all concatenated slide text unchanged after the test. Arabic title ribbon showed Noto Sans Arabic 43.5pt, Regular, Arabic (Saudi Arabia). This establishes bounded native editability; text insertion through the automation API was not verified.

Native visual review: slides1,2,3,5,13,14,23. Slide3 headline/image separation holds. Slide23 table fits and text remains real native table content. Full24-slide native visual/keyboard/RTL review is not claimed; prior headless review remains separate evidence.

PowerPoint Accessibility Assistant initially reported zero missing alt text, missing titles, missing table headers and text-contrast findings, but **24 check-reading-order items**. These are review prompts, not automatically24 proven failures. Slide5 reading-order inspection did verify a defect: footer identifiers are positions4–5 before product/image content; internal-review status is last at19. Review meaningful sequence on every slide, place main title first, keep product/image descriptions associated, then notes/status/footer; preserve overlapping artwork and decorative exclusions. Existing alternative text includes concept status and pending vector-master acceptance. Tag presence or checker zero counts do not validate Arabic alternatives.

## Results

| Check / finding | Location | Result | Required action / governing source |
|---|---|---|---|
| PowerPoint access | Native application | PASS | Prior permission blocker resolved; do not carry it forward as current. |
| Open/save/close/reopen | R2-derived private24-slide copy | PASS, bounded | Native Mac workflow completed; no Windows/Word/AT claim. D8 acceptance scope retained. |
| Editable Arabic title | Slide5 | PASS, bounded | Select/delete/undo restored real text; file text comparison unchanged. Insertion not verified. |
| Required font observed | Slide5 ribbon; local PDF | PASS, bounded | Noto Sans Arabic observed; local PDF uses Noto/Inter/Jost. Production/font-rights acceptance not inferred. |
| Repaired slide3 collision | Slide3 native view | PASS | Existing R2 geometry separation holds; Part A composition. |
| Native reading order | Slide5;24 slides flagged for review | FAIL / PENDING, P1 | Verified early-footer defect on slide5; remaining full sequence review pending. Part B accessibility. |
| Native punctuation | Slides5,23 square-bracket placeholders | FAIL, P1 | Brackets render facing inward incorrectly after explicit Latin punctuation split. Restore correct mirrored RTL bracket handling using prescribed fonts and test native/local export; retain exact logical placeholders. Part B mixed-direction rules. |
| Local PDF Arabic copy/search |24-page PowerPoint Best for printing export; p5 | FAIL, P0 | Quartz export uses incomplete Unicode mappings; extracted Arabic includes incorrect letters/marks. Use a font-faithful export with correct logical text. No text-as-image workaround. |
| Local PDF semantics | Same export | FAIL, P1 | Untagged; no language metadata. Must retain headings, alternatives, table semantics and language before accessibility validation. |
| Online accessible PDF fonts | Authorized Microsoft online export | FAIL, P0 | Only Calibri font subsets found; Noto Sans Arabic, Inter, Jost absent. Rejected immediately under user no-substitution instruction. Do not issue or use as brand master. |
| Online PDF text | p5 | FAIL, P0 | Arabic spaces/diacritics and character order differ; tagged flag does not pass copy/search or reading order. |
| Online PDF language | Root metadata | See PDF_Export_Audit.json / unvalidated | Language and per-span tags must be checked after a valid export exists. |
| Native-save asset preservation | Private PPTX | FAIL for strict byte-preserving master, P1 | Native save retained17 of21 media parts and removed four PNG compatibility fallbacks (image1,3,18,20). Original vector/media bytes retained among survivors; canonical R2 untouched. Restore supplied fallback parts/relationships or retain source-preserving master before controlled handoff. |
| Screen reader / complete semantic validation | All slides | PENDING | Available UI checker is not assistive-technology acceptance. |
| New Arabic language approval | All new paragraphs/alternatives | REQUIRES OWNER | HR01/M16. Existing approvals do not authorize new copy. |
| Notes / remaining batches | Part D notes; Parts A/B/C and company documents | PENDING | Scope remains incomplete. |
| Supplier / physical production | All concept products | REQUIRES SUPPLIER | Part C and retained FA01 deferrals; no invented values. |

## Governance and stop condition

Both PDF routes failed. The online conversion was explicitly authorized by the user, then stopped as a usable-output route when required fonts were substituted. Rejected PDFs are not included. PNGs are failure evidence only. No claim of completed localization, accessible release or approved production is made.

FA01 AC20 authorization with formal deferrals and scope exclusions remains unchanged. New Arabic derivative lacks external-issue permission; D8, rights, font/master acceptance, supplier and localization gates remain. No External Partners Brief used.

Next engineering work: correct native RTL punctuation and meaningful reading sequence in a source-preserving derivative, establish a font-faithful tagged PDF export, then retest complete Arabic strings and all-slide layout before linguistic/AT acceptance. Stop release of affected files until these pass.
