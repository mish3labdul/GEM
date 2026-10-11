# 03 · Existing Public Exposure (baseline `4ea0d11`)

**Rule applied:** only what is verifiably present is listed. **Presence in a public repository is not evidence that disclosure was authorized**, reviewed or intended; this document does not treat it as such. Counts come from `git ls-tree -r -l 4ea0d11` (`evidence/07`) and remote history (`evidence/08–10`). Image *content* was not inspected beyond what the repository's own documents state.

## Size of the baseline
`main` at `4ea0d11`: **413 files, 162.2 MB** (largest groups: Part D 96 MB, Parts A–C 43 MB, letterhead set 18 MB). Remote history reachable on `origin` (branches plus every pull-request head): **40 commits, 755 distinct paths ever present, 1,111 objects, 803 blobs ≈ 301 MB**.

## A · Governing brand material
| Item | Files | Size | Notes |
|---|---|---|---|
| Approval Register (`GEM_V3_RC2/00_originals/…Register_Prefilled.xlsx`) | 1 | 0.19 MB | Decision register with 466 rows; role holders unnamed |
| Parts A, B, C decks and PDFs (originals, working, pre-sync, release) | 16 | 43.3 MB | Editable PPTX plus PDF exports |
| Part D deck and PDF (originals, release) | 4 | 66.5 MB | "CONCEPT / NOT PRODUCTION ARTWORK" |
| Official asset kit and logo masters (`GEM_Brand_Assets_v1.0`) | 170 | 4.0 MB | Logo SVG (32), EPS (16), PDF (16), PNG, icons, motion, layout-matched files |
| Tokens (`PartB_RC2/*/tokens`) | 6 | 0.07 MB | JSON + CSS + notes |
| QA, audit and governance documents (`qa/`, `GEM_V3_RC2/03_qa/`, ecosystem audit) | 24 | 0.3 MB | Includes open evidence registers and the audit note |

## B · Application material
| Item | Files | Size | Notes |
|---|---|---|---|
| Letterhead set Rev03: templates, PDFs, specs, source scripts, release | 77 | 8.5 MB | 8 editable Word templates; "working application, pending validation" |
| Letterhead QA evidence and fixtures | 60 | 9.1 MB | Word-export PDFs, renders, fixtures, JSON checks |
| Part D concept mockups and register (`01_mockups`) | 16 | 29.5 MB | 15 PNG + `MOCKUP_REGISTER.csv` |
| Packaging concepts | within Part D deck | — | No dieline, supplier or production value is stated |

## C · Potentially sensitive IP (present)
| Category | Verifiably present | Not present |
|---|---|---|
| Editable PPTX | **14** (95.2 MB) | — |
| Editable DOCX | **30** (10.9 MB) | — |
| SVG / EPS / vector masters | 50 SVG, 16 EPS, 16 logo-PDF files (64 logo vector/PDF master files) | Embroidery and engraving masters are stated as not supplied |
| Logo source assets | The "supplied master kit, unchanged" (kit README); acceptance as production master **not** recorded (VAL-02) | Ownership documents |
| Font binaries | **3** static Regular TTF (Jost, Inter, Noto Sans Arabic) in the Rev03 `00_source/fonts`, each with an `OFL.txt` | — |
| Licensing documents | 3 × SIL OFL texts (copyright lines of The Jost Project, The Inter Project, The Noto Project authors) | **No repository LICENSE/NOTICE file**; no trademark or brand-use licence |
| Design-system material | Token package, Part B deck, `window.GEM` component *descriptions* | No component source, no Storybook (OD-SRC / VAL-13 open) |
| Supplier / process information | Placeholders only (`[REQUIRES SUPPLIER]`, `[PENDING PHYSICAL PROOF]`) | No named supplier, price, specification or contact found by text search |
| Internal governance decisions | Open evidence registers, change registers, release notes, the integrated audit | — |
| Audit evidence | Letterhead QA evidence (JSON, PDFs, renders); audit note states, for example, "zero rights-cleared images" | — |
| Personal / credential data | Secret-pattern scan of baseline text: **0 matches**; email-like strings are `example.invalid` placeholders or `noreply` | — |
| Document metadata | The two Part D PPTX files (original and release) embed creator "Walnut Exporter" and a named individual as last-modified-by | Parts A–C PPTX and the DOCX templates carry no named author |

## D · Rights-sensitive material
| Item | Evidence | Status |
|---|---|---|
| Photography | No JPG/JPEG files in the tree; the audit states no production photography exists | Not present |
| **AI-generated imagery** | Part D `CHANGE_LOG.md`: "All imagery is AI-generated concept imagery as the deck itself states; no image rights are recorded (VAL-06)". 15 PNG mockups (29.5 MB) are public, and embedded again in the Part D decks | Rights **not recorded** |
| Third-party / external marks | None identified by text search; **image content not inspected**, so marks inside images are UNKNOWN | UNKNOWN |
| Fonts | 3 OFL static files at baseline; see "Font binaries in remote history" | Licence text present; accepted builds and deployment acceptance **not** recorded (VAL-05) |
| Licensing references | OFL texts only | — |

## Font binaries in remote history (`origin`, incl. PR heads)
12 distinct font paths: the 3 baseline Regular files, plus 9 under `GEM_Letterhead_Set_v1.0/00_source/fonts` reachable only through open **PR #10** (`refs/pull/10/head`): Regular ×3, **Bold ×3**, and **variable ×3** (`Jost[wght]`, `Inter[opsz,wght]`, `NotoSansArabic[wdth,wght]`). The Bold and variable builds are the "archived input / working build" files that decision D5 treats as not accepted. `letterhead-fork` additionally carries Revision 02 copies (3 Regular).

## Other history already public
- Removed from the tree but present in history: Part D v1.0 portfolio build, release and QA files (52 paths); traced logo replicas (5); the whole v1.0 letterhead set (284 paths, including 88+ render images, QA evidence and fixtures) via PR #10.
- Second public repository `mashaelalh/GEM` carries, beyond everything reachable on `origin` (including its pull-request heads), **2 commits and 204 objects**: a Revision 02 letterhead set and a Revision 03 build, with their QA evidence (6 more Regular font files: 3 under each revision). Its other history overlaps with `origin`.

## Existing exposure vs the open gates
The public repositories already contain the unreviewed logo kit, the editable decks, the AI-generated imagery and the font files **while** VAL-03, VAL-04 and VAL-06 are "Not started" and VAL-05 is "In progress" (`05`). Whether that existing disclosure is acceptable is a Legal/IP question (`08`, Q1–Q4, Q7). It is not decided here.
