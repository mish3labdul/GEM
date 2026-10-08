# GEM™ V3.0 RC2 — Release Notes

**Edition:** V3.0 Release Candidate 2 · **Issue date:** 2026-10-06 · **State:** RC2 SYNCHRONIZED · NOT RELEASED · EVIDENCE GATES REMAIN · **Not** "Approved V3.0".

| Document | ID | RC2 file | Status |
|---|---|---|---|
| Part A — Brand Guidelines | GEM-BG-V3.0-RC2 | `GEM_V3_RC2/04_release/GEM Brand Guidelines V3.0 — Part A — RC2.pptx` (+ PDF) | Synchronized, working edition, AC20 pending |
| Part B — Digital Design System | GEM-DDS-V3.0-RC2 | `GEM_V3_RC2/04_release/PartB_RC2_Exact_Patch_Spec.md`; PDF unchanged | **Blocked: no editable source.** Patch spec issued |
| Part C — Production Standards | GEM-PS-V3.0-RC2 | `GEM_V3_RC2/04_release/GEM Production Standards V3.0 — Part C — RC2.pptx` (+ PDF) | Synchronized, working edition, pending production validation |

Authority: V3 Final Brand Approval Register (SHA-256 `ccce4613…e7ab3`). Originals untouched in `00_originals/` (checksums in `05_logs/originals_sha256.txt`).

---

## A. DOCUMENT FIXED — change record

Columns: Doc · Slide/page · Audit finding (change-register ID) · Register verification · Previous wording/state · New wording/state · Reason · Priority · Evidence status · QA result.

