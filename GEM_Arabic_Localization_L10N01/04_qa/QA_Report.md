# GEM™ Arabic localization L10N01 — QA report

11 October 2026. ARABIC LOCALIZATION WORKING DRAFT / PENDING LOCALIZATION APPROVAL. Overall: BLOCKED / NOT READY FOR USE.

| ID | File / location | Finding | Source / correction | Severity | Result |
|---|---|---|---|---|---|
| L10N-01 | Part D draft PDF, e.g. pages 1, 5, 14 | Exported Arabic text contains unmapped combining glyphs and incorrect bracket extraction (page 5: 0 left brackets, 14 right brackets). Native visual punctuation fidelity not established. | M16, D8, Part B mixed-language/accessibility guidance. Use a verified Arabic-capable native export; compare complete logical strings, punctuation, marks and copy/search; do not replace fonts silently. | P0 BLOCKER | FAIL |
| L10N-02 | Part D Arabic draft, slide 3 | Right-aligned headline uses a wide source textbox and runs underneath the image. | Part A composition + source slide 3. Constrain Arabic headline to the image-free left column or recompose within the existing layout; then render and inspect. | P1 HIGH | FAIL |
| L10N-03 | All new Arabic derivatives | New copy has no human linguistic approval. Existing HR01 decisions do not approve new translation. | HR01 Arabic Decision Log / M16. Mashal reviews terminology, paragraphs, punctuation, tone and new alt text. | P1 HIGH | REQUIRES OWNER |
| L10N-04 | Part D draft | Native PowerPoint open/edit/save/reopen and RTL validation unavailable; computer-use access rejected. | D8 / AR01. Test in native PowerPoint and required Windows/AT scope. No shell-based UI bypass attempted. | P1 HIGH | PENDING |
| L10N-05 | Part D notes and semantic order | English technical speaker notes retained; Arabic notes translation and complete logical reading-order review not completed. | User translation scope / HR01 accessibility lineage. Translate meaningful narrative notes, preserve machine identifiers; verify reading order including register table. | P2 MEDIUM | PENDING |

## Passed technical checks
Remote branch retrieved at 4e8c7f18f73d9f4b368fcd735c1cd5e3725a879d; 14/14 file hashes matched RP01 scope matrix. 24 source slides retained. 309 visible paragraphs drafted; no unmapped visible English paragraph in the source extraction apart from intentionally retained signature lines. All original media bytes preserved. Native table on slide 23 retained. Structural finalizer/import/font-family checks passed; this is not native rendering/accessibility acceptance. PDF rendered 24 pages; fonts observed were prescribed families after explicit font configuration.

## Actual visual coverage
All 24 pages rendered; pages 1–8 individually inspected. Slide 3 failure triggered quarantine. Remaining pages are not claimed visually reviewed. An initial baseline render used substituted Linux Libertine fonts; it was rejected and rerendered with exact repo Regular builds before translation QA. No substituted render is delivered.

## Deliverable boundary
No validated Arabic PPTX/DOCX/PDF release is delivered. Draft PPTX is quarantined, not for use. The diagnostic PDF remains private and is not issued as a matching PDF. Parts A/B/C translation, executive/minimal Arabic derivatives and complete company-document localization remain pending. Original source documents are unchanged.

## Governance
FA01 AC20 remains authorized with formal deferrals and scope exclusions. L10N01 is a new unapproved derivative; it does not inherit external-issue permission. D8 restrictions remain. Production, supplier, master/font rights and legal/AT gates are not closed. Physical values remain REQUIRES SUPPLIER.
