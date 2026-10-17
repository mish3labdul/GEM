# Naming rules and exceptions

1. Retain existing controlled document stems, version/date tokens, original language/variant qualifiers and release filenames. Apply `GEM_BRAND_<Asset>_<Variant>_v<version>_<YYYYMMDD>.<ext>` prospectively only when those values are established by source authority. Never replace source issue dates with the migration date.
2. X12 STREAM is BRAND. No new asset-ID algorithm is introduced. Supplied artwork keeps its original filename; the catalogue carries the existing proposed controlled name and PENDING artwork version/date. ASSET/VARIANT taxonomy acceptance is not inferred.
3. New working folder names and web derivatives use lowercase ASCII words separated by hyphens. Preserve approved public page names, anchors, existing descriptive crop/size suffixes and runtime entrypoint filenames. Do not change brand or product display names.
4. Matching editable/export files share a stem only where the source establishes the relationship. No PDF is generated or silently promoted by this cleanup.
5. Status belongs in the catalogue and navigation. Preserve existing semantic labels: WORKING ASSETS, WORKING EDITION, PROPOSED, CONCEPT / NOT PRODUCTION ARTWORK, PENDING and restricted external-issue use.
6. Preview ZIP names use `GEM_Website_Preview_v<documented-site-version>_<packaging-date-YYYY-MM-DD>.zip`. Packaging date uses Asia/Riyadh. Version is v0.5.1, with existing correction lineage recorded separately. No website version bump is inferred.

## Product display names

The [18 October 2026 owner naming approval](product-naming-approval-2026-10-18.md) governs English product-system names prospectively: no baseline collection name; Consistent GEM range as a B2B description; Room set, Wall-mounted set and Travel set; Concept packages; Property Edition and Bespoke Programme. Core Collection and Standard Range are not adopted. This resolves naming only and does not authorize artwork, commercial offers or website changes. Historical documents retain their original wording.

## Documented exceptions

- Historical package trees, localization evidence and original artwork retain supplied names, capitalization, underscores, numbering, Unicode and internal checksum filenames for integrity.
- Existing runtime/standard names such as `favicon.ico`, `README.md`, `SHA256SUMS.txt` and OFL licence filenames are retained.
- Archived `.gitignore` and two tracked `.pyc` files remain source evidence; new caches and operating-system metadata are ignored. Neither enters the website preview ZIP.
- Original transport archives under website records are retained as historical transfer evidence, not deployable content.
- Historical X12 names containing vX.Y or YYYYMMDD remain proposals only; no file with invented version/date is issued.
