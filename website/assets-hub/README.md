# GEM Assets hub

Independent static co-owner hub for `gemassets.mish3l.com`. Repository `mish3labdul/GEM`; branch `codex/gem-assets-hub-20261022`, target `main`. Source baseline `4bcaaf48b55d27084186e3e1c0ef7f2e69362b8a`. No dependency on PR #22 and no change to the existing GEM website deployment.

## Build and preview

Node 22+, installed Poppler (`pdfinfo`, `pdftoppm`) and the committed vendor archive are required. Run `npm ci`, `npm run build`, `npm test`, then `npm run serve` in this directory. Visit `http://localhost:4318/ar/` or `/en/`. `dist/` is generated and ignored. No external runtime fonts, scripts, analytics, forms or sign-in. The root redirects to Arabic on Pages, with an HTML fallback for local static servers.

`manifest.json` is the curated register, regenerated with the build. It records source commit, paths, hashes, versions, languages, status, original URLs and derivative relationships. `dist/artifact-hashes.json` inventories every deployed file except its own hash manifest. All hosted files must remain at or below 25 MiB.

## Documents

Reading order: A → D → E; supplementary specifications B and C follow. Counts A=80, B=35, C=78, D=24, E=24: **241 pages**. Original PowerPoints link to commit-pinned GitHub sources. Supplied Part E PDF remains byte-identical (`29b79ebd4693af7c3e584a5cfce2f06180d0cb4514931f8fbe433708a676b12d`). A–D derivatives have stakeholder-copy titles, source version and export date in PDF metadata, filenames and reader labels. All historical restrictions and source qualifications remain in force except the narrow derivative-distribution authorization recorded in `AUTHORIZATION.md`.

Export procedure used installed PowerPoint: open each exact released PPTX, File → Export → PDF → Best for printing, all slides, local destination. Never save back to the source. Quartz preserves appearance but damages Arabic Unicode extraction. Microsoft's online export was also tested and rejected because it substituted Calibri/Microsoft JhengHei for required families.

LibreOffice was tested with a fresh profile and the explicit `fontconfig.xml` pointing to the installed Jost, Inter, Noto Sans Arabic and Courier New files. The complete fallback exports were rejected for non-Arabic artwork drift (including Part A slide 30). Only A slides 37, 38, 39, 65, 66, 68 and B slide 9 use the visually compared fallback pages; the other 210 A–D pages retain native PowerPoint output. `prepare_reading_copies.py` assembles these pages and adds metadata without changing source decks. All pages remain present and retain source slide numbering. The committed final PDFs are the build inputs; routine builds do not re-export them. Re-exporting requires renewed visual and text checks.

## PDF.js

Official release **6.4.299** (`pdfjs-6.4.299-dist.zip`), SHA-256 `f2245eb7ef3f674c872fe568a177bfec15874f5c034613e55d8e307f93ebd86d`, verified against GitHub's release-asset digest. The build checks this digest and self-hosts the worker, CMaps, standard fonts, WASM, images, locales and upstream license. Two HTML entry copies and tiny bootstrap modules select Arabic/English using the official application options. The upstream viewer implementation remains unchanged. PDFs load only in dedicated reader routes; the landing pages request none.

## Validation

`npm test`: page totals, derivative hashes, unchanged E, pinned originals, bilingual routes, noindex configuration, required PDF.js resources and exclusion of restricted templates. `node qa/browser.mjs`: Chromium/Firefox readers, bounds, thumbnails, zoom, English/Arabic find, downloads, fullscreen, language equivalence, mobile reflow, keyboard access, font-failure alert and PDF-failure fallback. Set `HUB_URL` to test a preview. `FIREFOX_PATH` optionally selects an installed Firefox executable. Install the pinned Playwright browser with `npx playwright install firefox` when needed.

`qa/documents.py` uses pypdf/Pillow and Poppler to verify and render all pages and write `qa/document-results.json`; `qa/compare_exports.py` uses PyMuPDF/Pillow to compare export trials. Screenshots are local QA artifacts and ignored. The prepared comparison and all-page sheets were visually inspected; these checks do not grant native linguistic, screen-reader, localization or production acceptance of the source documents. The source's formal deferrals stay open.

## Hosting and rollback

Use only the separate Cloudflare Pages project **gem-assets-hub**, output `website/assets-hub/dist`. Deploy a preview branch first using `wrangler pages deploy dist --project-name gem-assets-hub --branch codex-gem-assets-hub-20261022`. After preview acceptance, deploy the exact same artifact to the project's production branch and associate only `gemassets.mish3l.com`. Never modify `gem-website-v01`, `gem.mish3l.com`, release `v3.0` or its attachments. Record deployment IDs, source commit and artifact digest in `DEPLOYMENT.md`.

`_headers` applies HTTP `X-Robots-Tag: noindex, nofollow, noarchive` to HTML, PDFs and all other assets. `robots.txt` disallows crawling. These are discoverability controls, not authentication. Confirm them on the deployed origin, including PDFs and worker files. Confirm HTTPS, root redirect, both languages, all original-download hashes, all PDF hashes, viewer controls and error fallbacks on the immutable preview before associating the custom domain.

Rollback: select the last accepted production deployment in **gem-assets-hub** and use Pages rollback; verify its identity, artifact hashes, HTTPS and noindex headers afterward. On the initial rollout there is no prior hub production artifact: remove only the new hub domain association if the initial deployment must be withdrawn. Do not touch the GEM website project's domain or deployment. iOS Safari physical-device checks must be recorded separately from desktop Safari and responsive browser emulation.
