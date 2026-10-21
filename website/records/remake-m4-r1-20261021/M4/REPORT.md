# M4-R1 bilingual integration

**Status:** Implemented locally. The owner's “Approved M2-R1” selected the recorded recommendation and authorized M3–M5. No publication, repository upload, merge or release occurred.

| Item | Evidence |
|---|---|
| Active implementation | `gem-site` |
| Selected comparison | `review/pilot`, M2-R1, preserved |
| Source repository / revision | `mish3labdul/GEM`, main, `5a9ab1e887300063f23c2d5bd884f4ac486ce80d`; refreshed unchanged at execution start |
| Local Git / branch / PR / target | Standalone folder; none created or authorized |
| Rollback | `before-integration/gem-site`; all 41 baseline file hashes verified |
| Source hashes | [integration.json](integration.json) records promotion; [final verification](../M5/verification.json) records final tested sources |
| Local preview | http://127.0.0.1:4195/ar/ and http://127.0.0.1:4195/en/ |

The active site now includes the selected responsive hero, five distinct product images and three format studies across Arabic and English. Image, name, detail, alt text and pressed state update together. Existing page structure, controlled product names, original logos, local-only brief and noindex preview behaviour remain.

Asset masters now live outside generated output. The dependency-free build copies canonical identity/font/social resources and the export family into a fresh `dist`. A disposable regression removes `dist`, rebuilds all assets, plants stale generated output and confirms that the next build removes it. Optional export regeneration uses the already installed Sharp module; building/serving requires no package installation.

Changed implementation paths: `build.mjs`, `app.js`, new `pilot.css`, new `pilot-art.mjs`, `prepare_assets.py`, new `export-assets.mjs`, new `assets/`, regression checks, README and regenerated `dist`. `style.css` and `content.mjs` retain baseline bytes. No speculative category copy or About image was added. Arabic format descriptions are working review copy; native acceptance is pending.

The historical duplicate, original archive and released brand documents were not edited. The micro favicon remains explicitly held, and existing social artwork is retained. See [M3 decisions](../M3/ASSET-DECISIONS.md) and [M5 report](../M5/REPORT.md).

To roll back, preserve the current candidate first, then replace the active folder with `before-integration/gem-site`. Do not overwrite the selected pilot or historical copies. This is a manual reversible local operation, not a remote rollback.
