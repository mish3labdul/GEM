# 04 · D3B — X12 STREAM Token: BRAND vs Logo

**Outcome: OWNER DECISION REQUIRED.** The evidence does not clearly establish either token as the one consistent with the existing X12 taxonomy. No recommendation is made. Nothing was renamed; no asset-ID or checksum rule was invented.

## The pattern and where STREAM is (not) defined
Register X12 (Approved): `GEM_[STREAM]_[ASSET]_[VARIANT]_vX.Y_YYYYMMDD.ext` — a shape only. **No STREAM values are listed anywhere in the Register.** Part C slide 56 adds: underscores separate fields, no spaces, "Latin letters and digits only", no "final/new/copy". Part A slide 75 adds: "A name should say what it is", "The stream field follows the asset library folder", and one example: `GEM_Logo_Horizontal_Black_v3.0_20261006.svg`.

## Answers to the eight questions
1. **What does STREAM mean in X12?** The only definition in the authority set is Part A slide 75: the stream field "follows the asset library folder". The folders are defined by Register X02–X11: 01 Brand Masters · 02 Type & Color · 03 Imagery · 04 Motion · 05 Applications · 06 Packaging · 07 Digital · 08 Localization · 09 Governance · 10 Archive. The folder-to-token spelling is **not** defined.
2. **Business/document stream, asset class, or another taxonomy?** Two readings coexist and are not reconciled. (a) *Library folder*: Part A slide 75. (b) *Business stream*: the Register uses "stream" for business streams (C03 Amenities & Packaging is "a business-stream descriptor"; C06 future streams only by formal architecture approval; C07 streams inherit GEM identity; C11/C12 descriptors are not locked into the logo and use ordinary typography). Under (b) the master brand has no business stream at all. Under neither reading is "asset class" the stated meaning, although the Part A example uses an asset-class word.
3. **How are other STREAM values formed?** No other STREAM value is defined. The only X12-shaped names in the repository are the 11 working files in `GEM_Brand_Assets_v1.0/01_svg`, all `GEM_BRAND_<ASSET>_<VARIANT>_v0.1_20261006.svg` (ASSET = TAGLINE, STATUS-LABEL, PALETTE-SHEET, STREAM-LINE). The kit README calls BRAND "a working choice for the owner to confirm".
4. **Does BRAND match that taxonomy?** Under reading (a), yes in kind: logos sit in 01 Brand Masters and BRAND is a plausible short form (spelling unconfirmed). Under (b), BRAND names the master brand, which is not a business stream. It contradicts the Part A example string.
5. **Does Logo match that taxonomy?** Under reading (a), no: there is no Logo folder. Under (b), no. It matches the Part A example exactly. It names an asset class, which is the job of the ASSET field, and "Logo" is a likely CATEGORY value in Part C Appendix N (the category list is not defined).
6. **Semantic collision with ASSET?** Not with ASSET=Horizontal/Stacked/Symbol/SymbolNoSpark (both options, 128/128 names unique, 0 collisions with the 11 working names). If ASSET carried the noun "Logo" (to keep names self-describing under BRAND), `Logo` as STREAM would repeat it in **128 of 128** names; `BRAND` would not (**0**).
7. **Which gives clearer examples** across horizontal / stacked / symbol / no-spark × Ink/Beige/Black/White? With ASSET held constant, `Logo` reads as self-describing (`GEM_Logo_Horizontal_Black…`); `BRAND` leaves "logo" implicit (`GEM_BRAND_Horizontal_Black…`) unless ASSET carries it (`GEM_BRAND_LogoHorizontal_Black…`). Examples below.
8. **Does either contradict existing controlled naming?** BRAND contradicts the Part A example. Logo contradicts the Part A folder rule on the same slide and would sit beside 11 BRAND-streamed working files in the same library folder, giving two STREAM values for one folder.

