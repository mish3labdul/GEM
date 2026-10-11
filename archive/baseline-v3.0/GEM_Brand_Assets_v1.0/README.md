# GEM™ Brand Assets

**Status: WORKING ASSETS. Vector logo kit received from the project owner; acceptance as production master is PENDING (VAL-02, VAL-03, VAL-04, H21).**

| Folder | Content |
|---|---|
| `04_official_kit` | The supplied master kit, unchanged: logo (horizontal, stacked, symbol, no-spark symbol in ink, beige, black, white; SVG, PDF, EPS, PNG, 2u clearspace, `metrics.json`), icons (favicon, apple-touch, android, maskable, mstile, avatars), motion reveal. Hashes in `SHA256SUMS.txt`. |
| `05_layout_matched` | The kit lockups and symbols fitted to the box of the old 654 × 207 and 229 × 207 rasters, so decks keep their layout. Only the SVG `viewBox` differs from the kit; no path is edited. PNG fallbacks at 4 to 8 times the old resolution. |
| `01_svg` | Created from the specification: outlined tagline (4 colourways), "Amenities & Packaging" descriptive line (2), palette sheet, four status labels. |
| `02_build` | `sync_logos.py` (swap rasters in PPTX for kit SVG), `build_assets.py` (the `01_svg` set). |

## Rules kept
Logos are used unchanged: never redrawn, traced, recoloured, mirrored or set in type. Minimum 120 px lockup, 32 px symbol; below 32 px use the no-spark symbol. Clearspace u = G-ring radius, 1u minimum, 2u preferred.

## Open
- Kit file names (`gem-horizontal-black.svg`) do not follow X12; rename at first manifest (VAL-16). The `BRAND` stream code in `01_svg` names is a working choice for the owner to confirm.
- Not supplied: embroidery and engraving masters; print colour values (Pantone, CMYK).
- Brand Owner acceptance of the kit as production master, and master artwork ID and version.
