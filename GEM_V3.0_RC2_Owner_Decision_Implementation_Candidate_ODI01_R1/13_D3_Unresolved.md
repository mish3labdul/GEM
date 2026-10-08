# 13 · D3 Unresolved (D3A sync corrections and D3B X12 STREAM token)

**No STREAM token is chosen. No recommendation is made**, because the governing text does not clearly support one. No source file is renamed. Both full mappings (34 official-kit SVGs each) are in `19_candidate_documents/d3a_carried_forward/x12_mapping_option_A_BRAND.csv` and `x12_mapping_option_B_Logo.csv`.

## What the authorities say
- **Register X12 (Approved):** `GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext`. It does not define the allowed STREAM values.
- **Part C slide 7:** "Controlled names follow X12 at first manifest (VAL-16); files are renamed, never redrawn." **Kit README:** kit names (`gem-horizontal-black.svg`) do not follow X12; rename at first manifest; "the `BRAND` stream code in `01_svg` names is a working choice for the owner to confirm."
- **Part A slide 75:** example `GEM_Logo_Horizontal_Black_v3.0_20261006.svg` — stream written "Logo", mixed case, version v3.0.
- The 11 working SVGs already in `GEM_Brand_Assets_v1.0/01_svg` use `GEM_BRAND_…_v0.1_20261006.svg` (palette sheet, status labels, stream line, tagline lockups). VAL-16 (controlled manifest) has not started.

## The two mappings
| | Option A — STREAM = `BRAND` | Option B — STREAM = `Logo` |
|---|---|---|
| Example (horizontal black) | `GEM_BRAND_HORIZONTAL_BLACK_v[X.Y]_[YYYYMMDD].svg` | `GEM_Logo_Horizontal_Black_v[X.Y]_[YYYYMMDD].svg` |
| Case convention | UPPER, as the 11 existing X12-shaped files | Title Case, as the Part A slide-75 example |
| Collision risk | None among the 34 (34 unique, case-insensitively unique); none against the 11 existing files | None among the 34 (34 unique, case-insensitively unique); none against the 11 existing files. Note: case-only differences from Option A would collide on case-insensitive file systems if both styles ever coexisted in one folder |
| Semantic clarity | "BRAND" is a generic family name; it does not say the asset is a logo, but ASSET/VARIANT do. Matches how the 11 non-logo working files (palette, status labels, tagline) are already named | "Logo" describes the 34 kit files exactly, but is **wrong** for the 11 existing non-logo working files (palette sheet, status labels, tagline, stream line): they would need a second stream token, so a manifest would mix two STREAM tokens |
| Compatibility with Register wording | `[STREAM]` normally reads as a business stream (Part A: Amenities & Packaging is "the descriptive stream under one master brand"). "BRAND" is not a business stream either; it is a working token the README asks the owner to confirm | Same issue: "Logo" is an asset class, not a stream. It does match the only worked example in the decks |
| Manifest effect | One STREAM token for all 45 assets (34 kit + 11 working); simplest manifest | 34 kit assets under `Logo`; the 11 working assets need another token (or `BRAND`), i.e. two tokens |
| Source-file impact | None until VAL-16: sources keep working names; names exist only in the manifest | Same |
| Longest generated name | 66 characters | 65 characters |

## Observation, not a recommendation
Because the Register's own vocabulary uses "stream" for business streams, a third reading (STREAM = a descriptive business stream such as Amenities & Packaging, with a master-brand token for GEM-wide assets) is also arguable. It was not requested and is not proposed here.

## What the owner must decide (D3B)
Choose the STREAM token (or define the permitted STREAM list), and whether the Part A slide-75 example is to be corrected to match or the manifest is to follow it. Until then: nothing renamed, no authority text changed, VAL-16 not started.

## R1
**D3 remains UNRESOLVED and was not implemented.** C1–C4 are not approved; the D3A candidate decks were not promoted to authoritative originals and were not re-copied (their AFC02 decks and PDFs, ~12 MB, stay in the ODI01 package; their release-language text and the two X12 mappings are carried in `19_candidate_documents/d3a_carried_forward/`). BRAND vs Logo for X12 was not chosen; no asset was renamed; no X12 mapping was implemented.
