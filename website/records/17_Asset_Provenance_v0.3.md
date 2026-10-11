# 17 · Asset provenance — v0.3

Supplements record 12. Status of every image: PROPOSED for website use, pending owner acceptance. No image was generated in this session.

## Added: website concept scenes (Part B Concepts group, revision 02)
Source: `website-assets-2026-10-10-02-branded/` (another agent's package, also carried in the design system and in `GEM_V3.0_RP01_Release_Artifact_Promotion/GEM_Website_Concept_Assets_20261010_02_Branded.zip`). Masters and exports were copied into `source-images/concept-r02/` (with the package's register, evidence and verification). **28/28 files match the SHA-256 values in the design system's `ASSET_REGISTER.csv`.** The site uses the 480/800/1200 exports unchanged. Generation: built-in ImageGen with the Part D images as references (package `evidence/*-generation.json`). Status in the register: PROPOSED / GENERATED CONCEPT / NOT PRODUCTION PHOTOGRAPHY.

| ID | Master SHA-256 (first 16) | Placement | Alt (register) |
|---|---|---|---|
| GEM-WEB-B01 amenity-family | ff07f001fed50521 | #amenities, beside the pilot-family list | Five GEM-branded amber and ivory pump bottles on a warm stone surface. |
| GEM-WEB-B02 packaging-study | 2cf20be3c9fc8d68 | #amenities › Concept applications | An open ivory GEM amenity box with five travel bottles and a branded lid. |
| GEM-WEB-B03 material-study | bf6c1827ed83ba28 | #approach | Close view of textured ivory GEM packaging, a debossed arc and contrasting dark material. |
| GEM-WEB-B04 guest-arrangement | adbb31cdd790f71a | #clients | GEM-branded bottles and guest stationery arranged on warm stone beside a white towel. |

**Inspection this session** (full masters and 100% crops): no geometry, texture, edge or text-garbling defects. Points that matter on a public site:
- **B02:** the lid reads "Amenities Collection". This is not an approved tier name; the caption says so.
- **B03:** the debossed wordmark has no ™.
- **B01/B04:** the hand-wash bottle is amber in B01 and ivory in B04. Colourway per product is [REQUIRES OWNER].
- **All four:** the rendered "GEM" lettering and ticked arcs are generated interpretations, not kit artwork, and must never be extracted.

## Added: label study (Part D slide 5)
| Web derivatives | Original | SHA-256 | Use | Alt (written this session, PROPOSED) |
|---|---|---|---|---|
| `label-study-{480,800,1200}.{webp,jpg}`, 3:2, no crop | `source-images/partD-s05-shampoo-stone_1536x1024.png`, from the connected Image-Assets folder (`slide-05_1536x1024_1689ccef.png`) | 1689ccef7a5a34938f625de5f3867658a20302e4138e9ae387af2c4ecbbc88f1 | reference.html › Label order | Concept image: an amber GEM shampoo bottle on a stone ledge. Its dark label reads GEM, then a short rule, then Shampoo in English with the Arabic name beneath, then an open field above a cropped ring. |

Covered by WD-06 ("yes show them"). The in-image Arabic (شامبو) is pixels: it is PENDING LOCALIZATION APPROVAL, and the caption says so. Derivatives were made with Pillow (LANCZOS; WebP q82, JPEG q84 progressive), which drops the original's C2PA manifest, as in v0.2.

## Image-Assets folder: full disposition
| File | Same as | Decision |
|---|---|---|
| partD-s07/s13/s16/s17/s19/s20, partA-s11, slide-07 (1024×1536), slide-13/16/17/19/20 | Hash-identical to v0.2 sources | Already in use or retired (see below) |
| slide-05 shampoo on stone | — | **Added** (label study) |
| slide-06 conditioner on stone | — | Not used: the same composition as slide 5; one is enough |
| slide-01, slide-04 ×4: studio cut-outs | — | Not used: B01 shows the family better; these are transparent cut-outs without context |
| slide-07 (1312×1199): 5L refill | — | Not used: it shows "5L ℮", a placeholder quantity and regulatory mark (card 13) that would read as a specification |
| slide-03: four-bottle counter | — | Still rejected (record 12): labels lack ™ |

## Retired from `site/` (kept in `records/retired-site-assets/`)
- `finish-*`: B03 now carries the material message on the homepage.
- `bespoke-box-*`: B02 shows the same subject, in English.
- `room-set-1536.*`: the room set moved to the reference page, where 1200px is the largest needed.

On the owner's Mac these files were moved, not deleted, because the Mac shell has no delete permission.
