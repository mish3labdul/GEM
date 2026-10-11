# 14 · AR01 — Findings, Severity and Open Items

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · D8 external Arabic/bilingual PDF validation OPEN · AC20 OPEN · ARABIC LINGUISTIC STATUS: PENDING NATIVE ARABIC REVIEW
**This is a technical Arabic / RTL validation. It is not native-speaker, translation or localization approval, and it closes no gate.**

## Severity summary (technical)
| Severity | Count | Items |
|---|---|---|
| **P0** | 0 | — |
| **P1** | 0 | The slide 39 mixed line was considered for P1 and rejected: the character sequence and the code's content are intact; only the visual placement relative to the label was wrong. |
| **P2** | 1 (**corrected in the AR01 candidate**) | AR01-F01: Part A slide 39 label + Latin code paragraph: native PowerPoint placed the code to the right of the label (LTR base direction, `lang=en-US`). |
| **P3** | 12 paragraphs (**all 12 corrected** in the AR01 candidates: 2 at stage 1, 10 under owner decision 1) | AR01-F02: technical language/direction metadata defect: Arabic runs carried `lang="en-US"` and no declared paragraph direction (Part A slides 37, 38 (3), 39 (2), 65, 66 (3), 68; Part B slide 9). No native visual defect on the ten single-script paragraphs. |
| OBSERVATION | 9 | see below |
| LINGUISTIC REVIEW | 44-item queue | `11_AR01_Native_Arabic_Reviewer_Queue.csv` |
| GOVERNANCE REVIEW | 8 | see below |

## Technical findings
- **AR01-F01 (P2) — CORRECTED IN CANDIDATE.** Fix: `rtl="1"` on the two slide 39 paragraphs and `lang="ar-SA"` on their Arabic runs (and, in the final owner decision, `lang="en-US"` on a separate Latin identifier run in Text 8); no text, spacing, font, size, colour or geometry change; one zip member differs; native positions measured; byte-identical to the natively tested variant (`07`).
- **AR01-F02 (P3) — 10 paragraphs CORRECTED under owner decision 1.** `rtl="1"` and `lang="ar-SA"` (anchored zip-level edits; `AR01_PowerPoint_Metadata_Correction_Register.csv`). A new Part B AR01 candidate supersedes NP01-R1 for Part B (slide-30 fix preserved byte-identically). Native revalidation: direction now right-to-left, text bounds unchanged, sub-pixel glyph-edge differences only (`07`).
- **Arabic tracking: 0 defects** (all 42 paragraphs, `spc` / `w:spacing` = 0). **Bold on Arabic: 0.** **Font-family defects: 0** (complex-script font Noto Sans Arabic on all 42). **Unaccepted Bold/variable file exercised: NO.** **Logo mirrored: NO** (no flipped pictures in any deck; none in the templates). **Manual-space layout hacks: none.** **Rotated or vertical Arabic: none.** **Arabic in notes, masters, layouts: none.**
- Word templates: 30 of 30 Arabic paragraphs statically correct (bidi, rtl, `ar-SA`, spacing 0, Noto, not bold) **and natively observed in Word** (43 of 43 paragraphs PASS in `17_qa/native_word_paragraphs.csv`: Arabic characters advance right-to-left, Latin placeholders left-to-right and left of the Arabic label, Noto Sans Arabic, not bold, spacing 0). No native Word technical defect found; no repair dialog.

