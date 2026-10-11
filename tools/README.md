# Collection tools

Run from any directory; these helpers locate the repository through their own path.

- `python3 tools/validate_collection.py`: verify source dispositions and byte identity, release-copy digests, Unicode/case filename collisions, active HTML/CSS references, catalogue integrity, historical byte identity, frozen remote release/branches, and the final collection checksums. Exits nonzero on failure. Use `--skip-remote` for explicitly offline validation, or `--skip-checksums` only while preparing a new checksum manifest. Add `--check-index` before committing to verify Git membership and absence of unstaged tracked changes.
- `python3 tools/package_website.py`: create a versioned, Asia/Riyadh-dated site-only ZIP without overwriting an existing package; excludes cache and Finder metadata and verifies archive membership/bytes.
- `python3 tools/refresh_manifests.py`: deliberately regenerate duplicate and checksum manifests after authorized changes. Run validation again afterward.
- `python3 tools/compare_website.py --baseline <site-directory> --out <new-directory>`: render the immutable baseline and migrated site with identical Chromium settings and compare all three pages at desktop/mobile sizes. Stores paired screenshots and pixel-difference evidence. Requires Playwright and Pillow.

Maintained website QA remains under `website/qa/`. Source-era brand build scripts remain archived as historical helpers, not active tools. These commands do not merge, release, deploy, contact anyone, follow mailto links, or alter original source files.
