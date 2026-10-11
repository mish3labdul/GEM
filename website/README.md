# GEM website — proposed working preview v0.5.2

The preserved v0.5.1 baseline matches all 80 entries of `GEM_Website_Preview_2026-10-11.zip`. The ZIP SHA-256 is recorded in [source-freeze.json](../governance/source-freeze.json). Current v0.5.2 applies [WD-18/WD-19](records/24_Owner_Concept_Discussion_and_Contact.md); [site-revisions.json](records/site-revisions.json) records exact changed-file lineage. Local Finder metadata is excluded. The existing post-v0.5.1 correction evidence is preserved in [records/remediation-2026-10-11-01](records/remediation-2026-10-11-01/START_HERE.md). This remains a proposed website, not a release or deployment.

| Folder | Purpose |
|---|---|
| `site/` | Only directory permitted as the public/preview document root |
| `source-images/` | Original imagery and concept provenance; not public |
| `records/` | Historical source/decision/QA records, retired assets, transport copies and correction evidence; not public |
| `qa/` | Maintained regression, correction and actual glyph/fallback checks |
| `previews/` | Versioned site-only downloadable ZIP |

From the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory website/site
python3 website/qa/run_qa.py --root website/site --out-base website/records/cleanup-qa/regression
python3 website/qa/run_corrections_qa.py --root website/site --out-base website/records/cleanup-qa/corrections
python3 tools/package_website.py
```

QA requires Python, Playwright with Chromium, and Pillow for the visual comparison helper. Font checks fail for missing required faces or unsupported glyphs. Existing Latin fonts do not establish Arabic support. Do not substitute fonts or claim native RTL validation from these checks.

[Historical website README](../archive/website-original/README.md) and existing records retain their original wording and paths. Resolve them through [path-migration.csv](../governance/path-migration.csv); they do not override the frozen site or current limitations. Original imagery and concept status are preserved. Forms draft locally and do not submit to a backend.

Experimental concept packages, independent audit folders, unrelated previews and prior exports are retained at their original local source locations and catalogued as outside this import; the active website does not depend on them. Its selected concept masters and provenance are included under `source-images/`.
