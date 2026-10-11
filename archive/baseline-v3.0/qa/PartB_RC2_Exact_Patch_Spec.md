# GEM™ Digital Design System V3.0 — Part B — RC2 Exact Patch Specification

**Document ID to apply:** GEM-DDS-V3.0-RC2 · **Target version string:** V3.0 RC2 · **Issue date:** 2026-10-06

## Blocking dependency: editable source not available

The workspace was searched for every plausible Part B source form (HTML, Markdown, React, Storybook, CSS, JSON tokens, PPTX, generator scripts, SVG assets). **None exists.** The only Part B artefact is the review PDF `GEM_Digital_Design_System_V3.0_1.pdf` (77 pages, produced by Chromium/Skia from an unavailable HTML source, SHA-256 `f5905ee9…6eb5c`). The PDF has been left untouched in `GEM_V3_RC2/00_originals/`.

Reconstructing 77 pages from the PDF was not authorized and is not attempted. The corrections below are page-exact and must be applied to the source by its maintainer (Digital Design Lead / Engineering Lead), after which the PDF is regenerated with the export requirements in §PB-EXPORT. Until then Part B remains at V3.0 working specification and fails the RC2 cross-document checks for version, stale references and authority order (see `GEM_V3_RC2_Consistency_Report.md`).

Status of this spec: **VERIFIED AGAINST THE V3 APPROVAL REGISTER**. Each entry cites the register decision(s) checked. Evidence gates are not closed by any entry.

---

## Patch entries

