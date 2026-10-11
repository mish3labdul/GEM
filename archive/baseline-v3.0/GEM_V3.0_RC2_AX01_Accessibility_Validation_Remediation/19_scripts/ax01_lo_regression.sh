#!/bin/bash
# AX01: LibreOffice full-deck render of source and AX01 candidate (internal working renders), page-raster comparison at 50 dpi. Usage: ax01_lo_regression.sh <repo_root> <package_dir>
R="$1"; P="$2"; O="$P/local_only/scratch/lo"; mkdir -p "$O/in" "$O/out" "$O/ras"
i=0
for key in A B C D; do
  case $key in
    A) S="$R/GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation/19_candidate_corrections/GEM Brand Guidelines V3.0 — Part A — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx";;
    B) S="$R/GEM_V3.0_RC2_AR01_Arabic_RTL_Native_Validation/19_candidate_corrections/GEM Digital Design System V3.0 — Part B — RC2 — AR01 CANDIDATE (UNAPPROVED).pptx";;
    C) S="$R/GEM_V3.0_RC2_D3_Owner_Decision_Package/12_Candidate_Files/deck_candidates/GEM Production Standards V3.0 — Part C — RC2 — D3 CANDIDATE (UNAPPROVED).pptx";;
    D) S="$R/GEM_V3.0_RC2_Owner_Decision_Implementation_Candidate_ODI01_R1/19_candidate_documents/deck_candidates/GEM Amenities & Packaging — Concept Product Portfolio V3.0 — Part D — RC2 — ODI01-R1 CANDIDATE (UNAPPROVED).pptx";;
  esac
  cp "$S" "$O/in/${key}_src.pptx"; cp "$(find "$P/21_candidate_corrections" -name "*Part ${key} *.pptx" | head -1)" "$O/in/${key}_ax.pptx"
done
for f in A_src A_ax B_src B_ax C_src C_ax D_src D_ax; do soffice -env:UserInstallation=file://$PWD/$P/local_only/scratch/lo_prof --headless --convert-to pdf --outdir "$O/out" "$O/in/$f.pptx" >/dev/null 2>&1; pdftoppm -r 50 -png "$O/out/$f.pdf" "$O/ras/$f"; done
echo done > "$O/done.flag"
