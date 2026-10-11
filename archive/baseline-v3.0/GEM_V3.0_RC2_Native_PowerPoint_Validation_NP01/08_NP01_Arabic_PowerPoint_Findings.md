# 08 · NP01 Arabic / RTL — Native PowerPoint Observation

**Status remains: PENDING LOCALIZATION APPROVAL. VAL-07, VAL-08 and VAL-15 are NOT closed. D8 stands: external Arabic/bilingual PDF issue remains BLOCKED. This is not Arabic approval.**
GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE · D7 PENDING / DO NOT PUSH · AC20 OPEN.

Scope: shaping, RTL flow, character order, punctuation placement, Latin/Arabic interaction, clipping, fallback font. Arabic text appears in Part A slides 37, 38, 39, 65, 66, 68 and Part B slide 9 (Part C and Part D carry none as text; Part D bottle labels are images). All strings are labelled working placeholders in the decks.

| Check | Observation (native, Part A unless stated) | Class |
|---|---|---|
| Shaping | "أهلاً بكم", "الأولوية للعربية", "الاستقبال", "العربية" and Part B's "أب" render as joined, correctly shaped glyphs with tanween intact | PASS (observation) |
| Fallback font | Runs set `cs` = Noto Sans Arabic; native families reported Noto Sans Arabic for the Arabic shapes (11 on Part A, 1 on Part B). No system Arabic fallback observed | PASS (observation) |
| Clipping | No Arabic text clipped on slides 37, 38, 65, 66 or Part B 9 | PASS (observation) |
| Single-word / single-phrase alignment | Right-aligned in their boxes; bilingual order panel on slide 65 shows Arabic top-right and English bottom-left as the slide states | PASS (observation) |
| Punctuation | "[عربي]" placeholder brackets render without visible displacement | PASS (observation) |
| **Mixed Arabic/Latin line order (slide 39)** | "رقم الحجز GEM-0000": the paragraph is `algn="r"` but has **no `rtl="1"`** and `lang="en-US"`, so PowerPoint resolves it with a **left-to-right base direction**. The Arabic label appears to the left of the Latin code; an RTL reading flow would put the label on the right. "غرفة 412" displays with the number to the left, which is also the correct visual order | **REQUIRES NATIVE REVIEW — P3** (placeholder strings; belongs to the localization pass) |
| Paragraph direction generally | Every Arabic paragraph in Part A (11 paragraphs on slides 37–39, 65, 66, 68) and Part B slide 9 has no `rtl="1"`; Part A's runs are `lang="en-US"` (Part B's `lang` was not checked) | **OBSERVATION** — for localization QA to decide (the decks themselves say "True RTL flow and dir=rtl on the document") |

Not tested: any Arabic outside these slides, PDF/Acrobat Arabic text layer (R03-03, LH03), Word letterheads, accessibility reading order of Arabic text, and real (approved) copy — none exists.

Evidence: `12_screenshots/A_slide037_arabic_native.jpg`, `A_slide038_arabic_native.jpg`, `A_slide039_arabic_mixed_order_native.jpg`, `A_slide065_arabic_native.jpg`, `A_slide066_arabic_native.jpg`, `B_slide009_native.jpg`. Slide 68 shares the single-bracket placeholder pattern of slide 65 and was not individually viewed.