| ID | Page | Current statement (verbatim) | Replacement | Reason / register |
|---|---|---|---|---|
| PB-01 | 1 (cover) and running footer on every page | `DIGITAL DESIGN SYSTEM V3.0 · WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING)`; footer `GEM Digital Design System V3.0 · working specification · n` | Cover: `DIGITAL DESIGN SYSTEM V3.0 RC2 · WORKING SPECIFICATION · NOT RELEASED (AC20 PENDING) · GEM-DDS-V3.0-RC2 · 2026-10-06`. Footer: `GEM™ Digital Design System V3.0 RC2 · working specification · n` | One synchronized version string and document ID across A/B/C (A11, VAL-21). |
| PB-02 | 2 | `**Hospitality, in perfect proportion.** Every arrival, precisely composed.` (bold, sentence case) | `HOSPITALITY, IN PERFECT PROPORTION` set with the `tagline` token (Jost 400, capitals, 0.18em), on its own line; then `Every arrival, precisely composed.` in body style. | The fixed tagline may not be lowercased or restyled (B04–B06, AC05; Part A slide 24 "WRONG · LOWERCASED"). |
| PB-03 | 2 | `This is the living digital design system for GEM™, updated from Design System v2.1 to V3.0 under the GEM V3 Final Brand Approval Register (466 decisions).` | Keep, and add after the status paragraph: `Edition: V3.0 Release Candidate 2 (RC2), synchronized with Part A and Part C RC2. Edition states are WORKING EDITION → RELEASE CANDIDATE → APPROVED; an edition becomes APPROVED only by Brand Owner authorization (AC20).` | Edition vocabulary shared with A 4 and C 3. |
| PB-04 | 3 (Organisation table, row C) | `C. Production Standards — Dielines, materials, finishes, tolerances, supplier … Referenced; not yet issued (DS04, VAL-11)` | `C. Production Standards — … Issued as Release Candidate 2 · WORKING EDITION / PENDING PRODUCTION VALIDATION (DS04; physical evidence open under AC17, VAL-09 to VAL-11)` | Stale; Part C exists. Do not imply production approval. |
| PB-05 | 3–4 (Authority order) | `1. V3 Final Brand Approval Register. 2. Design System v2.1. 3. Brand Guidelines V2/2.1. …` | `1. V3 Final Brand Approval Register. 2. Part A, Brand Guidelines V3.0: brand strategy and identity. 3. This system, Part B: digital implementation. 4. Part C, Production Standards V3.0: physical production. 5. Formal technical and legal standards (WCAG 2.2 AA and others) where they apply. 6. Design System v2.1, Brand Guidelines V2/2.1 and V1: historical, superseded. 7. Benchmarks and inspiration only.` Add: `Domain ownership: where Parts A, B and C have different implementation domains, the owning document governs that domain unless the Approval Register overrides it.` | One authority framework (RF01, RF02, DS01; register source hierarchy places formal standards above benchmarks). Identical wording now in A 3 and C 2. |
| PB-06 | 4 | `… and named role holders. See 17-qa-release .` | `… and named role holders. See pages 43–45 (QA and release).` | Folder names are not page references (RF12). |
| PB-07 | 5–6 (Owners table) | `Owners (all role holders TBD)` + twelve rows | Keep the twelve rows (they match the register). Add one line above the table: `The canonical twelve-role list is the register's Owners & Governance sheet, stated in Part A slide 72; this table adds only digital responsibilities.` | Single role taxonomy (CR-09). |
| PB-08 | 9 | `See 07-motion .` / `See 08-glyphs .` | `See page 22 (Motion).` / `See pages 23–24 (Functional glyphs).` | Page references. |
| PB-09 | 11 (Tracking scale table, navLabel row, Prohibited column) | `navLabel 0.08em 0.08 x pt Capital navigation Sentence-case navigation` | Prohibited column: `Tracked capitals in product UI (navLabel is for editorial signature surfaces only)` | Internal contradiction with p.13 and p.64, which make sentence case (tracking 0) the product-UI default. No register decision on navigation case; the p.64 rule is retained as the intended decision. |
| PB-10 | 13 | (navigation paragraph) `… 16px sentence case at tracking 0 is the default …` | Keep; add `(see page 64)`. | Cross-reference only. |
| PB-11 | 12 | `(see Licenses)` | `(licence, build and deployment control: Part C slide 15, Font control; VAL-05)` | The Licenses section does not exist in the PDF. |
| PB-12 | 12, 15, 54, 61 | Arabic specimens and inline Arabic | No text change. Export requirement: embed Noto Sans Arabic (see PB-EXPORT). | Current PDF renders inline Arabic in a fallback face (pdffonts: no Noto Sans Arabic embedded). |
| PB-13 | 28 (Locale table) | `Currency: show currency code or symbol per locale; no price is invented. [PENDING] until supplied.` | Add a table row: `currency-format · [REQUIRES OWNER · Arabic / Localization Lead] · SAR symbol/code position and spacing for ar-SA and en; no price is invented.` | DS06 locale-aware behaviour; no register decision on currency presentation, so a placeholder, not a rule. |
| PB-14 | 33 (Hospitality patterns, Social row) | `Templates are Part A deliverables.` | `Templates are an OPEN DELIVERABLE (W07 social starter set; AB10, AB11): none exists yet.` | A does not contain templates; recorded as a gate (CR-21). |
| PB-15 | 33 (Presentations row) | `Part A templates` (and similar wording) | `PowerPoint master: OPEN DELIVERABLE (W01, AB10); not yet produced.` | Same. |
| PB-16 | 35 (Packaging hierarchy) | six levels as listed | No change (matches register T05). Add: `Six levels per T05; Part A slide 61 and Part C slide 29 state the same.` | Audit recommendation to add a seventh level was rejected: register wins (CR-40). |
| PB-17 | 35 / 65 (ProductCard specimen) | `GEM — BATH AND BODY` at level 2 | Add caption: `Level 2 shows the pilot family name as a working placeholder. Whether a family name may occupy the collection/tier level is [REQUIRES OWNER · Product / Amenities Lead] (T02, T04).` | Register names bath/body as the pilot family (T02), not as a tier; policy decision required. |
| PB-18 | 36 | `Safe zones and bleeds are standardised (T13).` | `Safe-zone and bleed roles are standardised (T13); their dimensions come from the supplier dieline (Part C slide 20).` | Aligns with C 20. |
| PB-19 | 37 (Photography) | Full restatement of direction O01–O10 and six categories | Replace the direction paragraphs with: `Photography direction is owned by Part A slides 47–50 (O01–O10; required categories O11–O16). This page keeps only the digital rules: alt text, rights metadata (O18, VAL-06) and ratio tokens.` Keep the alt-text, rights and ratio content. | Unnecessary duplication with divergence risk (A lists nine subjects). |
| PB-20 | 40 (Wayfinding) | `[REQUIRES SITE VALIDATION] and belong to the Production Standards (Part C) once a project exists.` | Keep; add: `Bilingual order: Arabic first and right by default for Saudi/GCC wayfinding (S07) as stated in Part A slide 65; Part C slide 41 applies it to fabrication.` | Cross-reference to the owning principle (CR-10). |
| PB-21 | 41 (Token file listing) | JSON block showing `type`, `space`, `motion`, `layout`, `locale` as empty objects | Add heading line: `Excerpt: foundation and semantic colour groups shown in full; type, space, motion, layout and locale groups are abbreviated here and complete in tokens.json.` | Q01–Q09; avoids reading the excerpt as the full file. |
| PB-22 | 42 | `Semantic version for the system (V3.0.0).` | `Semantic version for the system: 3.0.0-rc.2 (document edition V3.0 RC2).` | One version convention (VAL-21). |
| PB-23 | 43 (Release checklist, Production row) | `Raster logos only; no supplier data; Production Standards not issued (VAL-02, VAL-09 to VAL-11)` | `Raster logos only; no supplier data; Production Standards issued as RC2, physical evidence open (VAL-02, VAL-09 to VAL-11, AC17)` | Stale. |
| PB-24 | 44–45 (Validation table) | VAL-17 followed by VAL-19 | Add footnote: `VAL-18 is not allocated in the V3 Approval Register; the sequence is complete as shown.` No renumbering. | Audit false positive (CR-18). |
| PB-25 | 45 (Change log) | `3.0.0-draft — Updated from v2.1 under the V3 approval register. …` | Add row: `3.0.0-rc.2 · 2026-10-06 · RC2 synchronization: version and document ID; authority order and domain ownership; stale Part C references; tagline treatment on page 2; navLabel rule; page references; currency placeholder; template gates; photography cross-reference; T13 wording; VAL-18 note. No token, component or rule values changed.` | Z24, AB19. |
| PB-26 | 47 (Supplied assets) | `GEM_Logo_Horizontal_Beige.png …` (five files without version/date) | Keep names as supplied; add: `Controlled names follow register convention X12 (GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext) at first manifest (VAL-16); the files are renamed, not redrawn.` | X12; H21. |
| PB-27 | 50 (Alert) / 23 (glyph set) | Alert has no warning variant; glyph `warning` is PENDING VALIDATION | Add to Alert README: `A warning variant is not provided (Q10). The warning glyph remains PENDING VALIDATION for use in Field error and Toast only until functional colour is decided.` | Q10. |
| PB-28 | 27, 29, 34, 46, 49, 51 | Near-empty pages (one paragraph or one line) | Re-flow at regeneration so no page carries fewer than three content blocks; renumber internal page references accordingly. | Optional polish (RF12). |
| PB-29 | 2 | `the named role holders are TBD` | Keep; add `(AC19)`. | ID consistency. |

