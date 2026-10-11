# GEM Letterhead QA Report

**Set v1.1 Application Revision 03 • 8 October 2026**

**WORKING APPLICATION / PENDING VALIDATION**

Revision 03 is a controlled derivative of Set v1.1 Application Revision 02. It makes four evidence-backed DOCX corrections plus a metadata update, adds the first **native Microsoft Word** verification of the set (Word for Mac 16.113.3), and re-measures the two open areas: Arabic/mixed-direction PDF extraction (LH03) and footer/status legibility (LH08). Visible design is unchanged. This is not an approved stationery system, production master or print-ready release.

## 1. Repository and baseline verification

| Item | Finding |
|---|---|
| `mish3labdul/GEM` `main` | `334744c72dbbb6681034996fcca595213a7623a2`. Contains **no** letterhead set. All nine governing files match the Revision 02 source snapshot byte for byte (re-hashed 2026-10-08). |
| Fork `mashaelalh/GEM` branch `codex/gem-letterhead-v1` | `59cac07`. Contains `GEM_Letterhead_Set_v1.0` (R1) only. |
| Set v1.1 Application Revision 02 | **Not on GitHub** (no branch, tag or tree path on either remote). It was available only as the user-supplied package `outputs/GEM_Letterhead_Set_v1.1_Application_Revision_02.zip` (SHA256 recorded in the change log). All 113 root and 26 release checksums verified, and `01_templates` equals `05_release`. It is preserved unmodified alongside this revision and was not recreated. |
| v1.0 | All 370 recorded v1.0 hashes still match (`verify.py`). Uncommitted Word re-saves in `GEM_Letterhead_Set_v1.0/05_release/` and unrelated Part D work were left untouched. |

Source authority: Register > Part A RC2 > Part B RC2/tokens > Part C RC2 > `GEM_Brand_Assets_v1.0` README/official kit > `qa/` and `GEM_V3_RC2/03_qa/` evidence. External Partners Brief not used.

## 2. Findings

Severity: P0 BLOCKER, P1 HIGH, P2 MEDIUM, P3 POLISH. Result: PASS, FAIL, PENDING, REQUIRES OWNER, REQUIRES SUPPLIER.

### New in Revision 03

