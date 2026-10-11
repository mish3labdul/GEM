# GEM™ V3.0 RC2 — Asset Sync Change Log (vector logo kit and Part D)

Date: 2026-10-06. Inputs from the project owner: the master asset kit (`GEM_Brand_Assets_v1.0/04_official_kit`) and the owner-designated Part D concept portfolio (PDF and PPTX). Pre-sync copies of A, B and C are kept unchanged in `GEM_V3_RC2/00_originals/RC2_pre_asset_sync/` with hashes. Edit scripts: `GEM_V3_RC2/05_logs/edit_assets_A.py`, `edit_assets_BC.py`; logo mapping `GEM_Brand_Assets_v1.0/02_build/sync_logos.py`.

**No evidence gate was closed.** VAL-02 (production masters), VAL-03, VAL-04 and H21 (artwork ID and version) stay open until the Brand Owner records acceptance. Nothing is labelled APPROVED V3.0.

## What changed in every document
| Document | Change |
|---|---|
| A, C, D | Every low-resolution logo raster (654 × 207 lockups, 229 × 207 symbols; A 24, C 3, D 6 placements) replaced by the kit SVG, embedded as vector with a high-resolution PNG fallback. Same slide box, same colourway, same visible bounds. No path edited, no logo redrawn or traced. |
| A 1, 26 | Status wording: "logo shown from supplied raster, PENDING PRODUCTION MASTER" → vector kit, acceptance PENDING (VAL-02). |
| A 27 | Logo set slide rebuilt: stacked and no-spark artwork shown, vector files noted. Title and eyebrow no longer say "five artworks, rest not supplied". |
| A 28, 29 | Construction note and the no-spark rule now cite the supplied kit. |
| A 74, 78 | Brand Masters folder note and open item: kit received, acceptance pending. |
| B 1 (notes), 31, 35 | Production row and Assets slide now list kit file names and contents; the X12 naming pattern is kept. B has no logo pictures. |
| C 1, 3, 7, 10, 75 | Status, master register table ("KIT RECEIVED · ACCEPTANCE PENDING"), clearspace slide, gate list. Fabrication and embroidery masters remain not supplied. |
| D | Approved mockups kept unchanged and extracted to `Amenities_Portfolio_PartD_RC2/01_mockups` with a register. Status wording on slide 10 and in speaker notes updated. |
| Token package (B) | One description string for the below-32px mark. |
| PDFs | A, B, C and D re-exported with Jost and Inter embedded, tagged. Tag quality still not verified with assistive technology (VAL-15). |

## Checks
- Cross-document consistency script: 112 PASS, 0 FAIL.
- OOXML validation passed for A, B, C and D.
- Visual check of every changed slide in A, B, C and D.

## Known limits
- The kit's file names do not follow X12; renaming is scheduled for the first manifest (VAL-16).
- Mockups in D are the supplied photorealistic images. Product labels baked into those images (including Arabic strings) cannot be changed here and stay PENDING LOCALIZATION APPROVAL.
- The supplied Part D PDF was exported without Jost and Inter (Calibri fallback). The re-export uses the brand fonts. Page layout otherwise matches.
- The deck calls itself v1.0 WORKING EDITION inside a file named V3.0 Part D RC2. Left as authored; for the owner to confirm.
- Not placed in any document yet: favicon and app icons, avatars, the motion reveal, clearspace art.