## PB-EXPORT — regeneration and export requirements

| Requirement | Register basis | Current state of the review PDF |
|---|---|---|
| Embed Jost 400 and 500 where used; Inter 400 and 500 where used (label, Link, selected Tabs specify 500) | L01, L02, L06, VAL-19 | Only `Jost-Regular`, `Inter-Regular` and `DejaVuSans` embedded (pdffonts). Inter 500 missing. |
| Embed Noto Sans Arabic for every Arabic string | M02, AB06 | Not embedded; inline Arabic falls back to DejaVu Sans. |
| Tagged PDF with logical reading order, document language, alt text on every image, decorative geometry marked artifact | V02, V03, V05, V13, VAL-15 | `Tagged: no`. |
| Document title metadata `GEM™ Digital Design System V3.0 RC2` and ID in the PDF info | A11 | Title metadata absent. |
| Do not mark font licence/build as approved | VAL-05 in progress | — |

**Embedded-font status is recorded, not fixed:** this spec cannot change the PDF. VAL-15 (native PDF QA) and VAL-19 remain open.

## Items deliberately not changed in Part B
- Token values, component behaviour, responsive matrix, accessibility rules, RTL mirror table, numeral mechanics: no change (register-approved; AC13).
- Twelve-role list (already matches the register).
- Packaging hierarchy with six levels (matches T05).
- No new component, flow or template was designed (out of scope; CR-47).
