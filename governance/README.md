# Governance and migration controls

- [source-freeze.json](source-freeze.json): four source branches, tag/ref objects, full release metadata and attachment digests/URLs, ZIP hash and capture time.
- [file-inventory.csv](file-inventory.csv): every inventoried source file, source scope/ref/path, destination, SHA-256, format, classification, language, restrictions, disposition and relationship.
- [path-migration.csv](path-migration.csv): source-scoped path resolution. A repeated path across commits is not an ambiguous rename; select its source ref first.
- [naming-rules.md](naming-rules.md): controlled names, web names and exceptions.
- [Product naming approval, 18 October 2026](product-naming-approval-2026-10-18.md): owner-approved English collection treatment, set and programme names; commercial and production scope remains pending.
- [limitations.md](limitations.md): current restrictions and outstanding acceptance.
- [duplicate-report.csv](duplicate-report.csv): exact SHA-256 duplicates retained deliberately.
- [SHA256SUMS.txt](SHA256SUMS.txt): all deliverable files except the checksum file itself and ignored machine caches.
- [cleanup-change-log.md](cleanup-change-log.md): implementation and verification.
- [published-v3.0-release-notes.md](published-v3.0-release-notes.md): unchanged published wording captured at freeze time.

CSV language values reflect path/name classification, not a content-language audit; `undetermined` means not established. `ar-en` and `ar` are organizational hints, not native-language acceptance. Generic historical-use restrictions defer to source governance; they are not an unrestricted-use grant.

An empty destination is intentional: excluded machine caches or out-of-scope local references remain untouched at their original locations. They are not required deployment dependencies. Branch inventories retain source-commit provenance even where multiple sources resolve to the same preserved file.
