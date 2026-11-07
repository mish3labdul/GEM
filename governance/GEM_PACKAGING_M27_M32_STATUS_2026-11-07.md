# GEM packaging M27–M32 status — 7 November 2026

Overall: **PASS WITH LIMITATIONS.** Owner decisions `-001`, `-002`, `-003` are unchanged. Nothing here is print-ready, manufacturing-approved, regulatory-cleared, commercial photography or owner-approved imagery.

| Milestone | Independent QA verdict |
|---|---|
| M27 physical reference + geometry fidelity (`M27a`) | PASS WITH LIMITATIONS (heel edge softened `13.89 → 7.05`; all dimensions remain PROVISIONAL pending physical bottle photo/drawings) |
| M28 amber glass + material realism (`m28_final`, D02) | PASS WITH LIMITATIONS (glass-to-liquid boundary IOR `1.1029` eliminates floor specks, side streaks and double ring; smooth dark heel band remains a geometry matter) |
| M29 selective premium CGI photography (13 finals) + consolidated master scene (`GEM_M29_MASTER_UNAPPROVED.blend`) | PASS WITH LIMITATIONS (bathroom pump glare and towel crowding resolved; paired studio symmetry `0.0%`; standalone `--from-texts` master reproduction verified across all 13 jobs; NOT owner-approved, NOT commercial photography) |
| M30 bilingual artwork + typography audit | PASS WITH LIMITATIONS (approved M15 textures unmodified; `0.10x` proxy failure confirmed as downsampling artefact; W–a kerning provenance isolated; optical proposals unapplied; native-reader review NOT done) |
| M31a rendering reliability + idle-machine performance | PASS (`gem_runner` + 65/65 unit tests pass; `ERRATA_M25_MASKING_CLAIM.md` published; idle-machine Run 1 separated `SIGABRT` crash from `79.9% < 80%` idle skip; Run 2 passed `6/6` full-profile renders, `exit=0`; Colab NOT TESTED) |
| M31b supplier/evidence requirements + spec tracking | PASS (109-row specification matrix + 14 reconciliation notes; `SUPPLIER_INFORMATION_REQUEST_V2.md` DRAFT NOT SENT) |
| M32 independent QA, governance, synchronization | PASS WITH LIMITATIONS |

Findings recorded: during M28 QA, `review/packaging-identity-M15-M20/m16_geometry/blender/scenes/GEM_M16_geometry_UNAPPROVED.blend` was found re-saved at 14:33 on 7 Nov 2026. The original was restored from the 14:25 local Time Machine snapshot (verified byte-identical to the M15–M20 manifest; Blender comparison confirmed identical 595 mesh vertex hashes and 6,725 material values), and all 10 historical `.blend` files (`M10`–`M23`) are now marked read-only (`0444`); see `GEM_PACKAGING_M16_SCENE_INCIDENT_REVIEW_2026-11-07.md`.

Evidence is held in the GEM-Web-remake workspace at `review/packaging-identity-M27-M32/` (not released repository assets).

Open gates: owner review of M27–M29 CGI studies; native-reader Arabic review; physical bottle photos/drawings and supplier inquiry authorization; back-label and regulatory content; capacities, dimensions, SKU, dielines; geometry evidence for Body Wash, Body Lotion, Hand Wash; manufacturing, print, commercial photography, launch.
