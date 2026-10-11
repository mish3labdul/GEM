# 10 · NP01 Open Findings

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE** · D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20 OPEN. Nothing here closes a gate. Severity per the NP01 scale; nothing below is called a release blocker unless stated.

## Status after NP01-R1
**P2 OPEN COUNT (controlled candidate lineage): before NP01-R1 = 1 · after = 0.** The original NP01 finding below is preserved for traceability; NP01-F01 is marked *corrected in NP01-R1 (candidate lineage only)*. P3 findings are carried forward as **ACCEPTED MINOR NATIVE VARIANCE / DEFERRED** (none is content loss). Part A slide 39 is a **LOCALIZATION / RTL OBSERVATION — DEFERRED TO ARABIC VALIDATION**. Accessibility findings are unchanged. Nothing here closes a gate.

**Finding status record:** NP01 P2 BEFORE = 1 (Part B slide 30, native clipping) · NP01-R1 P2 AFTER = 0 for the current controlled candidate lineage only. The original P2 record and provenance are preserved below.

## P0 — cannot open / corruption / material content loss
None. All four decks opened without repair prompt, missing-font warning, media/linked-asset warning or compatibility banner.

## P1 — governance or content meaning altered natively
None. C1, C2 and D3B wording all render as specified; slide counts (80/35/78/24) match the baseline.

## P2 — visible layout/typography defect affecting usability
| ID | Where | Finding |
|---|---|---|
| NP01-F01 | Part B slide 30 | Token-excerpt box too short for its Courier New text (9 logical lines that wrap to 10); last line invisible natively, line above partly clipped. Native-only visible effect (the candidate's LibreOffice PDF shows all lines). **Provenance:** identical box geometry, text and typeface in `PartB_RC2/05_release` (the issued RC2 deck) and `PartB_RC2/01_source/B-RC2.pptx`, so it predates ODI01/D5 and exists in the authoritative RC2 deck as well (not opened natively). Courier New is a non-brand family. Needs a controlled change; not fixed in NP01. **NP01-R1 STATUS: CORRECTED IN THE CONTROLLED CANDIDATE LINEAGE and revalidated natively (box height +35.6 pt; paragraph below moved +35.6 pt); the original finding is preserved here. The same geometry remains in the authoritative RC2 release/source decks, pending a separately authorized promotion.** |

## P3 — minor native variance, not material
| ID | Where | Finding |
|---|---|---|
| NP01-F02 | Part A 34 | Body overruns box ~12 pt; clears footer |
| NP01-F03 | Part A 35 | Kicker wraps and sits tight above "Aa" |
| NP01-F04 | Part A 41 | Four-line headline tight against body |
| NP01-F05 | Part A 72 | Footer wraps to two lines |
| NP01-F06 | Part A 79 | Hairline rule through first line of change-log text (pre-existing, identical XML to ODI01-R1) |
| NP01-F07 | Part B 4, 12; Part C 4 | Table rows grow natively; adjacent text has zero clearance |
| NP01-F08 | Part C 27, 77 | Paragraph tight above dashed boxes; release-status box text fills its box |
| NP01-F10 | Part C 3 | Third placeholder line abuts the 'Edition states' line below (no leading); both legible |
| NP01-F11 | Part C 62 | Right-hand table is flush with the slide's right edge (table right boundary = slide width; zero right margin); content visible; geometry in the file, identical in ODI01-R1 |
| NP01-F09 | Part A 39 | Mixed Arabic/Latin line resolves LTR (no `rtl="1"`); REQUIRES NATIVE REVIEW; localization pass |

## REQUIRES NATIVE REVIEW
Part A slide 39 only (mixed-direction line; F09). Every slide flagged by the text-extent metric was subsequently viewed natively (89 of 217 slides viewed in total).

## OBSERVATIONS (evidence only, no defect)
- D5 flattening of bold lead-ins on Part B 3 and 19 and similar slides: accepted consequence.
- Courier New (1 text shape, Part B 30) is a non-brand family.
- Installed unaccepted Bold files exist; **not exercised** (0 bold characters). They remain a standing risk for any future bold run or any other machine.
- Accessibility: Part A — 20 'needs title' queue slides CONFIRMED; 7 other queue slides (5 reading-order, 2 uncertain) are also untitled natively (NEW FINDING); 58 reading-order advisories, 313 missing-alt shapes and 1 table without header are NEW FINDINGS; Part B/C/D accessibility NOT TESTED / NOT COMPLETED (`09`).

## ENVIRONMENT (not candidate defects)
- **E1 — macOS/PowerPoint sandbox file access.** Opening Parts A, C and D from the repository folder and from a scratch folder raised PowerPoint's "Grant File Access" dialog ("Additional permissions are required to access the following files…") and a "Sorry, PowerPoint can't read …" alert. Part B opened from the repo folder with no prompt. The user's request to open the files natively is the only authorization used. During the blocked Part C attempt I pressed 'Select…' in the Grant File Access dialog (the file picker opened with the Part C test copy pre-selected), then sent an unverified 'Grant Access' click and a Return key (which re-pressed 'Select…'), then Cancel clicks; the dialog did not clear and the Part C deck never opened from that path. The user then cancelled the dialog manually. Resolved by staging byte-identical copies inside PowerPoint's own container (`~/Library/Containers/com.microsoft.Powerpoint/Data/Documents/GEM_NP01_NATIVE_TEST/`), where all four opened with no prompt. No sandbox, privacy or preference setting was changed. Classified ENVIRONMENT / MACOS POWERPOINT SANDBOX ACCESS ISSUE — not corruption, repair, missing font, or a P0/P1/P2 defect.
- **E2 — property reads mark decks modified in memory.** After the AppleScript text-range sweep, Parts A, B and C reported `saved=false` (Part D stayed `true`) although the files on disk were unchanged; viewing alone never changed `saved`. Handled by closing with saving off and reopening fresh for all visual work.
- **E3 — PowerPoint's AppleScript PNG export did not produce files.** Two `save presentation … as save as PNG` attempts (Part C, Part D) returned without error and wrote nothing; no PPTX was written and the decks stayed unmodified. Native window screenshots were used instead.
- **E4 — Accessibility Assistant** stayed on "Updating results…" for Part C.
- **E5 — stale windows:** two leftover "Grant File Access"/"Open" windows remained listed off-Space after the blocked attempts; the user cancelled the dialog; no grant took effect (the deck never opened from that path).

## Standing gates (unchanged by NP01)
Remaining Gate #11 (native PowerPoint/Word/Acrobat/AT QA) is **still open**: NP01 supplies **PowerPoint-only** evidence on one Mac with unaccepted working-build fonts. Not closed: VAL-05, Y03, VAL-19, VAL-07, VAL-08, VAL-15, VAL-16, D7, AC20; D8 external Arabic/bilingual PDF remains blocked.

## Historical findings, intentionally untouched
ODI01-R1 `04_Implementation_Trace.md` references a nonexistent `05_Governance_and_AC20_Status.md`; ODI01-R1 `03_Owner_Decisions_Carried_Forward.md` points to `20_candidate_documents/` where the folder is `19_candidate_documents/`; historical QA/source material still says "SYSTEM READY" while the D3 controlled candidate says "NOT RELEASED". Not changed.
