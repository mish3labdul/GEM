# 15 · Handoff — session 2 (2026-10-10)

## State
- Three pages: homepage, brand and design reference (secondary), temporary privacy and legal notice. Static HTML/CSS/JS, no build step, no third-party requests.
- All eleven owner decisions are applied (record 10). The audit's correction tasks GEM-01/02/03/04/05/06/09/14 are done with fresh evidence (records 13, 14). Content revisions GEM-10/11/12/13 are in place (record 11).
- All copy and imagery remain PROPOSED. Contact details are visibly temporary.
- Nothing was published, deployed, pushed or merged. No form destination is connected and no enquiry was sent. Release folders and the logo kit are unchanged.

## Read first next session
1. This file, then records 10, 13 and 14.
2. Before editing, compare the current files with `records/qa-runs/20261010T124726Z/environment.json`. If anything differs, someone else changed it: reconcile and retest.

## Concurrent work found during this session
`website-assets-2026-10-10-01/` appeared on the Mac while this session was working. It is another agent's proposal: four newly generated, unbranded concept images (amenity family, packaging study, material study, guest arrangement), with web exports, a gallery, placement mockups and its own handoff. It changed none of the website, records or audit files: the 70 audit-baseline files were re-verified unchanged before write-back, and none of its paths overlap with this session's. **It is not integrated.** It awaits owner acceptance, and it is a different direction from the Part D branded mockups the owner chose to show (WD-06). Choosing between them, or combining them, is an owner decision (item 8 below).

## Owner input still needed
1. **Real contact details and legal entity** (to replace the WD-03 temporaries on all three pages) and **approved privacy/legal text** (`privacy.html` and the privacy box are proposed best-practice wording).
2. **A receiving destination** and separate authorization to connect it. `site.js` has a switched-off `DELIVERY.endpoint`. Connecting it needs validated success and failure states and a test against an owner-approved inbox, never a third party.
3. **Alt text for the web crops** of the four mockups: they reuse Mashal's HR01 deck alt text. Please confirm that approval covers the website (OD-G03).
4. **Name for the consistent range**, if wanted ("Core Collection" is still [REQUIRES OWNER]).
5. **Motion:** keep the static mark, or commission the reveal from motion masters (VAL-14). If a reveal is wanted, the supplied artwork would need separate ring, spark and quarter layers from the artwork owner. Splitting the compound path here would amount to reconstructing it.
6. **Arabic edition:** the footer promises one (WD-08). It needs an Arabic font build with full glyph coverage, an RTL layout pass and native review before any route exists.
7. **Acceptance testing beyond Chromium** (GEM-15): Safari, Firefox, a physical phone, native zoom, and VoiceOver or NVDA. Owner time is needed for screen-reader observation, as in HR01.
8. **Image direction:** keep the Part D branded mockups (now on the page), adopt the unbranded generated set in `website-assets-2026-10-10-01/`, or use both. If adopted, follow that package's `CLAUDE_ASSET_HANDOFF.md`: full 3:2 frames and its own captions.

## Next actions not blocked by owner input
- Optional: tighten the 320×640 first screen (the action sits 89px below the fold).
- Optional: split the homepage sections into the planned pages once real offer details exist. The reference page could grow into the full `/reference/` area from Parts A–C.
- The owner may delete the empty `records/_update.tar.gz` and the transfer copies in `records/_transfer/`.
- Image files sent through the file-transfer channel get a C2PA manifest added. Send images inside an archive when exact bytes matter (record 13).

## How to run
See README.md. QA: `python3 qa/run_qa.py --root site --out-base records/qa-runs` (needs Playwright and Chromium).
