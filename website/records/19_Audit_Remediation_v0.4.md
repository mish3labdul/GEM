# 19 · UI/UX audit remediation — v0.4 (session 4, 2026-10-11)

**Input:** the UI/UX audit of the v0.3 preview (2026-10-11): 25 findings in five areas. The owner instructed "Proceed as recommended."
**Starting state:** live preview files matched the tested v0.3 run `20261010T132217Z` (site.css, site.js and reference.html hashes compared).
**Status:** every change below is PROPOSED pending owner acceptance. Nothing was published, deployed, pushed or merged; no form destination was connected.

## Finding by finding
| ID | Finding | Status | What changed |
|---|---|---|---|
| C1 | No working way to contact GEM | **Prepared, waiting on owner** | `site.js` has `DELIVERY.mailto = ""`. When GEM puts a real, monitored address there, the drafted enquiry gains an "Open in your email app" button with the subject and body filled. It refuses `.example`, `.invalid` and `.test` addresses. While the address is empty the button is hidden and has no link (tested). |
| C2 | One CTA in ~5,600 px; header scrolls away | Fixed | CTAs added at the end of Formats ("Discuss the pilot for a property") and Partners ("Start a partner conversation"). Each preselects the enquiry topic and fires `change`, so an existing draft is withdrawn (GEM-04 preserved). The header is sticky where the viewport is ≥560px tall: it tucks away while reading down and returns on scroll up (opacity only; instant under reduced motion). `scroll-padding-top` keeps anchors and focus clear of it. |
| C3 | Qualifier pile-up in Amenities | Fixed | Intro tightened. The status note is now one sentence ("The range is in development; everything shown here is a concept."). Caption repeats were removed (see A1). Claim-adjacent qualifications were kept. |
| C4 | 84 words of disclaimer before the first field | Fixed | Privacy box, form intro and lead were merged into one line plus a privacy link. "Nothing is sent" now sits beside the button. First field, measured from the section top: 128px on desktop (was 192px) and 426px at 375px wide (was 650px). The button is 1,162px into the section at 375px wide (was 1,586px). |
| C5 | Overlapping fields; Clear beside the primary action | Fixed | Role removed (the topic options already ask it). Organisation and property merged into one optional field. Four text inputs plus the topic (was six plus the topic). "Clear form" became a tertiary "Start again", below and apart from the primary action. |
| C6 | One action, four names | Fixed | "Draft an enquiry" (header, hero, footer), "Tell us about your property or project." (heading, Part B UX-writing example), "Draft enquiry" (button), "Enquiry drafted. It has not been sent." (result). Becomes "Send…" only when delivery exists. |
| C7 | Section endings lead to internal documentation | Fixed | Reference links kept as small secondary text; each offer section now ends with an enquiry CTA. |
| H1 | Logo, not message, is the hero focal point | Fixed | Mark capped at 300px (was 440). Headline spans 7 columns and fits on one line at 1440. New lead: "GEM is developing guest amenities and packaging for hospitality owners, developers and operators in Saudi Arabia and the wider GCC: one family of guest objects, under one identity." (PROPOSED). |
| H2 | Inconsistent text–image gutters | Fixed | Approach and Who it serves now leave one empty column (text in columns 1–5, image in 7–12), like the other sections. |
| H3 | 621 px void under the wall-mounted image | Fixed | The 4:5 image is sticky inside its grid row, so it travels beside the two landscape scenes. Note: full-page screenshots capture it at its end position. |
| H4 | Amenities 35% of the page, no structure | Fixed | Split into **Amenities & Packaging** (pilot family) and **Formats and programme directions** (applications and programmes), with a "Formats" item in the navigation and footer. |
| H5 | Status-label noise | Fixed | Homepage labels went from 9 to 7 (status note label and threshold label removed). Concept-image labels use the hairline base style instead of 2px dashed. |
| H6 | Repetitive imagery; low figure–ground on Beige | Partly fixed | The Ink hairline frame on images over Beige is fixed. **Owner decision:** whether Who it serves should show a setting rather than product. B04 stays there because the design system's asset register places it there. |
| H7 | Decorative image in the conversion area | Fixed | Threshold study moved to Reference › Imagery as the "arrival and threshold" example. |
| H8 | Four widths in one form column | Fixed | Every form block is capped at the 420px field width. |
| T1 | Status vocabulary beyond Part B | Fixed | A registry at the top of the status-label CSS maps each label to one Part B style plus one approved free-text line. "Concept" (the note label) is retired. |
| T2 | Reading width set five ways | Fixed | `--site-measure` (= the Part B token), `--site-measure-heading`, `--site-measure-display`. The 70ch, 36rem and 40rem literals are gone. |
| T3 | Untokenised sizes | Fixed | A site-token block for logo (2 sizes, was 4), mark (3), field, alert, textarea, ring, alert title and h1 step-down. QA now reads the allowed type sizes from the token declarations, not a hand-written list. |
| I1 | Missing hover and press states | Fixed | Menu button: Beige on hover, press and while open. Radio rows: Beige on hover. Text fields and select: edge thickens on hover. Hero primary: `:active`. |
| I2 | Loose mobile menu | Fixed | Part B scrim (Ink 64%) behind the open menu. Closes on outside tap and when focus leaves the header (tested). |
| I3 | Programme cards look clickable; cramped at tablet | Fixed | Top-rule list (no boxes); single column below 1024px. |
| I4 | 320×640: CTA below the fold under two logos | Fixed | Hero symbol 48px below 720px, with tighter compact spacing. CTA bottom at 589px (was 705px); now asserted. |
| I5 | No "you are here" | Fixed | IntersectionObserver sets `aria-current="location"` in the header navigation and the reference contents list, with the 2px underline. |
| A1 | Caption repeats for screen readers | Fixed | The register caption's first sentence is now the label itself ("Generated GEM concept"), followed by the rest of the caption. The required caption wording is kept, nothing is said twice. |
| A2 | 17px privacy link | Fixed | 44px text-link style. |
| A3 | Verification beyond Chromium | **Open (needs a person)** | Unchanged: VoiceOver/NVDA, Safari/Firefox, native text zoom. |

