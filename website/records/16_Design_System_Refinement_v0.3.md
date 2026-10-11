# 16 · Design-system refinement — v0.3 (session 3, 2026-10-10)

**Request:** "Refine the website according to the attached design system, add image assets accordingly as well."
**Design system read:** GEM™ Digital Design System V3.0 (Part B, GEM-DDS-V3.0, semantic version 3.0.0), Claude Design System artifact, version `1791637647-0c6b`. Cards read: README, 01 governance, 02 foundations, 03 typography, 05 layout, 06 accessibility, 07 motion, 09 UX writing, 11 components, 12 hospitality patterns, 13 Amenities & Packaging, 14 imagery, 16 engineering, the Concepts, Packaging, Imagery and Elements asset READMEs, `Concepts/ASSET_REGISTER.csv`, and the component cards for StatusLabel, Button, Field, Select, Textarea, RadioGroup, Navigation, Link, Alert, WebsiteConcepts and PackagingConcepts (plus `components/bundle.css` as the reference harness). `tokens.json` and `index.d.ts` were not opened.
**Starting state:** the Mac copy matched the v0.2 tested run `20261010T124726Z` (56/56 site files).
**Token file:** the system's `assets/Tokens/gem-tokens.v3.0.css` has the same SHA-256 as the site's copy (`0c9dfce3…5851`), so no token values changed. This refinement is about how the site *uses* the tokens and components.
**Status:** every change below is PROPOSED pending owner acceptance. Part B is a specification; this is a site implementation of it, not an authorized component library (VAL-13 open).

## What changed, by Part B card

| Card | Before (v0.2) | Now (v0.3) |
|---|---|---|
| 03 Typography | Off-scale sizes: lead/body-large 18/30, h2 28/36 and h3 20/28 on small screens, h4 20/28, compact nav 18px, specimens 40 and 18, word lists 20/32 | Only token sizes: body 16/26 everywhere, h2 32/40, h3/h4 24/32, nav label 16/24. h1 keeps a 40/48 step-down below 720px (mirrors the documented display step-down). Alert titles 18/26 as in the reference harness. A new QA check allows only {12, 13, 14, 16, 18, 24, 32, 40, 48} px. |
| StatusLabel | Radius 4px, 22px line height, no Approved / Conditional / Reference forms | labelSmall 12/16 capitals, square corners, word first. Approved = filled Ink; Conditional = 2px outline; Pending = dashed 2px; Reference = dotted 2px. "Being defined" programmes now use the Conditional form (tiers are CONDITIONAL in card 13). The reference page shows real specimens. |
| 14 Imagery / WebsiteConcepts | Mixed crops | Generated scenes and the label study keep the full 3:2 frame (`object-fit: contain` in a 3:2 box: no crop possible). Products 4:5, bands 16:9. Every image sits in a figure whose caption starts with its status label. |
| Field / Select / Textarea | Two-up rows; error above the input; gradient-drawn select chevron; textarea without a minimum height | One column; fields up to 420px; order is label → control → help → error; native select (the gradient chevron is gone: no gradients); textarea at least 120px; 2px border on focus and on error; error text uses the error-text token. The message field gained help text. Help stays in `aria-describedby` when an error is added or cleared (`site.js`). |
| RadioGroup | 20px native radio | 24px circle with a 2px Ink ring and a 12px Ink dot; the whole 44px label row is the target. Forced colours keep the dot. |
| Button | Secondary hover filled Ink; outline button on Ink hovered White | Secondary has a canvas fill and hovers Beige; on Ink, the outline button hovers Beige. Primary hover stays Black. |
| Link | Underline offset 0.2em | Offset 4px; underline thickens to 2px on hover. |
| Navigation | Hover underline from text decoration | 2px underline (border) on hover and on `aria-current`; footer links carry `aria-current="page"` on the reference and privacy pages. |
| Alert | No width limit | Error summary, prepared result and notices are capped at 560px, with 16/24 padding. |
| 02 Foundations | Raw `rgba()` hairlines in navigation, sequence list and footer; hero bottom padding 128px | Beige decorative border token; hero padding 96px (space-24). Inline `style` attributes moved into classes. |

