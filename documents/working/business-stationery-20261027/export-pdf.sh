#!/usr/bin/env bash
# Export the four A4 PDF review previews from the Word templates with LibreOffice.
# Prerequisites: soffice on PATH and three Regular font files (Jost, Inter and Noto Sans Arabic) in FONT_DIR.
# The fonts are copied into a throwaway LibreOffice profile so the export does not depend on system font registration.
# Run from any directory: FONT_DIR=/path/to/fonts bash export-pdf.sh
set -euo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
font_dir="${FONT_DIR:-$HOME/Library/Fonts}"
profile="$(mktemp -d)"
trap 'rm -rf "$profile"' EXIT

mkdir -p "$profile/user/fonts"
count=0
for pattern in "*Jost-Regular*.ttf" "*Inter-Regular*.ttf" "*NotoSansArabic-Regular*.ttf"; do
  match="$(find "$font_dir" -maxdepth 1 -name "$pattern" | head -n 1)"
  if [ -z "$match" ]; then
    echo "Missing font matching $pattern in $font_dir. Set FONT_DIR to the folder that holds it." >&2
    exit 1
  fi
  cp "$match" "$profile/user/fonts/"
  count=$((count + 1))
done
echo "Using $count font files from $font_dir"

soffice -env:UserInstallation="file://$profile" --headless --convert-to pdf --outdir "$here" "$here"/GEM_*_Template_working.docx
echo "Exported PDFs to $here"