| Doc | Slide | Finding | Register check | Previous | New | Reason | Pri | Evidence | QA |
|---|---|---|---|---|---|---|---|---|---|
| A | 1 | Edition/version unlabelled (CR-25, CR-69) | A11 | "Working edition · release not yet authorized · …" | "V3.0 RC2 · Working edition · release not yet authorized (AC20) · … · Document ID GEM-BG-V3.0-RC2 · issued 2026-10-06" | One version convention | P1 | AC20 open | PASS |
| A | 3 | Stale "Part C not yet issued" (CR-01) | DS04, AC17 | "Dielines, materials, tolerances, supplier proofs. [PENDING] not yet issued." | "… Issued as RC2, pending production validation." | Part C exists | P0 | AC17 open | PASS |
| A | 3 | Authority order omits A and C (CR-07) | RF01, RF02, DS01 | 1 register · 2 DDS V3.0 · 3 BG V2/2.1 · 4 V1 · 5 benchmarks · 6 WCAG | 1 register · 2 Part A · 3 Part B · 4 Part C · 5 formal standards · 6 V2/V2.1/V1 historical · 7 benchmarks + domain-ownership note | One framework; formal standards above benchmarks per register | P0 | — | PASS |
| A | 4 | Undeclared labels; no edition states (CR-25, CR-28) | AA01, A11 | three placeholders, one concept label | + PENDING PRODUCTION MASTER, PENDING LOCALIZATION APPROVAL, PROJECT-SPECIFIC / REQUIRES SITE VALIDATION, photography label; edition states | Vocabulary complete | P1 | — | PASS |
| A | 6, 41, 46 | Ring crosses text (CR-45) | N06–N08 | headline/subtitle under ring | text re-positioned/re-wrapped clear of ring; rule wording on 41/43 | Internal rule "never crowd the type" | P2 | — | PASS |
| A | 23 | "Jost light" (CR-11) | L01, L06, L08 | "Sentence case, Jost light." | "Sentence case, Jost 400." | No light weight approved | P1 | VAL-19 open | PASS |
| A | 33 | Beige-on-White stricter than register (CR-31) | K05, K07 | "Prohibited for text and logo." | "Not for essential text, boundaries or the logo (K05). Decorative only (K07)." | Register wording | P2 | — | PASS |
| A | 34, 36 | Tracking range, no status (CR-29) | L09, VAL-19 | ".04 to .12em" / no status | ".08 to .12em (Part B tokens, CONDITIONAL · VAL-19)"; "Values are CONDITIONAL until optical QA (VAL-19)" | Token alignment | P2 | VAL-19 open | PASS |
| A | 35 | Label example has no token (CR-32) | L02 | "LABEL · INTER 500 · CAPITALS" | "LABEL SMALL · INTER 400 · CAPITALS" | Part B labelSmall | P2 | — | PASS |
| A | 38, 65 | Bilingual default not stated (CR-10, CR-66) | S07, M13 | both orders shown; no default | 65: "For Saudi/GCC bilingual wayfinding Arabic leads by default: Arabic first and right, English secondary and left (S07)"; 38 cross-references 65 | Register S07; scoped to wayfinding | P0 | VAL-07 open | PASS |
| A | 43 | Placement wording (CR-45) | — | "behind the words" | "clear of the words"; "never behind or through text" | Consistent with 41 and B p.40 | P2 | — | PASS |
| A | 45 | Glyph wording (CR-53) | N15 | "circles, arcs, clean terminals" | "about a 2 px optical stroke on a defined optical box … (N15)" | Register wording | P3 | — | PASS |
| A | 48 | Nine subjects vs six categories (CR-23) | O11–O16 | no mapping | note: required categories O11–O16; others supplementary | Alignment with B | P2 | VAL-06 open | PASS |
| A | 50, 51 | Missing status (CR-51) | W07, VAL-14 | none | "RATIOS CONDITIONAL (W07)"; "Reveal timings CONDITIONAL; motion masters PENDING VALIDATION (VAL-14)" | Status discipline | P3 | VAL-14 open | PASS |
| A | 53 | "Square edges" (CR-13) | Q06 | "Square edges, hairline fields" | "Near-square edges (control radius per Part B) …" | B owns radius | P2 | — | PASS |
| A | 60 | Tier status (CR-14) | T01, E14, AC03, VAL-01 | "CONDITIONAL until confirmed against the approval register" | "All tiers are CONDITIONAL … (AC03, VAL-01) … the name Core Collection is [REQUIRES OWNER]" | Register verified; chronology not used | P1 | VAL-01 open | PASS |
| A | 61 | Seven levels (CR-40) | T05 | 7 levels (Product, Function separate) | 6 levels: Product / function merged; Quantity / size; Instructions / market information | **Register conflict with audit; register wins** | P2 | — | PASS |
| A | 65 | External signage (CR-43) | S02 | — | "EXTERNAL PROPERTY SIGNAGE: DEFERRED (S02)" | Register deferral | P2 | VAL-12 deferred | PASS |
| A | 68, 69 | Templates claimed elsewhere (CR-21) | W01, W07, W13, AB10 | — | "TEMPLATES: OPEN DELIVERABLE (AB10, W01, W13)"; "Social starter set: OPEN DELIVERABLE (W07), not yet produced" | Do not pretend they exist | P1 | OD-TPL open | PASS |
| A | 71 notes | False alt-text claim (CR-24) | V02, V03 | claim without alt text | alt text on all 87 pictures; decorative geometry flagged; notes reworded | Claim now true | P1 | VAL-08, VAL-15 open | PASS (87/87) |
| A | 72 | Eight roles (CR-09) | Owners & Governance sheet, A03–A08, AC19 | 8 tiles | 12 register roles, 4×3; note cites register; ™ placeholder [REQUIRES OWNER · Legal] (CR-57) | Canonical list | P1 | AC19 open | PASS |
| A | 75 | Naming convention (CR-34) | X12, X15, H21 | GEM_[Category]_[Asset]_[Variant]_vX.Y.ext; "no dates" | GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext; asset ID / SHA-256 as CONDITIONAL proposals | **Register conflict; register wins** | P1 | VAL-16 open | PASS |
| A | 78 | Gate list without IDs; stale Part C row (CR-02, CR-17) | VAL-01…21, AC17/19/20 | 10 themed rows | rows carry VAL/AC IDs; "Part C RC2 · ISSUED · AC17, VAL-10, VAL-11 OPEN"; "Also open: VAL-13 to VAL-17, VAL-19 to VAL-21, templates" | One ID set | P0 | all open | PASS |
| A | 79 (new) | No document control (CR-64) | A11, Z24, AB19 | — | Document ID, title, version, edition, issue date, owner, approver, status, supersedes, related; change log | Governance | P1 | AC20 open | PASS |
| A | 80 | Stale closing note (CR-03) | DS04 | "Part C … still to come" | "Part C … issued as Release Candidate 2 …"; line "V3.0 RC2 · Working edition · not released" | Stale | P1 | — | PASS |
| A | all | Footer version (CR-56) | A11 | "GEM™ BRAND GUIDELINES V3.0 · PART A" | "… V3.0 RC2 · PART A" (59 shapes) | Version sync | P3 | — | PASS |
| C | 1 | RC1 label (CR-25, CR-69) | A11 | "RELEASE CANDIDATE 1" | "RELEASE CANDIDATE 2"; status line + "Document ID GEM-PS-V3.0-RC2 · V3.0 RC2 · issued 2026-10-06" | Version sync | P1 | AC20 open | PASS |
| C | 2 | Third authority order (CR-08) | RF01, RF02, DS01 | "1 register · 2 Part A · 3 Part B · 4 approved assets · 5 standards" | seven-step order + domain-ownership sentence | One framework | P0 | — | PASS |
| C | 3 | Undeclared labels, RC undefined (CR-27, CR-62) | AA01, A11 | 8 placeholders | + [TO BE VERIFIED BY PROCESS TEST], [REQUIRES SUPPLIER / OWNER], [ENTER], [PENDING PREPRESS STANDARD], [LEGAL REVIEW REQUIRED]; edition states WORKING EDITION → RC → APPROVED PRODUCTION STANDARD | Vocabulary complete | P1 | — | PASS |
| C | 4 | Nine roles, non-register names (CR-09, CR-63) | Owners & Governance, A06 | Procurement, Supplier QA, Localization, Accessibility, Legal / Regulatory, Production Lead | Procurement / Supplier QA (merged), Arabic / Localization Lead, Accessibility QA, Legal / IP Counsel; "Production Lead [REQUIRES OWNER] *" not a register role; note cites A 72 | Canonical list | P1 | AC19 open | PASS |
| C | 7 | "Standalone Ink symbol" (CR-19) | H06, H08 | Ink symbol: None | "Standalone Black symbol · PNG supplied"; supplied file names listed; X12 at first manifest | Asset list parity with B p.47 | P1 | VAL-02 open | PASS |
| C | 12, 13 | No visual target (CR-36) | J16, T18, U13 | — | first formally approved physical proof becomes the process-specific reference and golden sample (App. M); "No value is created by this standard" | Workable first job | P1 | VAL-09 open | PASS |
| C | 14 | Footer prefix (CR-26) | — | "PART C · COLOUR" | full footer | Consistency | P3 | — | PASS |
| C | 17 notes | Circular numeral ownership (CR-15) | M11, M12, DS06 | "numeral logic follows Part A" | "numeral mechanics follow Part B" | B owns mechanics | P2 | — | PASS |
| C | 20 | T13 wording (CR-22) | T13 | "No universal dimensions are set where the process decides." | "Safe-zone and bleed roles are standardised (T13); their dimensions come from the supplier dieline" | Register-faithful, no conflict with B | P2 | — | PASS |
| C | 27 | Tier status (CR-14) | AC03, VAL-01, E14 | Core/Property "Approved direction" | all three "CONDITIONAL · AC03 / VAL-01"; Core Collection [REQUIRES OWNER] | Matches A 60 | P1 | VAL-01 open | PASS |
| C | 29 | Seven levels (CR-40) | T05 | 7 | 6 (T05) | Register wins | P2 | — | PASS |
| C | 39 | External signage (CR-43) | S02 | — | row "External / building identification · [DEFERRED] · Deferred (S02)" | Register deferral | P2 | VAL-12 | PASS |
| C | 41 | Language lead project-specific (CR-10) | S07 | "Which language leads · [PROJECT-SPECIFIC]" | "Arabic leads by default · Saudi/GCC (S07)"; exceptions = documented deviation (App. K) | Register S07 | P0 | VAL-07 open | PASS |
| C | 44 | Templates (CR-21) | AB10, AB11, W01–W10 | — | "Templates are an OPEN DELIVERABLE … none exists yet." | Gate | P1 | OD-TPL | PASS |
| C | 56, App. N | Naming, asset ID, checksum (CR-34) | X12, X15, H21 | old pattern; checksum method [PENDING] | X12 pattern; asset ID GEM-[CATEGORY]-[NNN] and SHA-256 as CONDITIONAL [REQUIRES OWNER] proposals | Register wins; proposals not standards | P1 | VAL-16 open | PASS |
| C | App. B | Artwork-use restriction (CR-35) | Y06 | — | row: "GEM artwork is used only for the authorized job; no reuse, distribution or adaptation outside the approved scope · LEGAL REVIEW REQUIRED" | Register Y06 | P1 | legal review open | PASS |
| C | App. D | Fields (CR-42) | — | — | Proof ID; Samples submitted (count) | Form completeness | P2 | — | PASS |
| C | App. E | Fields (CR-42) | C 23 | — | Grain direction; Supplier datasheet reference | Form completeness | P2 | — | PASS |
| C | App. F | Fields (CR-42) | T11, Y05 | "Pack format and closure" | "Primary pack: format and closure"; + Secondary pack, Market(s), Language / bilingual status | Form completeness | P2 | VAL-10 open | PASS |
| C | App. L | Fields (CR-42) | — | one Date | + Raised by; Date raised / date closed | Form completeness | P2 | — | PASS |
| C | 75 | Gate items without IDs (CR-17, CR-30) | VAL-01…21 | 17 names | 17 names with VAL/AC IDs; VAL-12 "deferred"; note on VAL-18 and digital gates | One ID set | P1 | all open | PASS |
| C | 76 | Gates unmapped (CR-17) | — | "Open" ×6 | each gate lists its VAL/AC IDs; "V3.0 RC2 · WORKING EDITION / PENDING PRODUCTION VALIDATION" | Traceability | P1 | all open | PASS |
| C | 77 (new) | Document control (CR-64) | A11, Z24, AB19 | — | document-control tiles and change log | Governance | P1 | AC20 open | PASS |
| C | 78 | RC1 closing (CR-25) | — | "RELEASE CANDIDATE 1 · …" | "RELEASE CANDIDATE 2 · WORKING EDITION / PENDING PRODUCTION VALIDATION" | Version sync | P1 | — | PASS |
| C | all | Footer (CR-56); alt text (CR-24) | A11; V02, V03 | — | 70 footers "V3.0 RC2"; alt text on 14/14 pictures | — | P3/P1 | — | PASS |
| B | all | 29 page-level corrections + export requirements | see patch spec | — | `PartB_RC2_Exact_Patch_Spec.md` PB-01…PB-29, PB-EXPORT | **No editable source; PDF untouched** | P0–P3 | OD-SRC blocking | n/a |

