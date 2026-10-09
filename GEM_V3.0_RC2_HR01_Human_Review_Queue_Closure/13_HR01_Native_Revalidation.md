# 13 · HR01 — Native Revalidation

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
Native checks of the HR01 candidates. They are technical evidence for the defined scope and not a WCAG conformance claim, linguistic approval or release statement.

## Environment
macOS 26.3.1 (25D2128); Microsoft PowerPoint 16.113.3 (16.113.26092714); Microsoft Word 16.113.3 (16.113.26092714). Candidates were copied into each application's sandbox folder, opened natively without repair, and their SHA-256 was confirmed unchanged after each session. No timestamps, recordings or tool dumps are committed.

## Lineage (proven by hash)
PowerPoint: the four AX01 candidates (hashes verified against the AX01 manifest) → HR01 candidates. Word: the eight Revision 03 templates were byte-identical to the AX01 baseline hashes; the four that carry Arabic content changed. Each HR01 file is proved by inverse transform to differ from its source only by the approved edits (`17_qa/candidate_build_log.json`, all `inverse_proof: PASS`).

## PowerPoint — Accessibility Assistant (built-in checker) and static corroboration
The rule views were read through the app; on Parts A, B and D the pane still showed "Updating results…" when the rules were opened, so those three readings are corroborated by the static predicate below. Only Part C was read after the Assistant finished.
| Deck | Missing alt text (AX01 → HR01) | Missing slide title (AX01 → HR01) | Notes |
|---|---|---|---|
| Part A (80 slides) | 31 → none | 27 → none | revised Arabic tile heading on slide 38 inspected natively: lays out correctly, geometry unchanged |
| Part B (35 slides) | 30 → none | not affected (0 in AX01) | |
| Part C (78 slides) | 26 → none | 3 → none | "Check reading order" advisory shows 75, unchanged from AX01 |
| Part D (24 slides) | 25 → none | not re-examined (unchanged by HR01; 0 in AX01) | the assistant stalled on "Updating results…" in one session (as AX01 observed); the rule result itself was readable after a fresh PowerPoint session |

**Static corroboration** (`16_scripts/hr01_static_accessibility_check.py`, `17_qa/hr01_static_accessibility_check.csv`): the AX01 walker, whose predicates reproduced AX01's native counts exactly (titles 27/0/3/0; shapes and pictures 31/30/26/25), gives for HR01: slides without a title 0/0/0/0 and shapes+pictures without alt text or a decorative flag 0/0/0/0 on Parts A/B/C/D. Tables (66: A 1, B 30, C 34, D 1) carry no alt text and are not counted by PowerPoint's rule; they were not classified by the content owner. Both sources agree; neither is a WCAG conformance claim.

The advisory "Check reading order" counts for Parts A, B and D were not re-read; HR01 changed no object order and the 13-slide manual sample (`08`) passed.

## Word — Accessibility Assistant
Arabic First Page, Arabic Continuation, Bilingual First Page, Bilingual Continuation: **"Looks good! No issues found."** Each opened with no repair prompt; the known "update fields?" prompt (AX01 documented that every template sets updateFields) was answered **No**, leaving cached field values untouched.

## Defect found and fixed during native validation
The first version of the localized footer label put the separator spaces inside the Arabic (right-to-left) run. Native Word rendered the contact initials and the page label with no gap (the "[W]" initial ran straight into the page number). The build was corrected so the separator spaces stay in a left-to-right run and the Arabic words are a separate right-to-left run; native Word then showed the gap restored and the label reading right-to-left as page 1 of 1. All checker and render results above are on the corrected files. PowerPoint candidates were unaffected (rebuilt byte-identical).

## Manual assistive-technology evidence
Separate and human: `07_HR01_Screen_Reader_Test_Register.csv` and `08_HR01_Reading_Order_Manual_Review.csv` (REVIEWER OBSERVED — MASHAL, macOS VoiceOver). Not recorded here as tool output because none exists.

## Not covered
Windows Word / Word Online, NVDA/JAWS (SR-12 deferred), Acrobat and tagged-PDF checks (SR-11 deferred to D8), save/reopen/export of final deliverables (VAL-15), contrast of text over pictures.
