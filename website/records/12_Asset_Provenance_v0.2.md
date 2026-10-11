# 12 · Asset provenance — v0.2

Supplements record 06 (kept as v0.1 history). Owner decisions WD-04, WD-05, WD-06, WD-10 apply (record 10). Assets are used unchanged apart from resizing and the crops listed. No new images were generated.

## New in v0.2: Part D concept mockups
Each original was extracted from the RP01 Part D deck (`GEM_BRAND_AmenitiesPackagingConcept_PartD_v3.0_20261009.pptx`), and its SHA-256 matches the slide entry in the repository's `Amenities_Portfolio_PartD_RC2/01_mockups/MOCKUP_REGISTER.csv`. Originals are in `source-images/` (not public).

| Web derivatives | Original | SHA-256 | Part D slide / label | Crop | Alt text (HR01-approved, item) |
|---|---|---|---|---|---|
| `room-set-{800,1200,1536}.{webp,jpg}` 16:9 | `partD-s20-room-set_1536x1024.png` | 0f85f9d1a75828faa445fd6b8e20288122f08f0abdc7242f5602e9eb91ee6b37 | 20 · CONCEPT / NOT PRODUCTION PHOTOGRAPHY | y 90–954 (keeps all five bottles, tray, towel, card) | A23 |
| `wall-mounted-{480,800}.{webp,jpg}` 4:5 | `partD-s07-wall-mounted_1024x1536.png` | c4738363559c7b77f9b64d49e07d0991c469809db2bc1454a7d077a5ec306590 | 7 · wall-mounted concept · SUPPLIER PROOF REQUIRED | y 110–1390 (keeps bottle and bracket) | A15 |
| `bespoke-box-{480,800,1200}.{webp,jpg}` 3:2 | `partD-s13-bespoke-box_1536x1024.png` | 385ca6f245c3571fc0f31623715a1fff44d55742179fe8e5970ae4207413009d | 13 · CONDITIONAL · STRUCTURAL CONCEPT · SUPPLIER PROOF REQUIRED | none | A21 |
| `arrival-{480,800,1200}.{webp,jpg}` 3:2 | `partD-s19-arrival_1536x1024.png` | 1b9bb8d732757fc1c0ab493e1b33cc9e3eeae0235cb47d39af5c6fd9240321d3 | 19 · CONCEPT / NOT PRODUCTION PHOTOGRAPHY | none | A22 |

**Inspection of these outputs (this session):** no geometry, texture or edge defects at full size. Things that would matter for a public site, and which the owner accepted under WD-06:
- **Arabic in the pixels:** product names, the welcome line and the box's collection name. Linguistic review was done in HR01 for the deck; the in-image Arabic is not live text.
- **Wordmark:** the renders show a typeset "GEM™" wordmark, not the kit lockup.
- **Collection name:** the box lid reads "Amenities Collection", which is not an approved name.
- **Ticked arc:** the labels' arc with tick marks is not one of the four documented forms.

Captions on the page state concept status beside every image.

## Embedded provenance found
The four Part D originals (and, by the same check, the deck media they came from) contain C2PA manifests (`jumb`/`c2pa` boxes), consistent with generation by an image model that records Content Credentials. The website derivatives were re-encoded with Pillow, which does not carry that manifest forward. If GEM wants the public images to carry Content Credentials, that needs a deliberate signing step; it is an owner choice, not done here.

## Rejected candidates from Part D
| Image | Reason |
|---|---|
| Slide 7 refill container (image12) | Jagged cut-out artifacts at the top edge |
| Slides 4, 8, 9 white bottles on black (image7, image8) | Artificial glow (Part A slide 49 "don't") |
| Slide 3 four-bottle counter (image4) | Labels lack ™, inconsistent with the other renders; the room set covers the same content |

## Provenance note on the session-1 studies
HR01 (`05_HR01_Accessibility_Content_Register.csv`, X01/X02) records that the materials and finish pictures previously carried "AI-generated … concept" alt text. They are therefore AI-generated renders, consistent with their "Concept study" captions. Rights stay owner risk (WD-05), not a rights register.

## Removed from the homepage
- `materials-*` moved to `reference.html` (Imagery).
- The hero no longer uses a second masked copy of the symbol. The single kit SVG is shown at rest.

## Unchanged
Kit artwork (4 SVG + 4 icons) and token CSS: bytes unchanged from session 1 (hashes in the correction report). Fonts: Jost 3.710 / Inter 4.001, weight 400, SIL OFL 1.1.
