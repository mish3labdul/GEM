# 09 · Letterhead Status (Revision 03 — carried forward from ODI01; not modified in R1)

**Status: WORKING APPLICATION / PENDING VALIDATION** (unchanged). Revision 03 (`GEM_Letterhead_Set_v1.1_Application_Revision_03/`, merged in `main`) is the latest reviewed package. No artifact labelled Revision 04 exists in `main`, open PR #10 or any upload. **The stale "R04 unavailable" language is retired** as a blocker and as a gate.

## All 8 templates re-verified (structural: zip/XML + poppler; script `17_scripts/audit_letterhead.py`)

Margins are top/right/bottom/left in twips (A4 = 11906 × 16838; sides 1417; top 1701, Executive 2041; bottom 2098).

| Template | Page | Margins | Header/footer | Fields | Logo bytes vs official kit | Real bold runs in content | Embedded fonts (DOCX) | PDF tagged; PDF fonts |
|---|---|---|---|---|---|---|---|---|
| Arabic_Continuation | A4 ✔ | 1701/1417/2098/1417 | default only | PAGE+NUMPAGES ✔ | — (continuation: no logo by design) | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular, NotoSansArabic-Regular |
| Arabic_First_Page | A4 ✔ | 1701/1417/2098/1417 | titlePg ✔ | PAGE+NUMPAGES ✔ | ce953ebf =kit, 6abbd491 =kit | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular, Jost-Regular, NotoSansArabic-Regular |
| Bilingual_Continuation | A4 ✔ | 1701/1417/2098/1417 | default only | PAGE+NUMPAGES ✔ | — (continuation: no logo by design) | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular, NotoSansArabic-Regular |
| Bilingual_First_Page | A4 ✔ | 1701/1417/2098/1417 | titlePg ✔ | PAGE+NUMPAGES ✔ | ce953ebf =kit, 6abbd491 =kit | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular, Jost-Regular, NotoSansArabic-Regular |
| English_Continuation | A4 ✔ | 1701/1417/2098/1417 | default only | PAGE+NUMPAGES ✔ | — (continuation: no logo by design) | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular |
| English_First_Page | A4 ✔ | 1701/1417/2098/1417 | titlePg ✔ | PAGE+NUMPAGES ✔ | ce953ebf =kit, 6abbd491 =kit | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular, Jost-Regular |
| Executive | A4 ✔ | 2041/1417/2098/1417 | titlePg ✔ | PAGE+NUMPAGES ✔ | ce953ebf =kit, 6abbd491 =kit | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular, Jost-Regular |
| Minimal | A4 ✔ | 1701/1417/2098/1417 | titlePg ✔ | PAGE+NUMPAGES ✔ | 2c49e1c6 =kit, 38d89d97 =kit | 0 | Inter, Jost, Noto Sans Arabic | yes; Inter-Regular, Jost-Regular |

Result: 8/8 A4; first-page templates use `titlePg` with first/default header+footer, continuation templates default-only; `PAGE`/`NUMPAGES` present in every footer; logo media byte-identical to the official kit (Minimal uses the black variant); only Inter, Jost and Noto Sans Arabic Regular embedded; 0 real bold runs in used content; tagline "HOSPITALITY, IN PERFECT PROPORTION" at 10.5 pt with 38 twips tracking (≈ 0.18 em), none on Arabic; status lines WORKING APPLICATION / PENDING VALIDATION on every page and PENDING LOCALIZATION APPROVAL on Arabic/bilingual pages.

Low-severity carry-overs: 102 unused bold style definitions and 4 Courier style references (not used in content).

## Bilingual Arabic-first hierarchy (verified from DOCX structure; script `17_scripts/letterhead_bilingual_hierarchy.py`)
In `Bilingual_First_Page` and `Bilingual_Continuation`, in every content pair the Arabic paragraph precedes its English counterpart: recipient block → subject → salutation → closing → signatory (first Arabic content paragraph is #1, first English content paragraph #4 / #3; the only English-leading paragraph is the "SAMPLE CONTENT · PENDING LOCALIZATION APPROVAL" status line). All Arabic paragraphs carry `bidi=1` with start alignment (right in RTL); all English paragraphs `bidi=0`, left. Arabic is set larger (11.5 pt body) than English (10.5 pt) in the DOCX run sizes. The header holds only the English tagline (no Arabic tagline exists; none was invented). **Structural PASS — not native Arabic approval.** Check results: 34 PASS / 0 REVIEW. Evidence: `18_qa_evidence/letterhead_bilingual_hierarchy.json`.

## Updated records
- **AUD-14** → UPDATED: Revision 03 verified for 8/8 templates; "R04 unavailable" retired; native gates below remain open (`18_qa_evidence/issue_register_odi01.csv`).
- **QA Status Matrix** → `18_qa_evidence/QA_Status_Matrix_ODI01.md`. **Remaining Gates** → `15`. **Coverage Matrix** → `18_qa_evidence/coverage_matrix_odi01.csv` (areas 08, 09, 14, 15, 16, 18, 19, 20).

## NOT closed by ODI01
| Item | State |
|---|---|
| Windows Word, Word Online, iPad | NOT TESTED |
| Acrobat Arabic Unicode text layer; Acrobat accessibility | NOT TESTED |
| Screen reader / AT (VoiceOver, NVDA, JAWS) | NOT TESTED |
| Native Arabic linguistic approval | REQUIRES OWNER (M01, M11, M16, VAL-07) |
| Physical print proof; 9 pt footer legibility on paper (LH08) | PENDING PHYSICAL PROOF / REQUIRES SUPPLIER |
| R03-03 Word-for-Mac Save-as-PDF breaks Arabic copy/search | FAIL — do not use for Arabic/bilingual external PDFs (see `10`) |
| LH03 generic extractors reorder Arabic | FAIL for pypdf/poppler/pdfplumber; PASS in PDFKit |

Inherited, not repeated: Word for Mac 16.113.3 results (43 jobs) and PDFKit copy/search from the package QA (`04_qa/`).

## R1
The letterhead package was **not modified** (`git diff HEAD` on `GEM_Letterhead_Set_v1.1_Application_Revision_03/` is empty). Carried forward: GEM™ Branded Letterhead Set — WORKING APPLICATION / PENDING VALIDATION; Arabic: PENDING LOCALIZATION APPROVAL. Open: native Windows Word, Word Online, Acrobat text layer, assistive technology and physical proof. The earlier "R04 unavailable" gate is retired.
