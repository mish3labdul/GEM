# M4-R1 reviewer checklist

**Review surface:** http://127.0.0.1:4195/ar/ and http://127.0.0.1:4195/en/. Restart with `python3 gem-site/serve.py --port 4195` from the workspace root. This is loopback only. Record reviewer, date, browser/device, route, finding and disposition. Leave unperformed checks pending.

## Owner visual selection

1. Compare the [complete asset sheet](../M3/asset-family.png) with the [M3 decisions](../M3/ASSET-DECISIONS.md). Top row: Shampoo, Conditioner, Body Wash, Body Lotion, Hand Wash. Bottom row: Room, Wall-mounted, Travel.
2. Review the Arabic and English homepages, then all five product selections and three format studies. Check mobile and desktop reading, image/name agreement and readable concept qualifications.
3. Record **accept for local preview**, **revise** with specific findings, or **hold** per asset. This does not approve production artwork, relative capacities, materials or supply readiness.
4. Keep the small favicon decision separately held unless the supplied micro artwork and its use are explicitly accepted.

## Native Arabic reviewer

1. Read every Arabic page naturally, including navigation, disclosures, format captions, Privacy and all five product descriptions. Confirm wording, joins, punctuation, line breaks and RTL reading order.
2. Check `Property Edition`, `Bespoke Programme`, GEM, email fields and the English signature for correct LTR isolation without mirroring artwork.
3. Fill the local brief in Arabic with mixed Arabic/Latin names, generate it, copy or download, edit and clear. Confirm readable output and localized errors/status text. It is not sent to GEM.
4. Report any corrupt glyph or unsupported substitution as **fail**, with route/text and screenshot. No fallback may be accepted as a workaround for corruption.

## Assistive-technology / browser reviewer

1. With an actual Arabic/English screen reader, follow the skip link, landmarks, heading order, navigation and equivalent-page language switch. Confirm pronunciation/language handling and logical focus order.
2. Operate all five product controls. Confirm the selected state/name/content is understandable, announcements are useful and images have appropriate descriptions without excessive duplicate speech.
3. Complete the brief, trigger invalid required fields, generate the output, copy/download, edit and reset. Confirm focus, errors, live status and the local-only explanation. Test denied clipboard access.
4. On Safari and a physical mobile device, check menu opening/escape, product scrolling, touch targets, captions and form controls.
5. At actual 400% browser zoom, check navigation, content reflow, product controls and the brief without two-dimensional page scrolling or lost controls. Also inspect forced colours and reduced motion.

## Decision record

| Area | Reviewer / environment | Result | Findings / evidence |
|---|---|---|---|
| Asset-family visual selection | Owner, 21 October 2026 | Accepted for local preview | “accepted, reflect on github GEM repo”; see OWNER-ACCEPTANCE.md |
| Native Arabic | Pending qualified reviewer | Pending | |
| Actual screen reader | Pending reviewer | Pending | |
| Safari / physical devices | Pending reviewer | Pending | |
| Actual 400% zoom | Pending reviewer | Pending | |
| Micro favicon | Pending owner/artwork disposition | Held | |

Return specific findings for correction. Do not mark untested checks passed or convert local visual acceptance into release authorization.
