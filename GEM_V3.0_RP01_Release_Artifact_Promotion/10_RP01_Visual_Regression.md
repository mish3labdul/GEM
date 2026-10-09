# 10 · RP01 — Visual Regression

**GEM™ V3.0 — OWNER AUTHORIZED FINAL BRAND-SYSTEM BASELINE — FORMAL DEFERRALS RECORDED — ARTIFACT-SPECIFIC EXTERNAL-ISSUE RESTRICTIONS APPLY**
AC20: AUTHORIZED WITH FORMAL DEFERRALS AND RELEASE-SCOPE EXCLUSIONS (FA01). RP01 promotes release-state labels only; no gate is closed.

## Method
Every FA01-baseline source and every promoted file was rendered with LibreOffice (headless PDF export) and rasterized at 72 dpi; each page or slide was compared pixel by pixel (difference above 24 per channel). This is a LibreOffice render, not a native PowerPoint or Word render: it detects unintended change, it does not certify native layout. Native opens are recorded in 09.

## Result
| Final class | Pages / slides |
|---|---|
| PIXEL IDENTICAL | 25 |
| EXPECTED RELEASE-LABEL CHANGE ONLY | 200 |
| SUB-PIXEL NATIVE VARIANCE | 0 |
| VISIBLE REGRESSION | 0 |
| **Total compared** | **225** |

12 pages were flagged automatically because their differing area was large (status and document-control slides whose wording changed and re-flowed). Each was reviewed side by side by the main session: A78, A79, B4, B30, B31, B33, B34, C1, C75, C76, C77, D23. Findings: only the intended status wording changed; four layout problems found in the first LibreOffice build (Part A and Part C change-log lines, the Part C edition-state cell, the Part C slide 75 gate cell) were fixed by shortening the new text and the pages re-rendered; three further problems visible only in native PowerPoint (A79, B33, C77) were fixed afterwards (see 09) and the visual regression was re-run. A single known pre-existing collision on A78 (left column text meeting the right column under the substitute font) is present in the source render too.

Per artifact: L-Arabic_Continuation {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; L-Arabic_First_Page {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; L-Bilingual_Continuation {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; L-Bilingual_First_Page {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; L-English_Continuation {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; L-English_First_Page {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; L-Executive {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; L-Minimal {'EXPECTED RELEASE-LABEL CHANGE ONLY': 1}; P-A {'EXPECTED RELEASE-LABEL CHANGE ONLY': 61, 'PIXEL IDENTICAL': 19}; P-B {'EXPECTED RELEASE-LABEL CHANGE ONLY': 35}; P-C {'EXPECTED RELEASE-LABEL CHANGE ONLY': 72, 'PIXEL IDENTICAL': 6}; P-D {'EXPECTED RELEASE-LABEL CHANGE ONLY': 24}

Letterheads: the four English templates differ only in the removed footer marker line; the four Arabic and bilingual templates differ only in the added restriction line at the footer; nothing above the footer moved.

Full page-level table: `16_qa/rp01_visual_regression.csv`.
