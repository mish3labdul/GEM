# 15 · HR01 — Evidence Index

**GEM™ V3.0 RC2 — SYNCHRONIZED / NOT RELEASED / EVIDENCE GATES REMAIN / UNAPPROVED IMPLEMENTATION CANDIDATE**
Paths are relative to the repository root. Nothing here is a release claim, a legal opinion or an accessibility certification.

## HR01 package
| File | Content |
|---|---|
| `01_HR01_Executive_Summary.md` | Queue outcomes, candidate changes, gates (none closed), publication scope |
| `02_HR01_Queue_Baseline.csv` | The four authoritative queues: source, count, authority, gates, dependencies, HR01 outcome |
| `03_HR01_Arabic_Review_Register.csv` | 44 items + 4 extras; dispositions; SHA-256 prefixes before/after; no Arabic text |
| `04_HR01_Arabic_Decision_Log.md` | Arabic decisions by batch |
| `05_HR01_Accessibility_Content_Register.csv` | 144 items + 2 extras; approved English titles and alt texts |
| `06_HR01_Accessibility_Decision_Log.md` | Accessibility content decisions and method |
| `07_HR01_Screen_Reader_Test_Register.csv` | 13 tests: 11 PASS (reviewer observed, macOS VoiceOver), 2 DEFERRED |
| `08_HR01_Reading_Order_Manual_Review.csv` | 13-slide sample (rules fixed before testing), all PASS |
| `09_HR01_Legal_IP_Evidence_Inventory.csv` | 16 evidence items |
| `10_HR01_Legal_IP_Disposition_Register.csv` | 8 gates; none closeable |
| `11_HR01_Gate_Impact_Matrix.csv` | 16 gates/items reassessed through the five levels; 0 closed |
| `12_HR01_Remaining_Evidence.csv` | 16 remaining evidence items with owners |
| `13_HR01_Native_Revalidation.md` | Native checker results, environment, defect found and fixed |
| `14_HR01_Visual_Regression_QA.md` | Raster comparison results |
| `16_scripts/` | Builders, QA and manifest scripts (relative paths only) |
| `17_qa/` | `hr01_visual_regression.csv`, `hr01_static_accessibility_check.csv`, `consistency_HR01.md` (112 assertions), `candidate_build_log.json`, QA results |
| `18_candidate_corrections/` | 4 PowerPoint and 4 Word HR01 candidates (UNAPPROVED) |
| `MANIFEST.json`, `SHA256SUMS.txt` | File list and checksums (neither hashes itself; the checksum file also covers the manifest) |

## Source evidence used (read-only, unchanged)
| Source | Used for |
|---|---|
| `GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/OD01_Mashal_Arabic_Review_Queue.csv`, `OD01_Mashal_Accessibility_Content_Queue.csv` | Queues 1 and 2 |
| `GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation/11_AR01_Native_Arabic_Reviewer_Queue.csv` | Queue 1 population cross-check |
| `GEM_V3.0_RC2_AX01_Accessibility_Validation_Remediation/` (`05`, `06`, `07`, `10`, `21_candidate_corrections/`) | Titles, alt text, reading order, test matrix, candidate lineage |
| `GEM_Letterhead_Set_v1.1_Application_Revision_03/01_templates/`, `00_source/fonts/*/OFL.txt`, `00_source/Original_Font_Manifest.json` | Word lineage; font licence evidence |
| `GEM_V3_RC2/00_originals/GEM_V3_Final_Brand_Approval_Register_Prefilled.xlsx` | Gate definitions, owners, acceptance conditions (unchanged) |
| `GEM_V3.0_RC2_D7_Repository_Visibility_Decision_Package/` | Legal/IP dependencies and exposure analysis |
| `GEM_V3.0_RC2_OD01_Owner_Decision_Formalization/08_OD01_Open_Evidence_After_Decisions.csv` | Gate baseline |
| `GEM_Brand_Assets_v1.0/README.md`, `Amenities_Portfolio_PartD_RC2/` | Logo and imagery provenance statements |

## Local-only (not committed)
Reviewer packets with Arabic wording, picture and slide renders, the working decisions file, native checker observations, LibreOffice renders, rasters, scratch. The folder `local_only/` is excluded from Git. Confidential Legal/IP documents, if supplied, belong there and are never committed.

## Related earlier evidence
AR01 and AX01 packages, OD01 package and the D7 package are unchanged by HR01.
