# Live bilingual acceptance worksheet

For native Arabic, accessibility and device reviewers. Start at https://gem.mish3l.com. This is the accepted concept preview, deliberately noindex. Review the current remake only. Each result starts **Pending**; checkmarks, HTTP success and automated CI do not establish human acceptance.

## Review identity

- Reviewer / role: Pending
- Date and time / timezone: Pending
- Source commit / deployment ID: Pending verification by reviewer; expected deployment `3e354187-a9f0-4727-81f6-a1e4b721ea6d` from source `cbd46be2289a6668463fbeac83af8f96e78f4883`
- OS / browser / version / physical device: Pending
- Screen reader / version / language voices, where applicable: Pending
- Viewport / browser zoom / motion or forced-colour settings: Pending
- Evidence location: Pending

Use a separate copy or separate result entries for each reviewer/environment. Record `Pass`, `Fail`, `Pending`, or an explained `Not applicable` per area. A review of one language or device does not pass the others. If the artifact changes, identify affected checks and rerun them.

## Route coverage — all ten pages

For each pair, read the complete page, use navigation and the equivalent-page language switch, and check keyboard/focus order, headings/landmarks, text and image descriptions. The native Arabic reviewer checks wording, joins, punctuation, mixed-script isolation and natural RTL reading order. Device review checks line wrapping, imagery, touch controls and overflow. Screen-reader review checks actual spoken language, names, order and duplicate or missing announcements.

| Route pair | Page-specific review | Native Arabic | Actual AT (AR + EN) | Safari / physical device | Evidence / finding IDs |
|---|---|---|---|---|---|
| [AR home](https://gem.mish3l.com/ar/) / [EN home](https://gem.mish3l.com/en/) | Hero text, concept qualifications, primary links and image descriptions | Pending | Pending | Pending | — |
| [AR about](https://gem.mish3l.com/ar/about/) / [EN about](https://gem.mish3l.com/en/about/) | Brand story, English signature and mixed-script names without mirrored artwork | Pending | Pending | Pending | — |
| [AR amenities and packaging](https://gem.mish3l.com/ar/amenities-packaging/) / [EN amenities and packaging](https://gem.mish3l.com/en/amenities-packaging/) | All five products, selected states, image/name agreement, three format studies and readable qualifications | Pending | Pending | Pending | — |
| [AR contact](https://gem.mish3l.com/ar/contact/) / [EN contact](https://gem.mish3l.com/en/contact/) | Labels, required-field errors, local-only explanation, generated brief and status feedback | Pending | Pending | Pending | — |
| [AR privacy](https://gem.mish3l.com/ar/privacy/) / [EN privacy](https://gem.mish3l.com/en/privacy/) | Readable and equivalent notice; distinguish linguistic acceptance from pending owner approval of actual public practices | Pending | Pending | Pending | — |

## Interactive journeys — repeat in both languages

| ID | Task and expected outcome | AR result | EN result | Evidence / finding IDs |
|---|---|---|---|---|
| J01 | Use skip link and keyboard navigation. Open/close mobile menu; Escape returns focus sensibly. No keyboard trap or hidden focus. | Pending | Pending | — |
| J02 | Switch language from each of the five pages. Land on the matching page with correct language/direction and meaningful focus/navigation. | Pending | Pending | — |
| J03 | Select each of the five products using keyboard and touch where available. Selected name/state/content and image descriptions are understandable with actual speech output. | Pending | Pending | — |
| J04 | Trigger invalid required fields. Errors identify the field and correction; focus and spoken feedback support recovery. | Pending | Pending | — |
| J05 | Enter mixed Arabic/Latin property and personal names. Generate a brief, edit it and regenerate. Text order and wording remain readable; interface clearly states nothing was sent. Use fictional review data. | Pending | Pending | — |
| J06 | Copy with permission, then deny clipboard access and check recovery. Download and open the text file; wording and encoding remain correct. Clear/reset without stale content or misleading success messages. | Pending | Pending | — |
| J07 | Check actual browser zoom/reflow, reduced motion and forced colours where supported. No lost controls, obscured focus or two-dimensional page scrolling. Name any unsupported setting. | Pending | Pending | — |
| J08 | On Safari and a physical mobile device, complete menu, product and brief journeys. Check touch targets, scrolling, captions, form controls and orientation changes. Record each environment separately. | Pending | Pending | — |

Any corrupt Arabic glyph or unsupported font substitution is a **Fail**. Record route, exact text, environment and screenshot; do not accept a fallback that corrupts text. Automated font coverage is supporting evidence only.

## Finding and sign-off template

For every finding, record: ID; route/journey; language; environment; steps; expected/actual result; impact/severity; screenshot or speech transcript; responsible person; correction commit/deployment; retest result/date. Use a plain text transcript if a screen-reader recording is unavailable. Keep personal information out of committed evidence.

| Area | Reviewer / environment | Result | Findings / evidence / date |
|---|---|---|---|
| Native Arabic, all pages and output | Unassigned | Pending | — |
| Actual Arabic/English screen reader | Unassigned | Pending | — |
| Safari | Unassigned | Pending | — |
| Physical mobile device(s) | Unassigned | Pending | — |
| Additional zoom / motion / forced-colour review | Unassigned | Pending | — |

Return results to the [readiness register](README.md) and [gate register](GATES.csv). Engineering can correct reported defects; qualified reviewers must supply their own acceptance evidence. This worksheet does not approve rights, favicon artwork, privacy practices, production/supplier claims, merge or removal of noindex.
