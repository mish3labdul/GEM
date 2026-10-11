# 06 · Asset provenance

All assets are used unchanged except for resizing and cropping of raster images. Status of every image: **PROPOSED for web use, pending owner acceptance and the image-rights register (VAL-06).** No images were generated in this session: no image-generation tool was available.

## Brand artwork (copied byte-for-byte from the kit; verified against `04_official_kit/SHA256SUMS.txt`, 8/8 OK)
| Site path | Kit source | Use |
|---|---|---|
| `assets/brand/gem-horizontal-beige.svg` | `logo/horizontal/svg/gem-horizontal-beige.svg` | Header (150 px desktop / 132 px mobile, ≥120 px minimum) and footer (180 px), Beige on Ink |
| `assets/brand/gem-horizontal-ink.svg`, `gem-horizontal-white.svg` | same folder | Shipped for later light/inverse placements; not yet used |
| `assets/brand/gem-symbol-beige.svg` | `logo/symbol/svg/gem-symbol-beige.svg` | Hero reveal, up to 440 px |
| `favicon.svg`, `favicon.ico`, `favicon-32.png`, `apple-touch-icon-180.png` | `icons/` | Browser icons |

Kit status: WORKING ASSETS, production-master acceptance PENDING (VAL-02); external issue RESTRICTED per RP01. **Public use needs owner acceptance.**

## Fonts
| File | Source | Licence | Notes |
|---|---|---|---|
| `jost-latin-400-normal.woff2` | npm `@fontsource/jost@5.3.0` (Jost 3.710) | SIL OFL 1.1 (`OFL-Jost.txt` shipped) | Static 400; 221 glyphs; covers Latin, ™, ©, dashes, curly quotes |
| `inter-latin-400-normal.woff2` | npm `@fontsource/inter@5.3.0` (Inter 4.001) | SIL OFL 1.1 (`OFL-Inter.txt` shipped) | Static 400; 230 glyphs; same coverage |
Not covered by either: "→" (not used). Part C slide 15 still lists the approved font source and build as PENDING (VAL-05); these builds need recording there.

## Images
| Web derivatives | Original (kept in `source-images/`, not public) | SHA-256 of original | Source location and label | Crop | Alt text |
|---|---|---|---|---|---|
| `finish-480/800.{webp,jpg}` (4:5) | `partD-s17-finish_1536x1024_8c851e0f.png` | 8c851e0f18075efb7fbd7aa462c09201bbbe9e86a41f21b55b38f447484ee1e2 | Part D slide 17 "Finish direction", CONCEPT / NOT PRODUCTION PHOTOGRAPHY; matches repo `MOCKUP_REGISTER.csv` | x 560–1379 | A white board box with a single ring debossed into its lid, resting on dark textured card. |
| `materials-480/800/1200.{webp,jpg}` (3:2) | `partD-s16-materials_1536x1024_b38b813d.png` | b38b813dee1a39066c0d79c92466c580e153fc1e66c84a6d390e78e83a33a989 | Part D slide 16 "Material direction", same label; matches mockup register | none | Layered sheets of warm white, black and beige uncoated card; the top sheet carries a debossed ring. |
| `threshold-480/800.{webp,jpg}` (4:5) | `partA-s11-space-threshold_1600x1000.jpeg` | 9e2cd4df2cccb0af02eae9a648346ded7fa56c7e187a0d164a814c0f1d2c50b8 | Part A slide 11 "Space is part of the identity", REFERENCE · CONCEPT / NOT PRODUCTION PHOTOGRAPHY | x 400–1200 | A tall pale opening of light in a dark room, its glow falling across the floor. |

All three are rendered studies (the prior audit records Part A images as "rendered studies"); none shows a GEM logo, text, product, property or person, so none implies a real product, property or completed project. Each carries a visible "Concept/Reference study, not production photography" caption. Origin of the renders (tool, author, rights) is not recorded in any source. VAL-06 is formally deferred as owner risk under FD01/FA01, not verified. Alt text is proposed; OD-G03 requires approval by the Accessibility Content Owner (Mashal).

## Considered and excluded
| Asset | Reason |
|---|---|
| Part D bottle, dispenser, refill, box, lineup, welcome-card mockups (13 images) | Baked-in Arabic (D8 restriction; Arabic not approved), a rendered "GEM™" wordmark that is not the kit lockup, and an unapproved collection name ("Amenities Collection") on the box. Owner decision requested. |
| Part A slide 48 abstract studies | Low information; one shows a decorative shadow, which Part B excludes |
| Kit motion study `gem-reveal.html` | Uses a brightness flash and an infinite pulse loop; Part B prohibits autoplay loops. The site implements its own reveal from the unchanged symbol SVG instead |
