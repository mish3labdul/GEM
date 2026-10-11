# 06 · HR01 — Accessibility Content Decision Log

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
Content decisions of the Accessibility Content Owner (Mashal, OD-G10). They do not close VAL-08 and are not a WCAG 2.2 AA claim. Item-level detail: `05_HR01_Accessibility_Content_Register.csv`.

## Method
Every proposal came from Claude and every wording was approved by the reviewer; nothing was applied on Claude's own judgment. Each of the 31 pictures was looked at before any alt text was proposed. Arabic label artwork in the images was **not transcribed**; the descriptions state purpose and visible content only and begin "Concept image" because the deck itself states all imagery is AI-generated concept imagery. No product specification was added (the volume printed on the refill container was deliberately left out). The method for titles follows OD-G02.

## Slide titles (30 slides: Part A 27, Part C 3)
- Approved as proposed, in three batches of ten. Every title is built from words already on the slide; the one derived title (Part A slide 76, from the DO / DON'T lists and the footer) was flagged to the reviewer as derived.
- **Method (reviewer choice): an off-slide title placeholder.** It sits outside the slide area, adds no visible object, shifts nothing and counts as the slide's title for navigation. This avoids the ~0.8 pt movement AX01 measured on the two covers (Part A slide 1, Part C slide 1) when the visible heading was mapped. It appears below the slide in PowerPoint's edit view only; slideshow and export do not show it.
- Verified: pixel-identical renders on all 217 slides except the three approved Arabic slides (`14`); native PowerPoint reports no missing slide title on Parts A and C (the Part A reading taken while the Assistant was still updating; corroborated by the static predicate, `13`).

## Alt text (31 pictures, Part D)
- 13 single bottle shots, 10 scenes/crops/formats (23 product pictures), 6 logo pictures whose generic text ("Supplied GEM raster artwork. PENDING PRODUCTION MASTER.") was replaced by "GEM logo", and 2 materials pictures whose generic "AI-generated … concept" text was replaced. All approved as proposed.
- The 6 generic-text pictures (AX01-F04) were identified by slide and shape from the deck; the AX01 registers only gave their count.

## The 89 unclassified shapes
AX01 had classed them as complex/unknown. Looking at the rendered slides showed that the ink-filled "panels" on Part A slides 43, 49, 58 and 63 are backing fields under pictures that already carry alt text, so they are redundant. Decisions by group (each shape recorded individually):
| Group | Shapes | Decision |
|---|---|---|
| Hairline rules and dividers | 18 | decorative |
| Backing panels under pictures that have alt text | 6 | decorative (redundant) |
| Dashed frames around the misuse examples (Part A slide 30) | 7 | decorative |
| Cover motifs, checklist boxes, booking-flow arrows | 26 | decorative |
| Palette swatches with adjacent captions | 8 | decorative (redundant with captions) |
| Clearspace boundary rectangles and the rounded container example | 3 | decorative (reviewer chose this over alt text) |
| Specimen sets (Part B slide 8 spacing squares, slide 14 grid columns) | 21 | one description per set on the first shape; the others decorative |
Totals: **87 decorative, 2 informative**. Descriptions for the two sets: "Spacing scale specimen: nine squares from 4 px to 96 px." and "Twelve-column grid specimen: twelve equal columns."

## Contrast
OD01-AC-C01: Part A slide 33 "Beige on White" (2.2 : 1) is a deliberate demonstration of the prohibited pairing and is labelled as such on the slide. The reviewer confirmed it is a palette specimen under OD-G05. No colour changed. The finding stays recorded as an owner-confirmed exception; the 113 text-over-picture runs remain unmeasured.

## Not decided here
Reading order (OD-G04) and screen-reader behaviour are covered by Queue 3 (`07`, `08`). The Register role "Accessibility QA" is unnamed and no independent verification has occurred; the content owner's decisions are not a substitute.
