# 07 · FD01 — D8 / PDF Validation Deferral (FD-G04, SR-11)

**GEM™ V3.0 RC2 — OWNER ACCEPTED WITH FORMAL DEFERRALS · SYNCHRONIZED · OWNER ACCEPTED AS-IS · FORMAL DEFERRALS RECORDED · NOT YET FINAL-RELEASE AUTHORIZED**

## Decision
PDF / Acrobat validation is **postponed**. D8 is recorded as **OPEN — FORMALLY DEFERRED BY BRAND OWNER**, and SR-11 as **FORMALLY DEFERRED BY BRAND OWNER**. PDF/Acrobat validation was **NOT PERFORMED**; no PDF artifact is generated in FD01 and no PDF or Acrobat result is claimed. D8 is not classified as failed and not as passed.

## The D8 operating rule is not changed
D8 was resolved by the Brand Owner (ODI01) as a conservative operating rule, carried forward in the ODI01-R1 PDF status record:
- **Internal working use is allowed** for Arabic or bilingual DOCX files and review PDFs if every page is marked "WORKING APPLICATION / PENDING VALIDATION" and "PENDING LOCALIZATION APPROVAL" and the documented limitations travel with the file.
- **External issue is blocked** (to a guest, supplier, partner, regulator or any external party) until each listed native test has a recorded passing result, including Windows Word, Word Online, Acrobat Unicode text layer, tagged-PDF structure, reading order and cross-reader assistive-technology tests.

Postponing the tests does not satisfy them, so **the external-issue block stays in force** unless the Brand Owner separately amends the rule. Owner acceptance of RC2 as-is therefore means continued controlled **internal** use and development of Arabic/bilingual documents. Since HR01, row 1 of that list (qualified Arabic linguistic review) has a recorded review by Mashal and macOS VoiceOver has a recorded pass; the other rows are unchanged, and final localization approval (AC10, VAL-07) has not been given.

Known limitations that travel with the files stay as documented (R03-03: do not use Word for Mac "Save as PDF" for Arabic; LH03: PDF text-extraction differences between readers).

## Register position
VAL-15 (final deliverables open, save, reopen and export without repair or accessibility regression) and the PDF parts of VAL-08 are unchanged and open. D8 is not a Register row; its deferral does not close any Register gate.

## Reopening trigger
Any plan to issue an Arabic or bilingual PDF or DOCX externally, or the AC20 decision requiring the evidence.