| ID | File | Page / template | Problem and evidence | Governing source | Exact correction | Severity | Result |
|---|---|---|---|---|---|---|---|
| R03-01 | All 8 `01_templates/*.docx`, 12 fixtures | Package `word/settings.xml` | Revision 02 sets `w:embedTrueTypeFonts` + `w:embedSystemFonts`. A single native Word save of an unchanged template grew it from 380 KB to **6.6 MB**: 21 font parts embedding unused **Times New Roman, Calibri, Cambria, Arial, Symbol, Courier** and Inter/Noto Sans Arabic Bold/Italic, 4 of them zero-byte. That redistributes third-party fonts the package has no recorded right to ship and reproduces LH10 for every user. Evidence: `04_qa/evidence/native_word/Font_Embedding_Save_Test.json`. | Register L06/VAL-19 (font build acceptance), AC20; Part C 5 (controlled masters); LH10 | Remove `w:embedSystemFonts` and add `w:saveSubsetFonts`. Of the three variants tested in Word, only this one stops it. The three full Regular payloads in the delivered templates are byte-identical to Rev02. | P1 HIGH | **PASS** (Word Mac): every native save across 43 jobs was 350–600 KB and embedded only Inter/Jost/Noto Sans Arabic. Word itself still writes 2–4 empty Bold/Italic stub parts on save (outside template control; noted for rights review). Windows/Online Word: PENDING |
| R03-02 | Arabic & Bilingual First Page; 8 Arabic/bilingual fixtures | Page 1 date/reference lines (`التاريخ: [DATE]`, `المرجع: [REFERENCE NUMBER]`) | Latin identifier runs inside RTL paragraphs start/end with neutral punctuation that the bidi algorithm resolves RTL. (a) macOS PDFKit (Preview copy/search engine) found **0 hits** for `[DATE]` and `[REFERENCE NUMBER]` in Rev02 PDFs; extraction gave `DATE ]` / `[`. (b) Native Word: replacing `[DATE]` with `8 October 2026` displayed **“October 2026 8”** (`native_word/Rev02_Word_render_Arabic_date_reversed.png`). | Register M11, M12 (codes stay LTR within RTL); Part A 38 (technical codes Latin, left to right); Part B 12–13 | Bound each `rtl=0` run inside a `bidi=1` paragraph with invisible U+200E LEFT-TO-RIGHT MARK (`rev03_fixes.py`): 2 runs per Arabic/bilingual first page. The marks sit outside the placeholder, so Find/Replace keeps them. Visual output is unchanged (sub-pixel only; `visual_review/Rev02_vs_Rev03_Arabic_metadata_crop.png`). | P1 HIGH | **PASS**: PDFKit search hits = 1 for both tokens; native Word shows `التاريخ: 8 October 2026` correctly after replacement; all date/reference lines in all Arabic/bilingual templates and fixtures pass native search. |
| R03-07 | Arabic & Bilingual Continuation | Page 1 placeholder `[نص الصفحة التالية]` | The published PDFs (LibreOffice export route, Rev02 and Rev03 candidates) silently dropped the ASCII brackets of this Noto Sans Arabic RTL run; native Word draws them. The text layer still contained them. Font coverage is complete (no missing glyph in any run), so this is a renderer behaviour, not a font defect. | Register M04/M06; Part A/B Arabic placeholder convention; user font/glyph rule | Use the set's existing Arabic placeholder punctuation: `«نص الصفحة التالية»` (as `«اسم المستلم»`, `«التوقيع»`). Remains working copy, PENDING LOCALIZATION APPROVAL. | P2 MEDIUM | **PASS**: both marks drawn in LibreOffice and Word exports |
| R03-08 | All 8 templates, 12 fixtures | Footer `Page n of N` | In every published PDF (LibreOffice route) the PAGE/NUMPAGES digits printed at 10.5 pt beside 9 pt “Page … of”, because `w:fldSimple` results take the paragraph style size in that exporter (native Word was correct). | Part B type tokens; LH05 | Rewrote each footer `fldSimple` as an equivalent complex field (begin / `PAGE \* MERGEFORMAT` / separate / result / end) carrying the existing 9 pt Inter Ink properties. Same live field codes. | P2 MEDIUM | **PASS**: uniform 9 pt in LibreOffice and native Word; fields update correctly over 1–4 pages in Word |
| R03-03 | Any completed Arabic/bilingual letter | Export step | Native Word for Mac **Save as PDF** looks correct but has an unusable Arabic text layer: PDFKit returns isolated presentation-form glyphs out of order (`native_word/Word_export_Arabic_First_Page__flow3.pdf`). Not fixable in the DOCX. | Register VAL-07/VAL-15/AC10; Part B 16; `qa/PartB_RC2_Accessibility_QA_Report.md` | Specification and README warn not to send Arabic/bilingual PDFs from this route until copy/search is verified. The packaged PDFs use the Revision 02 LibreOffice export plus ToUnicode/ActualText repair. | P1 HIGH | **FAIL** (Word for Mac PDF route). **REQUIRES OWNER**: choose and validate an approved export route. PENDING: Word “Best for electronic distribution and accessibility” (online service), Windows Word and Acrobat routes were not tested. |
| R03-04 | Arabic/bilingual letters (user content) | Arabic body / recipient text | Phone numbers and Latin IDs typed *into Arabic text runs* reorder in native Word (`+000 00 000 0000` → `0000 000 00 000+`). Footer contact fields are LTR paragraphs and stay correct. No template field is affected. | Register M11/M12; Part A 38 | Guidance only: keep identifiers in the footer/reference fields, or bound them with U+200E. No unapproved Arabic wording added. | P2 MEDIUM | **REQUIRES OWNER** (Arabic/Localization Lead to define the insertion practice) / PENDING |
| R03-05 | Long-field fixtures (QA only) | `[ID: TEST-2026-001]` | Long hyphenated IDs may wrap at a hyphen; search for the whole ID then fails (`TEST-2026-` / `001]`). Email, URL and phone in the same line are found. | Part A 38 | Guidance: keep long hyphenated IDs on their own line. No template change. | P3 POLISH | PENDING (guidance documented) |
| R03-06 | Arabic & Bilingual First Page | `[DATE]` | The Arabic date numeral convention (Latin 0–9 or Arabic-Indic) for correspondence is not signed off. M11 is contextual, and Part A 38 says the locale policy is not signed off. | Register M11; Part A 38 | Placeholder kept Latin/LTR; nothing invented. | P3 POLISH | **REQUIRES OWNER** |