## Examples (same assets, exact pattern; vX.Y and YYYYMMDD stay placeholders)
| Source file (unchanged) | If STREAM = BRAND | If STREAM = Logo |
|---|---|---|
| `gem-horizontal-black.svg` | `GEM_BRAND_Horizontal_Black_vX.Y_YYYYMMDD.svg` | `GEM_Logo_Horizontal_Black_vX.Y_YYYYMMDD.svg` |
| `gem-stacked-ink.pdf` | `GEM_BRAND_Stacked_Ink_vX.Y_YYYYMMDD.pdf` | `GEM_Logo_Stacked_Ink_vX.Y_YYYYMMDD.pdf` |
| `gem-symbol-beige.eps` | `GEM_BRAND_Symbol_Beige_vX.Y_YYYYMMDD.eps` | `GEM_Logo_Symbol_Beige_vX.Y_YYYYMMDD.eps` |
| `gem-symbol-nospark-white-1024.png` | `GEM_BRAND_SymbolNoSpark_White1024_vX.Y_YYYYMMDD.png` | `GEM_Logo_SymbolNoSpark_White1024_vX.Y_YYYYMMDD.png` |
| `gem-horizontal-ink-clearspace-2u.svg` | `GEM_BRAND_Horizontal_InkClearspace2u_vX.Y_YYYYMMDD.svg` | `GEM_Logo_Horizontal_InkClearspace2u_vX.Y_YYYYMMDD.svg` |
| `gem-symbol-nospark-black.svg` | `GEM_BRAND_SymbolNoSpark_Black_vX.Y_YYYYMMDD.svg` | `GEM_Logo_SymbolNoSpark_Black_vX.Y_YYYYMMDD.svg` |

Full mappings: `05_D3B_X12_BRAND_Mapping.csv`, `06_D3B_X12_Logo_Mapping.csv` — 128 logo files each (Horizontal 32, Stacked 32, Symbol 32, SymbolNoSpark 32; SVG 32, EPS 16, PDF 16, PNG 64) plus `metrics.json` marked "not mapped". ASSET and VARIANT values are held identical in both files so only STREAM differs.

Assumptions (labelled A1–A4 in the CSVs; **none is a naming rule**): ASSET = the kit's shape word in the Title-case style of the Part A example; VARIANT = colour word plus the kit's own qualifiers (2u clearspace, pixel size) appended, because the pattern has one VARIANT field and Part C allows letters and digits only; `vX.Y` and `YYYYMMDD` left as placeholders (version and manifest issue date undecided); extension as in the source.

## Semantic test (`07_D3B_X12_Semantic_Test.csv`, 13 criteria)
BRAND wins 6 · Logo wins 2 · Indeterminate 3 · Neither 2 (computed identical for both). The BRAND wins are on taxonomy-fit, scalability and grouping, mostly MODERATE or WEAK; the Logo wins are the exact match to the Part A example and name readability, both MODERATE. The criteria that carry authority (1 definition, 2 worked example, 3 internal consistency, 13 contradiction) point in **opposite directions** or are INDETERMINATE.

## Decision rule applied
"If the evidence clearly establishes one option as consistent with the existing X12 taxonomy: recommend it. If genuinely ambiguous: do not choose." The evidence is genuinely ambiguous:
1. Part A slide 75 gives a rule (stream = library folder) and an example (`Logo`) that cannot both hold; the Register defines no values.
2. Even if the folder rule governs, the folder-to-token spelling is undefined, so the folder rule supports "something derived from Brand Masters", not BRAND specifically.
3. The tally is not authority: the extra BRAND wins are design-quality criteria, not governing text.

## What the owner needs to decide (three short questions)
1. Is STREAM the asset-library folder (rule) or an asset class (example)?
2. If the folder: which token spells "01 Brand Masters" (BRAND, or another)? If an asset class: how do non-logo master-brand assets (tagline, palette sheet, status labels, stream lines) get a STREAM?
3. Which Part A slide 75 sentence is then corrected: the example, or the folder rule?

Consequences of each choice for other documents: `08`. Owner record: `09`.
