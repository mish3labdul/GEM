# Part B RC2 — Change Log

**Source:** `PartB_RC2/01_source/B-RC2.pptx` (from `GEM__Digital_Design_System_V3.0.pptx`, SHA-256 `4a6289fd…9708`, untouched in `00_originals/`). **Result:** GEM™ Digital Design System V3.0 — Part B — RC2, 35 slides (33 + booking-flow test + document control). Slide numbers below are **RC2 numbers**; original numbers in brackets where they differ.

| Slide | Patch / matrix ID | Previous | New | Register / authority | Phase |
|---|---|---|---|---|---|
| 1 | PB-01 | "WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING)" | "V3.0 RC2 · WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING) · GEM-DDS-V3.0-RC2 · ISSUED 2026-10-06"; notes updated | A11, VAL-21 | P0 |
| 2 | PB-03 | four classes + extra labels | + edition states WORKING EDITION → RC → APPROVED; "This edition is V3.0 RC2" | A11, AA01 (A 4, C 3) | P1 |
| 3 | PB-02 (rule) | "Tagline. … fixed, not translated without brand approval (M10)" | + "set only with the tagline token (Jost 400, capitals, 0.18em)"; secondary line "Jost 400, sentence case" | B04–B06, L09 (A 23/24) | P2 |
| 4 | PB-04 | row C "Referenced; not yet issued (DS04, VAL-11)" | "Issued as RC2 · WORKING EDITION / PENDING PRODUCTION VALIDATION (DS04, AC17)"; rows A/B/C labelled RC2 | DS04, AC17 | P0 |
| 4 | PB-05 | register → DS v2.1 → BG V2/2.1 → V1 → benchmarks → WCAG | register → Part A → Part B → Part C → formal standards → v2.1/V2/V1 historical → benchmarks; domain-ownership sentence | RF01, RF02, DS01 (A 3, C 2) | P0 |
| 4 | PB-06 | read order by PDF section numbers | read order by RC2 slide ranges | RF12 | P0 |
| 5 | PB-07, PB-29 | five non-register role names; no citation | register names (Product / Amenities Lead; Procurement / Supplier QA; Arabic / Localization Lead; Presentation / Document QA; Asset Librarian / Governance PM); "Canonical role list: register Owners & Governance, Part A slide 72; digital responsibilities only"; title "(… TBD, AC19)" | Owners & Governance, AC19 | P1 |
| 9 | PB-11, font record | "Fonts ship under SIL OFL 1.1; deployment rights PENDING VALIDATION" | + weights in use (Jost 400/500, Inter 400/500, Noto 400/500); "Licence, build and deployment control: Part C slide 15" | L06, L08, VAL-05 | P1 |
| 11 | PB-09 | no navigation case rule | "Product UI navigation is sentence case at tracking 0 (body or label tokens); navLabel tracked capitals only on editorial signature surfaces" | L09/L10; no register decision on case | P1 |
| 12 | PB-20 | row "Wayfinding: Arabic first and right, English left · S07" | "Bilingual default: Arabic leads for approved Saudi/GCC contexts (Arabic first and right, English secondary and left); exceptions are documented deviations · S07" | S07, RF08 | P0 |
| 13 | PB-20 | "Implementation. Logical properties only…" | "Part B owns the mechanics of the Arabic-first default (S07, Part A 65): dir=rtl, logical properties, bidi isolation… Fabrication follows Part C slide 41." | S07, M06 | P0 |
| 18 | PB-27 | "RTL. Only previous and next mirror…" | + warning glyph PENDING VALIDATION, used only inside Field error and Alert text until functional colour is decided (Q10); Alert has no warning variant | Q10 | P2 |
| 21 | PB-13 | five locale rows | + "currency-format · [REQUIRES OWNER] · Localization Lead; no price invented" | DS06 | P2 |
| 25 | PB-14/15 | "Presentations: Part A templates…"; Email row | "PowerPoint master: OPEN DELIVERABLE (W01, AB10), not yet produced"; "email template: OPEN DELIVERABLE (R13, AB11)" | W01, AB10, AB11 (A 68/69, C 44) | P1 |
| 26 (new) | B-FLOW | — | Booking flow · CONCEPT / IMPLEMENTATION TEST: five steps, components, primary-action, error, RTL, responsive, status notes | Q11–Q15, R11, R12 | P2 |
| 27 [26] | PB-16/17/18 | hierarchy six levels; no policy note | "six levels … Part A 61 and Part C 29 state the same"; family-name-at-tier-level [REQUIRES OWNER · Product / Amenities Lead]; tiers CONDITIONAL (AC03, VAL-01); notes: T13 roles standardised, values Part C | T05, T02, T13, AC03 | P1 |
| 28 [27] | PB-19 | direction tile restates O01–O10 | "Direction · owned by Part A": cross-reference to A 47–50; digital rules kept; required categories cite O11–O16 and A 48; ratio tokens CONDITIONAL | O01–O20 | P2 |
| 29 [28] | PB-20 | S07 row without default/exception | "… the default for Saudi/GCC (S07, Part A 65). Exceptions only by documented project deviation (Part C 41, Appendix K)" | S07 | P0 |
| 30 [29] | PB-21, PB-22 | code block unlabelled; "Versioning: semantic (V3.0.0)" | "EXCERPT — full set: gem-tokens.v3.0-rc2.json / .css"; source note (living source DS03 open; derived package); "semantic 3.0.0-rc.2 (document edition V3.0 RC2)" | Q01–Q09, VAL-21 | P0/P2 |
| 31 [30] | PB-23 | Production row "Part C not issued" | "Part C issued as RC2, physical evidence open (VAL-02, VAL-09 to VAL-11, AC17)" | DS04, AC17 | P1 |
| 32 [31] | PB-24 | footer note | + "VAL-18 is not allocated in the register; the sequence is complete as shown" | register | P1 |
| 33 [32] | PB-22 | "3.0.0 draft" | "3.0.0-rc.2 · V3.0 RC2 (this edition)" | VAL-21 | P0 |
| 34 (new) | B-DOC, PB-25 | — | Document control (ID, title, version, edition, issue date, owner, approver, status, supersedes, related) and change log (3.0.0-rc.2, 3.0.0-draft, 2.1) | A11, Z24, AB19 | P1 |
| 35 [33] | PB-26 | required-not-supplied list | + X12 naming at first manifest (VAL-16); files renamed, never redrawn | X12, H21 | P1 |
| all | PB-01 | "GEM Digital Design System V3.0 · working specification · n" | "GEM™ Digital Design System V3.0 RC2 · working specification · n" with n renumbered for the two inserted slides (34 footers) | A11 | FOOT |

**Not changed (by decision):** tagline on slide 1 (already capitals); six-level hierarchy (register T05); VAL table numbering (VAL-18 unallocated); 26 component names; all token values; Courier New code specimen (flagged, not a brand face, [REQUIRES OWNER]). **No evidence gate closed.**

Scripts: `PartB_RC2/06_logs/edit_partB.py` (phases P0, P1, P2, FLOW, FOOT), `fix_partB.py` (layout corrections), `build_tokens.py`.
