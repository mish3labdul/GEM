# 08 · D3B Cross-Document Consequences

No D3B option is recommended (`04`), so consequences are shown for **both**. Nothing below was modified. Categories: REQUIRES UPDATE · NO CHANGE · MANIFEST ONLY · SOURCE NAME MUST REMAIN UNCHANGED. **X12 controls controlled names and manifests; it does not authorize renaming the historical/source kit files.**

| Artifact | Scope | If BRAND is adopted | If Logo is adopted | Note |
|---|---|---|---|---|
| Part A slide 75 — example string `GEM_Logo_Horizontal_Black_v3.0_20261006.svg` | Part A slide 75 example | REQUIRES UPDATE | NO CHANGE | Example would need the chosen STREAM (and the ASSET-noun question under BRAND). |
| Part A slide 75 — sentence "The stream field follows the asset library folder." | Part A slide 75 rule | NO CHANGE | REQUIRES UPDATE | Under Logo the folder rule no longer describes the STREAM field and must be restated. |
| Part A slide 75 notes; slide 79 change log | Part A | NO CHANGE | NO CHANGE | Asset-ID and checksum proposals stay pending (VAL-16). |
| Part C slides 7, 56, 73 (pattern, Appendix N) | Part C | NO CHANGE | NO CHANGE | Pattern only; Appendix N "Category" field may need a note on overlap with STREAM if Logo is chosen (category list undefined). |
| Part B slide 35 (kit renaming statement) | Part B | NO CHANGE | NO CHANGE | Pattern only; lists source names, which stay. |
| Part D deck | Part D | NO CHANGE | NO CHANGE | No X12 reference. |
| Register X12 and X02–X11 | Register | NO CHANGE | NO CHANGE | Register wording is the pattern; an owner-authorized note listing STREAM values is optional, not required. |
| GEM_Brand_Assets_v1.0/README.md ("BRAND … working choice for the owner to confirm") | Kit README | REQUIRES UPDATE | REQUIRES UPDATE | Under BRAND: record it as confirmed. Under Logo: record that BRAND is superseded for logos. |
| Official kit logo files (128 images) and their `SHA256SUMS.txt` | Kit source | SOURCE NAME MUST REMAIN UNCHANGED | SOURCE NAME MUST REMAIN UNCHANGED | X12 controls controlled/manifest names at first manifest (Part C slide 7); it does not authorize renaming the source kit. |
| GEM_Brand_Assets_v1.0/01_svg working files (11 × GEM_BRAND_…_v0.1) | Kit working files | NO CHANGE | MANIFEST ONLY | Under Logo these non-logo assets keep BRAND or need another STREAM: two STREAM values in one library folder; decide in the manifest, not by renaming. |
| GEM_Brand_Assets_v1.0/05_layout_matched files | Kit working files | SOURCE NAME MUST REMAIN UNCHANGED | SOURCE NAME MUST REMAIN UNCHANGED | Referenced by build scripts; controlled names in the manifest only. |
| Letterhead package references to kit file names; build scripts (`sync_logos.py`, `edit_assets_*.py`, `package.py`, `spec.py`, `extra_checks.py`) | Dependents | SOURCE NAME MUST REMAIN UNCHANGED | SOURCE NAME MUST REMAIN UNCHANGED | They reference source names; touch only if a rename is separately authorized. |
| Controlled release manifest (VAL-16, not started) | Manifest | MANIFEST ONLY | MANIFEST ONLY | Controlled names live here; the chosen mapping CSV (05 or 06) becomes its input. |
| ODI01-R1 `13_D3_Unresolved.md` and the carried-forward X12 mapping CSVs | Earlier packages | NO CHANGE | NO CHANGE | History; superseded by this D3 package, not edited. |
| Open evidence register / release notes | qa/ | NO CHANGE | NO CHANGE | VAL-16 stays Not started. |

**D3A is separate:** its four candidates (`03`) do not depend on the D3B outcome. Promoting them into authoritative folders needs a separate authorized change.
