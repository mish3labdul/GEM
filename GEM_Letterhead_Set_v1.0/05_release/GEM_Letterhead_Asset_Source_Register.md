# GEM™ Letterhead Asset Source Register

**GEM™ Branded Letterhead Set v1.0 — WORKING APPLICATION / PENDING VALIDATION**  
Repository: `mish3labdul/GEM` · source commit `334744c72dbbb6681034996fcca595213a7623a2` · inspected 2026-10-07 (Asia/Riyadh).

## Authority and interpretation

1. `GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx` wins every conflict. Its approved decisions govern identity; its evidence statuses remain open.
2. `GEM_V3_RC2/04_release/GEM Brand Guidelines V3.0 — Part A — RC2.pptx` and review PDF govern the visual application. Slides 6–10 support the four principles; 26–29 logo rules; 33–38 colour/type/localization; 67 letterhead concept.
3. `PartB_RC2/05_release/GEM Digital Design System V3.0 — Part B — RC2.pptx` and PDF, plus `PartB_RC2/05_release/tokens/`, govern type implementation, accessibility and RTL.
4. `GEM_V3_RC2/04_release/GEM Production Standards V3.0 — Part C — RC2.pptx` and review PDF govern prepress and release. Slides 5, 19–21 and 44 are the stationery production controls.
5. `Amenities_Portfolio_PartD_RC2/README.md`, `04_release/` and `01_mockups/` are owner-designated concept references. The reference PDF hospitality expression and mockup register were inspected; no packaging dimensions, claims, material values or mockup photographs are reused in the letterheads.
6. `GEM_Brand_Assets_v1.0/README.md`, `04_official_kit/` and `05_layout_matched/` were inspected. Layout-matched assets preserve deck boxes and are unnecessary for this fresh A4 application; official kit files are used.
7. `qa/` and `GEM_V3_RC2/03_qa/` were checked, especially the verified-change, final open-evidence, visual, Part B accessibility and RTL reports. Current reports do not authorize stationery or close register gates.

`00_source/source_manifest.json` records paths and hashes. No supplied source file was modified. The External Partners Brief was not used for wording, design, layout, positioning or rules.

## Reused artwork

| Repository path | Filename | Type | Colour | Usage | Vector/raster | Status / unresolved gate |
|---|---|---|---|---|---|---|
| `GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal/svg/gem-horizontal-ink.svg` | `gem-horizontal-ink.svg` | Horizontal lockup | INK | First pages / Executive; header | Vector SVG | Owner-supplied working asset; production-master acceptance PENDING; VAL-02, VAL-03, VAL-04, H21 / AC07 remain open. |
| `GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal/png/gem-horizontal-ink-2048.png` | `gem-horizontal-ink-2048.png` | Horizontal lockup | INK | First pages / Executive; header | Raster PNG fallback | Owner-supplied working asset; production-master acceptance PENDING; VAL-02, VAL-03, VAL-04, H21 / AC07 remain open. |
| `GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal/svg/gem-horizontal-black.svg` | `gem-horizontal-black.svg` | Horizontal lockup | BLACK | Minimal; header | Vector SVG | Owner-supplied working asset; production-master acceptance PENDING; VAL-02, VAL-03, VAL-04, H21 / AC07 remain open. |
| `GEM_Brand_Assets_v1.0/04_official_kit/logo/horizontal/png/gem-horizontal-black-2048.png` | `gem-horizontal-black-2048.png` | Horizontal lockup | BLACK | Minimal; header | Raster PNG fallback | Owner-supplied working asset; production-master acceptance PENDING; VAL-02, VAL-03, VAL-04, H21 / AC07 remain open. |

Each SVG is embedded byte-for-byte; all four files match the kit SHA256SUMS. PNG is the unchanged compatibility fallback. Both PDF portfolios contain vector logo paths, not bitmap logo XObjects. No logo was redrawn, traced, recoloured, mirrored, distorted or built from text. Continuation identifiers use the brand name GEM™ as text, not a recreated logo. No extra spark is added.

`GEM_Brand_Assets_v1.0/04_official_kit/logo/metrics.json` supplies the horizontal u and viewBox measurements. It is copied unchanged to `00_source/reused_assets/metrics.json` and is measurement data, not artwork.

## Type assets

No TTF/OTF/WOFF font binaries were present in this repository snapshot. The approved family names are retained; no replacement family is used. Official Google Fonts sources were obtained for these working builds, with OFL text and metadata archived. This does not freeze or approve the RC2 deployment build (L06 / VAL-05 / VAL-19 / Y03 remain open).

| Font | External source | Usage | Type / colour | Status |
|---|---|---|---|---|
| Jost | `https://github.com/google/fonts/tree/2c605eeda2de57af2b34822b79986f5140299862/ofl/jost` | Subject, tagline, continuation identifier | TrueType outlines; Ink | Working rendering build; not RC2 approved build. |
| Inter | `https://github.com/google/fonts/tree/2c605eeda2de57af2b34822b79986f5140299862/ofl/inter` | English body, metadata, footer, LTR IDs | TrueType outlines; Ink | Working rendering build; not RC2 approved build. |
| Noto Sans Arabic | `https://github.com/google/fonts/tree/2c605eeda2de57af2b34822b79986f5140299862/ofl/notosansarabic` | Arabic working copy and placeholders | TrueType outlines; Ink | Working rendering build; not RC2 approved build. |

The original variable files, OFL.txt and METADATA.pb are retained under `00_source/fonts/`. Regular (400) and Bold (700) full static instances were generated with FontTools; Inter optical size 14, all other axes at defaults. Names are normalized to family plus Regular/Bold; outlines remain font-derived. R1 embeds only the three Regular instances in DOCX as full obfuscated fonts and subsets them in PDF exports. Bold inputs are archived and unused. No glyph was drawn or replaced. Font hashes and versions are in `00_source/font_manifest.json`.

## Proposed application values

A4, margin and footer dimensions, 32/36 mm logo widths, body size, sequential bilingual letter structure and optional tagline placement are application choices for review. They are not presented as newly approved RC2 brand or supplier standards. The 1.6× Latin body leading, Regular 400 display/body use and primary tagline tracking implement existing RC2 rules; these values are not new application exceptions. S07 is explicitly scoped to wayfinding in the approval register; correspondence adoption remains PROPOSED / REQUIRES OWNER. No reference-number convention was found; only replaceable fields are used.

No confirmed address, contact, company registration/VAT numbers or requirement to print them was found in the current authoritative sources. CR/VAT are omitted. No commercial relationship, certification or regulatory number is invented.

## Review revision R1

Current repo main was refreshed and is still commit 334744c72dbbb6681034996fcca595213a7623a2. Reused artwork hashes are unchanged. Only the archived Regular 400 Jost/Inter/Noto Sans Arabic builds are active and embedded after review; 700 Bold inputs remain archived and are not used. No external font or new artwork source was introduced during this review. Master, font and localization evidence gates remain open. See 04_qa/GEM_Letterhead_QA_Report.md and GEM_Letterhead_Change_Log.md.
