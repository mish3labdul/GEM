# GEM™ Arabic localization — L10N01 R2 QA

11 October 2026. ARABIC LOCALIZATION WORKING DRAFT / PENDING LOCALIZATION APPROVAL.

**INTERNAL EDITABLE REVIEW ONLY — NO VALIDATED DOCUMENT RELEASE.**

Source branch `claude/gem-worktree-safety-30b559`, commit `4e8c7f18f73d9f4b368fcd735c1cd5e3725a879d`, rechecked through GitHub API on this revision. Governing baseline: FA01/RP01. This iteration concerns the 24-slide Part D only. English source and unrelated work unchanged.

| ID | File / page | Finding and exact correction / next test | Authority | Severity | Result |
|---|---|---|---|---|---|
| L10N-01a | Part D, punctuation runs throughout; sample p5 | Exporter mapped shared Arabic-font punctuation incorrectly. Split ASCII punctuation into explicit Inter runs; retain Arabic in Noto Sans Arabic, no text changes or fallback. Brackets/slashes now visible and extracted on p5. | Part B mixed-script guidance; M16/D8 | P0 | PASS for tested punctuation repair only |
| L10N-01b | Diagnostic PDF, p5 and Arabic combining clusters | Remaining Arabic copy/extraction ordering defects: e.g. source `ملفًا` is extracted with the mark attached to another glyph and an inserted space. An evidence-derived private ToUnicode trial repairs 17 missing mappings; 105 exporter clusters then match character multisets, but this does not establish logical word/paragraph order. Do not issue PDF. Validate complete copy/search and reading order using native export and independent PDF tools. | Part B accessibility/RTL; D8 | P0 BLOCKER | FAIL |
| L10N-02 | Part D, slide3 headline | Constrained textbox width from 890 to 600 px. Headline right edge 696; image left edge 753, 57px separation. Rendered layout no longer collides. | Part A composition; source Part D slide3 | P1 HIGH | PASS for available renderer |
| L10N-06 | Part D slides3,9,15,18,22 internal-review labels | INK text on INK background invisible. Apply existing BEIGE #BCACA7. Same treatment verified on all seven dark slides including cover/closing. | Part A palette; status legibility; derivative control | P1 HIGH | PASS for available renderer |
| L10N-03 | All new Arabic copy and image descriptions | Proposed language has not received human linguistic approval. Review terminology, punctuation, meaning and alternative descriptions; no inherited HR01 approval claimed. | HR01 / M16 | P1 HIGH | REQUIRES OWNER |
| L10N-04 | Final PPTX | Native open/edit/save/close/reopen, font rendering, RTL and screen-reader testing unavailable. Computer-use access to Microsoft PowerPoint was rejected again. No alternative UI bypass used. | D8 / user acceptance requirements | P1 HIGH | PENDING |
| L10N-05 | Speaker notes; slides11,18,21,22,23 semantic sequence | Original English notes retained. Full Arabic notes, native reading order, tables and semantic sequencing remain to be checked. Source left-to-right numbered timelines retained; Arabic paragraph direction alone does not validate localized sequence. | User scope / Part B / HR01 | P2 MEDIUM | PENDING |
| L10N-07 | PDF metadata/tags/AT | Diagnostic PDF root language is en-US. Must be ar-SA with appropriate Latin spans; headings, table semantics, alt text, bookmarks and AT remain unvalidated. PDF withheld. | Part B accessibility / D8 | P1 HIGH | FAIL / PENDING |
| L10N-08 | Physical output and rights | No new supplier/physical specifications, font rights or production-master acceptance established. | Part C / FA01 retained deferrals | P1 HIGH | REQUIRES SUPPLIER / REQUIRES OWNER |

## Evidence and limits

PASS: 24 slides; final PPTX imports through Artifact Tool; structural integrity; required native table retained on slide23; encoded fonts restricted to Jost, Inter, Noto Sans Arabic. All source media bytes unchanged from the initial controlled Arabic draft, which preserved the promoted source media. Concatenated slide text is unchanged from that draft. Required repository Regular fonts used for headless rendering; PDF reports prescribed font families embedded. No external brief used.

All 24 R2 slides rendered at 1400px and individually visually inspected. No new clipping or geometry/text collision observed in this renderer. Product-image text remains unchanged source concept artwork. Small label placeholders are inherited source-scale content; native zoom/readability and accessibility are not passed. Three inherited off-slide cover objects remain recorded in the structural receipt.

PDF private trial: 24 pages rendered. ToUnicode repair trial based only on explicit exporter ActualText; 17 mappings repaired; 105 clusters tested with zero character-multiset mismatches. Word-level order still fails. Trial PDFs are private diagnostics, not delivered matching PDFs. Included PNGs are QA evidence, not PDF replacements.

Native PowerPoint and assistive-technology checks remain PENDING. Source master/font acceptance, localization, rights and supplier gates remain. FA01 AC20 stays authorized with formal deferrals and release-scope exclusions; this new Arabic derivative does not inherit external-issue permission. No PDF authorized for external issue.

Parts A/B/C, remaining company documents and complete notes localization are not completed in this batch. Stop affected document release until the Arabic export defect and required native validation are resolved.
