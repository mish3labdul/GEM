# 02 · D3A Authority Verification (C1–C4)

**Method.** Each correction was checked against the *actual current files*, not the AFC02 prose: the Approval Register workbook (`GEM_V3_RC2/00_originals/…Register_Prefilled.xlsx`), the authoritative Part A, Part B, Part C and Part D release files, the letterhead package, the open evidence registers, and the release-governance state (AC20 OPEN). Verification date 2026-10-09; baseline `4ea0d11`.

**Overall: C1, C2, C3 and C4 are each SUPPORTED. None introduces new policy; none needs an owner choice.** Under the owner's explicit instruction for this task, all four were implemented as candidate copies (`03`).

| | C1 | C2 | C3 | C4 |
|---|---|---|---|---|
| **Target** | Part A slides 79–80, speaker notes | Part C slide 44, body text | Part D `04_release/SHA256SUMS.txt` | "SYSTEM READY" in 3 release-notes files (4 occurrences) |
| **Verdict** | **SUPPORTED** | **SUPPORTED** | **SUPPORTED** | **SUPPORTED** |
| Visual content changes? | No | **Yes** (one body sentence; rendered and checked) | No (text list) | No (Markdown notes) |
| Notes-only? | **Yes** | No | n/a (not a deck) | n/a (not a deck) |
| New policy? | No | No | No | No |

## C1 — Part A slides 79–80 notes: Part B description
- **Current authoritative wording.** Slide 79 notes (part `notesSlide80.xml`): "Part B's document ID is applied through its patch specification until its source is regenerated." Slide 80 notes (part `notesSlide79.xml`): "Part B is the Digital Design System V3.0 (RC2 patch specification issued; PDF regeneration pending its source)." (The notes part numbers are swapped relative to the slide numbers in this deck; recorded exactly.)
- **Proposed wording.** Slide 79: "Part B is issued as its own RC2 deck with a token package (PartB_RC2/05_release); its component bundle does not yet exist (VAL-13, VAL-20)." Slide 80: "Closing. Part B is the Digital Design System V3.0, issued as Release Candidate 2 with a token package; its component bundle is pending (VAL-13, VAL-20). Part C …" (rest unchanged).
- **Governing evidence.** The Part B RC2 source and release deck exist (`PartB_RC2/01_source/B-RC2.pptx`, `05_release/…Part B — RC2.pptx`, 157,803 bytes) and carry document ID `GEM-DDS-V3.0-RC2` on the cover and on slide 34 ("Edition state · WORKING SPECIFICATION · NOT RELEASED"); a 35-page tagged PDF exists in `05_release`; a token package exists (`05_release/tokens`, 153 tokens). The component bundle does not exist: open evidence register — VAL-13 "In progress … no component source, no Storybook", VAL-20 "Not started", OD-SRC "Open". Part A slide 79's own body already lists "Related · GEM-DDS-V3.0-RC2 (Part B)". So the "patch specification … until its source is regenerated" statements are stale and the corrected text states only facts already recorded elsewhere.
- **Remark (not a defect).** The notes cite a repository path as a pointer; it names an existing folder and adds no rule.
- **Verdict: SUPPORTED.**

## C2 — Part C slide 44: letterhead status
- **Current authoritative wording.** "Templates are an OPEN DELIVERABLE (AB10, AB11, W01–W10): none exists yet."
- **Proposed wording.** "…W01–W10): a Letterhead Set (Application Revision 03) exists as a WORKING APPLICATION / PENDING VALIDATION; no template is accepted."
- **Governing evidence.** `GEM_Letterhead_Set_v1.1_Application_Revision_03/` exists in `main` with 8 Word templates; the package and its README call it a working application pending validation, and ODI01-R1 QA check 13 confirmed that all 8 templates carry the text "WORKING APPLICATION / PENDING VALIDATION". The Register records AB10, AB11 and W01–W14 as *scope decisions* (included in the final system), not as acceptance; OD-TPL (templates) is still an open deliverable and no template acceptance is recorded. The slide's own table keeps Letterhead as "[PENDING PRODUCTION MASTER]", which the new sentence agrees with. "None exists yet" is therefore contradicted by the repository, and "no template is accepted" is what the evidence supports.
- **Visual change.** Yes: the body sentence is replaced and still occupies two lines; rendered before and after (`11_QA_Evidence/C44_before_after.png`); no overflow or collision; all other 77 pages of the candidate PDF are text-identical to the ODI01-R1 PDF.
- **Remark.** The sentence names "Application Revision 03", a package revision; if a later revision supersedes it the slide will need the same kind of synchronization again.
- **Verdict: SUPPORTED.**

## C3 — Part D checksum list: self-reference
- **Current authoritative content.** `Amenities_Portfolio_PartD_RC2/04_release/SHA256SUMS.txt` has 3 lines; one is its own entry `0549416c92bd…  SHA256SUMS.txt`. That value cannot be correct (a file cannot contain its own final hash): recomputed, the file hashes to `a4545133…`, not `0549416c…`.
- **Proposed content.** The same list without the self-entry (the PDF and PPTX lines, unchanged).
- **Governing evidence.** The two release hashes in the list verify against the current files. Of the 10 checksum lists in the repository, this is the only one that lists itself; the other 9 exclude themselves (scan recorded in `11_QA_Evidence/checksum_list_scan.txt`). Repository checksum verification (ODI01-R1) reported exactly this one mismatch.
- **Visual / notes-only.** Not a deck; plain-text list.
- **Verdict: SUPPORTED** (defect correction; no policy).

## C4 — "SYSTEM READY" → "NOT RELEASED"
- **Current authoritative wording.** `qa/GEM_V3_RC2_Release_Notes.md` line 3 and its identical copy `GEM_V3_RC2/03_qa/GEM_V3_RC2_Release_Notes.md` line 3: "State: RC2 SYNCHRONIZED · SYSTEM READY — EVIDENCE GATES REMAIN"; `qa/GEM_V3_RC2_Final_Release_Notes.md` lines 3 and 48: the same phrase.
- **Proposed wording.** "SYNCHRONIZED · NOT RELEASED · EVIDENCE GATES REMAIN" in all four places.
- **Governing evidence.** No deck uses "SYSTEM READY" (0 occurrences in Parts A–D release and candidate decks), whereas "NOT RELEASED" is already the decks' edition-state wording (Part A slide 79 "WORKING EDITION · NOT RELEASED"; Part B cover and slide 34; Part C). The notes themselves say "Not 'Approved V3.0'"; AC20 is Evidence Required in the Register; the owner-adopted status label uses NOT RELEASED. The correction removes a phrase that could be read as release readiness and replaces it with existing vocabulary.
- **Scope note.** The historical audit note `GEM_V3.0_Integrated_Brand_Ecosystem_Audit.md` also contains "SYSTEM READY — EVIDENCE GATES REMAIN" (a target classification in the audit text). It is a historical record outside the three notes files named in C4, so it was **not** changed and is listed under observations in `10`.
- **Combination note.** For `Final_Release_Notes`, the candidate is built on the ODI01-R1 D6 candidate, so the accepted D6 wording and C4 are combined in one file.
- **Verdict: SUPPORTED.**

## Observation (no edit)
A scan of all current decks found exactly three stale statements of the C1/C2 kind (Part A notes ×2, Part C slide 44); C1 and C2 cover all three.
