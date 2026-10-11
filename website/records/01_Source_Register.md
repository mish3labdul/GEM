# 01 · Source register

Session 1 · 2026-10-10. Everything below was opened and read in this session; nothing is assumed from earlier sessions.

## Authority order (as stated in Part A slide 3, Part B slide 4, Part C slide 2)
1. V3 Final Brand Approval Register — **not supplied** (not in either folder or the GitHub repo). Register decision IDs cited in the decks are treated as the decks' own claims.
2. Part A Brand Guidelines (brand and identity)
3. Part B Digital Design System (digital implementation)
4. Part C Production Standards (physical production)
5. Formal standards (WCAG 2.2 AA)
6. V2 / V2.1 / V1 — historical
7. Benchmarks and inspiration — reference only (this includes the six reference galleries and all copy written in this session)

## Documents read

| Source | Version / ID | Status | Authority for the website | How it was read |
|---|---|---|---|---|
| Part A Brand Guidelines `GEM_BRAND_BrandGuidelines_PartA_v3.0_20261009.pptx` | V3.0 · GEM-BG-V3.0 · 2026-10-09 | Owner authorized baseline (AC20) with formal deferrals | Controlling for positioning, voice, identity, colour, type, graphic language, imagery, motion, Amenities & Packaging stream | All 80 slides, text extracted in full; key images extracted and viewed |
| Part B Digital Design System `…PartB_v3.0_20261009.pptx` | V3.0 · GEM-DDS-V3.0 · 3.0.0 | Authorized baseline; specification only, no component implementation | Controlling for tokens, layout bands, type scale, accessibility, motion tokens, UX writing | All 35 slides, text in full |
| Part C Production Standards `…PartC_v3.0_20261009.pptx` | V3.0 · GEM-PS-V3.0 | WORKING EDITION / PENDING PRODUCTION VALIDATION | Production release sequence (slide 5), font control (slide 15), "no production data invented" | Slides 1–5, 14–17 read; full text searched for web, image and rights terms |
| Part D Amenities & Packaging Concept Portfolio `…PartD_v3.0_20261009.pptx` | V3.0 · 2026-10-09 | CONCEPT / NOT PRODUCTION ARTWORK | Pilot family, tiers, label architecture, concept imagery | All 24 slides, text in full; all 21 media files extracted and viewed |
| Tokens `gem-tokens.v3.0.css/.json` + README | 3.0.0 | Authorized as documentation of values; "component implementation not authorized" | Token values used unchanged | Read in full (CSS) |
| Logo kit `GEM_Brand_Assets_v1.0/04_official_kit` + README, `metrics.json`, `SHA256SUMS.txt`, `kit-overview.png`, `motion/gem-reveal.html` | v1.0 | WORKING ASSETS; production-master acceptance PENDING (VAL-02); external issue RESTRICTED | Only logo artwork used on the site | Files listed; 8 used files verified against the kit checksum list (8/8 OK) |
| RP01 Executive Summary, Residual Limitations, Release Index, Release Scope Matrix, Restricted Artifact Register | RP01 · 2026-10-09 | Release records | Publication boundaries (D8 Arabic restriction, logo kit restriction) | Read in full |
| GitHub `mish3labdul/GEM` (main @ 4ea0d11, branches `claude/gem-worktree-safety-30b559`, `claude/pensive-mayer-s1xbmb`) | — | Version control for the brand system | Prior audit; Part D mockup register (image hashes) | Cloned read-only; no push |
| `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md` (repo root) | V3.0 audit of A/B/C | Prior audit (brand documents, not a website) | Findings re-assessed below | Sections 1, 5 (photography, motion), 12 read |

## Owner-decision layer (read after folder access was granted; parent folder `GEM-3.0 2`)
| Record | What it settles for the website |
|---|---|
| FA01 `04_FA01_Final_Owner_Decisions.csv`, `07_FA01_D8_External_Issue_Policy.md` | Brand Owner holder recorded as **Mashal**. AC20 authorized as a limited baseline. VAL-01 (commercial scope) and AC07/VAL-02 (logo master) **formally deferred**. VAL-03/04/05/06 (trademark, artwork ownership, font licence, image rights) accepted as **owner risk, not verified**. D8: Part D images containing Arabic are blocked from external issue |
| OD01 `02_OD01_Owner_Decision_Register.csv` | OD-G03: informative-image alt text must be written or approved by the Accessibility Content Owner (Mashal). OD-G05: Beige on White never for functional text. OD-G01: Arabic leads in Saudi/GCC bilingual correspondence (scope: correspondence only). OD-G11: public **repository** visibility approved — not a website publication decision |
| Root `README.md` | Confirms RP01 as the current release and all RC2 folders as historical |
Not yet read in full: AR01, AX01, D3, D7, FD01, HR01, NP01, ODI01 packages. Searched only for the decisions above; next session should read their executive summaries.

## Material findings

- **There is no existing website.** Neither folder nor any branch of the repo contains a site, a web page, a website audit or website copy. The only HTML file is the kit's motion study. The project description's "existing website" and "previous audit findings" therefore have no website counterpart; this session starts the implementation. *(Owner to confirm whether a site exists elsewhere.)*
- **The prior audit is a brand-system audit.** Findings still relevant to the website and retained: commercial scope and proof points not validated (VAL-01) so no public capability claim; commissioned, rights-cleared photography missing (VAL-06); Arabic native QA not done (VAL-07); no running component library (VAL-13). Its "do not redesign the identity" verdict is followed.
- **Business facts available are thin by design.** Documented: GEM is a hospitality supplier and partner, not a hotel operator; one master brand; Amenities & Packaging is the primary approved B2B stream; pilot family of five products (concept); three tiers named but CONDITIONAL; audiences; Saudi/GCC orientation; production release sequence (working standard). **Not documented anywhere:** contact details, company legal name, address, clients, projects, partners, capabilities, MOQs, prices, lead times, certifications, sustainability claims.

## Conflicts and how they were resolved

| Conflict | Resolution |
|---|---|
| Tokens say "component implementation not authorized"; the project instructions authorize a working website | Owner's project instruction governs this project. Token **values** are used unchanged; the site is not presented as the DS03 component library. Flagged for owner confirmation. |
| Logo kit is "external issue RESTRICTED / not a production master" | Used for the local working build and a private preview only. Public publication needs owner acceptance of the kit for web use. |
| Part D mockups were "designated approved by the project owner as the mockup set to use" (repo README), but most carry baked-in Arabic, which RP01 restricts (D8) and the project instructions say stakeholder permissions do not extend to public web | Images with Arabic or rendered "GEM™" wordmarks excluded. Only the two text-free material studies (slides 16, 17) used. Owner decision requested. |
| Part B: "No full dark mode" vs. generic web practice of dark-mode support | Brand governs: light canvas with Ink signature sections; no dark theme. |
| Weight 500 is "pending accepted font file" | Only weight 400 shipped and used. |
