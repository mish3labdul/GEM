# 10 · Owner website decisions — 2026-10-10

Given by the project owner in chat on 2026-10-10 (15:28 Asia/Riyadh), answering the eleven questions in `08_Handoff_and_Open_Decisions.md`. Owner wording is quoted verbatim. These are owner decisions for the **website**; they are not independent legal clearance, not production-master acceptance and not publication authorization (publishing, deploying, pushing and merging remain separately unauthorized).

| ID | Question | Owner answer (verbatim) | How it is applied in v0.2 |
|---|---|---|---|
| WD-01 | Does a website exist elsewhere? | "No" | v0.1 is the first website. The project description's "existing website" has no other counterpart. |
| WD-02 | Receiving destination and privacy text | "Proceed as best practice" | No destination exists, so nothing is connected and nothing is sent. Implemented: limits stated before data entry; fail-closed preparation (GEM-01); privacy summary beside the form; temporary privacy and legal notice page; a delivery adapter in `site.js` that stays off until an HTTPS endpoint is supplied under a separate authorization; honeypot field for that future endpoint. Privacy wording is proposed and needs legal review before public use. |
| WD-03 | Contact details, legal entity, legal/privacy pages | "Will be provided at a later stage, now use temporary random details." | Temporary details in the footer and privacy page, visibly labelled "Temporary details": GEM Hospitality Supplies Co. · Olaya Street, Riyadh 12211, Saudi Arabia · +966 11 000 0000 · hello@gem.example. The email uses the reserved `.example` domain (RFC 2606) and the phone number is all zeros, so neither can reach a real person or company. Each instance is marked `data-contact-status="temporary"` with a replace-me comment on all three pages. |
| WD-04 | Public web use of the logo kit | "disregard RP01, it's not restricted" | Kit artwork used for the website without the RP01 external-issue restriction. Production-master acceptance (VAL-02) is a separate matter and is not claimed. |
| WD-05 | Image rights for the three studies; rendered studies in public | "Yes they may appear." | Finish, materials and threshold studies retained with concept/reference captions. HR01 records the materials and finish studies as AI-generated concepts; the captions say "Concept study, not production photography". This is an owner-risk decision, not a rights register (VAL-06). |
| WD-06 | Part D product mockups | "yes show them." | Four mockups added (room set, wall-mounted, bespoke box, arrival). This is the Brand Owner "separately deciding otherwise" under FA01 D8 policy clause 2 for website use of Part D images containing Arabic. Excluded on quality grounds, not policy: refill container (cut-out edge artifact) and two white bottles with artificial glow (Part A slide 49 "don't"). |
| WD-07 | Programme options as "being defined"; consistent-range name | "Yes" | The three directions are shown with a "Being defined" label beside them. "Core Collection" is still not used, because the answer did not supply a name; the page says "A consistent GEM range". |
| WD-08 | Market statement and Arabic edition | "Confirmed" | "Saudi Arabia and the wider GCC" kept; footer keeps "English. An Arabic edition is in preparation." (overrides audit GEM-12's proposed removal of that line). |
| WD-09 | ™ usage in running text and hero mark | "Approved" | GEM™ kept in titles, descriptor and the kit symbol's ™. |
| WD-10 | Alt text for the three images | "Approved" | Three alt texts accepted as written (session 1). The four new mockups reuse the alt text Mashal approved for the same images in HR01 (`05_HR01_Accessibility_Content_Register.csv` A15, A21, A22, A23); the web crops keep every element those texts describe. Owner confirmation that deck approval extends to the web crops is still requested (audit GEM-15 note). |
| WD-11 | Token implementation | "Authorized" | Token values from `gem-tokens.v3.0.css` are implemented by the website. This is not the DS03 component library. |

## Audit items superseded or narrowed by these decisions
- GEM-07: "real contact journey" remains incomplete by fact (no destination), but contact details now exist as labelled temporaries.
- GEM-08: web use of kit, images, ™ and tokens now has a recorded owner decision (WD-04, 05, 09, 11). Exact files and hashes: `13_Correction_Report_Session2.md`.
- GEM-12: the Arabic-edition line stays (WD-08). The "examples will be added" promise is removed as the audit proposed; no owner commitment was given for it.

## Decisions of 2026-10-11 (12:48 Asia/Riyadh), answering record 19
| ID | Question | Owner answer (verbatim) | How it is applied in v0.4.1 |
|---|---|---|---|
| WD-12 | A real, monitored enquiry address (audit C1) | "mish3labdul@gmail.com" | Set as `DELIVERY.mailto` in `site.js`. After drafting, the visitor gets "Open in your email app": a `mailto:` link addressed there, with the subject and body filled from the draft. The site itself still sends nothing; the visitor sends from their own email program. Not done: the footer contact block still shows the WD-03 temporaries; no endpoint is connected; no test message was sent; the QA reads the link without following it. |
| WD-13 | Who it serves image (audit H6) | "keep the product scene" | GEM-WEB-B04 stays in #clients. |
| WD-14 | Approval of the proposed copy in record 19 | "Approval of the new copy: the full list" | Every line in record 19 "Proposed copy introduced in v0.4" is **ACCEPTED**. Copy written after this approval (record 20) is PROPOSED. |
| WD-15 | Screen-reader and cross-browser testing (audit A3) | "postpone testing by a person" | Postponed. It remains a release prerequisite, not done. |
| WD-16 | Ready packages: package set and names (13:31) | "Package set: as proposed / Names: keep as proposed." | Room set, Wall-mounted set and Travel set, built from the Part D formats, kept as working names (record 22). Product data stays unset. |
| WD-17 | Slider or static cards | No answer given | The recommended static cards were built. A carousel would first need a Part B component through change control. |