### Revision 02 findings re-verified

| ID | File / template | Revision 03 evidence | Severity | Result |
|---|---|---|---|---|
| LH01 versions/checksums | Whole package | New root and release SHA256SUMS regenerated and verified; release copies equal canonical files. | P1 HIGH | PASS |
| LH02 font policy | All | Every LibreOffice and native Word export uses only Inter, Jost and Noto Sans Arabic Regular; no Times/Calibri/Arial/Bold (`Technical_Checks.json`, `native_word/*Analysis*`). | P1 HIGH | PASS (Word Mac + LibreOffice); Windows/Online PENDING |
| LH03 Arabic PDF text layer | Arabic/bilingual PDFs, Digital/Print pp. 3–6 | **Still applicable to generic extractors.** Native PDFKit (Preview copy/search): all logical source lines in all 8 templates and 12 fixtures match whole or by native search (Rev02: 16 failures, Rev03: 0 template failures). pypdf, poppler and pdfplumber still reorder or omit Arabic fragments, identically in Rev02 and Rev03 (`Rev03_Checks.json → extraction_engines`). Glyph inventories and semantic ActualText pass. | P1 HIGH | **FAIL** (generic plain extraction) / PASS (native PDFKit copy/search) / **PENDING** (assistive technology, Acrobat) |
| LH04 mixed-direction token | Bilingual/Arabic first page | Superseded by R03-02 (copy/search and native replacement defects found and corrected). | P1 HIGH | PASS |
| LH05 PAGE/NUMPAGES | All | Native Word: correct “Page i of N” on every page of 43 jobs (1, 2, 3 and 4 pages; automatic flow and explicit breaks; field replacement; save/close/reopen). Exporter size inconsistency corrected by R03-08. | P1 HIGH | PASS (Word Mac) |
| LH06 localization status on continuations | Arabic/bilingual | `PENDING LOCALIZATION APPROVAL` is present on every native Word page. | P2 MEDIUM | PASS |
| LH07 tagline | First pages | Unchanged; 10.5 pt, 38 twips; no tracking on Arabic. | P2 MEDIUM | PASS |
| LH08 footer/status legibility | All footers | **Still applicable.** 9 pt Inter (12 px at 96 dpi), which meets the Part B `labelSmall` floor; legible in native Word renders; no collision in 1–4-page flows. It is a digital application choice, not an approved stationery minimum (Part C: physical minimums “to be verified by process test”). Status labels use 0 tracking whereas `labelSmall` specifies 0.08em, so the owner should confirm the token. | P2 MEDIUM | **REQUIRES OWNER / REQUIRES SUPPLIER** (physical proof) |
| LH09 stray symbols | English Continuation, Executive | No unintended symbols in any native Word or LibreOffice render. | P2 MEDIUM | PASS |
| LH10 empty font parts | Templates | Delivered templates: 3 valid Regular payloads, none empty. Word save behaviour addressed by R03-01. | P2 MEDIUM | PASS / PENDING rights acceptance |

## 3. Native Microsoft Word verification (Word for Mac 16.113.3)

Scripted through AppleScript on working copies only. Each job opened the file, edited it, saved it as a new DOCX, closed it, **reopened** the saved file and exported a PDF (`native_word/Template_Jobs_Rev03.json`, `Fixture_Jobs_Rev03.json`). All 43 jobs were run on the **final** Revision 03 files, after every correction.

