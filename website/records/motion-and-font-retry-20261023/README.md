# Motion enhancements and font-load resilience — 23 October 2026

Record of two production changes to the noindex concept preview at https://gem.mish3l.com, and the checks behind them. Scope: engineering evidence plus the owner's instruction to ship. It is not native-language, assistive-technology or physical-device acceptance, and it does not change indexing, privacy, contact or rights status.

## Owner decision

The owner reviewed the hosted preview (https://ui-motion-preview.gem-website-v01.pages.dev) and instructed: "I love them all, run full QA test then take it live". The owner later asked for the font failure to be investigated and fixed.

## Change 1 — motion and interaction enhancements (PR #26)

| Pillar | Behaviour |
|---|---|
| Scroll depth | Hero zoom and headline parallax, curtain reveals on images and text blocks, slower texture parallax on the arch and stone bands |
| Smart header | Fixed frosted header that hides on scroll down and returns on scroll up; progress line fills right-to-left in Arabic; the Privacy page keeps its static header |
| Product stage | Crossfade between the five products; zoom lightbox for the stage image, the three format cards and editorial photos; closes with Esc, the close button or a backdrop click |
| Micro-interactions | Card lift and image zoom on hover, arrow glide in the reading direction, cross-document view transitions (Chromium-based browsers; other browsers navigate as before) |

All motion is skipped under `prefers-reduced-motion: reduce`. The noindex, security-header and `form-action 'none'` policy were not changed.

## Change 2 — font-load retry (PR #27)

The required-font check hid the whole page behind a font-error screen if any single font request failed once. A browser does not refetch a face that failed, so the visitor had to reload. The check now retries each font twice by loading a fresh `FontFace` from script; a font that stays unavailable still shows the error screen.

## Chronology

| Event | Reference |
|---|---|
| Preview deployed | `e84748de-b6b0-4e12-a950-b24534d63705`, alias `ui-motion-preview` (preview environment) |
| PR #26 merged | `fab06a2` ; CI run 39899308996: collection integrity, Chromium QA, Remake QA Chromium and Firefox passed |
| Production deployment | `7a3f8614-db87-4c84-bee9-e90d72fad364` from `fab06a2` |
| PR #27 merged | `2552dc8` ; CI run 39901551880: all four jobs passed |
| Production deployment (current) | `52dd8d17-3feb-4926-b921-ec64df7900fc` from `2552dc8` |
| Rollback target before change 1 | `fd8cc682-0671-4841-a0c4-f4f4e31025ad` (source `a283d56`). Rollback is a documented route; it was not exercised |
| Diagnostic deployment | `b17d91f9-c1da-45dd-a422-e170517ba406`, branch `font-diag`, printed the font-load error on screen for a simulator experiment; created and deleted on 23 Oct 2026 and never served production |

## Checks run

- Build reproducibility: `node build.mjs`, `check.py`, and `git diff --exit-code -- dist` clean on a fresh checkout.
- `qa/production-check.test.py`: 5 tests pass.
- `qa/browser-regression.mjs`: 23 scenarios per browser for change 1; 25 after change 2 added two recovery tests (Chromium and Firefox).
- `tools/validate_collection.py --skip-remote --check-index` on a clean checkout of each branch.
- Live check after each deploy: eight routes return 200, `x-robots-tag: noindex, nofollow` still sent, header goes frosted on scroll, lightbox opens and Esc closes it, no script errors (Chromium).
- Live recovery check after change 2: the first request for one font was aborted; the page showed no error screen and requested the font again.

## iOS Simulator spot check (engineering evidence only)

Xcode simulators, Safari: iPhone 16 Pro (iOS 18.0) and iPhone SE, 3rd generation (iOS 17.2).

- iPhone 16 Pro, Arabic amenities page on the live site: header hid on scroll down and returned frosted on scroll up with the progress line starting at the right edge; images faded in on scroll; tapping the product image opened the lightbox with the Arabic close button; the close button worked.
- Not exercised: product-switch crossfade, hover effects (not applicable to touch), view transitions on the simulators' Safari, and any iPhone SE interaction, because the SE showed the font error on every attempt before the fix.

### Font-error finding

On first loads in the simulators the page sometimes showed the font-error screen ("A required display font could not be loaded"). It affected the previous production build (`fd8cc682`) as well as the new one, so the motion changes did not cause it. Server responses for all three fonts were correct (200, `font/woff2`, CORS header, about 0.3 s). An instrumented copy loaded correctly 8 of 8 times afterwards, so the original cause was **not reproduced and is not established**; the failures all fell in the first minutes after the simulators booted, which suggests a transient network fault. What was established: one failed font request is enough to hide the page, and the retry removes that sensitivity in Chromium. Safari's engine (WebKit) was not exercised for the retry; physical-device checking remains with the owner under L05.

## Access note

On 23 Oct 2026 the owner authorized the Cloudflare API connector (plugin `cloudflare@cloudflare`) for this project, including Pages edit scope on the account, to delete the diagnostic deployment. Revocation: Cloudflare dashboard, My Profile, Access management, Authorized apps. Relevant to M9 access ownership.
