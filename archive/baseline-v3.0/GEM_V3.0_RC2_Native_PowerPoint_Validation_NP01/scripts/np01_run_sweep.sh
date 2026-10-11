#!/bin/zsh
# NP01 native sweep driver (read-only: no save, no edit). Usage: np01_run_sweep.sh <outdir>
OUT="$1"; mkdir -p "$OUT"; HERE="${0:A:h}"
for spec in "Part_D:24" "Part_C:78" "Part_B:35" "Part_A:80"; do
  part="${spec%%:*}"; n="${spec##*:}"; name="NP01_${part}_test_copy.pptx"; f="$OUT/${part}.tsv"; : > "$f"; : > "$OUT/${part}.fail"
  for s in $(seq 1 $n); do
    ok=0
    for try in 1 2; do
      res=$(perl -e 'alarm 150; exec @ARGV' osascript "$HERE/np01_native_sweep_slide.applescript" "$name" $s 2>&1)
      if [[ $? -eq 0 && "$res" != *"script error"* && "$res" != *"execution error"* ]]; then ok=1; break; fi
      sleep 3
    done
    if [[ $ok -eq 1 ]]; then printf '%s\n' "$res" | sed '/^$/d' >> "$f"; else echo "slide $s: $res" >> "$OUT/${part}.fail"; fi
    echo "$part $s/$n ok=$ok" >> "$OUT/progress.log"
  done
done
echo DONE >> "$OUT/progress.log"