## Proposed copy introduced in v0.4
Hero lead (H1); Amenities intro and status sentence (C3); Formats heading "Formats and programme directions" and intro "How the family could meet guests in a room, and how a property could take it on. Each format needs supplier proof before it can be offered."; CTAs "Discuss the pilot for a property", "Start a partner conversation", and their helper lines; enquiry heading, lead and "Creates text for you to copy. Nothing is sent."; field label "Organisation or property (optional)"; "Start again"; "Enquiry drafted. It has not been sent."; reference caption "Arrival and threshold. One light source, long shadow, the guest implied rather than shown."

## Verification
Run `records/qa-runs/20261011T094027Z`: **450 checks, 450 PASS** (Chromium, axe-core 4.14.0, 3 pages × 5 widths plus journeys). Ten new checks cover:
- three routes to the enquiry;
- header sticks, tucks and returns;
- focus never hidden under the header across 45 tab stops (WCAG 2.4.11);
- the partner CTA preselects its topic and withdraws a stale draft;
- the email hand-off stays hidden without a real address;
- no requests are made;
- "you are here" marking;
- four inputs, with reset kept apart;
- the menu scrim, outside tap and tab-out;
- the hero CTA is visible at 320×640.

Two development runs (`20261011T093708Z`, `…093843Z`) failed on a hidden link with `href="#"` (fixed in the page) and on a focus test that did not wait for smooth scrolling (fixed in the test). Both are kept and marked SUPERSEDED.

**Lab performance** (same conditions as before, one cold sample): FCP 1.03s, LCP 1.85s (v0.3: 1.00s), CLS 0, 285,561 bytes, 10 requests. LCP rose because the smaller hero mark is no longer the largest element; the approach image, partly in the first viewport, now is. That is still under 2.5s, but it is a measurable cost of H1.

Visual review: 1440 and 375 full pages, the 768 middle band, the 320 fold and the open mobile menu.

## Before/after hashes (SHA-256, first 12)
| Path | v0.3 | v0.4 |
|---|---|---|
| site/index.html | 26bbd05cb829 | a0a97bf36452 |
| site/reference.html | 6637c4a88987 | 60a35bac36b6 |
| site/privacy.html | e8a1fac38162 | 1dce5a400843 |
| site/assets/css/site.css | 38bf62fd2ba1 | dfb86e228554 |
| site/assets/js/site.js | b13d2854799a | 5b816141ddc4 |
| qa/run_qa.py | 0072064c9797 | 10d1c4bd71cb |
No images, fonts, brand files or tokens changed.

## Owner decisions now needed
1. **C1:** a real, monitored address (unlocks the email hand-off with one line) and, separately, whether to connect a delivery endpoint.
2. **H6:** keep B04 in Who it serves, or use an image of a setting rather than product.
3. Acceptance of the proposed copy above and of the v0.3 items in record 18.
4. **A3:** screen-reader and cross-browser sessions.
