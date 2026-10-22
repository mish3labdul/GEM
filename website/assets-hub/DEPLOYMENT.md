# GEM Assets Hub — Deployment & Rollback Receipt (22 October 2026)

| Item | Value |
|---|---|
| Cloudflare Pages project | `gem-assets-hub` (direct upload, output `website/assets-hub/dist`) |
| Source repository & branch | `mish3labdul/GEM` · `codex/gem-assets-hub-20261022` (target `main`, Draft PR #23) |
| Source baseline commit | `4bcaaf48b55d27084186e3e1c0ef7f2e69362b8a` |
| Preview deployment | `cf3b10ed-b593-4b8a-b215-f2bafc4b3e4e` · https://cf3b10ed.gem-assets-hub.pages.dev (branch alias: https://codex-gem-assets-hub-2026102-oaqg.gem-assets-hub.pages.dev) |
| Production deployment | `83dbe8aa-34fb-4b77-86a0-7cc8ebcf9122` (`main`) · https://83dbe8aa.gem-assets-hub.pages.dev · https://gem-assets-hub.pages.dev |
| Artifact manifest SHA-256 (`dist/artifact-hashes.json`) | `7e1bd0a836ed87bed8ceb929e3bac7841cd2b973637460dcb0028c97b724bc41` |
| Custom domain association | `gemassets.mish3l.com` (`id: ac50808e-e662-471d-91f9-5cb03af6b4b3`, zone `c322f99479471d98681f7fd1257d4778`, status: `active`, HTTPS/TLS active, proxied DNS CNAME `gemassets` → `gem-assets-hub.pages.dev`) |
| Isolated from existing website | `gem-website-v01` (`gem.mish3l.com`), release `v3.0` and PR #22 were not modified. |

## Verification Summary

1. **Build & Unit Integrity (`npm run build && npm test`)**:
   - 5 documents / 241 pages (`part-a`=80, `part-d`=24, `part-e`=24, `part-b`=35, `part-c`=78), 15 curated supporting downloads, 474 total build files (all $\le$ 25 MiB).
   - Part E matches `29b79ebd4693af7c3e584a5cfce2f06180d0cb4514931f8fbe433708a676b12d` byte-for-byte.
   - Restricted Arabic/bilingual letterheads excluded; `_headers`, `_redirects`, and `robots.txt` enforce `noindex, nofollow, noarchive` and `/` $\to$ `/ar/` (`302`).
   - Open Graph (`og:title`, `og:description`, `og:site_name`, `og:type`, `og:url`, `og:locale`, `og:image` `1200×630` PNG at `https://gemassets.mish3l.com/assets/social.png`), Twitter/X (`summary_large_image`), `theme-color`, and `/favicon.svg` included on all Arabic, English, and document reader routes for WhatsApp and social media link cards.
2. **Browser & Responsiveness QA (`node qa/browser.mjs`)**:
   - 20/20 reader checks passed across Chromium and Firefox (5 documents $\times$ Arabic & English $\times$ 2 browsers) on local build and live `https://gemassets.mish3l.com`, covering page bounds, thumbnail toggle, zoom, English/Arabic find, PDF download, fullscreen PresentationMode, language toggle, and mobile/desktop page-width reflow.
   - Browser checks passed in both browsers (`mobile overflow` at 320/375/1440, `keyboard skip`, `no PDF preloads`, `PDF failure fallback`, `font failure alert`), plus 14-viewport responsiveness verification across portrait, landscape, tablet, and desktop sizes.
   - iOS 26.3 Safari simulator checked in portrait and landscape (including Arabic slides 37–39); physical-device iOS Safari and native linguistic/accessibility/production deferrals remain separate open items.
3. **Hosted Origin Verification (`node qa/hosted.mjs`)**:
   - Verified on preview (`https://cf3b10ed.gem-assets-hub.pages.dev`), production (`https://37bbae5c.gem-assets-hub.pages.dev` and `https://gem-assets-hub.pages.dev`), and live custom domain (`https://gemassets.mish3l.com`):
     - `hostedFilesChecked`: **470/470** (HTTP 200, `X-Robots-Tag: noindex`, exact SHA-256 match)
     - `originalDownloadsChecked`: **5/5** (exact SHA-256 match against commit `4bcaaf48b55d27084186e3e1c0ef7f2e69362b8a`)
     - `rootArabicRedirect`: **`true`** (`302` to `/ar/` with `X-Robots-Tag: noindex`)
     - `failures`: **`[]`**

## Rollback Procedure

- **Initial rollout withdrawal**: If the initial hub rollout must be withdrawn before a subsequent production deployment exists, remove only the custom domain association (`gemassets.mish3l.com`) from `gem-assets-hub`. Never touch `gem-website-v01` or `gem.mish3l.com`.
- **Subsequent production rollback**: Select the last accepted production deployment (`37bbae5c-2af2-4a39-a442-f2aaf66ca02a`) in the Cloudflare Pages project `gem-assets-hub` and invoke Pages rollback, then re-run `HUB_URL=https://gemassets.mish3l.com node qa/hosted.mjs` and `HUB_URL=https://gemassets.mish3l.com node qa/browser.mjs` to confirm artifact hashes, HTTPS, and `X-Robots-Tag: noindex` headers.