## Image assets added (details: record 17)
- **GEM-WEB-B01–B04** from the system's Concepts group (revision 02), placed where the register proposes: B03 material study in #approach, B01 amenity family beside the pilot-family list, B02 packaging study in Concept applications, B04 guest arrangement in #clients. The 480/800/1200 WebP and JPEG exports are used byte for byte: 28/28 files match `ASSET_REGISTER.csv`. Alt text and caption sentences come from the register.
- **Label study** (Part D slide 5, shampoo on stone) from the connected Image-Assets folder, added to the reference page under Label order.
- **Moved or retired:** the room set moved from the homepage to Reference › Imagery as the 16:9 band. The finish study (replaced by B03) and the bespoke box (replaced by B02, same subject) were removed from `site/`, together with the unused room-set 1536 derivatives. They are kept in `records/retired-site-assets/`; their originals stay in `source-images/`.

## New or changed visitor copy (PROPOSED)
| Where | Text |
|---|---|
| Amenities status note | "Every image in this section is a generated concept or concept render. None shows production photography, an available product or a real property." |
| Caption titles | "Material before decoration." · "One family, held together." · "Structure with restraint." · "Objects in quiet company." (titles from the asset register) · "Wall-mounted format." · "Arrival." · "Space to arrive." · "A 16:9 band." · "The order applied." |
| B02 caption | "A travel-set direction for a bespoke programme; the lid wording is illustrative, not an approved collection name." |
| Label study caption | "GEM first, then product and function, with the open field kept clear. The wordmark is rendered, not placed from the kit, and the Arabic is pending localization approval." |
| Message help | "For example: property type, the products you are considering, markets and timing." |
| Status labels | "Generated concept" · "Concept / not production artwork" · "Reference study" |

## Deliberate deviations from Part B (and why)
1. **The Prepare button stays natively `disabled` until the script is ready, instead of `aria-disabled`.** With `aria-disabled`, pressing Enter would submit the form when JavaScript is off (audit GEM-01). The reason is shown as a visible notice and linked to the button with `aria-describedby`. Once the script is running, the button is enabled.
2. **Field errors are not each `role="alert"`.** The error summary is the single alert, and focus moves to the first invalid field, as the Field card asks. Several simultaneous alerts would be announced on top of one another. Each error is linked to its field with `aria-describedby`.
3. **Visitor-facing status wording.** For generated scenes the label reads "Generated concept", not the register wording "PROPOSED / GENERATED CONCEPT / NOT PRODUCTION PHOTOGRAPHY". "Proposed" is internal approval language; the "not production photography" part is kept in the caption sentence, word for word. Part D renders use the register wording "Concept / not production artwork". The internal PROPOSED status is held in these records.
4. **"Being defined"** keeps the owner's wording (WD-07) and uses the Conditional visual form, rather than reading "CONDITIONAL".

## Not changed
Hero (identity-led, static mark: motion masters still pending, VAL-14), copy outside the table above, temporary contact details, the switched-off form destination, logo kit, fonts and token file.

## Verification
Run `records/qa-runs/20261010T132217Z`: **438 checks, 438 PASS**, comprising the 348 v0.2 checks and 90 new design-system checks (6 per page per width: type scale, full 3:2 frames, status-captioned images, fields ≤420px, 24px radios, square labels and images). Details: record 18.

## Before/after hashes (SHA-256, first 12)
| Path | v0.2 | v0.3 |
|---|---|---|
| site/index.html | ae1ac48c5f6f | 26bbd05cb829 |
| site/reference.html | 2a393d9ad8a3 | 6637c4a88987 |
| site/privacy.html | 6662e4668011 | e8a1fac38162 |
| site/assets/css/site.css | 89987a5e1ff8 | 38bf62fd2ba1 |
| site/assets/js/site.js | ed4bd5dfafcf | b13d2854799a |
| qa/run_qa.py | 5393c63e26c2 | 0072064c9797 |
| 30 image derivatives added, 12 removed | — | full list in `qa-runs/20261010T132217Z/environment.json` |
