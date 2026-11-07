# Integrity incident — M16 scene re-saved (7 Nov 2026, found during M28 QA)

**Finding.** `review/packaging-identity-M15-M20/m16_geometry/blender/scenes/GEM_M16_geometry_UNAPPROVED.blend` (an immutable, manifest-listed file) had a modification time of 14:33:49 and a SHA-256 (`1b3b3af2…fb5`) that no longer matched the manifest (`e161daf9…bf0f`). Raised as a low-severity open item by the M28 independent QA agent.

**Evidence.** The 14:25:06 Time Machine local snapshot holds the original (hash `e161daf9…bf0f`, mtime 04:44:29, equal to the manifest). A Blender-based comparison of the original and the modified file shows identical scene lists, object count (722), image count (36), all 595 mesh-object vertex hashes, and all 6,725 material node input values. The modified file is ~10 KB smaller. So the change was a re-save with no geometry or material change.

**Cause: NOT established.** No M27/M28 script references that file (searched); no `.blend` in the package tree was modified in the same window; no Blender process remained open at investigation time; the write falls in the window 14:25:06–14:33:49 (M28's first diagnostic runs, a quiet period for other agents, and the usage-limit interruption). Candidates (unproven): an agent process that opened and re-saved the scene, or another application/session. Confidence in any single candidate: low.

**Containment (7 Nov, ~16:50).** The modified file was kept as evidence (`GEM_M16_geometry_UNAPPROVED.MODIFIED_1433.blend`) with the snapshot original (`…ORIGINAL_from_snapshot_1425.blend`) and `hashes.txt` in `review/packaging-identity-M27-M32/governance/m16_scene_integrity_incident/`. The original was restored in place (atomic copy, original mtime preserved) and verified against the manifest. After restoration the M15–M20 and m16_geometry checksum lists verify with 0 failures. M11–M14, M14.1 and M21–M26 manifests also verify. All 10 historical `.blend` files (`M10` through `M23`) were set to `0444` (read-only).

**Impact.** None on any approved artwork, deliverable or render (no geometry/material difference). The M16/M17/M22/M23 renders were produced before the modification. Treat as an integrity-control finding.
