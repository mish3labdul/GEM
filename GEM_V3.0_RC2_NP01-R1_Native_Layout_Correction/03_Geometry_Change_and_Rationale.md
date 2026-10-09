# 03 · NP01-R1 — Exact Geometry Change and Rationale

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE** · D3 RESOLVED AT OWNER-DECISION LEVEL (X12 STREAM = BRAND) · D7 LEGAL/IP DECISION PENDING — DO NOT PUSH · AC20 OPEN · D8 external Arabic/bilingual PDF BLOCKED.

## The change (two numeric attributes in `ppt/slides/slide30.xml`; nothing else)
| Shape | Attribute | Before | After | Change |
|---|---|---|---|---|
| `Text 3` — token-excerpt box | `<a:ext cy>` | 2112963 EMU = 166.4 pt | **2565400 EMU = 202.0 pt** | +452437 EMU = **+35.6 pt** (taller; top edge, left edge and width unchanged) |
| `Text 5` — paragraph below the box | `<a:off y>` | 4094113 EMU = 322.4 pt | **4546550 EMU = 358.0 pt** | +452437 EMU = **+35.6 pt** (moved down by the same amount; keeps the existing 16.0 pt gap) |

**Text size changed? No** (12 pt throughout). **Line spacing changed? No** (exact 16.8 pt). Font family, colours, bold flags, insets, wording, shape order, and every other slide are unchanged. The box top (140.0 pt) still aligns with `Text 4` (the right-hand bullets).

## Why this and not the owner's earlier options (in order)
1. **Increase the box height if unused space permits.** Only **16.0 pt** is free between the box bottom (306.4 pt) and `Text 5` (322.4 pt). Growing the box by the 32.9 pt it needs would collide with `Text 5`, so height alone is insufficient.
2. **Adjust internal margins.** Even with all four insets at zero the text bounds (169.3 pt) exceed the box (166.4 pt), so margins cannot fix the height. Margins also cannot remove the line-1 wrap: the line is 51 Courier New characters = 367.2 pt; usable width is 358.4 pt, or 364.0 pt with the right inset at zero; only removing the left inset as well (380.0 pt) would fit it, which would shift the text indent away from the panel's consistent padding.
3. **Smallest vertical-position adjustment necessary.** Used: grow the box to 202.0 pt (inset-aware need 199.3 pt, **2.7 pt slack**) and move `Text 5` down by the same 35.6 pt. `Text 5` ends at 393.6 pt; the footer starts at 491.2 pt, leaving 97.6 pt clear.
4. **Line spacing / type size**: not needed, not touched.

`Text 5` is the paragraph directly below the panel; moving it is the minimum needed to keep the panel and paragraph apart, not a redesign or an unrelated object.

## Method
`scripts/np01r1_apply_slide30_fix.py`: base hash verified (22802377…), anchored single-match attribute replacements inside the two shape blocks, every other zip member raw-copied in the original order with its original ZipInfo (no python-pptx save, no re-serialization). Log: `qa_evidence/03_edit_log.json`. Output: `candidate_documents/GEM Digital Design System V3.0 — Part B — RC2 — NP01-R1 CANDIDATE (UNAPPROVED).pptx`.