| Check | Coverage | Result |
|---|---|---|
| Opens without repair, editable body/placeholders | 8 templates + 12 fixtures | PASS |
| Field replacement: long reference (main story and continuation header), recipient, organisation, address, signatory, footer e-mail/URL, long subject, Arabic placeholders | 8 templates | PASS: no layout damage. Bilingual long fields correctly repaginate to 2 pages with the closing/signature kept together. |
| Automatic overflow to 2 and 3 pages; explicit page breaks to 3 pages | EN, Executive, Minimal, Arabic, Bilingual first pages | PASS: expected page counts; signature block never split. |
| First-page vs continuation headers/footers, anchoring | All multi-page results | PASS: logo and tagline on page 1 only, continuation identifier and reference on pages 2+, footer fixed (`Word_render_*.png`). |
| Live PAGE/NUMPAGES after save/reopen | 43 jobs | PASS |
| Named styles (Normal, Body Text, Heading 1) retained; fields still live in saved XML | 43 jobs | PASS |
| Word vs LibreOffice pagination | 12 fixtures | PASS: identical page counts (1/2/3). |
| Fonts in Word output | 43 jobs | PASS: Inter, Jost, Noto Sans Arabic only. |
| Word for Mac PDF text layer (Arabic) | Arabic/bilingual | FAIL (R03-03) |
| Windows Word, Word Online, iPad | none | PENDING |

## 4. PDF, accessibility and print checks

| Area | Result | Evidence |
|---|---|---|
| A4, page count, embedded subset fonts, selectable text | PASS | `Technical_Checks.json`, `Rev03_Checks.json` |
| Tags, document/element languages, H1, vector-logo Figure alternative, bookmarks (Digital/Print 8) | PASS structural | `Technical_Checks.json`; tag presence is **not** accessibility acceptance |
| Native copy/search (PDFKit) | PASS for template content | `PDFKit_Native_Extraction.json` |
| Generic logical extraction (pypdf, poppler, pdfplumber) | FAIL remaining (LH03) | `Rev03_Checks.json` |
| Assistive technology (VoiceOver, NVDA/JAWS, Acrobat read-aloud) | PENDING. VoiceOver is present on this Mac but was not operated: automated control of assistive technology was not available to this session and needs a human tester. | — |
| Links | PASS for templates (no link annotations; contact fields are placeholders, nothing invented). PENDING for each completed letter. | `Rev03_Checks.json` |
| Repaired PDFs pixel-identical to raw exports; Digital = Print artwork | PASS | `Visual_Preservation.json` |
| Visual parity with Revision 02 | PASS: differences confined to the intended corrections. Footer page digits are now 9 pt in all files (≈414 px at 100 dpi). Arabic/bilingual files add sub-pixel shifts beside the invisible marks and the continuation placeholder punctuation. No layout, logo, margin or pagination change. | `Rev03_Checks.json`, `visual_review/` |
| Safe writing area | PASS: all text within the 25 mm side margins (1 pt glyph tolerance); footer/body clear in 1–4-page flows | `Rev03_Checks.json` |
| Grayscale / low ink | PASS screen proof: page-1 coverage 0.85–1.73 %; Minimal has no rule or tagline; no colour-only meaning | `visual_review/gray-sheet-*.png` |
| CMYK/Pantone/stock/GSM/profile/PDF-X/tolerances | REQUIRES SUPPLIER: none invented; Print PDF is an RGB print candidate | — |

## 5. Remaining acceptance gates (not closed by this revision)

1. **Brand Owner (AC20, S07):** application release, bilingual correspondence hierarchy, 9 pt footer/status exception and tracking token (LH08), Executive/Minimal variants, approved PDF export route (R03-03).
2. **Arabic/Localization Lead (M01, M11, M16):** all Arabic strings, date numerals (R03-06), identifier-insertion practice (R03-04). `PENDING LOCALIZATION APPROVAL` stays on every Arabic/bilingual page.
3. **Accessibility QA (VAL-08 “In progress”, VAL-15 “Not started” in `GEM_V3_RC2/03_qa/GEM_V3_RC2_Open_Evidence_Register.md`):** Arabic/English assistive-technology reading order and Acrobat accessibility; LH03 generic extraction.
4. **Document QA:** Windows Word and Word Online matrix.
5. **Supplier/Procurement (Part C 5, 19–21, 44):** prepress standard, profile, stock, physical legibility proof.
6. **Design Custodian/Legal (E01, L06, VAL-19):** logo production-master and exact font build/licence acceptance, including embedded Office stubs.

Do not describe this set as Approved, production-ready or commercially print-ready.
