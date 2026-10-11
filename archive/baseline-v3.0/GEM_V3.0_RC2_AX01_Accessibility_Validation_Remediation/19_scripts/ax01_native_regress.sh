#!/bin/bash
# (set AX01_PY to a Python with lxml/Quartz, e.g. the docling venv)
# AX01 native before/after capture for a deck: <repo_root> <package_dir> <key> <source_pptx> <candidate_pptx> <slides...>
R="$1"; P="$2"; K="$3"; S="$4"; C="$5"; shift 5
"${AX01_PY:-python3}" "$P/19_scripts/ax01_native_capture.py" "$P" "${K}_before" "$S" "$@"
"${AX01_PY:-python3}" "$P/19_scripts/ax01_native_capture.py" "$P" "${K}_after" "$C" "$@"
