# Verification — 20 October 2026

**Current candidate: M4-R1, 21 October 2026.** The authoritative current record is [M5 technical evidence and acceptance register](../records/remake-m4-r1-20261021/M5/REPORT.md), with [final machine evidence](../records/remake-m4-r1-20261021/M5/verification.json). Chromium and Firefox each pass 23 scenarios; four disposable build tests pass. Native Arabic, actual assistive technology, actual 400% zoom, Safari/devices and micro favicon acceptance remain open. The sections below preserve earlier baseline evidence and should not be read as the current candidate's complete result.

## Scope

Artifact: standalone `gem-site` build implementing the owner-approved fresh sitemap. GitHub business-document baseline: `mish3labdul/GEM`, `main`, commit `5a9ab1e887300063f23c2d5bd884f4ac486ce80d`. No repository changes, Site registration or deployment.

## Observed checks

- Build completed: ten localized HTML pages.
- Chromium: all ten routes returned HTTP 200 at widths 1440, 375 and 320 pixels; one H1 and a meta description per route; no horizontal overflow and no font-failure state in 30 route/width observations.
- Static link inspection: no broken internal page/fragment links; ten distinct localized titles and ten distinct localized descriptions.
- Responsive menu: opens, closes with Escape and returns focus to its trigger.
- Product selector: updates the selected product name and description; pressed state changes with selection.
- Equivalent-page language switching: Arabic portfolio switches to English portfolio.
- Enquiry validation: empty form, invalid email and whitespace-only required name blocked. Valid Arabic brief prepared successfully, with special characters retained as text.
- Clipboard content matched the prepared brief. Download event produced `GEM-project-brief-ar.txt`. Editing inputs hid the stale brief; reset cleared the fields.
- No non-GET network request occurred during the exercised enquiry flow.
- All three custom fonts loaded. Chromium platform-font inspection on Arabic Home H1, introduction and navigation CTA reported custom `Noto Sans Arabic`, with no system font in those inspected elements.
- Arabic homepage visually inspected in Chromium. Narrow/mobile layouts were checked for overflow; native linguistic review and complete RTL acceptance were not performed.

Subsequent refinements localized concept-image descriptions, isolated English programme names in Arabic prose, supplied the Arabic language-link font explicitly, added social metadata/artwork and changed the preview server to an HTTP Arabic-default redirect. The final build was rerun. These refinements do not add a backend or change the enquiry flow.

## Tool and acceptance limits

The installed Expect CLI was attempted but could not run because this standalone project is not a Git checkout. Direct Chromium checks supplied the observations above. A font-cmap audit was attempted but FontTools was unavailable in both checked Python environments; no encoded glyph-coverage claim is made. Browser platform-font evidence and visual inspection are narrower than complete character coverage.

Sites native hosting tools were absent from the session tool registry. No hosted URL, Site version or production publication is verified. The local preview is interactive and reachable on this device only.

Arabic copy is newly authored for review; native linguistic approval is pending. No Safari/Firefox/device testing, complete screen-reader testing, WCAG certification, regulatory acceptance, production-product approval or public privacy approval is claimed.

## Release dependencies

Confirm the public domain and receiving contact workflow; complete native Arabic and accessibility acceptance; verify any future product facts and image/public-use permissions; update privacy for actual hosting and data practices; register and publish through native Sites tools when available. Rebuild with the confirmed domain and verify canonical/hreflang/social/sitemap output before public indexing.
