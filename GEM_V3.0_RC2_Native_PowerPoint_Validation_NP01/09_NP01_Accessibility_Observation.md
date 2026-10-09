# 09 · NP01 Accessibility Observation (native; no remediation)

**Observation only.** The 30-slide queue (`ODI01-R1/11_Accessibility_Queue.md`) was **not** remediated: no title, reading order, alt text or decorative flag was changed, and none of PowerPoint's Quick Fix / Set as Slide Title / Add Slide Title buttons was pressed. VAL-08 and VAL-15 are not closed. GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE.

Tool: PowerPoint 16.113.3 `Tools ▸ Check Accessibility` (the "Accessibility Assistant" pane), run on the Part A and Part C test copies.

| Item | Native result | Against the existing queue | Verdict |
|---|---|---|---|
| Part A — missing slide titles | **27** (outline view: blank-title slides 1, 12, 19, 20, 23, 26, 28, 29, 30, 32, 34, 35, 38, 42, 48, 49, 53, 54, 56, 58, 62, 63, 65, 67, 76, 77, 80) | Queue lists the same 27 Part A slides but classifies them: **20 NEEDS ACCESSIBILITY TITLE** (1, 19, 20, 30, 32, 34, 35, 38, 42, 48, 49, 53, 54, 56, 58, 62, 63, 65, 67, 76), **5 NEEDS READING-ORDER FIX** (12, 23, 28, 29, 77) and **2 UNCERTAIN** (26, 80) | **CONFIRMED for the 20 'needs title' slides.** **NEW FINDING for the other 7** (5 reading-order + 2 uncertain slides): PowerPoint also finds no title on them, which the queue's classification did not say. The set of untitled slides equals the queue's Part A set exactly. |
| Part A — "Check reading order" | **58 slides** flagged | Queue carries 6 reading-order + 2 uncertain for Part A | **NEW FINDING** (broader advisory; PowerPoint flags many slides for review; not individually reviewed and not a defect determination) |
| Part A — missing alt text | **313 shapes** (Quick Fix offered "mark as decorative" — **not applied**) | Not in the queue | **NEW FINDING** |
| Part A — table without header row | **1** | Not in the queue | **NEW FINDING** |
| Part A — hard-to-read text contrast; duplicate titles; merged/split cells; section names; subtitles | No issues flagged | — | observation |
| Part C — queue slides 1, 10, 14 | The Assistant stayed on "Updating results…" for 35+ seconds and its category check marks cannot be trusted | Queue lists 3 Part C slides | **NOT TESTED / NOT COMPLETED** |
| Part B, Part D | Checker not run | Not in the queue | **NOT TESTED** |

PowerPoint's status bar showed "Accessibility: Investigate" on all four decks.

Side effect to know about: clicking an Assistant item switches the left pane to an outline list and selects a shape on the target slide. It is view state only; the test copy was closed with saving off.

**NP01-R1:** these accessibility findings are carried forward unchanged and unremediated; Parts B/C/D remain NOT COMPLETED; no accessibility gate is closed.