Audit findings **rejected or superseded by the register**: CR-40 (seven-level hierarchy → T05 six levels), CR-34 ("no dates in filename" → X12 requires the date field), CR-18 (VAL-18 "missing" → not allocated; no renumbering). Audit findings **deliberately not implemented**: CR-47 booking-flow concept, CR-49 A 15 table restyle, CR-52 tagline on C cover, CR-54 buyer sentence, CR-55 C section renumbering (new design content or avoidable layout drift). CR-67 (App. N as spreadsheet) recorded under VAL-16.

## B. EVIDENCE STILL OPEN
See `GEM_V3_RC2_Open_Evidence_Register.md`: VAL-01 to VAL-21 (no VAL-18), Y01–Y04, AC07, AC10, AC17, AC19 (holders), AC20, OD-TPL (templates), OD-SRC (Part B source). None closed.

## C. Final QA gate

| Gate | Result |
|---|---|
| A/B/C authority language synchronized | A, C: yes (identical seven-step order + domain note). B: specified in PB-05, not applied (no source). |
| No stale "Part C not issued" text remains | A, C: none (automated check). B: remains on p.3 and p.43 until PB-04/PB-23 applied. |
| No unsupported Jost Light remains | A, B, C: none. |
| Bilingual rule synchronized | A 38/65, C 41 state the S07 default; B p.14/40 already consistent; PB-20 adds the cross-reference. |
| Governance role system synchronized | A 72 = twelve register roles; C 4 uses register names and cites A 72; B already lists the twelve (PB-07 adds the citation). |
| Version state synchronized | A and C: V3.0 RC2 with document IDs and date. B: PB-01/PB-22 pending. |
| No unsupported production values introduced | Confirmed by automated scan (no Pantone/CMYK/ΔE/mm/gsm values in A, B, C). |
| No evidence gate incorrectly marked complete | Confirmed (automated scan + manual register comparison). |
| All modified PPTX slides visually rendered and checked | Yes: 28 A slides, 27 C slides, before/after pairs; full-deck sheets for drift. |
| Part B source availability explicitly recorded | Yes: none exists (CR-68, OD-SRC). |
| Arabic remains pending until native QA evidence exists | Yes (VAL-07, AC10). |
| Trademark/IP remain pending | Yes (VAL-03, VAL-04, Y01, Y02). |
| Production masters remain pending | Yes (VAL-02, AC07). |
| Final authorization remains pending | Yes (AC20). |
| Automated consistency check | 101 PASS · 9 FAIL, all 9 on Part B and mapped to patch entries. A and C: 0 FAIL. |
| File validation (OOXML) | A-RC2.pptx and C-RC2.pptx: all validations passed against their originals. |

**RC2 verdict:** A and C are RC2 SYNCHRONIZED. B is specified but not regenerated. The ecosystem is ready for external validation (VAL-17 usability test, VAL-07 native Arabic review, legal reviews, supplier pilot) **as soon as the Part B source is located or recreated and the patch spec applied**; the three-way usability test can start on A and C now.