## OBSERVATIONS (no correction)
0. **Slide 39 Text 8 — resolved by the final owner decision:** the mixed run was split into an Arabic run (`ar-SA`) and a Latin identifier run (`en-US`); see `01`, `07`, `12`.
1. The Latin technical code on slide 39 is requested in **Noto Sans Arabic**, not Inter/Jost.
2. (Superseded) The slide 39 mixed run formerly tagged the Latin code `ar-SA`; the run is now split (`12`); screen-reader behaviour remains untested.
3. Part D's Arabic is image-embedded only; bidi not testable.
4. Part B slide 9's Arabic specimen is left-aligned inside its tile, matching the sibling Latin specimen tiles.
5. Part A LibreOffice PDFs embed `DejaVuSans` for one symbol (identical in the delivered D3 PDF).
6. The slide 39 digits line uses Latin digits "until policy is signed off" (M11): a policy item, not a defect.
7. Native Word asks whether to update fields on opening every template (all set `w:updateFields`), including non-Arabic templates; not a repair dialog, not Arabic-specific.
8. The extracted PDF text layer of the bracketed placeholders on Part A pages 65 and 68 now records the logical RTL order (raster unchanged): an extraction-level observation that does not validate any PDF route (D8).

## Relationship to NP01
NP01 recorded Part A slide 39 as NP01-F09 (P3, REQUIRES NATIVE REVIEW, deferred to the localization pass). **NP01-F09 is technically corrected in the AR01 Part A candidate; the wording of the strings remains pending native Arabic review.** The NP01 record is unchanged.

## GOVERNANCE REVIEW (not defects; no edit)
1. **Scope of the Arabic-first rule.** The register's S07 decision is for *Saudi/GCC bilingual wayfinding* ("Arabic first/right and English secondary/left by default… adapt only where regulatory or operational context requires"). The decks restate it as a bilingual rule for "approved Saudi/GCC contexts", and the letterhead QA lists the *bilingual correspondence hierarchy* as awaiting Brand Owner acceptance (AC20, S07). The AR01 brief states the correspondence rule as current owner instruction. **The bilingual templates conform to that stated rule** (Arabic leads each content pair; only the English "sample content" status line leads), but the register does not literally cover correspondence. The rule is **not** generalized beyond Saudi/GCC.
2. Tagline translation (M10) requires explicit brand approval: the templates keep it in English.
3. The Arabic numeral convention for dates, numbers and page labels (M11, R03-06) is unsigned.
4. Arabic and bilingual templates carry English-only footer, status and "Page n of N" text.
5. Typography of Latin technical codes inside Arabic runs (observation 1).
6. Section direction is LTR with RTL paragraphs in the Word templates; native Word shows the intended paragraph behaviour; the design choice stays with the reviewer.
7. **Correspondence authority (owner decision 3).** The Approval Register was **not** updated. S07 governs Saudi/GCC *wayfinding*; Arabic-first correspondence exists in the working templates and the working rule, but formal register authority for it is incomplete. **GOVERNANCE REVIEW — OPEN.** S07 is not generalized beyond Saudi/GCC wayfinding.
8. The English-only footer, tagline and "Page n of N" label, LTR section direction and Latin-ID typography are carried as **GOVERNANCE / LINGUISTIC-LOCALIZATION REVIEW** items: native Word revealed no technical defect in them, so no template change is made.

## NOT TESTED
Windows Word, Word Online, iPad; Word's Save-as-PDF route and Acrobat Arabic text layer; screen readers; real Arabic content and genuine multi-page Word flow (the templates are single-page samples); Arabic acronym, filename, date, percentage and slash cases (no existing examples); any wayfinding, packaging, website or app implementation (out of scope). Inherited Word-for-Mac evidence is cited, not re-verified.

## ENVIRONMENT / PROCESS
- Native Word: access was granted for the dedicated temporary test folder only; a stale in-memory document from an earlier timed-out open (AppleEvent -1712) was closed unsaved; four byte-identical copies were tested one at a time and deleted; no repair was accepted; the Word field-update prompt was declined each time.
- PowerPoint property reads can mark a deck modified in memory (known from NP01); every test copy was closed without saving and verified unchanged.

## Added observation
9. Latin language tagging differs between the decks (`en-US`, throughout) and the Word letterhead templates (`en-GB`). No governance document found sets a Latin locale; nothing was changed.
