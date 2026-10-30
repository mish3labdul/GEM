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
