# Preserved history

- `baseline-v3.0/`: all 994 files from the published baseline, with original package names, internal structure and bytes. Its original `.gitignore` and build-cache file are deliberately retained as historical evidence.
- `branch-variants/`: any earlier branch-specific file not byte-identical to the baseline, grouped by source commit prefix.
- `website-original/`: original website README, historical helpers and pre-repair QA documentation.

These packages are immutable history, not the recommended current folder structure. Internal checksums remain original and relative to their original package directory. Old absolute paths and repository-root links are historical references: consult [path-migration.csv](../governance/path-migration.csv). Archive build scripts are not maintained entrypoints and must not be run against current assets.

No branch, tag, commit history or existing release download has been deleted or rewritten. New repository-root paths do not redirect old GitHub blob URLs; original commit/tag URLs remain available, and the migration register supplies current destinations.
