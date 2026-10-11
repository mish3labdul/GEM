# 04 · NP01-R1 — Native PowerPoint Revalidation (Part B slide 30)

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE** · D3 RESOLVED AT OWNER-DECISION LEVEL (X12 STREAM = BRAND) · D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20 OPEN · D8 external Arabic/bilingual PDF BLOCKED. PASS here means native integrity of this slide in PowerPoint 16.113.3 on this Mac with unaccepted working-build fonts; it is not design approval and closes no gate.

Method: byte-identical before (ODI01-R1) and after (NP01-R1) copies staged in PowerPoint's container, hash-verified before and after (`qa_evidence/05_native_test_copy_staging.json`), opened fresh, slide 30 captured under identical window conditions, then the NP01 property sweep run on slide 30. Both copies closed with saving off and deleted. NATIVE SCREENSHOT EVIDENCE EXISTS LOCALLY AND WAS REVIEWED. SCREENSHOTS ARE INTENTIONALLY EXCLUDED FROM VERSION CONTROL PENDING D7 LEGAL/IP REPOSITORY-VISIBILITY DECISION.

| Criterion | Before (ODI01-R1) | After (NP01-R1) | Result |
|---|---|---|---|
| All ten rendered lines visible | No — last line not visible, line above clipped | **Yes** — "motion · layout · locale" visible with clear space below | PASS |
| Clipping / overflow | Text escaped the box by 18.9 pt | Inset-aware need 199.3 pt vs box 202.0 pt: **2.7 pt slack**; text inside the fill | PASS |
| Collision with other objects | — | `Text 5` keeps its 16.0 pt gap; footer 97.6 pt clear; right column unchanged | PASS |
| Footer interference | none | none | PASS |
| Inter remains 400, no bold | Inter, bold=false | Inter, bold=false; the paragraph's range-level `bold=true` is the mixed state: **0 bold characters of 233** at character level | PASS |
| Excerpt font | Courier New (non-brand, unchanged) | Courier New (unchanged, per instruction) | observation |
| Type size / spacing | 12 pt / 16.8 pt | 12 pt / 16.8 pt | unchanged |
| Font-substitution warning / missing-font banner | none | none | PASS |
| Unrelated geometry change | — | none natively (text bounds of all six text shapes unchanged); structurally proven only `Text 3` height and `Text 5` y changed | PASS |

Numbers: `qa_evidence/08_native_slide30_before_after.csv`. The raw sweep TSVs behind it (`qa_evidence/06_native_sweep_slide30_BEFORE.tsv`, `07_native_sweep_slide30_AFTER.tsv`) exist locally only and are excluded from version control pending D7 (they contain short deck-text excerpts).

Process note: one command during this pass mistakenly tried to open a test copy that had already been deleted (an earlier container folder); PowerPoint showed a "can't read" alert, which was dismissed with OK. Nothing was granted or opened. Helper scripts `np01_open1.sh`, `np01_goto.sh`, `np01r1_open.sh` are included in `scripts/`.

Limits: one slide, one Mac; the object model reports requested not rendered fonts (viewed render consistent); the excerpt text remains in the non-brand Courier New by owner instruction. Visual evidence: `local_only_screenshots/B_s030_BEFORE_ODI01-R1_native.png` and `B_s030_AFTER_NP01-R1_native.png` — **local-only**.
