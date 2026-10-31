# Owner decisions recorded — 31 October 2026

Source: the owner's answers on the GEM Decision Sheet (a private claude.ai page), pasted into the Claude Code session on 31 Oct 2026. Owner-reported, no signed record. This adds to `../launch-readiness-2026-10-30/DECISIONS-20261030.md`; it does not overwrite the 21, 23 or 30 Oct records and closes no gate.

## A. Decide now
| # | Answer | Status |
|---|---|---|
| A1 | Require all four CI jobs on `main`: **yes, apply** | **Not applied.** The GitHub account used by Claude Code (`mashaelalh`) has push but not admin on `mish3labdul/GEM`, so the ruleset update returned 404. The owner must change it (Settings, Rules, Rulesets, `GEM main required checks`, add `Remake QA (chromium)` and `Remake QA (firefox)`; strict checks are already on; bypass list empty). |
| A2 | Close PR #32 | PR #32 now shows as **merged**: GitHub marked it merged once its commits reached `main` through PR #34. Nothing left to close. A comment pointing to #34 was added. |
| A3 | gem-assets-hub uncommitted change: leave it | No action. |
| A4 | Production deploy: after the privacy notice is merged | Pending the notice. Rollback target while it is still production: `718a9a58-1448-4952-be01-f1fe3ac5b77f`. |
| A5 | Rollback exercise window | **5 Nov 2026, 17:00 KSA.** Requires A4 to be done first; if the notice is not merged by then the window moves. |
| A6 | Stationery form deviations | Accepted for **internal use only**: compact frame, ink header fill, English-first label order, shortened status line. The remaining two (untracked uppercase labels, no official brand slot) were not separately answered; treated as open. |
| A7 | Cloudflare access | Second member stays postponed. |

## B. Privacy notice (L09)
| # | Answer |
|---|---|
| B1 | Operator name: "GEM" confirmed. |
| B2 | Privacy email `contact@mish3l.com`: confirmed as the address tested on 26 Oct and monitored by the owner. |
| B3 | Jurisdiction: "Riyadh, Saudi Arabia". |
| B4 | Hosting provider wording: keep "our hosting and network provider". |
| B5 | Logging list (Requests, Visitors, Performance, Security, Cache, Origin, DNS analytics): publish as listed. |
| B6 | Authorized-access wording: accepted as written. |
| B7 | Purpose wording: still accepted. |
| B8 | Retention: **adviser only**; no wording yet. |
| B9 | Response time (acknowledge 5 working days, handle within 30 calendar days): keep. |
| B10 | Change notice ("We update this notice and its date."): keep. |
| B11 | Rights and applicable law: the owner supplied the scope clause of the Personal Data Protection Law (it applies to processing in the Kingdom, including data of residents processed from outside). The pasted text was cut off mid-sentence. This establishes that the PDPL is to be treated as applicable; the final English and Arabic rights paragraphs are still to be settled by the adviser. |
| B12 | `cf_clearance` cookie: **needs consent or a banner**. Open: how to meet this (see Open points). |
| B13 | Adviser: "Mohammed", 31 Oct 2026. Surname, qualifications and the exact items reviewed are not recorded. |

## C. Imagery rights (L08)
| # | Answer | Note |
|---|---|---|
| C1 | Image model for the 30 Oct images: "openai imaggen" | **Conflicts with the evidence.** On 30 Oct Claude Code generated V02 (EN and AR), V03 and V09 in the Gemini web app on the owner's account (Create image, picker "3.1 Pro", 16:9) and the owner downloaded the pulled-back English plate from that chat. Earlier images (M3 log, 21 Oct) did use built-in ImageGen. The owner's statement is recorded as owner-reported, **not** as the model of the 30 Oct images, until clarified. |
| C2 | Old share photo (B7): moot, will not ship | Recorded. |
| C3 | Keep format images labelled "concept study render": **No** | Meaning unclear (stop using the label, or change what they are called). Not acted on. |
| C4 A, B, C, D | Public use: **yes** for Flow scenes and Veo videos, arches and textures, Part D product art, favicon/logos/share image | Owner dispositions, recorded. This is not independent rights clearance and does not close L08. |
| C5 | Consultant's written advice | Exists; the owner will not share it. It cannot be cited as evidence in this repository. |
| C6 | Remove unused files from the deployed bundle | **Done in this change**: `hero-desktop-640/960/1280.webp`, `hero-mobile-640/960.webp` and `social.svg` are no longer copied into `dist`. Sources and history are untouched. No page referenced them (checked in the rebuilt `dist`). |

