# M8 — brand presentation audit, 23 October 2026

**Status: audit complete. One defect fixed (M8-01) and two refinements accepted by the owner and shipped (M8-02, M8-03). One finding retracted (M8-06). M8-04 and M8-05 were taken forward by the owner on 23 Oct 2026 and are done. Gates L07 and L16 are closed.** M8's goal is one coherent GEM system across Arabic, English, phone and desktop. This record follows the roadmap's rule: preserve the accepted design, add no product facts, do not alter artwork or logo geometry, and ship only what the owner accepts.

## Method

All ten routes (five pages, two languages) captured from https://gem.mish3l.com at 390, 820 and 1440 px wide with Chromium and reduced motion, after scrolling the page so lazy images load. Home and Amenities were reviewed side by side in Arabic and English at desktop and phone width. Also checked: favicon rendering at 16, 32 and 64 px, the social preview image, page titles, headings and image alt text across all ten routes.

Limits: Chromium only, no physical devices, no native Arabic review, no Safari desktop. These are an engineering reviewer's observations; taste decisions belong to the owner.

## Verified as already consistent

- All ten routes load with one `h1` and a localized title; no image lacks an `alt` attribute (images with an empty `alt` are the decorative `tx-*` texture backgrounds).
- RTL mirroring is correct on every page: header, hero composition, product list order, arrows, footer.
- No horizontal overflow at 320, 375 or 1440 px (existing regression test).
- Phone layouts keep the same hierarchy as desktop; hero, cards and format images stack cleanly in both languages.

## Findings

| ID | Finding | Evidence | Action |
|---|---|---|---|
| M8-01 | **Defect.** On the Arabic Amenities page, the three format images (room, wall-mounted, travel) carried the English caption "Concept study; counts, materials, hardware and compatibility remain under review." A language check in `build.mjs` compared a cloned object to the original and was always false | [desktop](evidence/amenities-desktop-ar-en.jpg), [phone](evidence/amenities-mobile-ar-en-formats.jpg) | **Fixed** in this change: the Arabic wording that already existed in the code is now taken from `content.mjs` for each language; regression test added (Chromium and Firefox). Wording is unchanged and still needs native Arabic review |
| M8-02 | Format-image caption bars use a grey-mauve (`#BCACA7`) that sits cooler than the warm ivory and travertine tones around it; on desktop they read as heavy grey blocks under each image | [desktop](evidence/amenities-desktop-ar-en.jpg) | **Done.** Accepted by the owner. `.format-art` now uses the existing `--sand` band colour (`#EFE6D8`); no new colour. [after](evidence/after-amenities-desktop-ar-en.jpg) |
| M8-03 | Arabic body and lead text looks smaller than the English at the same nominal size (Arabic letterforms have a lower x-height). Most visible in hero intros and card text on desktop | [home](evidence/home-desktop-ar-en.jpg) | **Done.** Accepted by the owner. At 761 px and wider, Arabic body, card, caption, hint and disclosure text is 1 px larger; the Arabic hero intro scales 1 px larger at its widest. Phone sizes are unchanged. Measured: 16 to 17 px body, 15 to 16 px secondary, 12 to 13 px captions. Still needs a native reader's eye |
| M8-04 | The browser icon is the full GEM wordmark. At 16 and 32 px it is illegible, and on a dark tab bar the ink-coloured mark nearly disappears | [render](evidence/favicon-16-32-64.jpg) | **Done (gate L07 closed).** The owner chose to proceed. `favicon.svg` is now the supplied no-spark symbol from the brand kit, with its original geometry; it uses the supplied white fill when the browser is in dark mode. Added a 32 px PNG fallback and a 180 px touch icon (the symbol on the ivory brand tone). [after](evidence/after-favicon-light-dark.jpg) |
| M8-05 | The shared-link image (1200 x 630) shows the five bottles and the carton but no wordmark or headline; GEM appears only as small bottle labels. Also, `og:image` is a relative path in the current preview build; the indexable build writes an absolute URL | `assets/social.png` | **Done.** The owner chose to proceed. The share image is the original photograph, unaltered, with an ivory band (92 px) and the supplied ink logo lockup added along the bottom edge. The original is preserved as `assets/source/social-photo-original.png`; `make-brand-icons.mjs` regenerates both outputs. Size 262 KB against 269 KB before. [after](evidence/after-share-image.jpg) |
| M8-06 | **Retracted.** I reported the Home "One identity" band as a tall, near-empty stretch of texture. It is not: the band holds a portrait flatlay image (about 600 x 800 px) beside the text, and my capture had simply not painted that image yet. Checked live in normal and reduced-motion mode; the image paints in both | n/a | No change; the band is deliberate |

## Verification of the shipped refinements

Build reproducible; `check.py` and the production-check tests pass; browser regression passes in Chromium and Firefox, including the no-overflow test across all ten routes at 320, 375 and 1440 px. Additional capture at 320, 375, 820 and 1440 px, Arabic and English, Home, About, Amenities and Contact, with all images forced to load: no horizontal overflow in any of the 32 combinations; Arabic hero text fits beside the artwork at 1440 px.

**Method lesson:** full-page captures of lazy-loaded pages can miss images. The audit images were re-checked against the live DOM before any finding was acted on, which is how M8-06 was caught.

## Not changed

Product artwork, existing colours, copy, page structure, the sitemap, motion behaviour, and the privacy, contact and indexing policies. Logo geometry is unchanged: the favicon is the supplied symbol as supplied, and the share image only adds the supplied lockup outside the photograph.

## Decisions still open

None from the audit. Remaining M8 completion is the owner's acceptance of the shipped result and a native Arabic reader's check of the M8-03 sizing.

## Completion standard (from the roadmap)

The owner accepts the refined presentation; every implementation change has affected-route and bilingual regression evidence; no unapproved product facts or artwork alterations have entered through decorative work. Until those are met, M8 stays open.
