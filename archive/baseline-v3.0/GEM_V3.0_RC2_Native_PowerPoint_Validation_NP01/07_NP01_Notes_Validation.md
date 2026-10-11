# 07 · NP01 Notes Validation (user-visible PowerPoint Notes pane)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE** · D7 PENDING / DO NOT PUSH · AC20 OPEN.

Authority for this test: the Notes pane shown in PowerPoint's Normal view for the slide currently on screen, not OOXML part numbering. Part A test copy was opened fresh and unmodified (`saved=true`); the Notes pane was toggled on and slides 79 and 80 were selected through the UI model.

| Slide | What the Notes pane showed (native, user-visible) | Expected C1 wording | Result |
|---|---|---|---|
| Part A 79 (Document control and change log) | "Document control per register A11 and the change-log appendix (Z24, AB19). Owner and approver names are recorded by the Brand Owner before AC20. Part B is issued as its own RC2 deck with a token package (PartB_RC2/05_release); its component bundle does not yet exist (VAL-13, VAL-20)." | "Part B is issued as its own RC2 deck with a token package … its component bundle does not yet exist (VAL-13, VAL-20)." | **PASS** — C1 wording on the correct slide |
| Part A 80 (closing slide) | "Closing. Part B is the Digital Design System V3.0, issued as Release Candidate 2 with a token package; its component bundle is pending (VAL-13, VAL-20). Part C, Production Standards V3.0, is issued as Release Candidate 2, a working edition pending production validation." | "Part B is the Digital Design System V3.0, issued as Release Candidate 2 with a token package; its component bundle is pending (VAL-13, VAL-20)." | **PASS** — C1 wording on the correct slide |

**No slide 79/80 inversion in the user-visible UI.** The OOXML parts are numbered the other way round (slide 79 → `notesSlide80.xml`, slide 80 → `notesSlide79.xml`, per the D3 trace), which is why the UI test was required. The object model (`notes page` of each slide) returned the same text as the pane. The "Part B component bundle does not yet exist" statements are still conditional on VAL-13 and VAL-20, which stay open.

**C4 (release wording "NOT RELEASED")** is a Markdown release-notes change, not a deck/notes change, so it is not testable in PowerPoint. In the decks, the native render of Part A slide 79 shows "Edition state · WORKING EDITION · NOT RELEASED" and the Part A cover shows "release not yet authorized (AC20)". These are existing deck wording, not a C4 verification.

Other notes: 72 of 80 Part A notes slides, 8 of 35 Part B, 71 of 78 Part C and 24 of 24 Part D carry text (object-model count). No other notes slide was compared against a spec; NP01 does not judge notes content beyond 79/80.

Evidence: `12_screenshots/A_slide079_with_notes_pane.jpg`, `A_slide080_with_notes_pane.jpg`.
