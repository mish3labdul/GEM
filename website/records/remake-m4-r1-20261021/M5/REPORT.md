# M5 technical evidence and acceptance register

**Candidate:** M4-R1, 21 October 2026. **Status:** owner accepted the local visual candidate and asset family; technical checks delivered. Native Arabic and assistive-technology/device acceptance remain open. See [owner acceptance](OWNER-ACCEPTANCE.md). This is not production approval or an accessibility certification.

[Local Arabic preview](http://127.0.0.1:4195/ar/) · [English preview](http://127.0.0.1:4195/en/) · [Asset sheet](../M3/asset-family.png) · [Acceptance checklist](ACCEPTANCE.md)

## Verified result

| Check | Result and scope |
|---|---|
| Syntax, build, static checker | PASS after final implementation changes |
| Disposable build tests | 4 PASS: preview, production, deliberate metadata corruption rejection, clean/stale-output rebuild |
| Chromium | 23 scenarios PASS |
| Firefox | 23 scenarios PASS using the installed Firefox 1511 browser build |
| Routes / reflow | All ten routes at 320, 375 and 1440px in both engines; no horizontal document overflow |
| Interaction | Keyboard menu/escape focus, product pointer/keyboard selection, forced colours/reduced motion controls, local brief validation/download/edit/reset and clipboard-denial fallback |
| Failed scripts / fonts | CSP `form-action` violation observed and no native form navigation; all three required-font failures visibly reported in both languages |
| Captures | 20 full-page route captures plus 24 format/product-state captures; four overview sheets |
| Rendering samples | 40 Chromium platform-font samples across all routes: intended custom fonts, no system fallback in those samples |
| Assets | 16 exports and 10 canonical identity/font/license/social resources; source/export hashes match; five product encodings changed zero visible pixels |
| Preservation | Original logo bytes unchanged; all 41 pre-integration rollback hashes match |
| Local HTTP checker | PASS on port 4195, including preview metadata and asset delivery |
| Design scan | No deterministic findings in changed frontend targets; this is not a visual-quality certification |

Primary evidence: [verification.json](verification.json), [Chromium results](chromium.json), [Firefox results](firefox.json), [capture evidence](capture-evidence.json), [font samples](platform-fonts.json), [design scan](design-scan.json). Installed tools were used; nothing was installed. The preferred Expect CLI remains incompatible with this standalone non-Git folder; direct browser tests were used instead.

The blocked-form test initially assumed Chromium's return behaviour. Firefox throws an unnamed exception when blocking the action; the final test verifies the actual `form-action` policy event and absence of navigation in both engines. Firefox's valid cached 304 response is accepted only alongside a rendered route heading. These were test portability fixes, not weakened form protections.

## Visual review

Inspected the full-route overview sheets in both languages and sizes, original remaining product artwork, the complete asset-family board, and full-size format/product captures. The warm light/material family is coherent; labels remain supplied source artwork; concept captions remain readable next to the images. No original mark was redrawn or mirrored. Contact and Privacy retain their reading/action focus.

Fixed: remaining product states previously fell back to a generic image; all five now use their matching source views. The clean build no longer depends on retained `dist` assets. Suppressed: no new suppressions; the existing narrow Inter exception remains because the source brand documents specify it. Left standing: micro favicon acceptance, source concept artwork's existing stylistic variations, and the human acceptance items below. No blanket file/rule ignores were added.

The five product images preserve differing original framing/material appearances. Their scale is a visual study, not evidence of relative capacity. The format imagery contains unlabelled conceptual objects, with counts, hardware, materials and compatibility qualified in real HTML.

## Bounded performance observations

Three cold Chromium contexts per version/route, alternating versions, 375px viewport, loopback with no throttling. Measurements at 500ms after fonts ready exclude below-fold lazy assets. These are local samples, not WAN performance or Core Web Vitals acceptance.

| Route | M2-R1 median encoded resource bytes | M4-R1 median encoded resource bytes | M2 / M4 median LCP | M2 / M4 median CLS |
|---|---:|---:|---:|---:|
| Arabic Home | 166,785 | 166,706 | 48 / 48ms | 0.000213 / 0.000213 |
| Arabic portfolio | 562,475 | 570,236 | 64 / 68ms | 0 / 0 |

The portfolio adds 7,761 encoded bytes in this initial viewport, about 1.4%. The small timing difference does not establish a repeatable regression or gain. Full raw samples and method: [performance.json](performance.json). Individual format exports are 7,840–61,676 bytes; products are 423,952–705,972 bytes. Source-labelled product encoding deliberately remains lossless.

## Open acceptance register

| Item | Status / next evidence |
|---|---|
| Complete asset-family selection | Accepted for local preview by the owner on 21 October 2026; see OWNER-ACCEPTANCE.md |
| Native Arabic wording and reading order | Qualified native reviewer checks working copy, alt/qualifications, mixed names and brief output; no linguistic sign-off claimed |
| Actual screen-reader flows | VoiceOver/Safari or equivalent bilingual assistive-technology session, following the acceptance checklist; automation is not a substitute |
| Actual 400% browser zoom | Not exercised. 320px reflow passes; those are different checks |
| Safari / WebKit | Unavailable in the installed automated browser set; no Safari pass claimed |
| Physical iOS / Android | Not performed; desktop viewport emulation does not establish device acceptance |
| Complete encoded glyph coverage | Not established; sampled actual custom-font rendering and visual checks do not prove every possible character |
| Micro favicon | Held pending appropriate below-32px supplied artwork acceptance; current full lockup remains a limitation |
| Artwork / rights / production / supplier evidence | Existing repository deferrals remain; realistic concepts and preserved source art do not close them |
| Launch inputs | Domain, receiving contact workflow and actual public privacy/hosting details not supplied; no public deployment authorized or performed |

M3–M4 local work is delivered. M5 technical verification is delivered with the explicit human/device holds above. M6 remains separate. The next useful step is owner asset review and qualified native Arabic/assistive-technology validation, then correction of any concrete findings before launch readiness is assessed.
