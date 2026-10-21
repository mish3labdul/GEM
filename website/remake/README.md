# GEM — bilingual website preview

Ten complete static pages implement the approved fresh sitemap: Home, About GEM, Amenities & Packaging, Discuss your project, and Privacy, in Arabic and English. Arabic is the default.

## Preview

Hosted noindex preview: https://gem.mish3l.com/ar/ and https://gem.mish3l.com/en/. The owner authorized replacement of the old hosting deployment on 21 October 2026. See [deployment evidence](../records/deployment-2026-10-21/REPORT.md) and [Pages policy/manual deployment](hosting/cloudflare/README.md). CI validates this source on loopback and does not publish changes.

While the preview server is running:

- Arabic: http://127.0.0.1:4195/ar/
- English: http://127.0.0.1:4195/en/

These loopback addresses serve the local review copy. The separate hosted preview above is a Cloudflare Pages deployment; no Sites-plugin ID or publication is claimed.

To restart from this directory:

```sh
python3 serve.py --port 4195
```

The server binds only to loopback. `/` redirects to `/ar/` using HTTP 302. The preview server sets noindex headers and disables directory listings. Keep it for preview use, not public hosting.

## Edit and build

- `content.mjs`: all English and Arabic copy, localized title tags and meta descriptions.
- `build.mjs`: semantic HTML templates and asset copying from canonical sources.
- `style.css` and `pilot.css`: baseline and selected M2-R1/M4 visual treatment.
- `pilot-art.mjs`: selected responsive hero and source-product presentation.
- `assets/source/`: source concept images; original product artwork is preserved.
- `assets/static/`: canonical identity, fonts, licences and synchronized social assets.
- `assets/exports/` and `assets/manifest.json`: responsive/lossless outputs and provenance/hashes.
- `export-assets.mjs`: optional export regeneration using an existing Sharp module (`SHARP_MODULE`). No build dependency or installation required.
- `hosting/cloudflare/`: versioned noindex/security headers and redirects, copied into every clean build.
- `app.js`: menu, language switching, product selection and local project brief.
- `dist/`: generated pages and self-contained assets. Serve this as the document root.

```sh
node build.mjs
```

No dependencies are needed to build or serve. Original GEM artwork, font files and their licences are already included. `prepare_assets.py` is only needed to re-fetch the pinned assets and requires an authenticated/accessible GitHub CLI. Logo paths come from the brand library; font assets are reused as brand resources. No prior website markup, copy, design or sitemap was imported.

For a future metadata candidate, use an isolated copy and the confirmed HTTPS origin:

```sh
SITE_ORIGIN=https://gem.mish3l.com node build.mjs
```

This emits self-canonicals, reciprocal Arabic/English alternates, Arabic-default alternates, absolute social URLs, page schema, a ten-URL XML sitemap and production robots metadata. The deployed candidate remains in preview mode. Pages headers deliberately retain noindex independently of this metadata option; it is not indexing authorization. Do not replace the preserved preview or remove that policy without the separate release decision. The loopback preview server always sends noindex headers and is not the hosting process.

The social PNG is included as a binary asset and preserved on rebuild. The matching SVG derives from the original GEM logo, without editing the mark.

## Interaction and privacy

The enquiry page creates a project brief locally. It validates required fields, supports Arabic and special characters, and offers copy and text download. It never sends an enquiry, writes form data to local storage, or implies receipt. Editing a generated brief’s inputs hides the old output until regeneration. Clear removes the form state; it does not delete files already downloaded or clear the device clipboard.

Preparation stays disabled until the local JavaScript handlers are installed. A document policy (`form-action 'none'`) blocks native network submission, including when the application script fails. Both languages check all three required fonts and display a failure state if any font cannot load.

No analytics or remote font calls are installed. Privacy copy describes this preview only. A public service needs a reviewed notice reflecting its real operator, hosting, contact channel and retention practices.

## Publication status

The visual candidate is accepted and deployed as a noindex preview. Native Arabic linguistic acceptance, full assistive-technology/device acceptance, public privacy/contact information, commercial/SKU verification, micro favicon and rights acceptance remain open. Approved product names and realistic-looking concept illustrations do not establish availability or production approval.

See `VERIFICATION.md` for the checks performed and their limits.

The owner selected M2-R1 and authorized M3–M5 on 21 October 2026, then accepted the resulting local visual candidate and requested GitHub reflection. The selected pilot and rollback snapshot remain preserved in the original local workspace; they are not deployment dependencies. The build recreates `dist` from canonical sources, so edits inside `dist` are discarded. The five products use original Part D concept artwork; the hero and three format images are unlabelled generated concepts. These establish no commercial, supplier, material or hardware facts. Micro favicon acceptance remains held.

Current evidence and open acceptance items: [M5 report](../records/remake-m4-r1-20261021/M5/REPORT.md). A local technical pass does not close native Arabic, actual screen-reader, physical-device or production approval.

## Regression checks — 21 October 2026

```sh
python3 check.py
python3 qa/production-check.test.py
```

The build tests use disposable directories and leave this preview unchanged. After an actual production build, validate its expected origin explicitly:

```sh
python3 check.py --origin https://gem.mish3l.com
```

The checker validates canonical URLs, language alternates, social URLs, robots metadata and sitemap output for the selected mode. `--http` is for the noindex preview server only; `--base-url` selects its local address.

`node qa/browser-regression.mjs` exercises blocked scripts, all three font failures in both languages, local brief generation/download/edit/reset, and ten routes at three viewport widths. It requires an existing Playwright installation. Set `PLAYWRIGHT_MODULE` to an existing module path and `CHROMIUM_EXECUTABLE` to an installed Chromium executable when they are not resolved automatically. No test dependency is needed to build or serve the site.

See the [repository reflection record](../records/remake-m4-r1-20261021/README.md) for acceptance, source provenance and bounded verification. Historical site copies and original preview archives were preserved.
