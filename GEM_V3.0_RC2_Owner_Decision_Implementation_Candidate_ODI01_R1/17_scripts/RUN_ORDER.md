# ODI01-R1 — run order (reproduces every generated file)

Inputs: the worktree at `HEAD` 4ea0d11; the ODI01 package reassembled from its three delivered zips plus the loose Part D files (`<ODI01>` below). Python venv with `python-pptx lxml openpyxl pillow fonttools`; LibreOffice 26.8 (`soffice`) and poppler on PATH.

1. `r1_font_matrix.py <root> 07_Font_Claim_File_Matrix.csv`  (stops with exit 3 if any 500 file exists)
2. `r1_bold_inventory.py` on the ODI01 candidates → `07_Font_Bold_Flag_Inventory.csv/.md`
3. `r1_apply_d5.py <ODI01 deck_candidates> <out> <log>` then `r1_verify_edits.py` (must print OVERALL PASS)
4. LibreOffice render before/after (accepted Regular files in the profile font dir, tagged PDF) → `r1_render_compare.py`
5. `r1_token_status.py <root> <tokens dir>`
6. `r1_weight_search.py`, `r1_evidence.py`, `r1_bold_inventory.py` on the R1 decks (after)
7. `run_validation_id_tests.py` · `consistency_check_odi01.py` (candidates and originals) · `audit_tokens.py` · `partd_claim_audit.py`
8. `r1_build_docs.py`, `r1_preflight.py`
9. `cross_document_qa.py` → `generate_manifest.py` → `verify_manifest.py` → `cross_document_qa.py --manifest-results` → `r1_render_reports.py` → repeat from `generate_manifest.py` until `verify_manifest.py` and the QA JSON are stable.
