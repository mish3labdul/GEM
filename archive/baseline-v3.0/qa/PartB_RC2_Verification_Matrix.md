# Part B RC2 — Verification Matrix

**Editable source:** `GEM__Digital_Design_System_V3.0.pptx` (33 slides, SHA-256 `4a6289fd29b3fae2c3121b8d29a5599859ca77b6ff675bdfd1250ba436269708`). It is a condensed deck edition of the design system, not the generator of the 77-page review PDF (`f5905ee9…6eb5c`, unchanged, comparison only). It contains no images, no logo artwork, no token files, no component code and no Storybook; those remain absent from the workspace.

Authority used: V3 Approval Register (highest) → Part A RC2 → Part B (digital domain) → Part C RC2 → earlier versions historical → external standards. Every row below was checked against the register before classification.

| Patch ID | Current source state (deck) | Audit / patch recommendation | Approval-register verification | A/C dependency | Decision | Action | Status |
|---|---|---|---|---|---|---|---|
| PB-01 | Slide 1 "WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING)"; footers "GEM Digital Design System V3.0 · working specification · n" | Version string V3.0 RC2 + document ID on cover and footers | A11 (version/status on every asset); VAL-21 | A 1/79, C 1/77 use "V3.0 RC2", IDs GEM-BG / GEM-PS | IMPLEMENT | Cover status line + ID + date; all footers "GEM™ Digital Design System V3.0 RC2 · working specification · n" | planned |
| PB-02 | Slide 1 tagline in Jost capitals; slide 3 "Tagline. HOSPITALITY, IN PERFECT PROPORTION — fixed" | Reset lowercased bold tagline | B04–B06, AC05 | A 24 | DO NOT IMPLEMENT — ALREADY RESOLVED | None (deck never lowercased it) | n/a |
| PB-03 | Slide 2 has four status classes + extra labels; no edition states | Add edition vocabulary | A11; AA01 | A 4, C 3 define Working → RC → Approved | IMPLEMENT | Add edition-state sentence to slide 2 | planned |
| PB-04 | Slide 4 table row C: "Referenced; not yet issued (DS04, VAL-11)" | Stale; Part C RC2 exists | DS04; AC17 Evidence Required | C RC2 issued | IMPLEMENT | Row → "Issued as Release Candidate 2 · WORKING EDITION / PENDING PRODUCTION VALIDATION (DS04; AC17, VAL-09 to VAL-11 open)" | planned |
| PB-05 | Slide 4 authority: register → Design System v2.1 → BG V2/2.1 → V1 → benchmarks → WCAG | Seven-step order + domain-ownership note | RF01, RF02, DS01; register source hierarchy (formal standards above benchmarks) | A 3, C 2 (identical wording) | IMPLEMENT | Replace list and add note | planned |
| PB-06 | "See 17-qa-release" absent; slide 4 read-order cites PDF section numbers (01…17) | Page references | RF12 | — | IMPLEMENT WITH ADJUSTMENT | Read-order line rewritten with deck slide ranges | planned |
| PB-07 | Slide 5: twelve rows but five names differ from register (Product / Amenities; Procurement / QA; Localization Lead; Document QA; Asset Librarian) | Cite canonical list; digital duties only | Owners & Governance sheet (12 roles); AC19 | A 72 canonical | IMPLEMENT WITH ADJUSTMENT | Rename to register names; add citation sentence | planned |
| PB-08 | "See 07-motion / 08-glyphs" absent | Page references | — | — | DO NOT IMPLEMENT — ALREADY RESOLVED | None | n/a |
| PB-09 | Slide 10 navLabel "Capital navigation"; slide 11 prohibited list has no "sentence-case navigation"; no product-UI rule anywhere | One navigation rule | No register decision on case; L09/L10 tracking | A 36 | IMPLEMENT WITH ADJUSTMENT | Add one rule on slide 11: product UI navigation sentence case, tracking 0 (body/label); navLabel tracked capitals only on editorial signature surfaces | planned |
| PB-10 | p.13 cross-ref | n/a in deck | — | — | ALREADY RESOLVED (covered by PB-09 rule) | None | n/a |
| PB-11 | Slide 9 "deployment rights PENDING VALIDATION (VAL-05, Y03)"; no "see Licenses" | Real cross-reference | L06, VAL-05 | C 15 Font control | IMPLEMENT WITH ADJUSTMENT | Add "licence, build and deployment control: Part C slide 15" | planned |
| PB-12 | Slide 9 shows "أب" in Noto Sans Arabic | Embed Noto Sans Arabic in export | M02, AB06 | — | IMPLEMENT (export) | Export with brand fonts installed; record pdffonts | planned |
| PB-13 | Slide 21 locale table has no currency row | Add [REQUIRES OWNER] currency-format row | DS06; no currency decision | — | IMPLEMENT | Add row "currency-format · [REQUIRES OWNER] · Arabic / Localization Lead" | planned |
| PB-14 | Slide 25 "Presentations: Part A templates · native QA PENDING (VAL-15)"; Email row | Templates are an open deliverable | W01, W07, AB10, AB11 | A 68/69/78, C 44 (OPEN DELIVERABLE) | IMPLEMENT | Rows reworded to OPEN DELIVERABLE | planned |
| PB-15 | same slide | same | same | same | IMPLEMENT | merged with PB-14 | planned |
| PB-16 | Slide 26 already six levels "(T04, T05): GEM → collection or tier → product and function → quantity → instructions → SKU" | Keep six; cross-reference | T05 | A 61, C 29 now six | DO NOT IMPLEMENT — ALREADY RESOLVED (add cross-ref only) | Add "Part A 61 and Part C 29 state the same" | planned |
| PB-17 | No ProductCard specimen in deck; slide 23 "ProductCard: One SKU in approved hierarchy" | Flag family-name-at-tier-level policy | T02 (bath/body = pilot family), T04 | A 60/C 27 tier CONDITIONAL | IMPLEMENT WITH ADJUSTMENT | Add policy placeholder sentence on slide 26: "Whether a family name may occupy the collection/tier level is [REQUIRES OWNER · Product / Amenities Lead]" | planned |
| PB-18 | Slide 26 notes list T12–T19 release controls; no safe-zone wording | Roles standardised; values Part C | T13 | C 20 | IMPLEMENT WITH ADJUSTMENT | Add sentence to slide 26 notes | planned |
| PB-19 | Slide 27 restates direction O01–O10 and categories | Reduce to cross-reference + digital rules | O01–O20 | A 47–50 own direction | IMPLEMENT | Direction tile → cross-reference; keep crops, avoid, rights, ratios | planned |
| PB-20 | Slides 12, 13, 28 carry S07 rows without "default/exception" wording | Bilingual default + exception rule; B owns mechanics | S07, RF08, M13 | A 65 (principle), C 41 (fabrication) | IMPLEMENT | Reword slide 12 row and slide 28 row; add mechanics ownership sentence on slide 13 | planned |
| PB-21 | Slide 29 code block lists groups without values | Label as EXCERPT | Q01–Q09 | — | IMPLEMENT | Prefix "EXCERPT —"; point to token package | planned |
| PB-22 | Slide 29 "Versioning: semantic (V3.0.0)"; slide 32 "3.0.0 draft" | 3.0.0-rc.2 / V3.0 RC2 | VAL-21 | A, C "V3.0 RC2" | IMPLEMENT | Replace both | planned |
| PB-23 | Slide 30 Production row "Part C not issued" | Stale | DS04, AC17 | C RC2 | IMPLEMENT | Row → "Part C issued as RC2; physical evidence open (VAL-02, VAL-09 to VAL-11, AC17)" | planned |
| PB-24 | Slide 31 table VAL-17 → VAL-19 without note | VAL-18 unallocated note | Register has no VAL-18 | A 78, C 75 notes | IMPLEMENT | Footer note "VAL-18 is not allocated in the register" | planned |
| PB-25 | Slide 32 change log ends at "3.0.0 draft" | RC2 entry | Z24, AB19 | A 79, C 77 | IMPLEMENT | Add RC2 entry; new document-control slide | planned |
| PB-26 | Slide 33 file names without version/date | X12 note | X12, H21 | A 75, C 56 | IMPLEMENT | Add sentence; files renamed not redrawn at first manifest (VAL-16) | planned |
| PB-27 | Slide 7 Error row "optional warning glyph"; slide 18 Status glyphs PENDING VALIDATION | Clarify warning glyph | Q10 | — | IMPLEMENT | Add clause on slide 18 | planned |
| PB-28 | No near-empty slides | Reflow | — | — | DO NOT IMPLEMENT — ALREADY RESOLVED | None | n/a |
| PB-29 | Slide 5 title "(all role holders TBD)" | Add AC19 | AC19 | — | IMPLEMENT | Add "(AC19)" | planned |
| PB-EXPORT | Previous PDF untagged, no Inter 500 / Noto embedded | Tagged, fonts embedded | V13, VAL-15, L06 | — | IMPLEMENT (export) | LibreOffice tagged export with Jost/Inter/Noto installed; limits recorded | planned |
| B-DOC | No document-control block | Same block as A 79 / C 77 | A11, Z24 | A/C | IMPLEMENT | New slide after 32 | planned |
| B-TOK | No tokens.json / CSS anywhere | Machine-readable token package | Q01–Q09 (tokens approved); AB09 | — | IMPLEMENT WITH ADJUSTMENT | Generate JSON + CSS strictly from documented values; label derived, status per token; DS03 living source still open | planned |
| B-STORY | No component source | Build Storybook | DS03, VAL-13 | — | EVIDENCE-GATED | Cannot build without source; VAL-13 open; nothing fabricated | open |
| B-FLOW | No flow example | Annotated booking flow | Q11–Q15, R11, R12 | — | IMPLEMENT WITH ADJUSTMENT | New slide + checklist, CONCEPT / IMPLEMENTATION TEST; runtime behaviour NOT TESTED | planned |
| B-COMP | 26 names on slides 22–23 | Verify 26 components | DS07 | — | IMPLEMENT WITH ADJUSTMENT | Documentation-level check only (names, purposes, states vs PDF); runtime NOT TESTED | planned |
| B-A11Y | Deck has no images; tagged export possible | Accessibility QA | V02–V13, VAL-08 | — | IMPLEMENT WITH ADJUSTMENT | Deck-level checks recorded; component-level NOT TESTED; Arabic PENDING NATIVE QA | planned |
| B-MONO | Slide 29 code block in Courier New | — | No approved monospace in L01–L16 | — | OPTIONAL POLISH — FLAG | Keep specimen; record [REQUIRES OWNER] | flagged |
| B-GOV-NOTE | Slide 5 notes Y06 "Suppliers may not reuse GEM artwork" | — | Y06 | C App. B clause | ALREADY RESOLVED | None | n/a |

Decisions that the register overrides from the earlier audit remain in force: six-level hierarchy (T05), X12 naming with date field, VAL-18 unallocated.
