# M8 — brand presentation audit, 23 October 2026

**Status: audit complete, one defect fixed, five refinements proposed and waiting for owner decision (gate L16).** M8's goal is one coherent GEM system across Arabic, English, phone and desktop. This record follows the roadmap's rule: preserve the accepted design, add no product facts, do not alter artwork or logo geometry, and ship only what the owner accepts.

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
| M8-02 | Format-image caption bars use a grey-mauve (`#BCACA7`) that sits cooler than the warm ivory and travertine tones around it; on desktop they read as heavy grey blocks under each image | [desktop](evidence/amenities-desktop-ar-en.jpg) | **Proposal.** Use a warm neutral already used for section bands, or a translucent ink overlay; no new colour introduced |
| M8-03 | Arabic body and lead text looks smaller than the English at the same nominal size (Arabic letterforms have a lower x-height). Most visible in hero intros and card text on desktop | [home](evidence/home-desktop-ar-en.jpg) | **Proposal.** Raise Arabic body, lead and card text by 1 px at desktop widths and re-check 320 and 375 px. Needs a native reader's eye before accepting |
| M8-04 | The browser icon is the full GEM wordmark. At 16 and 32 px it is illegible, and on a dark tab bar the ink-coloured mark nearly disappears | [render](evidence/favicon-16-32-64.jpg) | **Decision (gate L07).** Either keep as is, or adopt the no-spark symbol option staged in M6-R2 (`review/tools/stage-m6-favicon.mjs`). Keeping it is a valid disposition |
| M8-05 | The shared-link image (1200 x 630) shows the five bottles and the carton but no wordmark or headline; GEM appears only as small bottle labels. Also, `og:image` is a relative path in the current preview build; the indexable build writes an absolute URL | `assets/social.png` | **Decision.** Keep (artwork unaltered), or add the logo lockup, which changes the image and needs approval. The absolute URL is handled in M7 |
| M8-06 | The Home "One identity" band is a very tall, low-content stretch of travertine (about 480 px of near-empty texture at desktop) between the cards and the CTA, which slows the page rhythm | [home](evidence/home-desktop-ar-en.jpg) | **Proposal.** Reduce the band's height by about a quarter, or let the texture frame the content more tightly. Layout-only |

## Not changed

Logo geometry, product artwork, colours, copy, page structure, the sitemap, motion behaviour and the privacy, contact and indexing policies.

## Decisions requested from the owner

1. M8-02, M8-03, M8-06: accept, adjust or decline each. Accepted items ship as one reviewable release with bilingual regression evidence at 320, 375, 820 and 1440 px.
2. M8-04 and M8-05: choose a disposition. The favicon one also closes gate L07.

## Completion standard (from the roadmap)

The owner accepts the refined presentation; every implementation change has affected-route and bilingual regression evidence; no unapproved product facts or artwork alterations have entered through decorative work. Until those are met, M8 stays open.
