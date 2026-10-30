# Brand alignment check — 30 October 2026

Independent visual check of the seven approved replacement files against the canonical Part D product art (`website/remake/assets/source/{shampoo,conditioner,body-wash,body-lotion,hand-wash}-source.png`) and the brand palette (Ink `#12171D`, Beige `#BCACA7`, White `#FFFFFF`; `brand/specification-assets/GEM_BRAND_PALETTE-SHEET_LIGHT_v0.1_20261006.svg`).

Method: each file was opened and viewed on 30 Oct 2026 and compared by eye with the canonical product images. Colours were not measured numerically (no image library was available), so tone findings are visual only. The earlier record's hashes were re-computed and all seven match.

This note records findings. It does not reverse the owner's 28 Oct visual approvals; it flags points for an explicit owner decision before the files ship.

| File | Finding | Kind |
|---|---|---|
| `scenes/family.webp`, `scenes/family-rtl.webp` | All five products are shown as amber glass bottles with a dark label. The canonical Body Lotion is a **cream** bottle with black pump and black label art. | Product-art mismatch |
| `scenes/family.webp`, `scenes/family-rtl.webp` | The Conditioner has a flat screw cap and no pump. The canonical Conditioner has a pump. | Product-art mismatch |
| `static/social.png` (V03) | The Conditioner is **cream**; the canonical Conditioner is dark amber. Body Lotion cream matches canon. | Product-art mismatch |
| `static/social.png` (V03) | A second sachet/card sits behind the first and its "GEM" wordmark is cut to "…M". A partly hidden wordmark does not respect the logo clear space. | Logo treatment |
| `source/format-wall-source.png` (V09) | Body Wash matches canon. The tile wall is a warm, saturated tan, visibly more orange than brand Beige `#BCACA7` (grey-pink). Mount hardware is not shown. | Palette (visual only); concept status |
| `scenes/tx-arches.webp` | Cream arches, no product or text. No brand conflict seen. | OK |
| Typography on labels | "GEM™", product name and Arabic names read correctly in all images. Product names match the approved list. | OK |

Related, outside this commit: `gem-assets-hub` has an uncommitted change that removes the beige left border from `.status` blocks in `style.css`. Beige is a palette colour used as a rule; the change is not recorded anywhere.

Decision needed from the owner: accept the product-art variance, or regenerate the affected images against canonical Part D art. Until then these files should not go to a public deploy.

## Addendum — root cause and a missing logo band (30 Oct 2026, later)

Checked against the pre-replacement files preserved in `originals/`:

- The amber bottles, the pump-less Conditioner (scenes) and the cream Conditioner and clipped second card (social) are **already present in the pre-28 Oct originals** (`originals/family.webp`, `originals/social-before-v03-crop.png`). The 28 Oct outpaint extended those scenes; it did not introduce the variance. Re-running an outpaint on the same reference image will reproduce it, because the existing prompts keep the reference pixels unchanged. The fix needs new base scenes built from the canonical product images.
- **New finding, V03:** the previous social image carried the GEM logo lockup band along the bottom. The approved V03 crop (`3f2fd71a…`) removes the footer and has **no GEM logo**; only the on-bottle wordmarks remain. A share card with no logo lockup is a brand regression against M8-05. The Nano Banana prompt for V03 reserves a 92 px band "for a branded lockup added later"; that overlay was not applied.

Owner decision of 30 Oct 2026 (given in session, no signed record): regenerate the affected images. See `REGENERATION-BRIEF-20261030.md`.
