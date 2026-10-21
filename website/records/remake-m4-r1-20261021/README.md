# Accepted bilingual remake — M4-R1

**Subsequent state:** this import record captured the candidate before hosting replacement. The later [owner-authorized deployment record](../deployment-2026-10-21/REPORT.md) identifies the hosted noindex preview and retained rollback. The source/provenance and initial acceptance evidence below keep their original scope.

The owner selected M2-R1, authorized M3–M5, then accepted the delivered visual candidate and asset family with **“accepted, reflect on github GEM repo”** on 21 October 2026. See [acceptance](M5/OWNER-ACCEPTANCE.md), [QA report](M5/REPORT.md), [review checklist](M5/ACCEPTANCE.md) and [asset sheet](M3/asset-family.png).

| Item | Repository state |
|---|---|
| Repository | `mish3labdul/GEM` |
| Base revision | `5a9ab1e887300063f23c2d5bd884f4ac486ce80d`, live main refreshed unchanged before import |
| Branch / target | `codex/gem-remake-m4-r1-20261021` → `main` |
| Source and generated preview | [`website/remake`](../../remake/README.md) |
| Asset provenance | [`assets/manifest.json`](../../remake/assets/manifest.json), [generation log](M3/GENERATION-LOG.md), [source manifest](source-manifest.json) |
| Imported file identities | [import-manifest.json](import-manifest.json) |
| Preservation | Existing `website/site`, open PR branches, historical packages and released documents unchanged |

The dated reports retain their original local test scope. References to `gem-site`, `review/pilot`, rollback copies and local generated-image paths describe the source workspace; those historical duplicates and 44 raw full-size captures were not uploaded. The asset sheet, four route overview sheets, measured results and machine test/font evidence are included. The live source masters are in `website/remake/assets/source`; canonical identity, fonts and social resources are in `assets/static`. Rendered exports are in `assets/exports`. Source document binaries are linked by revision rather than duplicated.

The imported candidate is self-contained and rebuilds without dependencies. Validate with:

```sh
cd website/remake
node build.mjs
python3 check.py
python3 qa/production-check.test.py
node qa/browser-regression.mjs
```

Browser checks require an existing Playwright installation. Use `PLAYWRIGHT_MODULE` and `CHROMIUM_EXECUTABLE`; Firefox uses `BROWSER_TYPE=firefox` and `BROWSER_EXECUTABLE`. No package installation or hosted browser success is implied by these instructions. Run generated QA evidence outside the checksummed checkout.

Owner visual acceptance does not establish native Arabic, screen-reader/device, actual 400% zoom, micro favicon, legal/IP, production or supplier acceptance. Existing B01/B02/D8 and document-specific restrictions remain. There is no confirmed production origin, receiving backend, deployment, release or merge under this reflection.