## D. Reviews (all pending, run on the final candidate)
D1 native Arabic: owner needs help. D2 VoiceOver: owner will do it. D3 physical devices: owner will do it. D4 WebKit font retry: owner needs help. D5 400% zoom: Claude Code runs it, on the final candidate.

## E. Stationery
E1: "GEM" only; the registered legal name, Commercial Registration No. and National Address are **still not supplied**. E2 to E6: to be filled. E7 Word check: not yet; the owner cannot open the `.bas` file (see below). E8: keep the Arabic-containing PDFs in the public repository. E9: to be decided.

## F. Launch approval (L12)
Not yet.

## Open points
1. **A1:** needs the owner's GitHub admin account (see above).
2. **B12 consent:** `cf_clearance` is set by Cloudflare before any page script runs, so a banner on the page cannot stop it. The realistic options are (a) turn off the Cloudflare feature that sets it (JavaScript detections or bot challenge settings, a dashboard change by the owner), (b) a banner and notice wording that describe it without gating it, or (c) the adviser's view that it is strictly necessary. The owner and adviser need to choose before the notice is wired.
3. **C1, C3:** the owner to clarify.
4. **B8, B11, B13:** adviser wording and details still needed.
5. **Word check without the macro:** `WORD-CHECK.bas` is a VBA text file. In Word: open the editor (Tools, Macro, Visual Basic Editor; Windows: Alt+F11), File, Import File, choose the `.bas`, then run it. Without the macro, open each `.docx`, press Select All then F9 to update fields, and check that subtotal, VAT and total change when you edit quantity, unit price and VAT rate.

## Follow-up answers (31 Oct 2026, later; owner-reported)
| Item | Answer | Action |
|---|---|---|
| B12 cookie approach | **Option (b)**: a banner and notice wording that describe `cf_clearance` without gating it | Implemented: an informational strip at the top of every page (the 26 Oct accepted cookie paragraph, English and Arabic, verbatim, with a link to the privacy page and a Close button remembered for the browser session only), and the same paragraph and a session-storage disclosure in the privacy notice. The banner cannot stop the provider's cookie. Whether option (b) satisfies the consent requirement is for the adviser to confirm. |
| C1 image model | **Gemini 3.1** | Recorded in `../visual-replacements-20261030/README.md`. This supersedes the earlier "openai imaggen" statement for the 30 Oct images. |
| C3 labels | **Drop the labels** | Interpreted as the "Concept study; counts, materials, hardware and compatibility remain under review." caption and alt text on the room, wall-mounted and travel format images. Removed from the page and from the content files (English and Arabic). **Still on the site, not removed:** "Concept illustration. Not production artwork." on product images, the "Concept · supplier proof required" tags, "Concept portfolio · commercial availability not established", and page titles and descriptions using "concepts". Internal manifests and governance limitations are unchanged. Tell Claude if these should go too; note that governance still classifies Part D as concept/not production artwork. |
| PR #35 | Merge | Merged as `0fcbc31`. |

## Privacy notice wiring (this change)
Filled from owner answers B1 to B10: operator "GEM, Riyadh, Saudi Arabia"; privacy contact `contact@mish3l.com`; hosting provider wording; logging list; purpose; access wording; response times; change notice. The publication date is no longer a stated date ("The publication date will be set at launch."). **Still pending:** the retention period (marked `[RETENTION PERIOD — PENDING]` in English and Arabic) and the final wording of rights under applicable law (a "Still being finalised" section says so). The new Arabic copy was written by Claude and needs the D1 native review. Before L12, search the built pages for `PENDING` and `قيد التحديد`; none may remain.
